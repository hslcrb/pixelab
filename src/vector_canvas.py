"""
Vector Canvas - Canvas that manages vector objects and rasterizes them for display
"""
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw
import copy

from .object_manager import ObjectManager


class VectorCanvas:
    """Vector-based canvas with pixel rendering"""
    
    def __init__(self, parent, width=32, height=32, on_change=None):
        self.parent = parent
        self.width = width
        self.height = height
        self.on_change = on_change
        
        # Vector object manager
        self.object_manager = ObjectManager()
        
        # View state
        self.zoom_level = 10.0
        self.pan_offset = [0, 0]
        self.show_grid = True
        
        # Canvas Widget and Scrollbars
        self.canvas_container = tk.Frame(parent, bg="#1e1e1e")
        self.canvas_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_container.grid_rowconfigure(0, weight=1)
        self.canvas_container.grid_columnconfigure(0, weight=1)
        
        self.canvas = Canvas(self.canvas_container, bg="#1e1e1e", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.v_scrollbar = tk.Scrollbar(self.canvas_container, orient=tk.VERTICAL, command=self._on_vscroll)
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.h_scrollbar = tk.Scrollbar(self.canvas_container, orient=tk.HORIZONTAL, command=self._on_hscroll)
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Rendering cache
        self.photo_image = None
        self.need_render = True
        
        # Mouse state
        self.is_panning = False
        self.pan_start = None
        
        # Preview object from current tool
        self.preview_object = None
        
        # Bind events
        self._bind_events()
        
        # Initial render
        self.canvas.after(100, self.render)
    
    def _bind_events(self):
        """Bind mouse and keyboard events"""
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)  # Linux
        self.canvas.bind("<Button-5>", self._on_mousewheel)  # Linux
    
    def _on_resize(self, event):
        """Handle canvas resize"""
        self.need_render = True
        self.render()
    
    def _on_mousewheel(self, event):
        """Handle zoom with mouse wheel"""
        x, y = event.x, event.y
        
        if event.num == 4 or event.delta > 0:
            factor = 1.1
        else:
            factor = 0.9
        
        old_zoom = self.zoom_level
        self.zoom_level *= factor
        self.zoom_level = max(0.5, min(100.0, self.zoom_level))
        
        if old_zoom != self.zoom_level:
            ratio = self.zoom_level / old_zoom
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            
            px = (x - canvas_w/2 - self.pan_offset[0]) / old_zoom
            py = (y - canvas_h/2 - self.pan_offset[1]) / old_zoom
            
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
        """Pan the canvas"""
        self.pan_offset[0] += dx
        self.pan_offset[1] += dy
        self.need_render = True
        self.render()
    
    def _on_vscroll(self, *args):
        """Handle vertical scrollbar"""
        if args[0] == 'scroll':
            # args[1] is amount, args[2] is units
            self.pan(0, -int(args[1]) * 20)
        elif args[0] == 'moveto':
            # args[1] is position (0 to 1)
            # This is complex to map accurately with logical pan, 
            # so we'll just support step scrolling for now
            pass

    def _on_hscroll(self, *args):
        """Handle horizontal scrollbar"""
        if args[0] == 'scroll':
            self.pan(-int(args[1]) * 20, 0)
        elif args[0] == 'moveto':
            pass
    
    def screen_to_canvas(self, screen_x, screen_y):
        """Convert screen coordinates to canvas pixel coordinates"""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        cx = screen_x - canvas_w/2 - self.pan_offset[0]
        cy = screen_y - canvas_h/2 - self.pan_offset[1]
        
        px = int(cx / self.zoom_level + self.width / 2)
        py = int(cy / self.zoom_level + self.height / 2)
        
        return px, py
    
    def canvas_to_screen(self, canvas_x, canvas_y):
        """Convert canvas pixel coordinates to screen coordinates"""
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        cx = (canvas_x - self.width / 2) * self.zoom_level
        cy = (canvas_y - self.height / 2) * self.zoom_level
        
        sx = cx + canvas_w/2 + self.pan_offset[0]
        sy = cy + canvas_h/2 + self.pan_offset[1]
        
        return sx, sy
    
    def get_pixel(self, x, y):
        """Get rendered pixel color at (x, y)"""
        pixels = self.object_manager.rasterize(self.width, self.height)
        if 0 <= y < len(pixels) and 0 <= x < len(pixels[0]):
            return pixels[y][x]
        return None
    
    def add_object(self, obj):
        """Add a vector object"""
        self.object_manager.add_object(obj)
        self.need_render = True
        if self.on_change:
            self.on_change()
    
    def set_preview_object(self, obj):
        """Set preview object for rendering"""
        self.preview_object = obj
        self.need_render = True
    
    def clear_preview(self):
        """Clear preview object"""
        self.preview_object = None
        self.need_render = True
    
    def clear(self, bg_color=(255, 255, 255, 255)):
        """Clear all objects"""
        self.object_manager.clear()
        self.need_render = True
        self.render()
    
    def resize_canvas(self, new_width, new_height):
        """Resize canvas"""
        self.width = new_width
        self.height = new_height
        self.need_render = True
        self.render()
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid
        self.need_render = True
        self.render()
    
    def copy_state(self):
        """Deep copy current state for history"""
        return self.object_manager.copy_objects()
    
    def restore_state(self, state):
        """Restore state from history"""
        self.object_manager.restore_objects(state)
        self.need_render = True
        self.render()
    
    def render(self):
        """Render vector objects to pixel canvas"""
        if not self.need_render:
            return
        
        try:
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            
            if canvas_w < 10 or canvas_h < 10:
                return
            
            # Create background image
            img = Image.new('RGB', (canvas_w, canvas_h), color='#1e1e1e')
            draw = ImageDraw.Draw(img)
            
            # Rasterize vector objects to pixels
            pixels = self.object_manager.rasterize(self.width, self.height)
            
            # Add preview object if exists
            if self.preview_object:
                preview_pixels = self.preview_object.rasterize(self.width, self.height)
                for x, y, color in preview_pixels:
                    if 0 <= y < self.height and 0 <= x < self.width:
                        # Simple blend for preview
                        pixels[y][x] = color
            
            # Render pixels to screen
            pixel_size = max(1, int(self.zoom_level))
            
            for y in range(self.height):
                for x in range(self.width):
                    sx, sy = self.canvas_to_screen(x, y)
                    
                    # Skip if outside view
                    if sx + pixel_size < 0 or sx > canvas_w:
                        continue
                    if sy + pixel_size < 0 or sy > canvas_h:
                        continue
                    
                    r, g, b, a = pixels[y][x]
                    
                    # Draw pixel with transparency handling
                    if a > 0:
                        if a < 255:
                            # Checkerboard for transparency
                            checker = ((x + y) % 2) * 30 + 200
                            base = (checker, checker, checker)
                            
                            alpha_f = a / 255.0
                            final_r = int(r * alpha_f + base[0] * (1 - alpha_f))
                            final_g = int(g * alpha_f + base[1] * (1 - alpha_f))
                            final_b = int(b * alpha_f + base[2] * (1 - alpha_f))
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
            
            # Draw selection outlines (Mint color)
            for obj in self.object_manager.selected_objects:
                if hasattr(obj, 'get_bounds'):
                    x0, y0, x1, y1 = obj.get_bounds()
                    sx0, sy0 = self.canvas_to_screen(x0 - 0.5, y0 - 0.5)
                    sx1, sy1 = self.canvas_to_screen(x1 + 0.5, y1 + 0.5)
                    
                    # Draw mint outline
                    draw.rectangle([sx0, sy0, sx1, sy1], outline='#00ffff', width=2)
            
            # Update canvas
            self.photo_image = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
            
            # Update scrollbars
            # Define logical range as current zoom * 2 + canvas dimensions
            # We use a simple 0..1 range update
            max_pan_x = max(1000, self.width * self.zoom_level)
            max_pan_y = max(1000, self.height * self.zoom_level)
            
            # Update scrollbar positions (very simplified)
            vx = 0.5 - (self.pan_offset[0] / max_pan_x)
            vy = 0.5 - (self.pan_offset[1] / max_pan_y)
            
            self.h_scrollbar.set(max(0, vx-0.1), min(1, vx+0.1))
            self.v_scrollbar.set(max(0, vy-0.1), min(1, vy+0.1))
            
            self.need_render = False
            
        except Exception as e:
            print(f"Render error: {e}")
            import traceback
            traceback.print_exc()
