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
            ("Select", "➦", "V"),
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
        
        from src.i18n import t
        
        # Title
        self.title_label = tk.Label(
            self, 
            text=t('tools_label'), 
            bg="#2b2b2b", 
            fg="#ffffff",
            font=("Arial", 10, "bold")
        )
        self.title_label.pack(pady=(10, 5))
        
        # Tool buttons
        for name, icon, key in self.tools:
            btn = tk.Button(
                self,
                text=f"{icon}\n{t(name.lower())}",
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
        separator.pack(fill=tk.X, pady=(15, 10), padx=10)
        
        self.options_label = tk.Label(
            self,
            text=t('options_label'),
            bg="#2b2b2b",
            fg="#61afef", # Bright accent color for section header
            font=("Arial", 10, "bold")
        )
        self.options_label.pack(pady=(0, 10))
        
        # --- Brush Size ---
        size_container = tk.Frame(self, bg="#2b2b2b")
        size_container.pack(fill=tk.X, padx=10, pady=5)
        
        self.size_label = tk.Label(
            size_container,
            text=t('size_label'),
            bg="#2b2b2b",
            fg="#abb2bf",
            font=("Arial", 9)
        )
        self.size_label.pack(side=tk.TOP, anchor=tk.W)
        
        self.size_var = tk.IntVar(value=3)
        # Using a Spinbox for more precise control and clarity
        self.size_spin = tk.Spinbox(
            size_container,
            from_=1, to=100,
            textvariable=self.size_var,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            buttonbackground="#3c3c3c",
            relief=tk.FLAT,
            font=("Arial", 10, "bold"),
            width=5,
            command=lambda: self._on_size_change(self.size_var.get())
        )
        self.size_spin.pack(side=tk.LEFT, pady=2, fill=tk.X, expand=True)
        # Add a small slider for quick adjustment too
        self.size_scale = tk.Scale(
            size_container,
            from_=1, to=100,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            bg="#2b2b2b",
            fg="#ffffff",
            highlightthickness=0,
            troughcolor="#1e1e1e",
            activebackground="#61afef",
            showvalue=0,
            command=self._on_size_change
        )
        self.size_scale.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # --- Fill Option ---
        self.filled_var = tk.BooleanVar(value=False)
        fill_frame = tk.Frame(self, bg="#3c3c3c", padx=5, pady=2)
        fill_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.filled_check = tk.Checkbutton(
            fill_frame,
            text=t('filled_label'),
            variable=self.filled_var,
            bg="#3c3c3c",
            fg="#ffffff",
            selectcolor="#1e1e1e",
            activebackground="#3c3c3c",
            activeforeground="#61afef",
            font=("Arial", 9),
            relief=tk.FLAT,
            command=self._on_filled_change
        )
        self.filled_check.pack(side=tk.LEFT)
        
        # Pixel scale (Zoom) removed as requested
        pass

    def refresh_texts(self):
        """Update texts for current language"""
        from src.i18n import t
        self.title_label.config(text=t('tools_label'))
        self.options_label.config(text=t('options_label'))
        self.size_label.config(text=t('size_label'))
        self.filled_check.config(text=t('filled_label'))
        
        for name, icon, _ in self.tools:
            if name in self.buttons:
                self.buttons[name].config(text=f"{icon}\n{t(name.lower())}")
    
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
        
    def _on_pixel_change(self, value):
        """Handle pixel scale change"""
        if hasattr(self.app, 'canvas_widget'):
            self.app.canvas_widget.zoom_level = float(value)
            self.app.canvas_widget.need_render = True
            self.app.canvas_widget.render()
            if hasattr(self.app, 'zoom_label'):
                self.app.zoom_label.config(text=f"{int(value)}x")
    
    def select_tool_by_name(self, name):
        """Programmatically select a tool"""
        if name in [t[0] for t in self.tools]:
            self._select_tool(name)
