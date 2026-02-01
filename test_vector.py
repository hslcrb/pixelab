#!/usr/bin/env python3
"""
PixeLab Vector Edition - Test Entry Point
간단한 벡터 시스템 테스트
"""
import sys
import tkinter as tk
from tkinter import messagebox

try:
    from src.vector_canvas import VectorCanvas
    from src.vector_tools import *
    from src.palette import ColorPalette
    from src.vector_file_handler import VectorFileHandler
    from src.object_manager import ObjectManager
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all vector modules are in src/")
    sys.exit(1)


class SimpleVectorApp:
    """Simplified vector app for testing"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PixeLab Vector - Test")
        self.root.geometry("800x600")
        
        # State
        self.current_color = (0, 0, 0, 255)
        self.current_tool = None
        
        # Canvas
        self.canvas_widget = VectorCanvas(root, width=32, height=32)
        
        # Tools
        self.tools = {
            "Select": VectorSelectTool(),
            "Pencil": VectorPencilTool(self.current_color),
            "Line": VectorLineTool(self.current_color),
            "Rectangle": VectorRectangleTool(self.current_color, False),
            "Circle": VectorCircleTool(self.current_color, False),
        }
        
        self.current_tool = self.tools["Pencil"]
        
        # Bind mouse events
        self.canvas_widget.canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self.canvas_widget.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas_widget.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        
        # Bind keys
        self.root.bind("v", lambda e: self.select_tool("Select"))
        self.root.bind("p", lambda e: self.select_tool("Pencil"))
        self.root.bind("l", lambda e: self.select_tool("Line"))
        self.root.bind("r", lambda e: self.select_tool("Rectangle"))
        self.root.bind("c", lambda e: self.select_tool("Circle"))
        self.root.bind("g", lambda e: self.canvas_widget.toggle_grid())
        
        print("PixeLab Vector Edition")
        print("Keys: V=Select, P=Pencil, L=Line, R=Rectangle, C=Circle, G=Grid")
    
    def select_tool(self, name):
        if name in self.tools:
            self.current_tool = self.tools[name]
            self.current_tool.set_color(self.current_color)
            print(f"Tool: {name}")
    
    def _on_mouse_press(self, event):
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        if 0 <= px < self.canvas_widget.width and 0 <= py < self.canvas_widget.height:
            self.current_tool.on_press(px, py, self.canvas_widget.object_manager)
            
            # Update preview
            if hasattr(self.current_tool, 'get_preview_object'):
                self.canvas_widget.set_preview_object(self.current_tool.get_preview_object())
            
            self.canvas_widget.render()
    
    def _on_mouse_drag(self, event):
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        self.current_tool.on_drag(px, py, self.canvas_widget.object_manager)
        
        # Update preview
        if hasattr(self.current_tool, 'get_preview_object'):
            self.canvas_widget.set_preview_object(self.current_tool.get_preview_object())
        
        self.canvas_widget.render()
    
    def _on_mouse_release(self, event):
        px, py = self.canvas_widget.screen_to_canvas(event.x, event.y)
        self.current_tool.on_release(px, py, self.canvas_widget.object_manager)
        
        # Clear preview
        self.canvas_widget.clear_preview()
        self.canvas_widget.render()


def main():
    root = tk.Tk()
    app = SimpleVectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
