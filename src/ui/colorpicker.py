"""
Color Picker Component
"""
import tkinter as tk
from tkinter import colorchooser


class ColorPicker(tk.Frame):
    """Color selection and palette panel"""
    
    def __init__(self, parent, app, palette):
        super().__init__(parent, bg="#2b2b2b", width=200)
        self.app = app
        self.palette = palette
        self.pack_propagate(False)
        
        self.current_color = (0, 0, 0, 255)
        
        # Title
        title = tk.Label(
            self,
            text="Colors",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 10, "bold")
        )
        title.pack(pady=(10, 5))
        
        # Current color display
        color_frame = tk.Frame(self, bg="#2b2b2b")
        color_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(
            color_frame,
            text="Current:",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 9)
        ).pack(side=tk.LEFT)
        
        self.current_color_canvas = tk.Canvas(
            color_frame,
            width=60,
            height=30,
            bg="#000000",
            highlightthickness=1,
            highlightbackground="#ffffff"
        )
        self.current_color_canvas.pack(side=tk.LEFT, padx=(10, 0))
        
        # Color picker button
        btn_pick = tk.Button(
            self,
            text="Choose Color...",
            command=self._pick_color,
            bg="#3c3c3c",
            fg="#ffffff",
            activebackground="#4c4c4c",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            font=("Arial", 9),
            padx=10,
            pady=5,
            cursor="hand2"
        )
        btn_pick.pack(padx=10, pady=5, fill=tk.X)
        
        # Add to palette button
        btn_add = tk.Button(
            self,
            text="Add to Palette",
            command=self._add_to_palette,
            bg="#3c3c3c",
            fg="#ffffff",
            activebackground="#4c4c4c",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            font=("Arial", 9),
            padx=10,
            pady=5,
            cursor="hand2"
        )
        btn_add.pack(padx=10, pady=5, fill=tk.X)
        
        # Palette section
        separator = tk.Frame(self, bg="#444444", height=2)
        separator.pack(fill=tk.X, pady=10, padx=10)
        
        palette_label = tk.Label(
            self,
            text="Palette",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 9, "bold")
        )
        palette_label.pack(pady=(5, 5))
        
        # Scrollable palette
        palette_container = tk.Frame(self, bg="#2b2b2b")
        palette_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.palette_canvas = tk.Canvas(
            palette_container,
            bg="#2b2b2b",
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            palette_container,
            orient="vertical",
            command=self.palette_canvas.yview
        )
        
        self.palette_frame = tk.Frame(self.palette_canvas, bg="#2b2b2b")
        self.palette_frame.bind(
            "<Configure>",
            lambda e: self.palette_canvas.configure(
                scrollregion=self.palette_canvas.bbox("all")
            )
        )
        
        self.palette_canvas.create_window((0, 0), window=self.palette_frame, anchor="nw")
        self.palette_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.palette_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh palette display
        self.refresh_palette()
        
        # Set initial color
        self.set_color((0, 0, 0, 255))
    
    def _pick_color(self):
        """Open color picker dialog"""
        # Convert current color to hex
        r, g, b, a = self.current_color
        initial_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Show color chooser
        color = colorchooser.askcolor(
            color=initial_color,
            title="Choose Color"
        )
        
        if color and color[0]:
            # color[0] is RGB tuple (float)
            r, g, b = [int(c) for c in color[0]]
            new_color = (r, g, b, 255)
            self.set_color(new_color)
    
    def _add_to_palette(self):
        """Add current color to palette"""
        self.palette.add_color(self.current_color)
        self.refresh_palette()
    
    def set_color(self, color):
        """Set current color"""
        self.current_color = tuple(color)
        
        # Update display
        r, g, b, a = color
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.current_color_canvas.config(bg=hex_color)
        
        # Notify app
        self.app.set_color(color)
    
    def refresh_palette(self):
        """Refresh palette display"""
        # Clear existing buttons
        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        
        # Create color buttons in grid (4 columns)
        for i, color in enumerate(self.palette):
            row = i // 4
            col = i % 4
            
            r, g, b, a = color
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            btn = tk.Button(
                self.palette_frame,
                bg=hex_color,
                width=3,
                height=1,
                relief=tk.RAISED,
                borderwidth=2,
                cursor="hand2",
                command=lambda c=color: self.set_color(c)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Right-click to remove
            btn.bind("<Button-3>", lambda e, idx=i: self._remove_color(idx))
        
        # Configure grid weights
        for i in range(4):
            self.palette_frame.columnconfigure(i, weight=1)
    
    def _remove_color(self, index):
        """Remove color from palette"""
        self.palette.remove_color(index)
        self.refresh_palette()
