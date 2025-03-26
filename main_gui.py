import tkinter as tk
from scan_window import ScanWindow

def main():
    root = tk.Tk()
    app = ScanWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
