"""
Spotify Keychain 3D Model Generator - Simple GUI
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import os
import sys
import glob
import webbrowser

import cadquery as cq
import requests
import io
from PIL import Image
import utils


class SpotifyKeychainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify Keychain Generator")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Get script directory (works for both Python script and PyInstaller exe)
        if getattr(sys, 'frozen', False):
            # Running as compiled exe
            self.script_dir = os.path.dirname(sys.executable)
        else:
            # Running as Python script
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_models_dir = os.path.join(self.script_dir, "base_models")
        
        # Build UI
        self.create_ui()
        
        # Load .step files
        self.refresh_step_files()
        
    def create_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        # ===== TOP ROW: URL + Save Location =====
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 15))
        
        # URL Section
        url_frame = tk.Frame(top_frame)
        url_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Label(url_frame, text="Spotify URL:").pack(anchor="w")
        self.url_entry = tk.Entry(url_frame)
        self.url_entry.pack(fill="x", pady=(5, 0))
        
        # Save Location Section
        save_frame = tk.Frame(top_frame)
        save_frame.pack(side="right", fill="x", expand=True)
        
        tk.Label(save_frame, text="Save Location:").pack(anchor="w")
        
        save_row = tk.Frame(save_frame)
        save_row.pack(fill="x", pady=(5, 0))
        
        self.output_path = tk.StringVar(value=os.path.join(self.script_dir, "model.stl"))
        self.path_entry = tk.Entry(save_row, textvariable=self.output_path)
        self.path_entry.pack(side="left", fill="x", expand=True)
        
        tk.Button(save_row, text="...", command=self.browse_output, width=3).pack(side="right", padx=(5, 0))
        
        # ===== BASE MODEL SELECTION =====
        model_frame = tk.LabelFrame(main_frame, text="Base Model Selection (.step files)", padx=10, pady=10)
        model_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Listbox with scrollbar
        list_frame = tk.Frame(model_frame)
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.step_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=8)
        self.step_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.step_listbox.yview)
        
        # Refresh button
        tk.Button(model_frame, text="Refresh", command=self.refresh_step_files).pack(anchor="e", pady=(10, 0))
        
        # ===== STATUS & GENERATE =====
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill="x")
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(bottom_frame, textvariable=self.status_var, anchor="w")
        self.status_label.pack(side="left", fill="x", expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(bottom_frame, length=150, mode="determinate")
        self.progress.pack(side="left", padx=(10, 10))
        
        # Generate button
        self.generate_btn = tk.Button(bottom_frame, text="Generate", command=self.start_generation, width=12)
        self.generate_btn.pack(side="right")
        
        # ===== FOOTER =====
        footer_frame = tk.Frame(main_frame)
        footer_frame.pack(fill="x", pady=(15, 0))
        
        # GitHub link (left)
        github_link = tk.Label(footer_frame, text="github.com/ottamina", fg="blue", cursor="hand2")
        github_link.pack(side="left")
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/ottamina"))
        
        # Credits (right)
        tk.Label(footer_frame, text="Made by Osman Teksoy").pack(side="right")
        
    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".stl",
            filetypes=[("STL files", "*.stl"), ("All files", "*.*")],
            initialfile="model.stl"
        )
        if file_path:
            self.output_path.set(file_path)
            
    def refresh_step_files(self):
        """Scan base_models directory for .step files"""
        self.step_listbox.delete(0, tk.END)
        
        # Check if base_models folder exists
        if not os.path.exists(self.base_models_dir):
            os.makedirs(self.base_models_dir)
            self.step_listbox.insert(tk.END, "(base_models folder is empty)")
            return
        
        step_files = glob.glob(os.path.join(self.base_models_dir, "*.step"))
        step_files += glob.glob(os.path.join(self.base_models_dir, "*.STEP"))
        
        # Remove duplicates (case-insensitive)
        seen = set()
        unique_files = []
        for f in step_files:
            filename_lower = os.path.basename(f).lower()
            if filename_lower not in seen:
                seen.add(filename_lower)
                unique_files.append(f)
        
        if unique_files:
            for f in unique_files:
                filename = os.path.basename(f)
                self.step_listbox.insert(tk.END, filename)
            self.step_listbox.selection_set(0)  # Select first item
        else:
            self.step_listbox.insert(tk.END, "(No .step files found)")
            
    def get_selected_step_file(self):
        """Get the selected .step file path"""
        selection = self.step_listbox.curselection()
        if not selection:
            return None
        filename = self.step_listbox.get(selection[0])
        if filename.startswith("("):  # No files message
            return None
        return os.path.join(self.base_models_dir, filename)
        
    def start_generation(self):
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a Spotify URL")
            return
            
        step_file = self.get_selected_step_file()
        if not step_file:
            messagebox.showerror("Error", "Please select a base model")
            return
            
        self.generate_btn.config(state="disabled")
        self.progress["value"] = 0
        
        thread = threading.Thread(target=self.generate_model, args=(url, step_file))
        thread.daemon = True
        thread.start()
        
    def generate_model(self, url, step_file):
        try:
            # Parse URL
            self.update_status("Parsing URL...", 10)
            data = utils.get_link_data(url)
            
            if not data or len(data) != 2:
                self.show_error("Invalid Spotify link")
                return
                
            # Download Spotify code
            self.update_status("Downloading Spotify code...", 30)
            code_url = f"https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2F000000%2Fwhite%2F640%2Fspotify%3A{data[0]}%3A{data[1]}"
            
            r = requests.get(code_url)
            if not r.ok:
                self.show_error("Failed to download Spotify code")
                return
                
            # Process image
            self.update_status("Processing image...", 50)
            img = Image.open(io.BytesIO(r.content)).crop((160, 0, 640-31, 160))
            width, height = img.size
            pix = img.load()
            
            # Get bar heights
            bar_heights = []
            max_height = 0
            
            for x in range(width):
                at_bar = False
                curr_height = 0
                
                for y in range(height):
                    if pix[x, y][0] > 20 or pix[x, y][1] > 20 or pix[x, y][2] > 20:
                        at_bar = True
                        curr_height += 1
                        
                if at_bar and curr_height > max_height:
                    max_height = curr_height / 20
                elif not at_bar and max_height > 0:
                    bar_heights.append(max_height)
                    max_height = 0
                    
            # Generate 3D model
            self.update_status(f"Generating 3D model ({len(bar_heights)} bars)...", 70)
            
            model = cq.importers.importStep(step_file)
            
            for i, bar in enumerate(bar_heights):
                model = (
                    model.pushPoints([(15.5 + i * 1.88, 7.5)])
                    .sketch()
                    .slot(9 / 5 * bar, 1, 90)
                    .finalize()
                    .extrude(4)
                )
                
            # Export
            self.update_status("Saving STL file...", 90)
            output_path = self.output_path.get()
            cq.exporters.export(model, output_path)
            
            self.update_status(f"Completed: {os.path.basename(output_path)}", 100)
            self.root.after(100, lambda: messagebox.showinfo("Success", f"Model saved to:\n{output_path}"))
            
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.root.after(0, lambda: self.generate_btn.config(state="normal"))
            
    def update_status(self, message, progress):
        self.root.after(0, lambda: self.status_var.set(message))
        self.root.after(0, lambda: self.progress.configure(value=progress))
        
    def show_error(self, message):
        self.root.after(0, lambda: self.status_var.set(f"Error: {message}"))
        self.root.after(0, lambda: messagebox.showerror("Error", message))
        self.root.after(0, lambda: self.generate_btn.config(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    app = SpotifyKeychainApp(root)
    root.mainloop()
