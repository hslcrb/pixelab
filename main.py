#!/usr/bin/env python3
"""
PixeLab - Professional Pixel Art Editor
Entry point
"""
import sys
import tkinter as tk
from src.app import PixelLabApp


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PixelLabApp(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.quit)
    
    # Run
    root.mainloop()


if __name__ == "__main__":
    main()
