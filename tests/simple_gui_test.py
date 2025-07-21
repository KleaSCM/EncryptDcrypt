#!/usr/bin/env python3
"""
Simple GUI Test
==============

Just opens the GUI window to test if it's visible.
"""

import customtkinter as ctk

def main():
    """Open a simple GUI window."""
    print("Opening simple GUI test...")
    
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create window
    root = ctk.CTk()
    root.title("EncryptDecrypt Test")
    root.geometry("600x400")
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Make sure it's visible
    root.lift()
    root.focus_force()
    
    # Add some content
    label = ctk.CTkLabel(root, text="EncryptDecrypt GUI Test", font=ctk.CTkFont(size=20, weight="bold"))
    label.pack(pady=20)
    
    info_label = ctk.CTkLabel(root, text="If you can see this window, the GUI is working!")
    info_label.pack(pady=10)
    
    close_button = ctk.CTkButton(root, text="Close Window", command=root.quit)
    close_button.pack(pady=20)
    
    print("GUI window should be visible now. Press the Close button to exit.")
    
    # Start the GUI
    root.mainloop()
    
    print("GUI test completed.")

if __name__ == "__main__":
    main() 