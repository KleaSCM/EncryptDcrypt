"""
Modern GUI Interface
==================

Professional graphical user interface for the encryption system.

Author: KleaSCM <KleaSCM@gmail.com>
"""

import threading
from pathlib import Path
from typing import Dict
import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging

from ..core.engine import EncryptionEngine
from ..utils.file_utils import is_encrypted_file

logger = logging.getLogger(__name__)


class ModernGUI:
    """
    Modern GUI Interface for EncryptDecrypt System
    
    Provides a professional, user-friendly interface for file encryption and decryption.
    """
    
    def __init__(self):
        """Initialize the modern GUI with professional styling."""
        try:
            print("Initializing GUI components...")
            # Set appearance mode and color theme
            ctk.set_appearance_mode("dark")  # Dark mode 
            ctk.set_default_color_theme("blue")  # Blue theme
            
            # Create main window
            self.root = ctk.CTk()
            self.root.title("EncryptDecrypt - Advanced File Encryption System")
            self.root.geometry("800x600")
            self.root.resizable(True, True)
            
            # Ensure window stays on top initially and is visible
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.root.focus_force()
            
            # Keep window on top for a few seconds to ensure visibility
            self.root.after(3000, lambda: self.root.attributes('-topmost', False))
            
            # Center the window on screen
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')
            
            print("Main window created successfully")
        except Exception as e:
            print(f"Error initializing GUI: {e}")
            raise
        
        # Initialize encryption engine
        try:
            print("Initializing encryption engine...")
            self.encryption_engine = EncryptionEngine()
            print("Encryption engine initialized successfully")
        except Exception as e:
            print(f"Error initializing encryption engine: {e}")
            raise
        
        # GUI variables
        self.selected_directory = ctk.StringVar()
        self.progress_var = ctk.DoubleVar()
        self.status_var = ctk.StringVar(value="GUI loaded successfully - Ready to encrypt/decrypt files")
        
        try:
            print("Creating GUI widgets...")
            self._create_widgets()
            print("Setting up layout...")
            self._setup_layout()
            print("GUI setup completed successfully")
        except Exception as e:
            print(f"Error setting up GUI: {e}")
            raise
    
    def _create_widgets(self):
        """Create and configure all GUI widgets."""
        # Main title
        self.title_label = ctk.CTkLabel(
            self.root,
            text="EncryptDecrypt System",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        
        # Directory selection frame
        self.dir_frame = ctk.CTkFrame(self.root)
        self.dir_label = ctk.CTkLabel(self.dir_frame, text="Select Directory:")
        self.dir_entry = ctk.CTkEntry(self.dir_frame, textvariable=self.selected_directory, width=400)
        self.browse_button = ctk.CTkButton(
            self.dir_frame,
            text="Browse",
            command=self._browse_directory,
            width=100
        )
        
        # Action buttons frame
        self.button_frame = ctk.CTkFrame(self.root)
        self.encrypt_button = ctk.CTkButton(
            self.button_frame,
            text="Encrypt Files",
            command=self._encrypt_files,
            fg_color="green",
            hover_color="darkgreen",
            height=40
        )
        self.decrypt_button = ctk.CTkButton(
            self.button_frame,
            text="Decrypt Files",
            command=self._decrypt_files,
            fg_color="red",
            hover_color="darkred",
            height=40
        )
        
        # Progress frame
        self.progress_frame = ctk.CTkFrame(self.root)
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Progress:")
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        
        # Status frame
        self.status_frame = ctk.CTkFrame(self.root)
        self.status_label = ctk.CTkLabel(self.status_frame, text="Status:")
        self.status_display = ctk.CTkLabel(
            self.status_frame,
            textvariable=self.status_var,
            wraplength=600
        )
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self.root)
        self.results_label = ctk.CTkLabel(self.results_frame, text="Results:")
        self.results_text = ctk.CTkTextbox(self.results_frame, height=200)
    
    def _setup_layout(self):
        """Configure the layout of all widgets."""
        # Title
        self.title_label.pack(pady=20)
        
        # Directory selection
        self.dir_frame.pack(pady=10, padx=20, fill="x")
        self.dir_label.pack(anchor="w", padx=10, pady=(10, 5))
        self.dir_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.browse_button.pack(side="right", padx=10, pady=10)
        
        # Action buttons
        self.button_frame.pack(pady=10, padx=20, fill="x")
        self.encrypt_button.pack(side="left", padx=10, pady=10, expand=True)
        self.decrypt_button.pack(side="right", padx=10, pady=10, expand=True)
        
        # Progress
        self.progress_frame.pack(pady=10, padx=20, fill="x")
        self.progress_label.pack(anchor="w", padx=10, pady=(10, 5))
        self.progress_bar.pack(padx=10, pady=(0, 10), fill="x")
        
        # Status
        self.status_frame.pack(pady=10, padx=20, fill="x")
        self.status_label.pack(anchor="w", padx=10, pady=(10, 5))
        self.status_display.pack(padx=10, pady=(0, 10), fill="x")
        
        # Results
        self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.results_label.pack(anchor="w", padx=10, pady=(10, 5))
        self.results_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)
    
    def _browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory.set(directory)
            self.status_var.set(f"Selected directory: {directory}")
    
    def _encrypt_files(self):
        """Encrypt all files in the selected directory."""
        directory = self.selected_directory.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first!")
            return
        
        # Run encryption in separate thread
        thread = threading.Thread(target=self._encrypt_files_thread, args=(directory,))
        thread.daemon = True
        thread.start()
    
    def _encrypt_files_thread(self, directory: str):
        """Thread function for file encryption."""
        try:
            self.status_var.set("Starting encryption...")
            self.encrypt_button.configure(state="disabled")
            self.decrypt_button.configure(state="disabled")
            
            # Get all files in directory (excluding already encrypted files)
            files = [f for f in Path(directory).iterdir() if f.is_file() and not is_encrypted_file(str(f))]
            
            if not files:
                self.status_var.set("No files found to encrypt!")
                return
            
            results = []
            for i, file_path in enumerate(files):
                # Update progress
                progress = (i + 1) / len(files)
                self.progress_bar.set(progress)
                self.status_var.set(f"Encrypting: {file_path.name}")
                
                # Encrypt file
                result = self.encryption_engine.encrypt_file(str(file_path))
                results.append(result)
                
                # Update results display
                self.results_text.insert("end", f"✅ {file_path.name}: {result['status']}\n")
                self.results_text.see("end")
            
            self.status_var.set(f"Encryption complete! Processed {len(files)} files")
            self.progress_bar.set(1.0)
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            logger.error(f"Encryption error: {e}")
        finally:
            self.encrypt_button.configure(state="normal")
            self.decrypt_button.configure(state="normal")
    
    def _decrypt_files(self):
        """Decrypt all encrypted files in the selected directory."""
        directory = self.selected_directory.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first!")
            return
        
        # Run decryption in separate thread
        thread = threading.Thread(target=self._decrypt_files_thread, args=(directory,))
        thread.daemon = True
        thread.start()
    
    def _decrypt_files_thread(self, directory: str):
        """Thread function for file decryption."""
        try:
            self.status_var.set("Starting decryption...")
            self.encrypt_button.configure(state="disabled")
            self.decrypt_button.configure(state="disabled")
            
            # Get all encrypted files
            files = [f for f in Path(directory).iterdir() if f.is_file() and is_encrypted_file(str(f))]
            
            if not files:
                self.status_var.set("No encrypted files found!")
                return
            
            results = []
            for i, file_path in enumerate(files):
                # Update progress
                progress = (i + 1) / len(files)
                self.progress_bar.set(progress)
                self.status_var.set(f"Decrypting: {file_path.name}")
                
                # Decrypt file
                result = self.encryption_engine.decrypt_file(str(file_path))
                results.append(result)
                
                # Update results display
                self.results_text.insert("end", f"✅ {file_path.name}: {result['status']}\n")
                self.results_text.see("end")
            
            self.status_var.set(f"Decryption complete! Processed {len(files)} files")
            self.progress_bar.set(1.0)
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            logger.error(f"Decryption error: {e}")
        finally:
            self.encrypt_button.configure(state="normal")
            self.decrypt_button.configure(state="normal")
    
    def run(self):
        """Start the modern GUI application."""
        self.root.mainloop() 