#!/usr/bin/env python3
"""
Simple GUI Test Script
======================

Test script to debug GUI issues and ensure the interface works properly.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def test_basic_tkinter():
    """Test if basic tkinter works."""
    try:
        root = tk.Tk()
        root.title("Tkinter Test")
        root.geometry("300x200")
        
        label = tk.Label(root, text="Tkinter is working!")
        label.pack(pady=20)
        
        button = tk.Button(root, text="Click Me", command=lambda: messagebox.showinfo("Test", "Button works!"))
        button.pack(pady=20)
        
        print("Basic tkinter test successful")
        root.mainloop()
        return True
    except Exception as e:
        print(f"Basic tkinter test failed: {e}")
        return False

def test_customtkinter():
    """Test if customtkinter works."""
    try:
        import customtkinter as ctk
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        root = ctk.CTk()
        root.title("CustomTkinter Test")
        root.geometry("400x300")
        
        label = ctk.CTkLabel(root, text="CustomTkinter is working!")
        label.pack(pady=20)
        
        button = ctk.CTkButton(root, text="Test Button", command=lambda: print("Button clicked!"))
        button.pack(pady=20)
        
        print("CustomTkinter test successful")
        root.mainloop()
        return True
    except Exception as e:
        print(f"CustomTkinter test failed: {e}")
        return False

def main():
    """Run GUI tests."""
    print("Starting GUI tests...")
    
    # Test basic tkinter
    print("\n1. Testing basic tkinter...")
    tkinter_works = test_basic_tkinter()
    
    # Test customtkinter
    print("\n2. Testing customtkinter...")
    customtkinter_works = test_customtkinter()
    
    # Summary
    print("\n" + "="*50)
    print("GUI TEST RESULTS:")
    print(f"Tkinter: {'✅ Working' if tkinter_works else '❌ Failed'}")
    print(f"CustomTkinter: {'✅ Working' if customtkinter_works else '❌ Failed'}")
    print("="*50)
    
    if not tkinter_works:
        print("\n❌ Tkinter is not working. This is a system issue.")
        print("Try installing tkinter: sudo pacman -S tk")
    elif not customtkinter_works:
        print("\n❌ CustomTkinter is not working. Check installation.")
        print("Try: pip install customtkinter")
    else:
        print("\n✅ Both GUI libraries are working correctly!")

if __name__ == "__main__":
    main() 