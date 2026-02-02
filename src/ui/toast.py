"""
Toast Notification UI - Premium styled popups
"""
import tkinter as tk
from src.i18n import t

class ToastNotification(tk.Toplevel):
    """Sleek popup notification for updates"""
    
    def __init__(self, parent, version_str, update_url):
        super().__init__(parent)
        self.update_url = update_url
        
        # Window settings
        self.overrideredirect(True) # Remove title bar
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.0) # Start transparent for fade-in
        
        self.configure(bg="#1e1e1e") # Dark background
        
        # Content
        main_frame = tk.Frame(self, bg="#1e1e1e", highlightthickness=1, highlightbackground="#61afef")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        title_lbl = tk.Label(
            main_frame, 
            text=t('new_version_title'),
            bg="#1e1e1e", fg="#61afef",
            font=("Arial", 10, "bold")
        )
        title_lbl.pack(padx=15, pady=(15, 5), anchor="w")
        
        msg_lbl = tk.Label(
            main_frame,
            text=t('new_version_msg').format(v=version_str),
            bg="#1e1e1e", fg="#abb2bf",
            font=("Arial", 9)
        )
        msg_lbl.pack(padx=15, pady=(0, 15), anchor="w")
        
        btn_frame = tk.Frame(main_frame, bg="#1e1e1e")
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        update_btn = tk.Button(
            btn_frame,
            text=t('update_now'),
            bg="#61afef", fg="#1e1e1e",
            activebackground="#528bff",
            relief=tk.FLAT,
            font=("Arial", 9, "bold"),
            command=self._on_update,
            padx=10, cursor="hand2"
        )
        update_btn.pack(side=tk.LEFT)
        
        later_btn = tk.Button(
            btn_frame,
            text=t('later'),
            bg="#2c313a", fg="#abb2bf",
            activebackground="#3e4451",
            relief=tk.FLAT,
            font=("Arial", 9),
            command=self._fade_out,
            padx=10, cursor="hand2"
        )
        later_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Position (Bottom Right)
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        
        self.geometry(f"{w}x{h}+{sw-w-20}+{sh-h-60}")
        
        # Animations
        self._fade_in()

    def _fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 0.95:
            alpha += 0.05
            self.attributes("-alpha", alpha)
            self.after(20, self._fade_in)

    def _fade_out(self):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= 0.05
            self.attributes("-alpha", alpha)
            self.after(20, self._fade_out)
        else:
            self.destroy()

    def _on_update(self):
        """Open update URL in browser and close"""
        import webbrowser
        webbrowser.open(self.update_url)
        self._fade_out()

def show_update_toast(parent, version, url):
    """Helper to ensure thread-safe UI call"""
    parent.after(0, lambda: ToastNotification(parent, version, url))
