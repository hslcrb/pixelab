"""
Layer Panel Component
"""
import tkinter as tk
from tkinter import messagebox, simpledialog

class LayerPanel(tk.Frame):
    """Component to manage layers"""
    
    def __init__(self, parent, object_manager, refresh_callback):
        super().__init__(parent, bg="#2b2b2b", width=200)
        self.object_manager = object_manager
        self.refresh_callback = refresh_callback
        self.pack_propagate(False)
        
        from src.i18n import t
        
        # Title
        tk.Label(
            self,
            text=t('layers'),
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 10, "bold")
        ).pack(pady=(10, 5))
        
        # Layer List Container
        self.list_container = tk.Frame(self, bg="#2b2b2b")
        self.list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollable list
        self.canvas = tk.Canvas(self.list_container, bg="#2b2b2b", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2b2b2b")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        btn_frame = tk.Frame(self, bg="#2b2b2b")
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(btn_frame, text="+", command=self._add_layer, bg="#3c3c3c", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="-", command=self._remove_layer, bg="#3c3c3c", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="↑", command=self._move_layer_up, bg="#3c3c3c", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="↓", command=self._move_layer_down, bg="#3c3c3c", fg="white", width=3).pack(side=tk.LEFT, padx=2)
        
        self.refresh_list()
    
    def refresh_list(self):
        """Update layer list display"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        for i, layer in reversed(list(enumerate(self.object_manager.layers))):
            is_active = (i == self.object_manager.current_layer_index)
            bg_color = "#4c4c4c" if is_active else "#3c3c3c"
            
            item_frame = tk.Frame(self.scrollable_frame, bg=bg_color, pady=2)
            item_frame.pack(fill=tk.X, pady=1, padx=2)
            
            # Visibility toggle (eye)
            eye_text = "👁" if layer.visible else "◌"
            eye_btn = tk.Label(item_frame, text=eye_text, bg=bg_color, fg="white", width=2, cursor="hand2")
            eye_btn.pack(side=tk.LEFT, padx=2)
            eye_btn.bind("<Button-1>", lambda e, idx=i: self._toggle_visibility(idx))
            
            # Layer Name
            name_label = tk.Label(item_frame, text=layer.name, bg=bg_color, fg="white", anchor="w", cursor="hand2")
            name_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            name_label.bind("<Button-1>", lambda e, idx=i: self._select_layer(idx))
            name_label.bind("<Double-Button-1>", lambda e, idx=i: self._rename_layer(idx))
            
            # Lock toggle
            lock_text = "🔒" if layer.locked else "🔓"
            lock_btn = tk.Label(item_frame, text=lock_text, bg=bg_color, fg="white", width=2, cursor="hand2")
            lock_btn.pack(side=tk.RIGHT, padx=2)
            lock_btn.bind("<Button-1>", lambda e, idx=i: self._toggle_lock(idx))

    def _add_layer(self):
        self.object_manager.add_layer()
        self.refresh_list()
        self.refresh_callback()

    def _remove_layer(self):
        if self.object_manager.remove_layer(self.object_manager.current_layer_index):
            self.refresh_list()
            self.refresh_callback()
        else:
            messagebox.showwarning("Warning", "Cannot remove last layer")

    def _select_layer(self, index):
        self.object_manager.current_layer_index = index
        self.refresh_list()
        self.refresh_callback()

    def _toggle_visibility(self, index):
        self.object_manager.layers[index].visible = not self.object_manager.layers[index].visible
        self.refresh_list()
        self.refresh_callback()

    def _toggle_lock(self, index):
        self.object_manager.layers[index].locked = not self.object_manager.layers[index].locked
        self.refresh_list()
        self.refresh_callback()

    def _rename_layer(self, index):
        current_name = self.object_manager.layers[index].name
        new_name = simpledialog.askstring("Rename Layer", "Enter new name:", initialvalue=current_name)
        if new_name:
            self.object_manager.layers[index].name = new_name
            self.refresh_list()
            self.refresh_callback()

    def _move_layer_up(self):
        idx = self.object_manager.current_layer_index
        if idx < len(self.object_manager.layers) - 1:
            self.object_manager.layers[idx], self.object_manager.layers[idx+1] = \
                self.object_manager.layers[idx+1], self.object_manager.layers[idx]
            self.object_manager.current_layer_index = idx + 1
            self.refresh_list()
            self.refresh_callback()

    def _move_layer_down(self):
        idx = self.object_manager.current_layer_index
        if idx > 0:
            self.object_manager.layers[idx], self.object_manager.layers[idx-1] = \
                self.object_manager.layers[idx-1], self.object_manager.layers[idx]
            self.object_manager.current_layer_index = idx - 1
            self.refresh_list()
            self.refresh_callback()
