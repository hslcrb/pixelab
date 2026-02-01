"""
Toolbar Component - Drawing tools panel
"""
import tkinter as tk
from tkinter import ttk


class Toolbar(tk.Frame):
    """Toolbar with drawing tools"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2b2b2b", width=80)
        self.app = app
        self.pack_propagate(False)
        
        # Tool definitions (name, icon, shortcut)
        self.tools = [
            ("Pencil", "✏️", "P"),
            ("Brush", "🖌️", "B"),
            ("Eraser", "🧹", "E"),
            ("Fill", "🪣", "F"),
            ("Eyedropper", "💧", "I"),
            ("Line", "📏", "L"),
            ("Rectangle", "▢", "R"),
            ("Circle", "○", "C"),
        ]
        
        self.buttons = {}
        self.selected_tool = None
        
        # Title
        title = tk.Label(
            self, 
            text="Tools", 
            bg="#2b2b2b", 
            fg="#ffffff",
            font=("Arial", 10, "bold")
        )
        title.pack(pady=(10, 5))
        
        # Tool buttons
        for name, icon, key in self.tools:
            btn = tk.Button(
                self,
                text=f"{icon}\n{name}",
                command=lambda n=name: self._select_tool(n),
                bg="#3c3c3c",
                fg="#ffffff",
                activebackground="#4c4c4c",
                activeforeground="#ffffff",
                relief=tk.FLAT,
                font=("Arial", 9),
                padx=5,
                pady=8,
                cursor="hand2"
            )
            btn.pack(fill=tk.X, padx=8, pady=2)
            self.buttons[name] = btn
        
        # Tool options
        separator = tk.Frame(self, bg="#444444", height=2)
        separator.pack(fill=tk.X, pady=10, padx=8)
        
        options_label = tk.Label(
            self,
            text="Options",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 9, "bold")
        )
        options_label.pack(pady=(5, 5))
        
        # Brush size (for brush and eraser)
        size_frame = tk.Frame(self, bg="#2b2b2b")
        size_frame.pack(fill=tk.X, padx=8, pady=5)
        
        size_label = tk.Label(
            size_frame,
            text="Size:",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 8)
        )
        size_label.pack(side=tk.LEFT)
        
        self.size_var = tk.IntVar(value=3)
        self.size_scale = tk.Scale(
            size_frame,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            bg="#3c3c3c",
            fg="#ffffff",
            highlightthickness=0,
            troughcolor="#2b2b2b",
            activebackground="#4c4c4c",
            command=self._on_size_change
        )
        self.size_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Fill option (for shapes)
        self.filled_var = tk.BooleanVar(value=False)
        self.filled_check = tk.Checkbutton(
            self,
            text="Filled",
            variable=self.filled_var,
            bg="#2b2b2b",
            fg="#ffffff",
            selectcolor="#3c3c3c",
            activebackground="#2b2b2b",
            activeforeground="#ffffff",
            command=self._on_filled_change
        )
        self.filled_check.pack(padx=8, pady=2)
    
    def _select_tool(self, name):
        """Select a tool"""
        # Deselect previous
        if self.selected_tool and self.selected_tool in self.buttons:
            self.buttons[self.selected_tool].config(
                bg="#3c3c3c",
                relief=tk.FLAT
            )
        
        # Select new
        self.selected_tool = name
        if name in self.buttons:
            self.buttons[name].config(
                bg="#5c5c5c",
                relief=tk.SUNKEN
            )
        
        # Notify app
        self.app.select_tool(name)
    
    def _on_size_change(self, value):
        """Handle size change"""
        self.app.set_tool_size(int(value))
    
    def _on_filled_change(self):
        """Handle filled option change"""
        self.app.set_tool_filled(self.filled_var.get())
    
    def select_tool_by_name(self, name):
        """Programmatically select a tool"""
        if name in [t[0] for t in self.tools]:
            self._select_tool(name)
