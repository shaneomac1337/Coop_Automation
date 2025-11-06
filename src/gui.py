#!/usr/bin/env python3
"""
Store Configuration Generator GUI

A simple graphical user interface for generating and validating
store configuration files.

Usage:
    python gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import sys
from pathlib import Path
from typing import Optional
import json

# Import existing modules
from generate_store_config import StoreConfigGenerator
from validate_config import ConfigValidator

# Import for Excel conversion (optional - will check if available)
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class StoreConfigGUI:
    """Simple GUI for Store Configuration Generator."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Coop Store Configuration Generator")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Variables
        self.generator: Optional[StoreConfigGenerator] = None
        self.validator = ConfigValidator()
        self.store_list: list = []
        
        # Create UI
        self.create_widgets()
        self.load_store_list()
        
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # ===== Title =====
        title_label = ttk.Label(
            main_frame, 
            text="🏪 Coop Store Configuration Generator",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # ===== Configuration Section =====
        config_frame = ttk.LabelFrame(main_frame, text="Configuration Files", padding="10")
        config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Mapping file
        ttk.Label(config_frame, text="Store Mapping:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mapping_var = tk.StringVar(value="config/mappings/store_wall_mapping.json")
        mapping_entry = ttk.Entry(config_frame, textvariable=self.mapping_var, width=40)
        mapping_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Template file
        ttk.Label(config_frame, text="Template File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.template_var = tk.StringVar(value="config/templates/template.xml")
        template_entry = ttk.Entry(config_frame, textvariable=self.template_var, width=40)
        template_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Output directory
        ttk.Label(config_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar(value="output")
        output_entry = ttk.Entry(config_frame, textvariable=self.output_var, width=40)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # ===== Excel Conversion Section =====
        excel_frame = ttk.LabelFrame(main_frame, text="Service Cards Conversion", padding="10")
        excel_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        excel_frame.columnconfigure(1, weight=1)
        
        # Excel file
        ttk.Label(excel_frame, text="Excel File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.excel_var = tk.StringVar(value="service-cards.xlsx")
        excel_entry = ttk.Entry(excel_frame, textvariable=self.excel_var, width=30)
        excel_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Button(
            excel_frame, 
            text="Browse...", 
            command=self.browse_excel_file
        ).grid(row=0, column=2, padx=5)
        
        # JSON output file
        ttk.Label(excel_frame, text="JSON Output:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.json_output_var = tk.StringVar(value="config/mappings/service_cards_mapping.json")
        json_entry = ttk.Entry(excel_frame, textvariable=self.json_output_var, width=30)
        json_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Convert button
        convert_button_frame = ttk.Frame(excel_frame)
        convert_button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.convert_btn = ttk.Button(
            convert_button_frame, 
            text="📊 Convert Excel to JSON", 
            command=self.convert_excel_to_json
        )
        self.convert_btn.pack(side=tk.LEFT, padx=5)
        
        # Show warning if pandas not available
        if not PANDAS_AVAILABLE:
            warning_label = ttk.Label(
                excel_frame,
                text="⚠️ pandas not installed. Install with: pip install pandas openpyxl",
                foreground="orange"
            )
            warning_label.grid(row=3, column=0, columnspan=3, pady=5)
            self.convert_btn.config(state="disabled")
        
        # ===== Store Selection Section =====
        store_frame = ttk.LabelFrame(main_frame, text="Store Selection", padding="10")
        store_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        store_frame.columnconfigure(0, weight=1)
        
        # Radio buttons for generation mode
        self.gen_mode = tk.StringVar(value="all")
        
        radio_frame = ttk.Frame(store_frame)
        radio_frame.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            radio_frame, 
            text="Generate All Stores (Separate Files)", 
            variable=self.gen_mode, 
            value="all"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            radio_frame, 
            text="Generate All Stores (Combined File)", 
            variable=self.gen_mode, 
            value="combined"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            radio_frame, 
            text="Generate Single Store", 
            variable=self.gen_mode, 
            value="single"
        ).pack(side=tk.LEFT, padx=5)
        
        # Store selection combobox
        store_select_frame = ttk.Frame(store_frame)
        store_select_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(store_select_frame, text="Select Store:").pack(side=tk.LEFT, padx=5)
        self.store_combo = ttk.Combobox(store_select_frame, width=50, state="readonly")
        self.store_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # ===== Action Buttons =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, pady=10)
        
        self.generate_btn = ttk.Button(
            button_frame, 
            text="🚀 Generate Configuration", 
            command=self.generate_config,
            style="Accent.TButton"
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.validate_btn = ttk.Button(
            button_frame, 
            text="✓ Validate Output", 
            command=self.validate_output
        )
        self.validate_btn.pack(side=tk.LEFT, padx=5)
        
        self.open_output_btn = ttk.Button(
            button_frame, 
            text="📁 Open Output Folder", 
            command=self.open_output_folder
        )
        self.open_output_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="🔄 Reload Stores", 
            command=self.load_store_list
        ).pack(side=tk.LEFT, padx=5)
        
        # ===== Output Log =====
        log_frame = ttk.LabelFrame(main_frame, text="Output Log", padding="10")
        log_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Create scrolled text widget
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            width=80,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        ttk.Button(
            log_frame, 
            text="Clear Log", 
            command=self.clear_log
        ).grid(row=1, column=0, pady=(5, 0))
        
        # ===== Status Bar =====
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=6, column=0, sticky=(tk.W, tk.E))
        
    def log(self, message: str):
        """Add message to log output."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear the log output."""
        self.log_text.delete(1.0, tk.END)
        
    def set_status(self, message: str):
        """Update status bar."""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def load_store_list(self):
        """Load list of stores from mapping file."""
        try:
            mapping_file = self.mapping_var.get()
            with open(mapping_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.store_list = []
            for store_id, store_data in data.get('stores', {}).items():
                store_name = store_data.get('name', 'Unknown')
                self.store_list.append(f"{store_id} - {store_name}")
            
            self.store_combo['values'] = self.store_list
            if self.store_list:
                self.store_combo.current(0)
                
            self.log(f"✓ Loaded {len(self.store_list)} stores from {mapping_file}")
            
        except FileNotFoundError:
            self.log(f"⚠️ Mapping file not found: {mapping_file}")
        except json.JSONDecodeError as e:
            self.log(f"❌ Invalid JSON in mapping file: {e}")
        except Exception as e:
            self.log(f"❌ Error loading stores: {e}")
            
    def generate_config(self):
        """Generate configuration files."""
        # Disable button during generation
        self.generate_btn.config(state="disabled")
        
        # Run in thread to keep GUI responsive
        thread = threading.Thread(target=self._generate_config_thread)
        thread.daemon = True
        thread.start()
        
    def _generate_config_thread(self):
        """Thread worker for configuration generation."""
        try:
            self.clear_log()
            self.log("🚀 Starting configuration generation...")
            self.set_status("Generating...")
            
            # Initialize generator
            generator = StoreConfigGenerator(
                mapping_file=self.mapping_var.get(),
                template_file=self.template_var.get(),
                ip_mapping_file="config/mappings/store_ip_mapping.properties",
                service_cards_file="config/mappings/service_cards_mapping.json"
            )
            
            output_dir = self.output_var.get()
            mode = self.gen_mode.get()
            
            if mode == "all":
                # Generate all stores (separate files)
                self.log("📦 Generating separate files for all stores...")
                files = generator.generate_all_stores(output_dir, combined=False)
                self.log(f"\n✅ Generated {len(files)} configuration files!")
                for f in files:
                    self.log(f"   📄 {f}")
                    
            elif mode == "combined":
                # Generate all stores (combined file)
                self.log("📦 Generating combined file for all stores...")
                files = generator.generate_all_stores(output_dir, combined=True)
                self.log(f"\n✅ Generated combined configuration file!")
                self.log(f"   📄 {files[0]}")
                
            else:  # single
                # Generate single store
                selected = self.store_combo.get()
                if not selected:
                    self.log("❌ Please select a store")
                    return
                    
                store_id = selected.split(" - ")[0]
                self.log(f"📦 Generating configuration for store {store_id}...")
                
                output_file = generator.save_store_config(store_id, output_dir)
                self.log(f"\n✅ Generated configuration file!")
                self.log(f"   📄 {output_file}")
            
            self.set_status("Generation completed successfully!")
            messagebox.showinfo("Success", "Configuration generated successfully!")
            
        except Exception as e:
            self.log(f"\n❌ Error: {e}")
            self.set_status("Generation failed")
            messagebox.showerror("Error", f"Configuration generation failed:\n{e}")
            
        finally:
            # Re-enable button
            self.generate_btn.config(state="normal")
            
    def validate_output(self):
        """Validate generated configuration files."""
        # Disable button during validation
        self.validate_btn.config(state="disabled")
        
        # Run in thread
        thread = threading.Thread(target=self._validate_thread)
        thread.daemon = True
        thread.start()
        
    def _validate_thread(self):
        """Thread worker for validation."""
        try:
            self.clear_log()
            self.log("🔍 Starting validation...")
            self.set_status("Validating...")
            
            output_dir = self.output_var.get()
            
            if not Path(output_dir).exists():
                self.log(f"❌ Output directory not found: {output_dir}")
                self.set_status("Validation failed")
                return
            
            # Validate all files in output directory
            results = self.validator.validate_directory(output_dir)
            
            if not results:
                self.log("⚠️ No XML files found to validate")
                self.set_status("No files to validate")
                return
            
            # Show results
            valid_count = sum(1 for r in results if r["valid"])
            invalid_count = len(results) - valid_count
            
            self.log(f"\n📊 Validation Summary:")
            self.log(f"   ✅ Valid files: {valid_count}")
            self.log(f"   ❌ Invalid files: {invalid_count}")
            self.log(f"   📁 Total files: {len(results)}")
            
            # Show details for invalid files
            if invalid_count > 0:
                self.log(f"\n❌ Invalid files:")
                for result in results:
                    if not result["valid"]:
                        self.log(f"\n   {result['file']}")
                        for error in result['errors']:
                            self.log(f"      - {error}")
            
            self.set_status(f"Validation complete: {valid_count}/{len(results)} valid")
            
            if invalid_count == 0:
                messagebox.showinfo("Success", "All configurations are valid!")
            else:
                messagebox.showwarning("Warning", f"{invalid_count} invalid file(s) found. Check log for details.")
                
        except Exception as e:
            self.log(f"\n❌ Error: {e}")
            self.set_status("Validation failed")
            messagebox.showerror("Error", f"Validation failed:\n{e}")
            
        finally:
            # Re-enable button
            self.validate_btn.config(state="normal")
            
    def open_output_folder(self):
        """Open the output folder in file explorer."""
        try:
            output_dir = Path(self.output_var.get())
            if not output_dir.exists():
                messagebox.showwarning("Warning", f"Output directory does not exist:\n{output_dir}")
                return
                
            # Open in file explorer (cross-platform)
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", str(output_dir)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(output_dir)])
            else:  # Linux
                subprocess.run(["xdg-open", str(output_dir)])
                
            self.log(f"📁 Opened output folder: {output_dir}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder:\n{e}")
    
    def browse_excel_file(self):
        """Browse for Excel file."""
        filename = filedialog.askopenfilename(
            title="Select Service Cards Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ],
            initialdir="."
        )
        if filename:
            self.excel_var.set(filename)
            self.log(f"📄 Selected Excel file: {filename}")
    
    def convert_excel_to_json(self):
        """Convert Excel file to JSON."""
        if not PANDAS_AVAILABLE:
            messagebox.showerror(
                "Error", 
                "pandas library is not installed.\n\n"
                "Please install it with:\n"
                "pip install pandas openpyxl"
            )
            return
        
        # Disable button during conversion
        self.convert_btn.config(state="disabled")
        
        # Run in thread
        thread = threading.Thread(target=self._convert_excel_thread)
        thread.daemon = True
        thread.start()
    
    def _convert_excel_thread(self):
        """Thread worker for Excel to JSON conversion."""
        try:
            self.clear_log()
            self.log("📊 Starting Excel to JSON conversion...")
            self.set_status("Converting...")
            
            excel_file = self.excel_var.get()
            output_file = self.json_output_var.get()
            
            # Check if Excel file exists
            if not Path(excel_file).exists():
                self.log(f"❌ Error: Excel file not found: {excel_file}")
                self.set_status("Conversion failed")
                messagebox.showerror("Error", f"Excel file not found:\n{excel_file}")
                return
            
            self.log(f"📖 Reading Excel file: {excel_file}")
            
            # Read the Excel file
            df = pd.read_excel(excel_file)
            
            # Group by SiteID (store)
            stores_dict = {}
            
            for _, row in df.iterrows():
                site_id = str(int(row['SiteID'])) if pd.notna(row['SiteID']) else None
                admin_card = str(int(row['Admin cards'])) if pd.notna(row['Admin cards']) else None
                
                if site_id and admin_card:
                    if site_id not in stores_dict:
                        stores_dict[site_id] = []
                    stores_dict[site_id].append(admin_card)
            
            # Create the JSON structure
            service_cards_data = {
                "metadata": {
                    "description": "Store to service card mapping for WDM configuration",
                    "version": "1.0",
                    "source": excel_file,
                    "total_stores": len(stores_dict),
                    "total_cards": sum(len(cards) for cards in stores_dict.values())
                },
                "stores": {}
            }
            
            # Add each store's cards
            for store_id in sorted(stores_dict.keys(), key=int):
                cards = stores_dict[store_id]
                service_cards_data["stores"][store_id] = {
                    "cards": cards,
                    "card_count": len(cards)
                }
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(service_cards_data, f, indent=2, ensure_ascii=False)
            
            self.log(f"\n✅ Conversion completed successfully!")
            self.log(f"   📁 Output file: {output_file}")
            self.log(f"\n📊 Summary:")
            self.log(f"   Total stores: {len(stores_dict)}")
            self.log(f"   Total cards: {service_cards_data['metadata']['total_cards']}")
            
            # Show top stores
            top_stores = sorted(stores_dict.items(), key=lambda x: len(x[1]), reverse=True)[:5]
            self.log(f"\n   Stores with most cards:")
            for store_id, cards in top_stores:
                self.log(f"      Store {store_id}: {len(cards)} cards")
            
            self.set_status("Conversion completed successfully!")
            messagebox.showinfo(
                "Success", 
                f"Excel file converted successfully!\n\n"
                f"Stores: {len(stores_dict)}\n"
                f"Cards: {service_cards_data['metadata']['total_cards']}\n\n"
                f"Output: {output_file}"
            )
            
        except FileNotFoundError:
            self.log(f"\n❌ Error: Excel file not found: {excel_file}")
            self.set_status("Conversion failed")
            messagebox.showerror("Error", f"Excel file not found:\n{excel_file}")
            
        except KeyError as e:
            self.log(f"\n❌ Error: Missing required column in Excel file: {e}")
            self.log("   Expected columns: 'SiteID', 'Admin cards'")
            self.set_status("Conversion failed")
            messagebox.showerror(
                "Error", 
                f"Missing required column in Excel file: {e}\n\n"
                "Expected columns: 'SiteID', 'Admin cards'"
            )
            
        except Exception as e:
            self.log(f"\n❌ Error: {e}")
            self.set_status("Conversion failed")
            messagebox.showerror("Error", f"Conversion failed:\n{e}")
            
        finally:
            # Re-enable button
            self.convert_btn.config(state="normal")


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    
    # Set application icon (if available)
    try:
        # You can add an icon file later
        # root.iconbitmap("icon.ico")
        pass
    except:
        pass
    
    # Create and run application
    app = StoreConfigGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Start GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
