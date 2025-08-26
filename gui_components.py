"""
GUI Components for Fire Suppression System
Contains all Tkinter interface elements and visual components
"""

import tkinter as tk
from tkinter import ttk
import math
from PIL import Image, ImageTk
from fuzzy_logic_controller import FuzzyLogicController


class FireSuppressionGUI:
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("Fire Suppression Sprinkler System - Fuzzy Logic Control")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Initialize fuzzy logic controller
        self.fuzzy_controller = FuzzyLogicController()
        
        # System state variables
        self.heat_level = tk.DoubleVar(value=70)
        self.is_triggered = False
        self.water_drops = []
        self.animation_running = False
        
        # Setup the user interface
        self.setup_ui()
        self.update_system()
        
        try:
            self.fire_img_orig = Image.open("Images/fire.png")
        except Exception:
            self.fire_img_orig = None

    def setup_ui(self):
        """Setup the main user interface layout"""
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.setup_control_panel(main_frame)
        self.setup_sprinkler_panel(main_frame)
        self.setup_status_panel(main_frame)
        
    def setup_control_panel(self, parent):
        """Setup the left control panel with sliders and system controls"""
        control_frame = tk.Frame(parent, bg='#34495e', relief=tk.RAISED, bd=2)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        title_label = tk.Label(control_frame, text="Fire Suppression Control", 
                              font=('Arial', 16, 'bold'), fg='#ecf0f1', bg='#34495e')
        title_label.pack(pady=10)
        
        self.create_heat_control(control_frame)
        self.create_status_display(control_frame)
        
        reset_btn = tk.Button(control_frame, text="Reset System", 
                             font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                             command=self.reset_system, relief=tk.RAISED, bd=2)
        reset_btn.pack(pady=20, padx=10, fill=tk.X)
        
        start_btn = tk.Button(control_frame, text="Start Fire", 
                              font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                              command=self.start_fire, relief=tk.RAISED, bd=2)
        start_btn.pack(pady=5, padx=10, fill=tk.X)
        self.start_btn = start_btn

    def create_heat_control(self, parent):
        """Create heat level control widgets"""
        heat_frame = tk.Frame(parent, bg='#34495e')
        heat_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(heat_frame, text="Fire Heat Level (°F):", 
                font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        
        self.heat_scale = tk.Scale(heat_frame, from_=70, to=300, orient=tk.HORIZONTAL,
                                  variable=self.heat_level, command=self.on_heat_change,
                                  bg='#34495e', fg='#ecf0f1', highlightbackground='#34495e',
                                  troughcolor='#2c3e50', activebackground='#e74c3c')
        self.heat_scale.pack(fill=tk.X, pady=5)
        
        self.heat_value_label = tk.Label(heat_frame, text="70°F", 
                                        font=('Arial', 12), fg='#3498db', bg='#34495e')
        self.heat_value_label.pack()
        
    def create_status_display(self, parent):
        """Create system status display widgets"""
        status_frame = tk.Frame(parent, bg='#34495e')
        status_frame.pack(fill=tk.X, padx=10, pady=20)
        
        tk.Label(status_frame, text="System Status:", 
                font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        
        self.status_label = tk.Label(status_frame, text="STANDBY", 
                                    font=('Arial', 14, 'bold'), fg='#4ecdc4', bg='#34495e')
        self.status_label.pack(pady=5)
        
        tk.Label(status_frame, text="Water Pressure:", 
                font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        
        self.pressure_label = tk.Label(status_frame, text="0%", 
                                      font=('Arial', 12), fg='#3498db', bg='#34495e')
        self.pressure_label.pack()
        
        tk.Label(status_frame, text="Trigger Threshold: 155°F - 165°F", 
                font=('Arial', 10), fg='#95a5a6', bg='#34495e').pack(pady=(10, 0))
        
    def setup_sprinkler_panel(self, parent):
        """Setup the center panel with sprinkler visualization"""
        sprinkler_frame = tk.Frame(parent, bg='#2c3e50')
        sprinkler_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Timer label for fire duration (pack BEFORE canvas)
        self.timer_label = tk.Label(sprinkler_frame, text="", font=('Arial', 16, 'bold'), fg='#e74c3c', bg='#2c3e50')
        self.timer_label.pack(pady=5)
        
        self.canvas = tk.Canvas(sprinkler_frame, bg='#1a252f', width=400, height=600)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.draw_sprinkler()

    def on_canvas_resize(self, event):
        """Handle canvas resize and redraw background image"""
        self.load_background_image(event.width, event.height)
        self.draw_sprinkler()

    def load_background_image(self, width=400, height=600):
        """Load and display background image, scaled to canvas size"""
        self.canvas.delete("bg_img")
        try:
            bg_image = Image.open("Images/background.jpg")
            bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.canvas.create_image(width // 2, height // 2, image=self.bg_photo, tags="bg_img")
        except:
            self.canvas.create_rectangle(0, 0, width, height, fill='#1a252f', outline='', tags="bg_img")

    def setup_status_panel(self, parent):
        """Setup the right panel with fuzzy logic display"""
        status_frame = tk.Frame(parent, bg='#34495e', relief=tk.RAISED, bd=2)
        status_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        fuzzy_title = tk.Label(status_frame, text="Fuzzy Logic Controller", 
                              font=('Arial', 16, 'bold'), fg='#ecf0f1', bg='#34495e')
        fuzzy_title.pack(pady=10)
        
        self.create_fuzzy_display(status_frame)
        self.create_membership_display(status_frame)
        
    def create_fuzzy_display(self, parent):
        """Create fuzzy logic output display"""
        heat_fuzzy_frame = tk.Frame(parent, bg='#34495e')
        heat_fuzzy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(heat_fuzzy_frame, text="Heat Level:", 
                font=('Arial', 12), fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT)
        
        self.heat_fuzzy_label = tk.Label(heat_fuzzy_frame, text="Low", 
                                        font=('Arial', 12, 'bold'), fg='#f39c12', bg='#34495e')
        self.heat_fuzzy_label.pack(side=tk.RIGHT)
        
        # Water Output
        water_fuzzy_frame = tk.Frame(parent, bg='#34495e')
        water_fuzzy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(water_fuzzy_frame, text="Water Output:", 
                font=('Arial', 12), fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT)
        
        self.water_fuzzy_label = tk.Label(water_fuzzy_frame, text="None", 
                                         font=('Arial', 12, 'bold'), fg='#f39c12', bg='#34495e')
        self.water_fuzzy_label.pack(side=tk.RIGHT)
        
    def create_membership_display(self, parent):
        """Create membership values display section"""
        separator = tk.Frame(parent, height=2, bg='#7f8c8d')
        separator.pack(fill=tk.X, padx=10, pady=20)
        
        membership_title = tk.Label(parent, text="Membership Values", 
                                   font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e')
        membership_title.pack(pady=(0, 10))
        
        self.heat_membership_frame = tk.Frame(parent, bg='#34495e')
        self.heat_membership_frame.pack(fill=tk.X, padx=10, pady=5)
        
    def animate_water_spray(self):
        """Animate a very fast, realistic outward water splash from the sprinkler head"""
        if not self.animation_running:
            return

        self.canvas.delete("water")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x_center = canvas_width // 2
        y_start = canvas_height // 3 + 55

        num_drops = 40
        splash_length = canvas_height // 2
        spread_angle = math.radians(120)
        base_angle = math.pi / 2

        if not hasattr(self, 'water_splash_drops') or len(self.water_splash_drops) != num_drops:
            self.water_splash_drops = []
            for i in range(num_drops):
                angle = base_angle - spread_angle / 2 + (spread_angle * i / (num_drops - 1))
                self.water_splash_drops.append({'angle': angle, 'progress': 0})

        speed = 0.22
        for drop in self.water_splash_drops:
            drop['progress'] += speed
            if drop['progress'] > 1:
                drop['progress'] = 0

            length = splash_length * drop['progress']
            x = x_center + length * math.cos(drop['angle'])
            y = y_start + length * math.sin(drop['angle'])
            drop_radius = 7 + 10 * drop['progress']

            self.canvas.create_oval(
                x - drop_radius, y - drop_radius,
                x + drop_radius, y + drop_radius,
                fill='#3498db', outline='#2980b9', tags="water"
            )

        self.root.after(16, self.animate_water_spray)

    def animate_fire(self):
        """Show realistic fire image based on heat and timer"""
        self.canvas.delete("fire")

        if not self.is_triggered or not self.fire_img_orig or self.fire_timer <= 0:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x_center = canvas_width // 2
        y_bottom = canvas_height - 40

        min_height, max_height = 60, 320
        timer_ratio = self.fire_timer / int(3 + 12 * ((self.initial_heat - 70) / 230))
        fire_height = int(min_height + (max_height - min_height) * ((self.initial_heat - 70) / 230))
        fire_height = int(fire_height * timer_ratio)
        fire_width = int(fire_height * 0.7)

        fire_img = self.fire_img_orig.resize((fire_width, fire_height), Image.Resampling.LANCZOS)
        self.fire_img = ImageTk.PhotoImage(fire_img)
        self.canvas.create_image(x_center, y_bottom - fire_height // 2, image=self.fire_img, tags="fire")

    def on_heat_change(self, value):
        """Handle heat level slider change"""
        self.heat_value_label.config(text=f"{int(float(value))}°F")
        self.update_system()
        
    def update_system(self):
        """Update the entire system based on current inputs"""
        result = self.fuzzy_controller.calculate_system_response(
            self.heat_level.get(), 0
        )
        self.heat_fuzzy_label.config(text=result['dominant_heat'])
        self.water_fuzzy_label.config(text=result['water_level'])
        self.status_label.config(text=result['system_status'], fg=result['status_color'])
        self.pressure_label.config(text=f"{result['water_pressure']}%")
        self.update_membership_display(result)

    def update_membership_display(self, result):
        for widget in self.heat_membership_frame.winfo_children():
            widget.destroy()
        tk.Label(self.heat_membership_frame, text="Heat:", 
                font=('Arial', 10, 'bold'), fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        for key, value in result['heat_memberships'].items():
            if value > 0.01:
                text = f"{key.capitalize()}: {value:.2f}"
                tk.Label(self.heat_membership_frame, text=text, 
                        font=('Arial', 9), fg='#bdc3c7', bg='#34495e').pack(anchor=tk.W)

    def reset_system(self):
        """Reset the entire system to initial state and unlock inputs"""
        self.is_triggered = False
        self.animation_running = False
        self.heat_level.set(70)
        self.heat_scale.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.NORMAL)
        self.canvas.delete("water")
        self.draw_sprinkler()
        self.update_system()
        self.animate_fire()
        self.timer_label.config(text="")

    def draw_sprinkler(self):
        """Draw the sprinkler head centered on canvas"""
        self.canvas.delete("sprinkler")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width < 1 or canvas_height < 1:
            canvas_width, canvas_height = 400, 600
        x = canvas_width // 2
        y = canvas_height // 3
        self.canvas.create_oval(x-25, y-40, x+25, y+40, 
                               fill='#bdc3c7', outline='#7f8c8d', width=2, tags="sprinkler")
        if not self.is_triggered:
            self.canvas.create_oval(x-8, y+25, x+8, y+40, 
                                   fill='#e74c3c', outline='#c0392b', width=2, tags="sprinkler")
        else:
            self.canvas.create_oval(x-8, y+25, x+8, y+40, 
                                   fill='', outline='#7f8c8d', width=1, tags="sprinkler")
        self.canvas.create_oval(x-20, y+45, x+20, y+55, 
                               fill='#95a5a6', outline='#7f8c8d', width=2, tags="sprinkler")
        self.canvas.create_rectangle(x-15, y-60, x+15, y-40, 
                                    fill='#7f8c8d', outline='#34495e', width=2, tags="sprinkler")

    def start_fire(self):
        """Start the fire demo with selected heat, disable slider and button, and start timer"""
        if self.is_triggered:
            return
        self.heat_scale.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        self.is_triggered = True
        self.initial_heat = self.heat_level.get()
        self.fire_timer = int(3 + 12 * ((self.initial_heat - 70) / 230))
        self.total_fire_time = self.fire_timer  # Store total time for display

        # Only activate sprinkler if heat is above threshold
        if self.initial_heat >= 155:
            self.animation_running = True
            self.timer_label.config(
                text=f"Fire will be extinguished in {self.fire_timer}s (Total: {self.total_fire_time}s)"
            )
            self.animate_water_spray()
        else:
            self.animation_running = False
            self.timer_label.config(
                text=f"Fire is too small for sprinkler activation.\nFire will be extinguished in {self.fire_timer}s (Total: {self.total_fire_time}s)"
            )
            self.canvas.delete("water")

        self.draw_sprinkler()
        self.animate_fire()
        self.countdown_fire_timer()

    def countdown_fire_timer(self):
        """Decrease fire timer, shrink fire as timer runs out"""
        if self.fire_timer > 0 and self.is_triggered:
            self.timer_label.config(
                text=f"Fire will be extinguished in {self.fire_timer}s (Total: {self.total_fire_time}s)"
            )
            self.fire_timer -= 1
            self.animate_fire()
            self.root.after(1000, self.countdown_fire_timer)
        else:
            self.timer_label.config(text="Fire extinguished!")
            self.is_triggered = False
            self.animation_running = False
            self.animate_fire()
            self.heat_scale.config(state=tk.NORMAL)
            self.start_btn.config(state=tk.NORMAL)
