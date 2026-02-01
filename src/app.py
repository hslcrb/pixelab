"""
Main Application Class
"""
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import copy

from .canvas import PixelCanvas
from .palette import ColorPalette
from .file_handler import FileHandler
from .tools import (
    PencilTool, BrushTool, EraserTool, FillTool,
    EyedropperTool, LineTool, RectangleTool, CircleTool
)
from .ui.menubar import MenuBar
from .ui.toolbar import Toolbar
from .ui.colorpicker import ColorPicker


class History:
    """Undo/Redo history manager"""
    
    def __init__(self, max_size=50):
        self.max_size = max_size
        self.undo_stack = []
        self.redo_stack = []
    
    def push(self, state):
        """Push new state"""
        self.undo_stack.append(copy.deepcopy(state))
        
        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)
        
        self.redo_stack.clear()
    
    def can_undo(self):
        return len(self.undo_stack) > 1
    
    def can_redo(self):
        return len(self.redo_stack) > 0
    
    def undo(self):
        if self.can_undo():
            current = self.undo_stack.pop()
            self.redo_stack.append(current)
            return copy.deepcopy(self.undo_stack[-1])
        return None
    
    def redo(self):
        if self.can_redo():
            state = self.redo_stack.pop()
            self.undo_stack.append(state)
            return copy.deepcopy(state)
        return None


class PixelLabApp:
    """Main PixeLab application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PixeLab - Pixel Art Editor")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")
        
        # Application state
        self.current_file = None
        self.modified = False
        self.palette = ColorPalette()
        self.history = History()
        self.current_color = (0, 0, 0, 255)
        
        # Tools
        self.tools = {}
        self._init_tools()
        self.current_tool = self.tools["Pencil"]
        
        # Setup UI
        self._setup_ui()
        
        # Bind global shortcuts
        self._bind_shortcuts()
        
        # Canvas mouse events
        self.is_drawing = False
        self.canvas_widget.canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self.canvas_widget.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas_widget.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        
        # Space for panning
        self.root.bind("<KeyPress-space>", self._on_space_press)
        self.root.bind("<KeyRelease-space>", self._on_space_release)
        
        # Save initial state
        self.history.push(self.canvas_widget.copy_pixels())
    
    def _init_tools(self):
        """Initialize all tools"""
        self.tools["Pencil"] = PencilTool(self.current_color)
        self.tools["Brush"] = BrushTool(self.current_color, size=3)
        self.tools["Eraser"] = EraserTool(size=3)
        self.tools["Fill"] = FillTool(self.current_color)
        self.tools["Eyedropper"] = EyedropperTool(color_callback=self._on_eyedropper_pick)
        self.tools["Line"] = LineTool(self.current_color)
        self.tools["Rectangle"] = RectangleTool(self.current_color, filled=False)
        self.tools["Circle"] = CircleTool(self.current_color, filled=False)
    
    def _setup_ui(self):
        """Setup user interface"""
        # Menu bar
        self.menubar = MenuBar(self.root, self)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#1e1e1e")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar (left)
        self.toolbar = Toolbar(main_container, self)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Canvas (center)
        canvas_container = tk.Frame(main_container, bg="#1e1e1e")
        canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Top bar (zoom controls)
        top_bar = tk.Frame(canvas_container, bg="#2b2b2b", height=40)
        top_bar.pack(side=tk.TOP, fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Zoom controls
        tk.Label(
            top_bar,
            text="Zoom:",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(10, 5))
        
        self.zoom_var = tk.DoubleVar(value=10.0)
        zoom_scale = tk.Scale(
            top_bar,
            from_=0.5,
            to=100.0,
            orient=tk.HORIZONTAL,
            variable=self.zoom_var,
            command=self._on_zoom_change,
            bg="#3c3c3c",
            fg="#ffffff",
            highlightthickness=0,
            troughcolor="#2b2b2b",
            length=200
        )
        zoom_scale.pack(side=tk.LEFT, padx=5)
        
        self.zoom_label = tk.Label(
            top_bar,
            text="1000%",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 9),
            width=6
        )
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        # Canvas
        self.canvas_widget = PixelCanvas(
            canvas_container,
            width=32,
            height=32,
            on_pixel_change=self._on_canvas_change
        )
        
        # Color picker (right)
        self.color_picker = ColorPicker(main_container, self, self.palette)
        self.color_picker.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_bar = tk.Frame(self.root, bg="#2b2b2b", height=25)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="Ready",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 9),
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.pos_label = tk.Label(
            self.status_bar,
            text="",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 9)
        )
        self.pos_label.pack(side=tk.RIGHT, padx=10)
        
        # Mouse position tracking
        self.canvas_widget.canvas.bind("<Motion>", self._on_mouse_move)
        
        # Select default tool (after canvas is created)
        self.toolbar.select_tool_by_name("Pencil")
    
    def _bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-S>", lambda e: self.save_file_as())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        
        # Tool shortcuts
        self.root.bind("p", lambda e: self.select_tool("Pencil"))
        self.root.bind("b", lambda e: self.select_tool("Brush"))
        self.root.bind("e", lambda e: self.select_tool("Eraser"))
        self.root.bind("f", lambda e: self.select_tool("Fill"))
        self.root.bind("i", lambda e: self.select_tool("Eyedropper"))
        self.root.bind("l", lambda e: self.select_tool("Line"))
        self.root.bind("r", lambda e: self.select_tool("Rectangle"))
        self.root.bind("c", lambda e: self.select_tool("Circle"))
        
        # View shortcuts
        self.root.bind("g", lambda e: self.toggle_grid())
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.reset_zoom())
    
    def _on_mouse_move(self, event):
        """Update mouse position display"""
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        if 0 <= px < self.canvas_widget.width and 0 <= py < self.canvas_widget.height:
            self.pos_label.config(text=f"({px}, {py})")
        else:
            self.pos_label.config(text="")
    
    def _on_mouse_press(self, event):
        """Handle mouse press"""
        if self.canvas_widget.is_panning:
            return
        
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        if 0 <= px < self.canvas_widget.width and 0 <= py < self.canvas_widget.height:
            self.is_drawing = True
            self.current_tool.on_press(px, py, self.canvas_widget)
            self.canvas_widget.render()
    
    def _on_mouse_drag(self, event):
        """Handle mouse drag"""
        if self.canvas_widget.is_panning:
            if self.canvas_widget.pan_start:
                dx = event.x - self.canvas_widget.pan_start[0]
                dy = event.y - self.canvas_widget.pan_start[1]
                self.canvas_widget.pan(dx, dy)
                self.canvas_widget.pan_start = (event.x, event.y)
            return
        
        if not self.is_drawing:
            return
        
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        self.current_tool.on_drag(px, py, self.canvas_widget)
        self.canvas_widget.render()
    
    def _on_mouse_release(self, event):
        """Handle mouse release"""
        if self.canvas_widget.is_panning:
            return
        
        if not self.is_drawing:
            return
        
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        self.current_tool.on_release(px, py, self.canvas_widget)
        self.canvas_widget.render()
        self.is_drawing = False
        
        # Save state for undo
        self._push_history()
    
    def _on_space_press(self, event):
        """Enable pan mode"""
        self.canvas_widget.set_pan_mode(True, event)
    
    def _on_space_release(self, event):
        """Disable pan mode"""
        self.canvas_widget.set_pan_mode(False)
    
    def _on_canvas_change(self):
        """Canvas was modified"""
        self.modified = True
        self._update_title()
    
    def _on_zoom_change(self, value):
        """Zoom slider changed"""
        zoom = float(value)
        self.canvas_widget.zoom_level = zoom
        self.canvas_widget.need_render = True
        self.canvas_widget.render()
        
        percent = int(zoom * 10)
        self.zoom_label.config(text=f"{percent}%")
    
    def _on_eyedropper_pick(self, color):
        """Eyedropper picked a color"""
        self.set_color(color)
        self.color_picker.set_color(color)
    
    def _update_title(self):
        """Update window title"""
        filename = self.current_file or "Untitled"
        modified = "*" if self.modified else ""
        self.root.title(f"PixeLab - {filename}{modified}")
    
    def _push_history(self):
        """Save current state to history"""
        self.history.push(self.canvas_widget.copy_pixels())
    
    # Menu commands
    
    def new_file(self):
        """Create new file"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Save Changes",
                "Do you want to save changes before creating a new file?"
            )
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_file()
        
        # Ask for canvas size
        width = simpledialog.askinteger("New Canvas", "Width (pixels):", initialvalue=32, minvalue=1, maxvalue=512)
        if not width:
            return
        
        height = simpledialog.askinteger("New Canvas", "Height (pixels):", initialvalue=32, minvalue=1, maxvalue=512)
        if not height:
            return
        
        self.canvas_widget.resize_canvas(width, height)
        self.canvas_widget.clear()
        self.current_file = None
        self.modified = False
        self.history = History()
        self._push_history()
        self._update_title()
        self.status_label.config(text=f"New canvas created: {width}x{height}")
    
    def open_file(self):
        """Open PLB file"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Save Changes",
                "Do you want to save changes before opening a file?"
            )
            if response is None:
                return
            elif response:
                self.save_file()
        
        filepath = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("PixeLab Files", "*.plb"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            data = FileHandler.load_plb(filepath)
            
            # Resize canvas
            self.canvas_widget.resize_canvas(data['width'], data['height'])
            
            # Load pixels
            self.canvas_widget.set_flat_pixels(data['pixels'])
            
            # Load palette
            if 'palette' in data:
                self.palette.from_hex_list(data['palette'])
                self.color_picker.refresh_palette()
            
            self.current_file = filepath
            self.modified = False
            self.history = History()
            self._push_history()
            self._update_title()
            self.status_label.config(text=f"Opened: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}")
    
    def save_file(self):
        """Save current file"""
        if self.current_file:
            try:
                FileHandler.save_plb(self.current_file, self.canvas_widget, self.palette)
                self.modified = False
                self._update_title()
                self.status_label.config(text=f"Saved: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save as new file"""
        filepath = filedialog.asksaveasfilename(
            title="Save Project As",
            defaultextension=".plb",
            filetypes=[("PixeLab Files", "*.plb"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            filepath = FileHandler.save_plb(filepath, self.canvas_widget, self.palette)
            self.current_file = filepath
            self.modified = False
            self._update_title()
            self.status_label.config(text=f"Saved as: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")
    
    def export_png(self):
        """Export as PNG"""
        # Ask for scale
        scale = simpledialog.askinteger(
            "Export PNG",
            "Scale factor (1-16):",
            initialvalue=1,
            minvalue=1,
            maxvalue=16
        )
        
        if not scale:
            return
        
        filepath = filedialog.asksaveasfilename(
            title="Export PNG",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            filepath = FileHandler.export_png(filepath, self.canvas_widget, scale)
            self.status_label.config(text=f"Exported PNG: {filepath}")
            messagebox.showinfo("Success", f"Exported to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PNG:\n{e}")
    
    def export_svg(self):
        """Export as SVG"""
        filepath = filedialog.asksaveasfilename(
            title="Export SVG",
            defaultextension=".svg",
            filetypes=[("SVG Files", "*.svg"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            filepath = FileHandler.export_svg(filepath, self.canvas_widget)
            self.status_label.config(text=f"Exported SVG: {filepath}")
            messagebox.showinfo("Success", f"Exported to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export SVG:\n{e}")
    
    def undo(self):
        """Undo last action"""
        state = self.history.undo()
        if state:
            self.canvas_widget.restore_pixels(state)
            self.status_label.config(text="Undo")
    
    def redo(self):
        """Redo last undone action"""
        state = self.history.redo()
        if state:
            self.canvas_widget.restore_pixels(state)
            self.status_label.config(text="Redo")
    
    def clear_canvas(self):
        """Clear canvas"""
        if messagebox.askyesno("Clear Canvas", "Clear entire canvas?"):
            self._push_history()
            self.canvas_widget.clear()
            self.status_label.config(text="Canvas cleared")
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        self.canvas_widget.toggle_grid()
        state = "shown" if self.canvas_widget.show_grid else "hidden"
        self.status_label.config(text=f"Grid {state}")
    
    def zoom_in(self):
        """Zoom in"""
        self.canvas_widget.zoom_level *= 1.2
        self.canvas_widget.zoom_level = min(100.0, self.canvas_widget.zoom_level)
        self.zoom_var.set(self.canvas_widget.zoom_level)
        self.canvas_widget.need_render = True
        self.canvas_widget.render()
    
    def zoom_out(self):
        """Zoom out"""
        self.canvas_widget.zoom_level /= 1.2
        self.canvas_widget.zoom_level = max(0.5, self.canvas_widget.zoom_level)
        self.zoom_var.set(self.canvas_widget.zoom_level)
        self.canvas_widget.need_render = True
        self.canvas_widget.render()
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        self.canvas_widget.zoom_level = 10.0
        self.zoom_var.set(10.0)
        self.canvas_widget.need_render = True
        self.canvas_widget.render()
    
    def select_tool(self, tool_name):
        """Select a tool"""
        if tool_name in self.tools:
            self.current_tool = self.tools[tool_name]
            self.current_tool.set_color(self.current_color)
            self.canvas_widget.canvas.config(cursor=self.current_tool.get_cursor())
            self.status_label.config(text=f"Tool: {tool_name}")
    
    def set_color(self, color):
        """Set current color"""
        self.current_color = tuple(color)
        for tool in self.tools.values():
            if hasattr(tool, 'set_color') and tool != self.tools["Eraser"]:
                tool.set_color(color)
    
    def set_tool_size(self, size):
        """Set tool size (for brush/eraser)"""
        if isinstance(self.current_tool, (BrushTool, EraserTool)):
            self.current_tool.set_size(size)
    
    def set_tool_filled(self, filled):
        """Set filled option (for shapes)"""
        if isinstance(self.current_tool, (RectangleTool, CircleTool)):
            self.current_tool.filled = filled
    
    def quit(self):
        """Quit application"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Save Changes",
                "Do you want to save changes before quitting?"
            )
            if response is None:
                return
            elif response:
                self.save_file()
        
        self.root.quit()
