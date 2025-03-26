import tkinter as tk
from tkinter import ttk
from typing import List, Dict
from file_utils import FileScanner

class ScanWindow:
    """GUI window for visualizing file system scan progress."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.scanner = FileScanner()
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the user interface components."""
        self.root.title("File System Scanner")
        self.root.geometry("800x600")
        
        # Progress frame
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.progress_frame,
            orient=tk.HORIZONTAL,
            length=600,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(
            self.progress_frame,
            text="Ready to scan",
            font=('Arial', 10)
        )
        self.status_label.pack(pady=5)
        
        # Results treeview
        self.results_tree = ttk.Treeview(
            self.progress_frame,
            columns=('path', 'size', 'type', 'modified'),
            show='headings'
        )
        self.results_tree.heading('path', text='Path')
        self.results_tree.heading('size', text='Size')
        self.results_tree.heading('type', text='Type')
        self.results_tree.heading('modified', text='Last Modified')
        self.results_tree.column('path', width=400)
        self.results_tree.column('size', width=100)
        self.results_tree.column('type', width=150)
        self.results_tree.column('modified', width=150)
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Control buttons
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_button = ttk.Button(
            self.control_frame,
            text="Start Scan",
            command=self.start_scan
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            self.control_frame,
            text="Stop Scan",
            command=self.stop_scan,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.export_button = ttk.Button(
            self.control_frame,
            text="Export Results",
            command=self.export_results,
            state=tk.DISABLED
        )
        self.export_button.pack(side=tk.RIGHT, padx=5)
    
    def start_scan(self):
        """Start the scanning process."""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.DISABLED)
        self.results_tree.delete(*self.results_tree.get_children())
        self.progress['value'] = 0
        self.status_label.config(text="Scanning...")
        
        # Start scan in a separate thread
        import threading
        self.scan_thread = threading.Thread(
            target=self.perform_scan,
            args=('c:/Users/casey/OneDrive/Documents/GitHub/Local-File-Organizer', True)
        )
        self.scan_thread.start()
    
    def stop_scan(self):
        """Stop the scanning process."""
        self.scanner.stop_scan = True
        self.status_label.config(text="Scan stopped")
        self.stop_button.config(state=tk.DISABLED)
        self.export_button.config(state=tk.NORMAL)
    
    def perform_scan(self, path: str, exhaustive: bool):
        """Perform the actual scanning process."""
        results = self.scanner.scan_directory(path, exhaustive)
        self.root.after(0, self.update_results, results)
    
    def update_results(self, results: List[Dict]):
        """Update the UI with scan results."""
        for result in results:
            self.results_tree.insert('', 'end', values=(
                result['path'],
                result['size'],
                result['file_type'],
                result['modified']
            ))
        self.progress['value'] = 100
        self.status_label.config(text="Scan complete")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.export_button.config(state=tk.NORMAL)
    
    def export_results(self):
        """Export scan results to a file."""
        import json
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            results = []
            for item in self.results_tree.get_children():
                values = self.results_tree.item(item, 'values')
                results.append({
                    'path': values[0],
                    'size': values[1],
                    'type': values[2],
                    'modified': values[3]
                })
            
            with open(file_path, 'w') as f:
                json.dump(results, f, indent=2)
            self.status_label.config(text=f"Results exported to {file_path}")

def main():
    """Main function to run the scan window."""
    root = tk.Tk()
    app = ScanWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
