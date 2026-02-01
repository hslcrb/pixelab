"""
Color Palette Management
"""


class ColorPalette:
    """Manages color palette for quick access"""
    
    def __init__(self):
        # Default palette
        self.colors = [
            (0, 0, 0, 255),          # Black
            (255, 255, 255, 255),    # White
            (128, 128, 128, 255),    # Gray
            (255, 0, 0, 255),        # Red
            (0, 255, 0, 255),        # Green
            (0, 0, 255, 255),        # Blue
            (255, 255, 0, 255),      # Yellow
            (0, 255, 255, 255),      # Cyan
            (255, 0, 255, 255),      # Magenta
            (255, 128, 0, 255),      # Orange
            (128, 0, 255, 255),      # Purple
            (0, 128, 64, 255),       # Dark Green
        ]
    
    def add_color(self, color):
        """Add color to palette"""
        color = tuple(color)
        if color not in self.colors:
            self.colors.append(color)
    
    def remove_color(self, index):
        """Remove color at index"""
        if 0 <= index < len(self.colors):
            del self.colors[index]
    
    def get_color(self, index):
        """Get color at index"""
        if 0 <= index < len(self.colors):
            return self.colors[index]
        return None
    
    def to_hex_list(self):
        """Convert palette to hex color strings"""
        return [self._rgba_to_hex(c) for c in self.colors]
    
    def from_hex_list(self, hex_list):
        """Load palette from hex color strings"""
        self.colors = [self._hex_to_rgba(h) for h in hex_list]
    
    def _rgba_to_hex(self, rgba):
        """Convert RGBA tuple to hex string"""
        r, g, b, a = rgba
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _hex_to_rgba(self, hex_str):
        """Convert hex string to RGBA tuple"""
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            return (r, g, b, 255)
        return (0, 0, 0, 255)
    
    def __len__(self):
        return len(self.colors)
    
    def __iter__(self):
        return iter(self.colors)
