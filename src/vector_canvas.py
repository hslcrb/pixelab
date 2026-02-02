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
        
        # Current tool
        self.current_tool = None
        self.current_tool_name = "Pencil"
        
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
        
        # Tool events
        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        
        # Panning (Middle click or Space+Left click handled via set_pan_mode)
        self.canvas.bind("<Button-2>", lambda e: self.set_pan_mode(True, e))
        self.canvas.bind("<ButtonRelease-2>", lambda e: self.set_pan_mode(False, e))

    def _on_press(self, event):
        """Handle mouse press"""
        if self.is_panning:
            self.pan_start = (event.x, event.y)
            return
            
        px, py = self.screen_to_canvas(event.x, event.y)
        if self.current_tool_name == "Eyedropper":
            color = self.get_pixel(px, py)
            if color and self.current_tool:
                self.current_tool.pick_color(color)
            return

        if self.current_tool:
            self.current_tool.on_press(px, py, self.object_manager)
            self.preview_object = self.current_tool.get_preview_object()
            self.force_render()

    def _on_drag(self, event):
        """Handle mouse drag"""
        if self.is_panning and self.pan_start:
            dx = event.x - self.pan_start[0]
            dy = event.y - self.pan_start[1]
            self.pan(dx, dy)
            self.pan_start = (event.x, event.y)
            return
            
        px, py = self.screen_to_canvas(event.x, event.y)
        if self.current_tool:
            self.current_tool.on_drag(px, py, self.object_manager)
            self.preview_object = self.current_tool.get_preview_object()
            self.force_render()

    def _on_release(self, event):
        """Handle mouse release"""
        if self.is_panning:
            return
            
        px, py = self.screen_to_canvas(event.x, event.y)
        if self.current_tool:
            self.current_tool.on_release(px, py, self.object_manager)
            self.preview_object = None
            self.force_render()
            
            if self.on_change:
                self.on_change()
    
    def set_tool(self, tool_name):
        """Set active tool"""
        from .vector_tools import (
            VectorPencilTool, VectorBrushTool, VectorEraserTool,
            VectorLineTool, VectorRectangleTool, VectorCircleTool,
            VectorEyedropperTool, VectorSelectTool, VectorFillTool
        )
        
        self.current_tool_name = tool_name
        
        # Create tool instance
        color = (0, 0, 0, 1) # dummy, will be set by app
        if tool_name == "Select":
            self.current_tool = VectorSelectTool()
        elif tool_name == "Pencil":
            self.current_tool = VectorPencilTool()
        elif tool_name == "Line":
            self.current_tool = VectorLineTool()
        elif tool_name == "Rectangle":
            self.current_tool = VectorRectangleTool()
        elif tool_name == "Circle":
            self.current_tool = VectorCircleTool()
        elif tool_name == "Eraser":
            self.current_tool = VectorEraserTool()
        elif tool_name == "Brush":
            self.current_tool = VectorBrushTool()
        elif tool_name == "Fill":
            self.current_tool = VectorFillTool()
        elif tool_name == "Eyedropper":
            # Callback will be set by the caller (app)
            self.current_tool = VectorEyedropperTool()
        # Other tools as needed
        
        self.canvas.config(cursor=self.current_tool.get_cursor() if self.current_tool else "crosshair")

    def force_render(self):
        """Request a render as soon as the UI is idle"""
        self.need_render = True
        if not hasattr(self, '_render_queued'):
            self._render_queued = False
        
        if not self._render_queued:
            self._render_queued = True
            # Use after_idle to debounce multiple render requests during a single event loop
            self.canvas.after_idle(self._execute_render)
    
    def _execute_render(self):
        """Internal method to execute the queued render"""
        self._render_queued = False
        self.render()
    
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
            cursor = self.current_tool.get_cursor() if self.current_tool else "crosshair"
            self.canvas.config(cursor=cursor)
    
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
        img = self.object_manager.rasterize(self.width, self.height)
        if 0 <= x < self.width and 0 <= y < self.height:
            return img.getpixel((x, y))
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
        return copy.deepcopy(self.object_manager.layers)
    
    def restore_state(self, state):
        """Restore state from history"""
        self.object_manager.layers = state
        self.need_render = True
        self.render()

    def render(self):
        """Render vector objects to pixel canvas using Image scaling for performance"""
        if not self.need_render:
            return
        
        try:
            canvas_w = self.canvas.winfo_width()
            canvas_h = self.canvas.winfo_height()
            
            if canvas_w < 10 or canvas_h < 10:
                return
            
            # 1. Get Project Raster (1:1)
            project_img = self.object_manager.rasterize(self.width, self.height)
            
            # 2. Add preview object if exists
            if self.preview_object:
                draw_p = ImageDraw.Draw(project_img)
                self.preview_object.draw_to_image(draw_p)
            
            # 3. Create view buffer (Screen size)
            view_img = Image.new('RGB', (canvas_w, canvas_h), color='#1e1e1e')
            draw = ImageDraw.Draw(view_img)
            
            # 4. View properties
            pixel_size = self.zoom_level
            sw = int(self.width * pixel_size)
            sh = int(self.height * pixel_size)
            off_x = int(canvas_w/2 + self.pan_offset[0] - sw/2)
            off_y = int(canvas_h/2 + self.pan_offset[1] - sh/2)
            
            # 5. Draw Checkerboard background efficiently
            c_size = max(4, int(pixel_size / 2))
            if sw > 0 and sh > 0:
                # Create a 2x2 pattern and tile it
                pattern = Image.new('RGB', (c_size*2, c_size*2), (200, 200, 200))
                p_draw = ImageDraw.Draw(pattern)
                p_draw.rectangle([0, 0, c_size-1, c_size-1], fill=(220, 220, 220))
                p_draw.rectangle([c_size, c_size, c_size*2-1, c_size*2-1], fill=(220, 220, 220))
                
                # Create a tiled background by tiling the pattern
                # PIL doesn't have a direct tile method, so we manually paste in a loop
                # but with much larger chunks (c_size*2)
                for y in range(0, sh, c_size*2):
                    for x in range(0, sw, c_size*2):
                        view_img.paste(pattern, (off_x + x, off_y + y))

            # 6. Scale and Paste Project Image
            if sw > 0 and sh > 0:
                scaled_project = project_img.resize((sw, sh), Image.NEAREST)
                view_img.paste(scaled_project, (off_x, off_y), scaled_project)
            
            # 7. Draw Grid
            if self.show_grid and self.zoom_level >= 4:
                grid_color = '#404040'
                for i in range(self.width + 1):
                    gx = off_x + int(i * pixel_size)
                    if 0 <= gx < canvas_w:
                        draw.line([gx, off_y, gx, off_y + sh], fill=grid_color)
                for i in range(self.height + 1):
                    gy = off_y + int(i * pixel_size)
                    if 0 <= gy < canvas_h:
                        draw.line([off_x, gy, off_x + sw, gy], fill=grid_color)
            
            # 8. Draw selection outlines
            for obj in self.object_manager.selected_objects:
                if hasattr(obj, 'get_bounds'):
                    bx0, by0, bx1, by1 = obj.get_bounds()
                    sx0 = off_x + int((bx0 - 0.5) * pixel_size)
                    sy0 = off_y + int((by0 - 0.5) * pixel_size)
                    sx1 = off_x + int((bx1 + 0.5) * pixel_size)
                    sy1 = off_y + int((by1 + 0.5) * pixel_size)
                    draw.rectangle([sx0, sy0, sx1, sy1], outline='#00ffff', width=2)
            
            # 9. Update Graphics
            self.photo_image = ImageTk.PhotoImage(view_img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
            
            # 10. Update Scrollbars
            max_view_w = max(canvas_w, sw + 400)
            max_view_h = max(canvas_h, sh + 400)
            vx = 0.5 - (self.pan_offset[0] / max_view_w)
            vy = 0.5 - (self.pan_offset[1] / max_view_h)
            self.h_scrollbar.set(max(0, vx-0.1), min(1, vx+0.1))
            self.v_scrollbar.set(max(0, vy-0.1), min(1, vy+0.1))
            
            self.need_render = False
            
        except Exception as e:
            print(f"Render error: {e}")
            import traceback
            traceback.print_exc()

