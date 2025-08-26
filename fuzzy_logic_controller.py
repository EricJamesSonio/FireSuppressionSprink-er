"""
Fuzzy Logic Controller for Fire Suppression System
Handles all fuzzy logic calculations and membership functions
"""

class FuzzyLogicController:
    def __init__(self):
        """Initialize the fuzzy logic controller"""
        pass
    
    def get_heat_membership(self, temp):
        """
        Calculate membership values for heat level fuzzy sets
        
        Args:
            temp (float): Temperature in Fahrenheit
            
        Returns:
            dict: Membership values for each heat level category
        """
        memberships = {
            'low': 0,
            'medium': 0,
            'high': 0,
            'critical': 0
        }
        
        # Low: 70-120°F
        if temp <= 120:
            memberships['low'] = max(0, (120 - temp) / 50)
        
        # Medium: 100-180°F
        if 100 <= temp <= 180:
            if temp <= 140:
                memberships['medium'] = (temp - 100) / 40
            else:
                memberships['medium'] = (180 - temp) / 40
        
        # High: 150-220°F
        if 150 <= temp <= 220:
            if temp <= 185:
                memberships['high'] = (temp - 150) / 35
            else:
                memberships['high'] = (220 - temp) / 35
        
        # Critical: 200°F+
        if temp >= 200:
            memberships['critical'] = min(1, (temp - 200) / 100)
        
        return memberships
    
    def get_duration_membership(self, duration):
        """
        Calculate membership values for duration fuzzy sets
        
        Args:
            duration (float): Duration in seconds
            
        Returns:
            dict: Membership values for each duration category
        """
        memberships = {
            'short': 0,
            'medium': 0,
            'long': 0
        }
        
        # Short: 0-15s
        if duration <= 15:
            memberships['short'] = max(0, (15 - duration) / 15)
        
        # Medium: 10-35s
        if 10 <= duration <= 35:
            if duration <= 22.5:
                memberships['medium'] = (duration - 10) / 12.5
            else:
                memberships['medium'] = (35 - duration) / 12.5
        
        # Long: 25s+
        if duration >= 25:
            memberships['long'] = min(1, (duration - 25) / 35)
        
        return memberships
    
    def get_fuzzy_output(self, heat_memberships, duration_memberships):
        """
        Apply fuzzy rules and calculate defuzzified output
        
        Args:
            heat_memberships (dict): Heat level membership values
            duration_memberships (dict): Duration membership values
            
        Returns:
            float: Defuzzified water output value (0-1)
        """
        rules = [
            # Rule 1: Low heat, any duration = No water
            {'heat': 'low', 'duration': 'short', 'output': 0},
            {'heat': 'low', 'duration': 'medium', 'output': 0},
            {'heat': 'low', 'duration': 'long', 'output': 0},
            
            # Rule 2: Medium heat, short duration = Low water
            {'heat': 'medium', 'duration': 'short', 'output': 0.2},
            {'heat': 'medium', 'duration': 'medium', 'output': 0.4},
            {'heat': 'medium', 'duration': 'long', 'output': 0.6},
            
            # Rule 3: High heat = Medium to high water
            {'heat': 'high', 'duration': 'short', 'output': 0.6},
            {'heat': 'high', 'duration': 'medium', 'output': 0.8},
            {'heat': 'high', 'duration': 'long', 'output': 1.0},
            
            # Rule 4: Critical heat = Maximum water
            {'heat': 'critical', 'duration': 'short', 'output': 0.8},
            {'heat': 'critical', 'duration': 'medium', 'output': 1.0},
            {'heat': 'critical', 'duration': 'long', 'output': 1.0}
        ]
        
        numerator = 0
        denominator = 0
        
        for rule in rules:
            strength = min(
                heat_memberships[rule['heat']],
                duration_memberships[rule['duration']]
            )
            
            numerator += strength * rule['output']
            denominator += strength
        
        return numerator / denominator if denominator > 0 else 0
    
    def get_dominant_membership(self, memberships):
        """
        Get the fuzzy set with highest membership value
        
        Args:
            memberships (dict): Membership values
            
        Returns:
            str: Name of dominant fuzzy set
        """
        max_value = 0
        dominant = ''
        
        for key, value in memberships.items():
            if value > max_value:
                max_value = value
                dominant = key
        
        return dominant if dominant else list(memberships.keys())[0]
    
    def calculate_system_response(self, heat_level, duration):
        """
        Main function to calculate fire suppression system response
        
        Args:
            heat_level (float): Temperature in Fahrenheit
            duration (float): Duration in seconds
            
        Returns:
            dict: Complete system response with all calculated values
        """
        heat_memberships = self.get_heat_membership(heat_level)
        duration_memberships = self.get_duration_membership(duration)
        water_output = self.get_fuzzy_output(heat_memberships, duration_memberships)
        
        # Determine dominant fuzzy sets
        dominant_heat = self.get_dominant_membership(heat_memberships)
        dominant_duration = self.get_dominant_membership(duration_memberships)
        
        # Determine if sprinkler should trigger (155°F-165°F threshold)
        should_trigger = heat_level >= 155 and duration > 0
        
        # Calculate spray duration based on heat level and water output
        base_duration = 5000  # 5 seconds base
        heat_multiplier = max(1, (heat_level - 155) / 50)
        output_multiplier = max(0.5, water_output)
        spray_duration = base_duration * heat_multiplier * output_multiplier
        
        # Determine system status
        if should_trigger:
            system_status = 'ACTIVE'
            status_color = '#ff4444'
        elif heat_level >= 140:
            system_status = 'WARNING'
            status_color = '#ffa726'
        else:
            system_status = 'STANDBY'
            status_color = '#4ecdc4'
        
        # Determine water output level
        if water_output > 0:
            if water_output < 0.3:
                water_level = 'Low'
            elif water_output < 0.7:
                water_level = 'Medium'
            else:
                water_level = 'High'
        else:
            water_level = 'None'
        
        return {
            'heat_memberships': heat_memberships,
            'duration_memberships': duration_memberships,
            'water_output': water_output,
            'dominant_heat': dominant_heat.capitalize(),
            'dominant_duration': dominant_duration.capitalize(),
            'should_trigger': should_trigger,
            'spray_duration': int(spray_duration),
            'system_status': system_status,
            'status_color': status_color,
            'water_level': water_level,
            'water_pressure': int(water_output * 100)
        }
