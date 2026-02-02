"""
Toast Notification UI - Premium styled popups
"""
import tkinter as tk
from src.i18n import t

class ToastNotification(tk.Toplevel):
    """Sleek popup notification for updates"""
    
    def __init__(self, parent, updater, version_str):
        super().__init__(parent)
        self.parent = parent
        self.updater = updater
        
        # Window settings
        self.overrideredirect(True) # Remove title bar
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.0)
        self.configure(bg="#1e1e1e")
        
        # Content
        main_frame = tk.Frame(self, bg="#1e1e1e", highlightthickness=1, highlightbackground="#61afef")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        tk.Label(
            main_frame, 
            text=t('new_version_title'),
            bg="#1e1e1e", fg="#61afef",
            font=("Arial", 10, "bold")
        ).pack(padx=15, pady=(15, 5), anchor="w")
        
        tk.Label(
            main_frame,
            text=t('new_version_msg').format(v=version_str),
            bg="#1e1e1e", fg="#abb2bf",
            font=("Arial", 9)
        ).pack(padx=15, pady=(0, 15), anchor="w")
        
        btn_frame = tk.Frame(main_frame, bg="#1e1e1e")
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Button(
            btn_frame,
            text=t('update_now'),
            bg="#61afef", fg="#1e1e1e",
            activebackground="#528bff",
            relief=tk.FLAT,
            font=("Arial", 9, "bold"),
            command=self._on_update,
            padx=10, cursor="hand2"
        ).pack(side=tk.LEFT)
        
        tk.Button(
            btn_frame,
            text=t('later'),
            bg="#2c313a", fg="#abb2bf",
            activebackground="#3e4451",
            relief=tk.FLAT,
            font=("Arial", 9),
            command=self._fade_out,
            padx=10, cursor="hand2"
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Position (Bottom Right)
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{sw-w-20}+{sh-h-60}")
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
        """Start auto-update process"""
        from tkinter import messagebox
        from src.image_import import ProgressDialog
        
        self.withdraw()
        progress = ProgressDialog(self.parent, t('updating'))
        
        def on_progress(p, status):
            self.parent.after(0, lambda: progress.update(p, status))
            
        def on_finish(success, msg):
            def _ui_finish():
                if success:
                    messagebox.showinfo(t('updating'), msg)
                else:
                    messagebox.showerror(t('error'), msg)
                    progress.close()
            self.parent.after(0, _ui_finish)

        self.updater.start_auto_update(self.parent, on_progress, on_finish)

def show_update_toast(parent, updater, version):
    """Helper to ensure thread-safe UI call"""
    parent.after(0, lambda: ToastNotification(parent, updater, version))
