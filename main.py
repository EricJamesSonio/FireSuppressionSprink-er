"""
Main entry point for Fire Suppression System
Imports and runs the modularized application
"""

import tkinter as tk
from gui_components import FireSuppressionGUI


def main():
    """Main function to start the Fire Suppression System application"""
    # Create the main Tkinter window
    root = tk.Tk()
    
    # Initialize the GUI application
    app = FireSuppressionGUI(root)
    
    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
