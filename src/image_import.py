"""
Image Import - Import bitmap/vector images and trace them to pixel objects
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import threading
from .vector_objects import VectorPixel, VectorGroup


class ProgressDialog:
    """Progress dialog for long-running operations"""
    
    def __init__(self, parent, title=None):
        from src.i18n import t
        if title is None:
            title = t('processing')
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("400x150")
        self.top.transient(parent)
        self.top.grab_set()
        
        # Center window
        self.top.update_idletasks()
        x = (self.top.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.top.winfo_screenheight() // 2) - (150 // 2)
        self.top.geometry(f"400x150+{x}+{y}")
        
        # Status label
        from src.i18n import t
        self.status_label = tk.Label(self.top, text=t('initializing'), font=("Arial", 10))
        self.status_label.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.top,
            orient="horizontal",
            length=360,
            mode="determinate"
        )
        self.progress.pack(pady=10)
        
        # Detail label
        self.detail_label = tk.Label(self.top, text="", font=("Arial", 8), fg="gray")
        self.detail_label.pack(pady=5)
        
        self.cancelled = False
    
    def update(self, value, status="", detail=""):
        """Update progress (0-100)"""
        self.progress['value'] = value
        if status:
            self.status_label.config(text=status)
        if detail:
            self.detail_label.config(text=detail)
        self.top.update()
    
    def close(self):
        """Close dialog"""
        self.top.grab_release()
        self.top.destroy()


class ImageImporter:
    """Import and trace images to vector objects"""
    
    @staticmethod
    def import_image(parent, canvas_width, canvas_height, on_complete=None):
        """
        Import image file and convert to vector objects
        Shows file dialog, progress dialog, and returns VectorGroup
        """
        # File dialog
        from src.i18n import t
        filepath = filedialog.askopenfilename(
            title=t('import_image_title'),
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("All Files", "*.*")
            ]
        )
        
        if not filepath:
            return None
        
        # Create progress dialog
        progress = ProgressDialog(parent, t('import_image_title'))
        
        result = {'group': None, 'error': None}
        
        def import_thread():
            try:
                # Load image
                progress.update(10, t('loading_image'), filepath)
                img = Image.open(filepath)
                
                # Convert to RGBA
                progress.update(20, t('converting'))
                img = img.convert('RGBA')
                
                # Resize if too large
                orig_width, orig_height = img.size
                scale = 1.0
                
                if orig_width > canvas_width or orig_height > canvas_height:
                    scale = min(canvas_width / orig_width, canvas_height / orig_height)
                    new_width = int(orig_width * scale)
                    new_height = int(orig_height * scale)
                    
                    progress.update(30, f"{t('resizing')} ({new_width}x{new_height})...",
                                   f"Original: {orig_width}x{orig_height}")
                    img = img.resize((new_width, new_height), Image.NEAREST)
                else:
                    new_width, new_height = orig_width, orig_height
                
                # Trace to pixels
                progress.update(40, t('tracing_pixels'),
                               f"Processing {new_width}x{new_height} pixels")
                
                pixels_data = img.load()
                objects = []
                total_pixels = new_width * new_height
                processed = 0
                
                for y in range(new_height):
                    for x in range(new_width):
                        r, g, b, a = pixels_data[x, y]
                        
                        # Skip fully transparent pixels
                        if a > 0:
                            obj = VectorPixel(x, y, (r, g, b, a))
                            objects.append(obj)
                        
                        processed += 1
                        if processed % 100 == 0:
                            percent = 40 + int((processed / total_pixels) * 50)
                            progress.update(
                                percent,
                                t('tracing_pixels'),
                                f"{processed}/{total_pixels} pixels"
                            )
                
                # Create group
                progress.update(95, t('creating_group'),
                               f"{len(objects)} objects created")
                
                import os
                filename = os.path.basename(filepath)
                group = VectorGroup(objects, f"Imported: {filename}")
                
                progress.update(100, t('complete'), f"{t('imported')} {len(objects)} pixels")
                
                result['group'] = group
                
            except Exception as e:
                result['error'] = str(e)
                progress.update(0, t('error'), str(e))
        
        # Run import in thread
        thread = threading.Thread(target=import_thread, daemon=True)
        thread.start()
        
        # Wait for completion
        while thread.is_alive():
            parent.update()
            thread.join(timeout=0.01)
        
        # Close progress dialog
        parent.after(500, progress.close)  # Show completion for a moment
        parent.update()
        
        # Check for errors
        if result['error']:
            messagebox.showerror(t('import_error'), f"Failed to import image:\n{result['error']}")
            return None
        
        # Call callback
        if on_complete and result['group']:
            on_complete(result['group'])
        
        return result['group']
    
    @staticmethod
    def quick_import(filepath, canvas_width, canvas_height):
        """Import image without GUI (for programmatic use)"""
        try:
            img = Image.open(filepath).convert('RGBA')
            
            # Resize if needed
            if img.width > canvas_width or img.height > canvas_height:
                scale = min(canvas_width / img.width, canvas_height / img.height)
                new_size = (int(img.width * scale), int(img.height * scale))
                img = img.resize(new_size, Image.NEAREST)
            
            # Trace to pixels
            pixels_data = img.load()
            objects = []
            
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b, a = pixels_data[x, y]
                    if a > 0:
                        objects.append(VectorPixel(x, y, (r, g, b, a)))
            
            return VectorGroup(objects, f"Imported")
            
        except Exception as e:
            print(f"Import error: {e}")
            return None
