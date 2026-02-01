"""
Menu Bar Component
"""
import tkinter as tk
from tkinter import messagebox


class MenuBar:
    """Application menu bar"""
    
    def __init__(self, parent, app):
        self.app = app
        self.menubar = tk.Menu(parent)
        
        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(
            label="New", 
            command=app.new_file, 
            accelerator="Ctrl+N"
        )
        self.file_menu.add_command(
            label="Open...", 
            command=app.open_file, 
            accelerator="Ctrl+O"
        )
        self.file_menu.add_command(
            label="Save", 
            command=app.save_file, 
            accelerator="Ctrl+S"
        )
        self.file_menu.add_command(
            label="Save As...", 
            command=app.save_file_as, 
            accelerator="Ctrl+Shift+S"
        )
        self.file_menu.add_separator()
        
        # Export submenu
        self.export_menu = tk.Menu(self.file_menu, tearoff=0)
        self.export_menu.add_command(
            label="Export as PNG...", 
            command=app.export_png
        )
        self.export_menu.add_command(
            label="Export as SVG...", 
            command=app.export_svg
        )
        self.file_menu.add_cascade(label="Export", menu=self.export_menu)
        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=app.quit)
        
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(
            label="Undo", 
            command=app.undo, 
            accelerator="Ctrl+Z"
        )
        self.edit_menu.add_command(
            label="Redo", 
            command=app.redo, 
            accelerator="Ctrl+Y"
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Clear Canvas", 
            command=app.clear_canvas
        )
        
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # View menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_command(
            label="Toggle Grid", 
            command=app.toggle_grid, 
            accelerator="G"
        )
        self.view_menu.add_separator()
        self.view_menu.add_command(
            label="Zoom In", 
            command=app.zoom_in, 
            accelerator="Ctrl++"
        )
        self.view_menu.add_command(
            label="Zoom Out", 
            command=app.zoom_out, 
            accelerator="Ctrl+-"
        )
        self.view_menu.add_command(
            label="Reset Zoom", 
            command=app.reset_zoom, 
            accelerator="Ctrl+0"
        )
        
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        
        # Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(
            label="User Guide", 
            command=self.show_user_guide
        )
        self.help_menu.add_command(
            label="About PixeLab", 
            command=self.show_about
        )
        
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        
        parent.config(menu=self.menubar)
    
    def show_user_guide(self):
        """Show user guide"""
        guide = """PixeLab User Guide

Basic Controls:
- Left Click: Draw with current tool
- Mouse Wheel: Zoom in/out
- Space + Drag: Pan canvas
- G: Toggle grid

Tools:
- P: Pencil
- B: Brush
- E: Eraser
- F: Fill
- I: Eyedropper
- L: Line
- R: Rectangle
- C: Circle

For more details, see docs/USER_GUIDE.md
"""
        messagebox.showinfo("User Guide", guide)
    
    def show_about(self):
        """Show about dialog"""
        about = """PixeLab - Pixel Art Editor
Version 1.0.0

Professional pixel art and dot art creation tool.

Features:
• High-resolution grid canvas
• Multiple drawing tools
• Zoom and pan
• PLB project files
• PNG and SVG export

Created by rheehose
"""
        messagebox.showinfo("About PixeLab", about)
