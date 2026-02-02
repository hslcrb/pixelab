"""
File I/O Handler - Save/Load PLB, Export PNG/SVG
"""
import json
from datetime import datetime
from PIL import Image
import os


class FileHandler:
    """Handles all file operations"""
    
    @staticmethod
    def save_plb(filepath, canvas, palette):
        """Save project as .plb file"""
        # Set palette in manager before saving
        canvas.object_manager.palette_colors = palette.to_hex_list()
        
        # Get data from object manager (includes layers and objects)
        mgr_data = canvas.object_manager.to_dict()
        
        data = {
            "version": "2.1",
            "width": canvas.width,
            "height": canvas.height,
            "layers": mgr_data['layers'],
            "current_layer_index": mgr_data['current_layer_index'],
            "palette": mgr_data['palette'],
            "logs": mgr_data.get('logs', []),
            "metadata": {
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "author": "PixeLab User",
                "software": "PixeLab v2.1"
            }
        }
        
        # Ensure .plb extension
        if not filepath.endswith('.plb'):
            filepath += '.plb'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @staticmethod
    def load_plb(filepath):
        """Load project from .plb file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate data
        if 'width' not in data or 'height' not in data:
            raise ValueError("Invalid PLB file: missing width/height")
        
        return data
    
    @staticmethod
    def export_png(filepath, canvas, scale=1):
        """Export as PNG image"""
        # Create image
        img = Image.new('RGBA', (canvas.width, canvas.height))
        
        # Get pixel data
        pixels = []
        for y in range(canvas.height):
            for x in range(canvas.width):
                pixels.append(canvas.get_pixel(x, y))
        
        img.putdata(pixels)
        
        # Scale up if needed (using NEAREST for pixel art)
        if scale > 1:
            new_size = (canvas.width * scale, canvas.height * scale)
            img = img.resize(new_size, Image.NEAREST)
        
        # Ensure .png extension
        if not filepath.lower().endswith('.png'):
            filepath += '.png'
        
        img.save(filepath, 'PNG')
        return filepath
    
    @staticmethod
    def export_svg(filepath, canvas):
        """Export as SVG vector image"""
        # Ensure .svg extension
        if not filepath.lower().endswith('.svg'):
            filepath += '.svg'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # SVG header
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<svg width="{canvas.width}" height="{canvas.height}" ')
            f.write('xmlns="http://www.w3.org/2000/svg" ')
            f.write('viewBox="0 0 {} {}">\n'.format(canvas.width, canvas.height))
            
            # Write each pixel as a rectangle
            for y in range(canvas.height):
                for x in range(canvas.width):
                    r, g, b, a = canvas.get_pixel(x, y)
                    
                    # Skip fully transparent pixels
                    if a == 0:
                        continue
                    
                    opacity = a / 255.0
                    f.write(f'  <rect x="{x}" y="{y}" width="1" height="1" ')
                    f.write(f'fill="rgb({r},{g},{b})" ')
                    
                    if opacity < 1.0:
                        f.write(f'opacity="{opacity:.3f}" ')
                    
                    f.write('/>\n')
            
            f.write('</svg>\n')
        
        return filepath
    
    @staticmethod
    def get_file_info(filepath):
        """Get file information"""
        if not os.path.exists(filepath):
            return None
        
        stat = os.stat(filepath)
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime)
        }
