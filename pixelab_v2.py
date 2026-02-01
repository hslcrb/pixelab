#!/usr/bin/env python3
"""
PixeLab v2.1 - Full Featured Vector Edition
완전한 기능의 벡터 에디터 (이미지 가져오기, 그룹화, 한영전환)
"""
import sys
import tkinter as tk
from tkinter import messagebox, Menu

try:
    from src.vector_canvas import VectorCanvas
    from src.vector_tools import *
    from src.palette import ColorPalette
    from src.vector_file_handler import VectorFileHandler
    from src.object_manager import ObjectManager
    from src.image_import import ImageImporter
    from src.i18n import t, toggle_language, get_language
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all modules are in src/")
    sys.exit(1)


class PixelLabVectorApp:
    """Full-featured vector pixel editor"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PixeLab v2.1 - Vector Edition")
        self.root.geometry("1000x700")
        
        # State
        self.current_color = (0, 0, 0, 255)
        self.current_tool = None
        self.file_handler = VectorFileHandler()
        self.palette = ColorPalette()
        
        # Create UI
        self._create_menu()
        
        # Canvas
        self.canvas_widget = VectorCanvas(root, width=32, height=32)
        
        # Tools
        self.tools = {
            "Mouse": VectorMouseTool(),
            "Select": VectorSelectTool(),
            "Pencil": VectorPencilTool(self.current_color),
            "Brush": VectorBrushTool(self.current_color, 3),
            "Eraser": VectorEraserTool(3),
            "Line": VectorLineTool(self.current_color),
            "Rectangle": VectorRectangleTool(self.current_color, False),
            "Circle": VectorCircleTool(self.current_color, False),
        }
        
        self.current_tool = self.tools["Mouse"]
        
        # Bind events
        self._bind_events()
        
        # Status
        self._update_status()
        
        print("=" * 60)
        print("PixeLab v2.1 - Vector Edition")
        print("=" * 60)
        print("단축키:")
        print("  한/영: F1 (한영 전환)")
        print("  V/M: Mouse/Select")
        print("  P: Pencil, B: Brush, E: Eraser")
        print("  L: Line, R: Rectangle, C: Circle")
        print("  G: Grid 토글")
        print("  Ctrl+I: 이미지 가져오기")
        print("  Ctrl+G: 그룹 만들기")
        print("  Ctrl+U: 그룹 해제")
        print("  Delete: 선택 삭제")
        print("=" * 60)
    
    def _create_menu(self):
        """Create menu bar"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=t('file'), menu=file_menu)
        file_menu.add_command(label=t('import_image'), command=self.import_image, accelerator="Ctrl+I")
        file_menu.add_separator()
        file_menu.add_command(label=t('exit'), command=self.root.quit)
        
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
        view_menu.add_separator()
        view_menu.add_command(label="한/영 전환", command=self.toggle_language, accelerator="F1")
        
        self.menubar = menubar
    
    def _update_menu(self):
        """Update menu texts for current language"""
        # Recreate menu
        self._create_menu()
    
    def _bind_events(self):
        """Bind keyboard and mouse events"""
        # Mouse events
        self.canvas_widget.canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self.canvas_widget.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas_widget.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        
        # Keyboard shortcuts
        self.root.bind("<F1>", lambda e: self.toggle_language())
        
        self.root.bind("v", lambda e: self.select_tool("Mouse"))
        self.root.bind("m", lambda e: self.select_tool("Select"))
        self.root.bind("p", lambda e: self.select_tool("Pencil"))
        self.root.bind("b", lambda e: self.select_tool("Brush"))
        self.root.bind("e", lambda e: self.select_tool("Eraser"))
        self.root.bind("l", lambda e: self.select_tool("Line"))
        self.root.bind("r", lambda e: self.select_tool("Rectangle"))
        self.root.bind("c", lambda e: self.select_tool("Circle"))
        
        self.root.bind("g", lambda e: self.toggle_grid())
        self.root.bind("<Control-i>", lambda e: self.import_image())
        self.root.bind("<Control-g>", lambda e: self.group_objects())
        self.root.bind("<Control-u>", lambda e: self.ungroup_objects())
        self.root.bind("<Delete>", lambda e: self.delete_selected())
    
    def select_tool(self, name):
        """Select tool"""
        if name in self.tools:
            self.current_tool = self.tools[name]
            self.current_tool.set_color(self.current_color)
            self._update_status(f"{t('tool')}: {t(name.lower())}")
    
    def toggle_grid(self):
        """Toggle grid"""
        self.canvas_widget.toggle_grid()
        status = t('grid_shown') if self.canvas_widget.show_grid else t('grid_hidden')
        self._update_status(status)
    
    def toggle_language(self):
        """Toggle Korean/English"""
        lang = toggle_language()
        self._update_menu()
        self._update_status(f"Language: {'한국어' if lang == 'ko' else 'English'}")
    
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
    
    def group_objects(self):
        """Group selected objects"""
        group = self.canvas_widget.object_manager.group_selected()
        if group:
            self.canvas_widget.render()
            self._update_status(f"{t('grouped')}: {len(group.objects)} {t('objects')}")
        else:
            messagebox.showinfo("그룹", "2개 이상의 객체를 선택하세요")
    
    def ungroup_objects(self):
        """Ungroup selected groups"""
        count = self.canvas_widget.object_manager.ungroup_selected()
        if count > 0:
            self.canvas_widget.render()
            self._update_status(f"{t('ungrouped')}: {count} {t('objects')}")
    
    def delete_selected(self):
        """Delete selected objects"""
        self.canvas_widget.object_manager.delete_selected()
        self.canvas_widget.render()
        self._update_status(t('ready'))
    
    def clear_canvas(self):
        """Clear canvas"""
        if messagebox.askyesno("Clear", "Clear all objects?"):
            self.canvas_widget.clear()
            self._update_status(t('canvas_cleared'))
    
    def _on_mouse_press(self, event):
        """Mouse press"""
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        if 0 <= px < self.canvas_widget.width and 0 <= py < self.canvas_widget.height:
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
        self._update_status(f"{t('position')}: ({px}, {py})")
    
    def _on_mouse_release(self, event):
        """Mouse release"""
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        self.current_tool.on_release(px, py, self.canvas_widget.object_manager)
        
        self.canvas_widget.clear_preview()
        self.canvas_widget.render()
        
        # Update status with selection info
        obj_count = len(self.canvas_widget.object_manager.objects)
        sel_count = len(self.canvas_widget.object_manager.selected_objects)
        self._update_status(f"{obj_count} {t('objects')}, {sel_count} {t('selected')}")
    
    def _update_status(self, message=""):
        """Update status"""
        if not message:
            obj_count = len(self.canvas_widget.object_manager.objects)
            message = f"{t('ready')} - {obj_count} {t('objects')}"
        
        self.root.title(f"PixeLab v2.1 - {message}")


def main():
    root = tk.Tk()
    app = PixelLabVectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
