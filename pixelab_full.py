#!/usr/bin/env python3
"""
PixeLab Full - Complete Vector-Pixel Editor with Full UI
완전한 UI를 갖춘 벡터-픽셀 에디터
"""
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Menu

try:
    from src.vector_canvas import VectorCanvas
    from src.vector_tools import *
    from src.palette import ColorPalette
    from src.vector_file_handler import VectorFileHandler
    from src.object_manager import ObjectManager  
    from src.image_import import ImageImporter
    from src.i18n import t, toggle_language, get_language
    from src.ui.toolbar import Toolbar
    from src.ui.colorpicker import ColorPicker
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all modules are in src/")
    sys.exit(1)


class PixelLabFullApp:
    """Complete PixeLab application with full UI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PixeLab v2.1 - Vector-Pixel Editor")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")
        
        # State
        self.current_color = (0, 0, 0, 255)
        self.current_tool = None
        self.file_handler = VectorFileHandler()
        self.palette = ColorPalette()
        self.current_file = None
        self.modified = False
        
        # Init tools first
        self._init_tools()
        
        # Setup UI
        self._setup_ui()
        self._create_menu()
        self._bind_events()
        
        # Status
        self._update_status()
        
        print("PixeLab v2.1 - Full UI Version")
        print("단축키: F1(한/영) V(선택) P(연필) Ctrl+I(가져오기) Ctrl+G(그룹)")
    
    def _setup_ui(self):
        """Setup UI components"""
        # Main container
        main_container = tk.Frame(self.root, bg="#1e1e1e")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Toolbar
        self.toolbar = Toolbar(main_container, self)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Center - Canvas frame
        canvas_frame = tk.Frame(main_container, bg="#2b2b2b")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Zoom controls
        zoom_frame = tk.Frame(canvas_frame, bg="#2b2b2b")
        zoom_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        self.zoom_title = tk.Label(zoom_frame, text=t('zoom_label'), bg="#2b2b2b", fg="white")
        self.zoom_title.pack(side=tk.LEFT, padx=5)
        
        zoom_out_btn = tk.Button(zoom_frame, text="-", command=self._zoom_out, bg="#3c3c3c", fg="white")
        zoom_out_btn.pack(side=tk.LEFT, padx=2)
        
        self.zoom_label = tk.Label(zoom_frame, text="10x", bg="#2b2b2b", fg="white", width=6)
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        zoom_in_btn = tk.Button(zoom_frame, text="+", command=self._zoom_in, bg="#3c3c3c", fg="white")
        zoom_in_btn.pack(side=tk.LEFT, padx=2)
        
        # Canvas Widget
        self.canvas_widget = VectorCanvas(canvas_frame, width=32, height=32, on_change=self._on_canvas_change)
        
        # Right panel - Container for ColorPicker and LayerPanel
        right_container = tk.Frame(main_container, bg="#2b2b2b", width=200)
        right_container.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Color picker (Top half of right panel)
        self.color_picker = ColorPicker(right_container, self.palette, self._on_color_change)
        self.color_picker.pack(side=tk.TOP, fill=tk.X)
        self.color_picker.config(height=350)
        
        # Separator
        tk.Frame(right_container, bg="#444444", height=2).pack(fill=tk.X, pady=5)
        
        # Layer panel (Bottom half of right panel)
        from src.ui.layerpanel import LayerPanel
        self.layer_panel = LayerPanel(right_container, self.canvas_widget.object_manager, self.canvas_widget.force_render)
        self.layer_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg="#2b2b2b", height=25)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text=f"{t('ready')}",
            bg="#2b2b2b",
            fg="#ffffff",
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.pos_label = tk.Label(
            status_frame,
            text="",
            bg="#2b2b2b",
            fg="#ffffff",
            anchor=tk.E,
            padx=10
        )
        self.pos_label.pack(side=tk.RIGHT)
        
        # Mouse tracking
        self.canvas_widget.canvas.bind("<Motion>", self._on_mouse_move)
        
        
        # Select default tool after UI is ready
        self.toolbar.select_tool_by_name("Mouse")
    
    def _init_tools(self):
        """Initialize tools"""
        self.tools = {
            "Mouse": VectorMouseTool(),
            "Select": VectorSelectTool(),
            "Pencil": VectorPencilTool(self.current_color),
            "Brush": VectorBrushTool(self.current_color, 3),
            "Eraser": VectorEraserTool(3),
            "Line": VectorLineTool(self.current_color),
            "Rectangle": VectorRectangleTool(self.current_color, False),
            "Circle": VectorCircleTool(self.current_color, False),
            "Fill": VectorFillTool(self.current_color),
            "Eyedropper": VectorEyedropperTool(self._on_eyedropper_pick),
        }
        self.current_tool = self.tools["Mouse"]
    
    def _create_menu(self):
        """Create menu bar"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=t('file'), menu=file_menu)
        file_menu.add_command(label=t('new'), command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label=t('open'), command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label=t('save'), command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label=t('save_as'), command=self.save_file_as, accelerator="Ctrl+Sh+S")
        file_menu.add_separator()
        file_menu.add_command(label=t('import_image'), command=self.import_image, accelerator="Ctrl+I")
        file_menu.add_separator()
        file_menu.add_command(label=t('export_png'), command=self.export_png)
        file_menu.add_command(label=t('export_svg'), command=self.export_svg)
        file_menu.add_separator()
        file_menu.add_command(label=t('canvas_size'), command=self.change_canvas_size)
        file_menu.add_separator()
        file_menu.add_command(label=t('exit'), command=self.quit_app)
        
        # Edit menu
        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=t('edit'), menu=edit_menu)
        edit_menu.add_command(label=t('group'), command=self.group_objects, accelerator="Ctrl+G")
        edit_menu.add_command(label=t('ungroup'), command=self.ungroup_objects, accelerator="Ctrl+U")
        edit_menu.add_separator()
        edit_menu.add_command(label=t('clear_canvas'), command=self.clear_canvas)
        
        # View menu
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=t('view'), menu=view_menu)
        view_menu.add_command(label=t('toggle_grid'), command=self.toggle_grid, accelerator="G")
        view_menu.add_command(label=t('zoom_in'), command=self._zoom_in, accelerator="+")
        view_menu.add_command(label=t('zoom_out'), command=self._zoom_out, accelerator="-")
        view_menu.add_separator()
        view_menu.add_command(label="한/영 전환", command=self.toggle_language, accelerator="F1")
        
        self.menubar = menubar
    
    def _bind_events(self):
        """Bind keyboard and mouse events"""
        # Mouse (Right click and Panning)
        self.canvas_widget.canvas.bind("<ButtonPress-3>", self._on_right_click)
        
        # Keyboard
        self.root.bind("<F1>", lambda e: self.toggle_language())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-S>", lambda e: self.save_file_as())
        self.root.bind("<Control-i>", lambda e: self.import_image())
        self.root.bind("<Control-g>", lambda e: self.group_objects())
        self.root.bind("<Control-u>", lambda e: self.ungroup_objects())
        self.root.bind("<Delete>", lambda e: self.delete_selected())
        
        # Tool shortcuts
        self.root.bind("v", lambda e: self.select_tool("Select"))
        self.root.bind("m", lambda e: self.select_tool("Select"))
        self.root.bind("p", lambda e: self.select_tool("Pencil"))
        self.root.bind("b", lambda e: self.select_tool("Brush"))
        self.root.bind("e", lambda e: self.select_tool("Eraser"))
        self.root.bind("l", lambda e: self.select_tool("Line"))
        self.root.bind("r", lambda e: self.select_tool("Rectangle"))
        self.root.bind("c", lambda e: self.select_tool("Circle"))
        self.root.bind("f", lambda e: self.select_tool("Fill"))
        self.root.bind("i", lambda e: self.select_tool("Eyedropper"))
        
        self.root.bind("g", lambda e: self.toggle_grid())
        self.root.bind("<plus>", lambda e: self._zoom_in())
        self.root.bind("<minus>", lambda e: self._zoom_out())
        self.root.bind("<Control-plus>", lambda e: self._zoom_in())
        self.root.bind("<Control-equal>", lambda e: self._zoom_in())
        self.root.bind("<Control-minus>", lambda e: self._zoom_out())
        
        # Arrow key navigation
        self.root.bind("<Left>", lambda e: self.canvas_widget.pan(20, 0))
        self.root.bind("<Right>", lambda e: self.canvas_widget.pan(-20, 0))
        self.root.bind("<Up>", lambda e: self.canvas_widget.pan(0, 20))
        self.root.bind("<Down>", lambda e: self.canvas_widget.pan(0, -20))
    
    def select_tool(self, name):
        """Select tool"""
        self.canvas_widget.set_tool(name)
        if self.canvas_widget.current_tool:
            self.canvas_widget.current_tool.set_color(self.current_color)
            if hasattr(self.canvas_widget.current_tool, 'set_size'):
                self.canvas_widget.current_tool.set_size(self.toolbar.size_var.get())
            if hasattr(self.canvas_widget.current_tool, 'filled'):
                self.canvas_widget.current_tool.filled = self.toolbar.filled_var.get()
            if name == "Eyedropper":
                self.canvas_widget.current_tool.color_callback = self._on_eyedropper_pick
                
        self.canvas_widget.force_render()
        self._update_title() # Might be modified
        self._update_status(f"{t('tool')}: {t(name.lower())}")
    
    def set_tool_size(self, size):
        """Set brush/eraser size"""
        if hasattr(self.canvas_widget.current_tool, 'set_size'):
            self.canvas_widget.current_tool.set_size(size)
    
    def set_tool_filled(self, filled):
        """Set shape filled option"""
        if hasattr(self.canvas_widget.current_tool, 'filled'):
            self.canvas_widget.current_tool.filled = filled
    
    def _on_color_change(self, color):
        """Handle color change"""
        self.current_color = color
        if self.canvas_widget.current_tool:
            self.canvas_widget.current_tool.set_color(color)
        
        # PROACTIVE: If we have selected objects, change their color too!
        # This addresses "Can I never change pixel color once set?"
        sel_count = len(self.canvas_widget.object_manager.selected_objects)
        if sel_count > 0:
            count = self.canvas_widget.object_manager.change_selected_color(color)
            self.canvas_widget.force_render()
            if count > 0:
                self._update_status(f"{count} {t('objects')} {t('selected')} -> {t('color')} {t('changed')}")
    
    def _on_eyedropper_pick(self, color):
        """Handle eyedropper color pick"""
        self.current_color = color
        self.color_picker.update_current_color(color)
    
    def _on_canvas_change(self):
        """Handle canvas change"""
        self.modified = True
        self._update_title()
    
    def _on_mouse_press(self, event):
        """Mouse press"""
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        if 0 <= px < self.canvas_widget.width and 0 <= py < self.canvas_widget.height:
            # Eyedropper special handling
            if isinstance(self.current_tool, VectorEyedropperTool):
                color = self.canvas_widget.get_pixel(px, py)
                if color:
                    self.current_tool.pick_color(color)
                return
            
            self.current_tool.on_press(px, py, self.canvas_widget.object_manager)
            
            if hasattr(self.current_tool, 'get_preview_object'):
                self.canvas_widget.set_preview_object(self.current_tool.get_preview_object())
            
            self.canvas_widget.render()
    
    def _on_mouse_drag(self, event):
        """Mouse drag"""
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        self.current_tool.on_drag(px, py, self.canvas_widget.object_manager)
        
        if hasattr(self.current_tool, 'get_preview_object'):
            self.canvas_widget.set_preview_object(self.current_tool.get_preview_object())
        
        self.canvas_widget.render()
        self.pos_label.config(text=f"{t('position')}: ({px}, {py})")
    
    def _on_mouse_release(self, event):
        """Mouse release"""
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        self.current_tool.on_release(px, py, self.canvas_widget.object_manager)
        
        self.canvas_widget.clear_preview()
        self.canvas_widget.render()
        
        obj_count = len(self.canvas_widget.object_manager.objects)
        sel_count = len(self.canvas_widget.object_manager.selected_objects)
        self._update_status(f"{obj_count} {t('objects')}, {sel_count} {t('selected')}")
    
    def _on_mouse_move(self, event):
        """Mouse move"""
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        if 0 <= px < self.canvas_widget.width and 0 <= py < self.canvas_widget.height:
            self.pos_label.config(text=f"{t('position')}: ({px}, {py})")
    
    def _on_right_click(self, event):
        """Right-click context menu"""
        sel_count = len(self.canvas_widget.object_manager.selected_objects)
        
        print(f"[DEBUG] Right-click: {sel_count} objects selected")
        
        if sel_count == 0:
            print("[DEBUG] No objects selected, showing no menu")
            return
        
        context_menu = Menu(self.root, tearoff=0)
        
        # Change Color
        context_menu.add_command(
            label=f"{t('change_color')}... ({sel_count})",
            command=self.change_selected_color
        )
        
        context_menu.add_separator()
        
        # Group/Ungroup
        if sel_count >= 2:
            context_menu.add_command(label=t('group'), command=self.group_objects)
        
        from src.vector_objects import VectorGroup
        has_groups = any(isinstance(obj, VectorGroup) for obj in self.canvas_widget.object_manager.selected_objects)
        if has_groups:
            context_menu.add_command(label=t('ungroup'), command=self.ungroup_objects)
        
        context_menu.add_separator()
        context_menu.add_command(
            label=t('delete'),
            command=self.delete_selected
        )
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def _zoom_in(self):
        """Zoom in"""
        self.canvas_widget.zoom_level = min(100, self.canvas_widget.zoom_level * 1.2)
        self.canvas_widget.need_render = True
        self.canvas_widget.render()
        self.zoom_label.config(text=f"{int(self.canvas_widget.zoom_level)}x")
    
    def _zoom_out(self):
        """Zoom out"""
        self.canvas_widget.zoom_level = max(0.5, self.canvas_widget.zoom_level / 1.2)
        self.canvas_widget.need_render = True
        self.canvas_widget.render()
        self.zoom_label.config(text=f"{int(self.canvas_widget.zoom_level)}x")
        
    def show_help(self):
        """Show help dialog"""
        help_win = tk.Toplevel(self.root)
        help_win.title(t('help_text'))
        help_win.geometry("400x300")
        help_win.resizable(False, False)
        
        frame = tk.Frame(help_win, padx=20, pady=20, bg="#2b2b2b")
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text=t('help_text'), fg="white", bg="#2b2b2b", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        tk.Label(frame, text=t('panning_help'), fg="white", bg="#2b2b2b", justify=tk.LEFT).pack(anchor="w", pady=5)
        tk.Label(frame, text=t('tools_help'), fg="white", bg="#2b2b2b", justify=tk.LEFT).pack(anchor="w", pady=5)
        
        shortcuts = [
            "Ctrl + N: New",
            "Ctrl + O: Open",
            "Ctrl + S: Save",
            "Ctrl + I: Import",
            "Ctrl + G: Group",
            "Ctrl + U: Ungroup",
            "Delete: Delete Selected",
            "G: Toggle Grid",
            "F1: Toggle Language",
            "Shift + Mouse Wheel: Horizontal Pan"
        ]
        
        s_frame = tk.Frame(frame, bg="#3c3c3c", padx=10, pady=10)
        s_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        for s in shortcuts:
            tk.Label(s_frame, text=s, fg="#cccccc", bg="#3c3c3c", font=("Courier", 9)).pack(anchor="w")
            
        tk.Button(frame, text="OK", command=help_win.destroy).pack(pady=10)

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(t('about'), "PixeLab v2.1\nVector-Pixel Hybrid Editor\nCreated by rheehose")
    
    def toggle_grid(self):
        """Toggle grid"""
        self.canvas_widget.toggle_grid()
        status = t('grid_shown') if self.canvas_widget.show_grid else t('grid_hidden')
        self._update_status(status)
    
    def toggle_language(self):
        """Toggle Korean/English"""
        lang = toggle_language()
        self._create_menu()  # Recreate menu
        
        # Update component labels
        self.zoom_title.config(text=t('zoom_label'))
        self.toolbar.refresh_texts()
        self.color_picker.refresh_texts()
        self.layer_panel.refresh_list()
        
        self._update_status(f"Language: {'한국어' if lang == 'ko' else 'English'}")
    
    def change_canvas_size(self):
        """Change canvas dimensions with dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(t('canvas_size'))
        dialog.geometry("250x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Width
        tk.Label(main_frame, text=f"{t('width')}:").grid(row=0, column=0, sticky=tk.W, pady=5)
        width_var = tk.StringVar(value=str(self.canvas_widget.width))
        width_entry = tk.Entry(main_frame, textvariable=width_var, width=10)
        width_entry.grid(row=0, column=1, padx=10)
        
        # Height
        tk.Label(main_frame, text=f"{t('height')}:").grid(row=1, column=0, sticky=tk.W, pady=5)
        height_var = tk.StringVar(value=str(self.canvas_widget.height))
        height_entry = tk.Entry(main_frame, textvariable=height_var, width=10)
        height_entry.grid(row=1, column=1, padx=10)
        
        def apply():
            try:
                w = int(width_var.get())
                h = int(height_var.get())
                if 1 <= w <= 1024 and 1 <= h <= 1024:
                    self.canvas_widget.resize_canvas(w, h)
                    dialog.destroy()
                    self._update_status(f"Canvas resized to {w}x{h}")
                else:
                    messagebox.showerror("Error", "Size must be between 1 and 1024")
            except ValueError:
                messagebox.showerror("Error", "Invalid input")
        
        btn_apply = tk.Button(main_frame, text=t('apply'), command=apply)
        btn_apply.grid(row=2, column=0, columnspan=2, pady=10)
    
    def new_file(self):
        """New file"""
        if self.modified:
            if not messagebox.askyesno(t('save_changes'), t('save_before_close')):
                return
            self.save_file()
        
        # Get canvas size
        size = simpledialog.askinteger(t('new'), f"{t('canvas_size')}:", initialvalue=32, minvalue=8, maxvalue=512)
        if size:
            self.canvas_widget.resize_canvas(size, size)
            self.canvas_widget.object_manager.clear()
            self.layer_panel.refresh_list()
            self.canvas_widget.render()
            self.current_file = None
            self.modified = False
            self._update_title()
    
    def open_file(self):
        """Open file"""
        filepath = filedialog.askopenfilename(
            title="Open PLB File",
            filetypes=[("PixeLab Files", "*.plb"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                data = self.file_handler.load_plb(filepath)
                
                # Resize canvas
                self.canvas_widget.resize_canvas(data['width'], data['height'])
                
                # Load objects
                self.canvas_widget.object_manager.from_dict(data)
                
                # Refresh Layer list
                self.layer_panel.refresh_list()
                
                # Load palette if present
                if 'palette' in data:
                    self.palette.from_hex_list(data['palette'])
                    self.color_picker.refresh()
                
                self.canvas_widget.render()
                self.current_file = filepath
                self.modified = False
                self._update_title()
                self._update_status(f"Loaded: {filepath}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")
    
    def save_file(self):
        """Save file"""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save as"""
        filepath = filedialog.asksaveasfilename(
            title="Save PLB File",
            defaultextension=".plb",
            filetypes=[("PixeLab Files", "*.plb"), ("All Files", "*.*")]
        )
        if filepath:
            self._save_to_file(filepath)
    
    def _save_to_file(self, filepath):
        """Actually save to file"""
        try:
            self.file_handler.save_plb(filepath, self.canvas_widget, self.palette)
            self.current_file = filepath
            self.modified = False
            self._update_title()
            self._update_status(f"Saved: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")
    
    def import_image(self):
        """Import image"""
        def on_import_complete(group):
            if group:
                self.canvas_widget.object_manager.add_object(group)
                self.canvas_widget.render()
                self._update_status(f"{t('imported')}: {len(group.objects)} {t('objects')}")
        
        ImageImporter.import_image(
            self.root,
            self.canvas_widget.width,
            self.canvas_widget.height,
            on_import_complete
        )
    
    def export_png(self):
        """Export PNG"""
        filepath = filedialog.asksaveasfilename(
            title="Export PNG",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        if filepath:
            scale = simpledialog.askinteger("Export Scale", "Scale (1-16):", initialvalue=1, minvalue=1, maxvalue=16)
            if scale:
                try:
                    self.file_handler.export_png(filepath, self.canvas_widget, scale)
                    self._update_status(f"Exported: {filepath}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export:\n{e}")
    
    def export_svg(self):
        """Export SVG"""
        filepath = filedialog.asksaveasfilename(
            title="Export SVG",
            defaultextension=".svg",
            filetypes=[("SVG Files", "*.svg"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                self.file_handler.export_svg(filepath, self.canvas_widget)
                self._update_status(f"Exported: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{e}")
    
    def group_objects(self):
        """Group selected objects"""
        sel_count = len(self.canvas_widget.object_manager.selected_objects)
        print(f"[DEBUG] group_objects: {sel_count} objects selected")
        
        group = self.canvas_widget.object_manager.group_selected()
        if group:
            print(f"[DEBUG] Created group with {len(group.objects)} objects")
            self.canvas_widget.render()
            self.modified = True
            self._update_status(f"{t('grouped')}: {len(group.objects)} {t('objects')}")
            self.layer_panel.refresh_list()
            self.canvas_widget.force_render()
        else:
            print("[DEBUG] Failed to create group (need 2+ objects)")
            messagebox.showinfo(t('group'), "Select 2+ objects to group")
    
    def ungroup_objects(self):
        """Ungroup selected groups"""
        print(f"[DEBUG] ungroup_objects called")
        count = self.canvas_widget.object_manager.ungroup_selected()
        print(f"[DEBUG] Ungrouped {count} objects")
        if count > 0:
            self.canvas_widget.render()
            self.modified = True
            self._update_status(f"{t('ungrouped')}: {count} {t('objects')}")
            self.layer_panel.refresh_list()
            self.canvas_widget.force_render()
        else:
            print("[DEBUG] No groups to ungroup")
    
    def delete_selected(self):
        """Delete selected objects"""
        self.canvas_widget.object_manager.delete_selected()
        self.canvas_widget.render()
        self._update_status(t('ready'))
    
    def change_selected_color(self):
        """Change color of selected objects"""
        from tkinter import colorchooser
        
        sel_count = len(self.canvas_widget.object_manager.selected_objects)
        print(f"[DEBUG] change_selected_color: {sel_count} objects selected")
        
        if sel_count == 0:
            print("[DEBUG] No objects selected for color change")
            return
        
        # Show color picker
        color = colorchooser.askcolor(
            color=f"#{self.current_color[0]:02x}{self.current_color[1]:02x}{self.current_color[2]:02x}",
            title="색상 선택" if get_language() == 'ko' else "Choose Color"
        )
        
        print(f"[DEBUG] Color picker result: {color}")
        
        if color and color[0]:
            r, g, b = [int(c) for c in color[0]]
            new_color = (r, g, b, 255)
            
            print(f"[DEBUG] New color: {new_color}")
            
            count = self.canvas_widget.object_manager.change_selected_color(new_color)
            print(f"[DEBUG] Changed {count} objects")
            
            # Force re-render by setting need_render flag
            self.canvas_widget.need_render = True
            self.canvas_widget.render()
            print("[DEBUG] Canvas rendered")
            
            msg = f"{count}개 객체 색상 변경됨" if get_language() == 'ko' else f"Changed color of {count} objects"
            self._update_status(msg)
    
    def clear_canvas(self):
        """Clear canvas"""
        if messagebox.askyesno("Clear", "Clear all objects?"):
            self.canvas_widget.clear()
            self._update_status(t('canvas_cleared'))
    
    def quit_app(self):
        """Quit application"""
        if self.modified:
            response = messagebox.askyesnocancel(t('save_changes'), t('save_before_close'))
            if response is None:  # Cancel
                return
            if response:  # Yes
                self.save_file()
        
        self.root.quit()
    
    def _update_status(self, message=""):
        """Update status"""
        if not message:
            obj_count = len(self.canvas_widget.object_manager)
            message = f"{t('ready')} - {obj_count} {t('objects')}"
        
        self.status_label.config(text=message)
    
    def _update_title(self):
        """Update window title"""
        title = "PixeLab v2.1"
        if self.current_file:
            title += f" - {self.current_file}"
        if self.modified:
            title += " *"
        self.root.title(title)


def main():
    root = tk.Tk()
    app = PixelLabFullApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
