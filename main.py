#!/usr/bin/env python3
"""
PixeLab - Main Entry Point
Runs the full-featured vector-pixel editor
"""
import sys
import tkinter as tk
from tkinter import messagebox

# 전체 UI 앱 실행
try:
    from pixelab_full import PixelLabFullApp
    
    def main():
        root = tk.Tk()
        app = PixelLabFullApp(root)
        root.mainloop()
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Error: {e}")
    print("Running simple version...")
    
    # v2.1 간단 버전으로 대체
    try:
        from pixelab_v2 import PixelLabVectorApp, main as v2_main
        v2_main()
    except Exception as e2:
        print(f"Failed to run: {e2}")
        sys.exit(1)
