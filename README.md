# Fire Suppression Sprinkler System with Fuzzy Logic Control

A realistic fire suppression sprinkler system simulation using fuzzy logic to control water release based on fire heat level and duration.

## Features

### 🔥 Realistic Sprinkler Design
- **Wet Pipe System**: Simulates the most common sprinkler type used in offices, malls, and homes
- **Glass Bulb Mechanism**: Visual representation of the fusible element that bursts at trigger temperature
- **Deflector Plate**: Realistic sprinkler head design with water distribution deflector
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 🧠 Fuzzy Logic Controller
- **Heat Level Input**: Temperature range from 70°F to 300°F
- **Duration Input**: Fire duration from 0 to 60 seconds
- **Membership Functions**: 
  - Heat: Low, Medium, High, Critical
  - Duration: Short, Medium, Long
  - Output: None, Low, Medium, High water pressure

### 💧 Water Spray System
- **Trigger Threshold**: Activates at 155°F-165°F (realistic temperature range)
- **Dynamic Water Pressure**: Spray intensity based on fuzzy logic output
- **Animated Water Drops**: Realistic falling water animation
- **Auto-Duration Control**: Spray duration calculated based on heat level and required water output

### 📊 Real-time Monitoring
- **System Status**: STANDBY, WARNING, ACTIVE states
- **Water Pressure**: 0-100% pressure indication
- **Fuzzy Logic Display**: Shows current fuzzy set memberships
- **Visual Feedback**: Glass bulb burst animation and color-coded status

## How It Works

### Fuzzy Logic Rules
1. **Low Heat** (70-120°F) + Any Duration = No Water Release
2. **Medium Heat** (100-180°F) + Short Duration = Low Water Release
3. **Medium Heat** + Medium/Long Duration = Medium Water Release  
4. **High Heat** (150-220°F) = Medium to High Water Release
5. **Critical Heat** (200°F+) = Maximum Water Release

### Trigger Mechanism
- System activates when temperature ≥ 155°F AND duration > 0 seconds
- Glass bulb "bursts" with animation effect
- Water spray begins 0.5 seconds after trigger (realistic delay)
- Spray duration calculated: Base 5s × Heat Multiplier × Output Multiplier

## Usage

1. **Adjust Fire Heat Level**: Use the slider to set temperature (70-300°F)
2. **Set Fire Duration**: Use the slider to set how long the fire has been detected (0-60s)
3. **Monitor System**: Watch the fuzzy logic controller determine appropriate response
4. **Reset System**: Click "Reset System" to return to standby mode

## Technical Implementation

- **HTML5**: Semantic structure with accessibility features
- **CSS3**: Advanced animations, gradients, and responsive design
- **Vanilla JavaScript**: Fuzzy logic algorithm implementation
- **Background Integration**: Uses provided background.jpg image

## Files Structure
```
Fire/
├── index.html          # Main HTML structure
├── styles.css          # CSS styling and animations  
├── script.js           # Fuzzy logic controller
├── README.md           # This documentation
└── Images/
    └── background.jpg  # Background image
```

## Browser Compatibility
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

---
*Developed as a fire suppression system simulation with realistic fuzzy logic control algorithms.*
