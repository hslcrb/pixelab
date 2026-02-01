"""
File I/O Handler - Save/Load PLB with Vector Objects, Export PNG/SVG
"""
import json
from datetime import datetime
from PIL import Image
import os


class VectorFileHandler:
    """Handles all file operations for vector-based canvas"""
    
    @staticmethod
    def save_plb(filepath, canvas, palette):
        """Save project as .plb file with vector objects"""
        data = {
            "version": "2.0",  # New version for vector support
            "width": canvas.width,
            "height": canvas.height,
            "palette": palette.to_hex_list(),
            "objects": canvas.object_manager.to_dict()['objects'],
            "metadata": {
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "author": "PixeLab User",
                "format": "vector"
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
        
        # Version check
        version = data.get('version', '1.0')
        
        # Support both old pixel-based (1.0) and new vector-based (2.0) formats
        if version not in ['1.0', '2.0']:
            raise ValueError(f"Unsupported PLB version: {version}")
        
        return data
    
    @staticmethod
    def export_png(filepath, canvas, scale=1):
        """Export as PNG image (rasterized from vectors)"""
        # Rasterize vector objects
        pixels_2d = canvas.object_manager.rasterize(canvas.width, canvas.height)
        
        # Create image
        img = Image.new('RGBA', (canvas.width, canvas.height))
        
        # Flatten 2D pixels to 1D
        pixels = []
        for y in range(canvas.height):
            for x in range(canvas.width):
                pixels.append(pixels_2d[y][x])
        
        img.putdata(pixels)
        
        # Scaleup if needed (using NEAREST for pixel art)
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
        """Export as SVG - export vector objects directly"""
        # Ensure .svg extension
        if not filepath.lower().endswith('.svg'):
            filepath += '.svg'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # SVG header
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<svg width="{canvas.width}" height="{canvas.height}" ')
            f.write('xmlns="http://www.w3.org/2000/svg" ')
            f.write('viewBox="0 0 {} {}">\n'.format(canvas.width, canvas.height))
            
            # Rasterize for now (can be enhanced to export true vector later)
            pixels_2d = canvas.object_manager.rasterize(canvas.width, canvas.height)
            
            for y in range(canvas.height):
                for x in range(canvas.width):
                    r, g, b, a = pixels_2d[y][x]
                    
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
