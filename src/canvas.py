"""
Pixel Canvas - Core drawing surface with zoom and pan capabilities
"""
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw
import copy


class PixelCanvas:
    """High-performance pixel canvas with zoom and pan"""
    
    def __init__(self, parent, width=32, height=32, on_pixel_change=None):
        self.parent = parent
        self.width = width
        self.height = height
        self.on_pixel_change = on_pixel_change
        
        # Pixel data: 2D array of (R, G, B, A) tuples
        self.pixels = [[(255, 255, 255, 255) for _ in range(width)] for _ in range(height)]
        
        # View state
        self.zoom_level = 10.0  # pixels per canvas pixel
        self.pan_offset = [0, 0]
        self.show_grid = True
        
        # Canvas widget
        self.canvas = Canvas(parent, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Rendering cache
        self.photo_image = None
        self.need_render = True
        
        # Mouse state
        self.is_panning = False
        self.pan_start = None
        self.last_draw_pos = None
        
        # Bind events
        self._bind_events()
        
        # Initial render
        self.canvas.after(100, self.render)
    
    def _bind_events(self):
        """Bind mouse and keyboard events"""
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mousewheel)  # Linux scroll down
    
    def _on_resize(self, event):
        """Handle canvas resize"""
        self.need_render = True
        self.render()
    
    def _on_mousewheel(self, event):
        """Handle zoom with mouse wheel"""
        # Get mouse position
        x, y = event.x, event.y
        
        # Determine zoom direction
        if event.num == 4 or event.delta > 0:
            factor = 1.1
        else:
            factor = 0.9
        
        # Calculate new zoom level
        old_zoom = self.zoom_level
        self.zoom_level *= factor
        self.zoom_level = max(0.5, min(100.0, self.zoom_level))
        
        # Adjust pan to zoom toward mouse position
        if old_zoom != self.zoom_level:
            ratio = self.zoom_level / old_zoom
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            
            # Pixel position under mouse
            px = (x - canvas_w/2 - self.pan_offset[0]) / old_zoom
            py = (y - canvas_h/2 - self.pan_offset[1]) / old_zoom
            
            # New offset to keep pixel under mouse
            self.pan_offset[0] = x - canvas_w/2 - px * self.zoom_level
            self.pan_offset[1] = y - canvas_h/2 - py * self.zoom_level
            
            self.need_render = True
            self.render()
    
    def set_pan_mode(self, enabled, event=None):
        """Enable/disable pan mode"""
        if enabled and event:
            self.is_panning = True
            self.pan_start = (event.x, event.y)
            self.canvas.config(cursor="fleur")
        else:
            self.is_panning = False
            self.pan_start = None
            self.canvas.config(cursor="crosshair")
    
    def pan(self, dx, dy):
        """Pan the canvas by screen pixels"""
        self.pan_offset[0] += dx
        self.pan_offset[1] += dy
        self.need_render = True
        self.render()
    
    def screen_to_canvas(self, screen_x, screen_y):
        """Convert screen coordinates to canvas pixel coordinates"""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        # Center of screen to center of canvas
        cx = screen_x - canvas_w/2 - self.pan_offset[0]
        cy = screen_y - canvas_h/2 - self.pan_offset[1]
        
        # Scale by zoom
        px = int(cx / self.zoom_level + self.width / 2)
        py = int(cy / self.zoom_level + self.height / 2)
        
        return px, py
    
    def canvas_to_screen(self, canvas_x, canvas_y):
        """Convert canvas pixel coordinates to screen coordinates"""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        # Relative to canvas center
        cx = (canvas_x - self.width / 2) * self.zoom_level
        cy = (canvas_y - self.height / 2) * self.zoom_level
        
        # Add screen center and pan
        sx = cx + canvas_w/2 + self.pan_offset[0]
        sy = cy + canvas_h/2 + self.pan_offset[1]
        
        return sx, sy
    
    def get_pixel(self, x, y):
        """Get pixel color at (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return None
    
    def set_pixel(self, x, y, color):
        """Set pixel color at (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = tuple(color)
            self.need_render = True
            
            if self.on_pixel_change:
                self.on_pixel_change()
    
    def get_flat_pixels(self):
        """Get pixels as flat list for serialization"""
        flat = []
        for row in self.pixels:
            for pixel in row:
                flat.append(list(pixel))
        return flat
    
    def set_flat_pixels(self, flat_pixels):
        """Set pixels from flat list"""
        if len(flat_pixels) != self.width * self.height:
            raise ValueError("Pixel data size mismatch")
        
        idx = 0
        for y in range(self.height):
            for x in range(self.width):
                self.pixels[y][x] = tuple(flat_pixels[idx])
                idx += 1
        
        self.need_render = True
        self.render()
    
    def clear(self, color=(255, 255, 255, 255)):
        """Clear canvas with given color"""
        for y in range(self.height):
            for x in range(self.width):
                self.pixels[y][x] = color
        self.need_render = True
        self.render()
    
    def copy_pixels(self):
        """Deep copy of pixel data for history"""
        return copy.deepcopy(self.pixels)
    
    def restore_pixels(self, pixels):
        """Restore pixel data from history"""
        self.pixels = copy.deepcopy(pixels)
        self.need_render = True
        self.render()
    
    def resize_canvas(self, new_width, new_height):
        """Resize canvas (destructive)"""
        new_pixels = [[(255, 255, 255, 255) for _ in range(new_width)] for _ in range(new_height)]
        
        # Copy existing pixels
        for y in range(min(self.height, new_height)):
            for x in range(min(self.width, new_width)):
                new_pixels[y][x] = self.pixels[y][x]
        
        self.width = new_width
        self.height = new_height
        self.pixels = new_pixels
        self.need_render = True
        self.render()
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid
        self.need_render = True
        self.render()
    
    def render(self):
        """Render canvas to screen"""
        if not self.need_render:
            return
        
        try:
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            
            if canvas_w < 10 or canvas_h < 10:
                return
            
            # Create image
            img = Image.new('RGB', (canvas_w, canvas_h), color='#1e1e1e')
            draw = ImageDraw.Draw(img)
            
            # Calculate visible area
            pixel_size = max(1, int(self.zoom_level))
            
            # Draw pixels
            for y in range(self.height):
                for x in range(self.width):
                    sx, sy = self.canvas_to_screen(x, y)
                    
                    # Skip if outside view
                    if sx + pixel_size < 0 or sx > canvas_w:
                        continue
                    if sy + pixel_size < 0 or sy > canvas_h:
                        continue
                    
                    r, g, b, a = self.pixels[y][x]
                    
                    # Draw pixel
                    if a > 0:
                        # Handle transparency with checkerboard
                        if a < 255:
                            # Checkerboard pattern
                            checker = ((x + y) % 2) * 30 + 200
                            base_color = (checker, checker, checker)
                            
                            # Alpha blend
                            alpha = a / 255.0
                            final_r = int(r * alpha + base_color[0] * (1 - alpha))
                            final_g = int(g * alpha + base_color[1] * (1 - alpha))
                            final_b = int(b * alpha + base_color[2] * (1 - alpha))
                            color = (final_r, final_g, final_b)
                        else:
                            color = (r, g, b)
                        
                        draw.rectangle(
                            [sx, sy, sx + pixel_size, sy + pixel_size],
                            fill=color
                        )
            
            # Draw grid
            if self.show_grid and self.zoom_level >= 4:
                for y in range(self.height + 1):
                    sx1, sy = self.canvas_to_screen(0, y)
                    sx2, _ = self.canvas_to_screen(self.width, y)
                    draw.line([sx1, sy, sx2, sy], fill='#404040', width=1)
                
                for x in range(self.width + 1):
                    sx, sy1 = self.canvas_to_screen(x, 0)
                    _, sy2 = self.canvas_to_screen(x, self.height)
                    draw.line([sx, sy1, sx, sy2], fill='#404040', width=1)
            
            # Update canvas
            self.photo_image = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
            
            self.need_render = False
            
        except Exception as e:
            print(f"Render error: {e}")
