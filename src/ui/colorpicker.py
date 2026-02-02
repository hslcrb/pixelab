"""
Color Picker Component
"""
import tkinter as tk
from tkinter import colorchooser


class ColorPicker(tk.Frame):
    """Color selection and palette panel"""
    
    def __init__(self, parent, palette, on_change_callback):
        super().__init__(parent, bg="#2b2b2b", width=200)
        self.palette = palette
        self.on_change_callback = on_change_callback
        self.pack_propagate(False)
        
        self.current_color = (0, 0, 0, 255)
        
        from src.i18n import t
        
        # Title
        self.title_label = tk.Label(
            self,
            text=t('colors_label'),
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 10, "bold")
        )
        self.title_label.pack(pady=(10, 5))
        
        # Current color display
        color_frame = tk.Frame(self, bg="#2b2b2b")
        color_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.current_color_label = tk.Label(
            color_frame,
            text=t('current_color'),
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 9)
        )
        self.current_color_label.pack(side=tk.LEFT)
        
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
        self.btn_pick = tk.Button(
            self,
            text=t('choose_color'),
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
        self.btn_pick.pack(padx=10, pady=5, fill=tk.X)
        
        # Add to palette button
        self.btn_add = tk.Button(
            self,
            text=t('add_to_palette'),
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
        self.btn_add.pack(padx=10, pady=5, fill=tk.X)
        
        # Palette section separator
        separator = tk.Frame(self, bg="#444444", height=2)
        separator.pack(fill=tk.X, pady=10, padx=10)

    def refresh_texts(self):
        """Update texts for current language"""
        from src.i18n import t
        self.title_label.config(text=t('colors_label'))
        self.current_color_label.config(text=t('current_color'))
        self.btn_pick.config(text=t('choose_color'))
        self.btn_add.config(text=t('add_to_palette'))
        
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
        from src.i18n import t
        color = colorchooser.askcolor(
            color=initial_color,
            title=t('choose_color')
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
        
        # Notify caller
        if self.on_change_callback:
            self.on_change_callback(color)
    
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
                activebackground=hex_color,
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
    
    def update_current_color(self, color):
        """Update current color (alias for set_color)"""
        self.set_color(color)
    
    def refresh(self):
        """Refresh palette (alias for refresh_palette)"""
        self.refresh_palette()
