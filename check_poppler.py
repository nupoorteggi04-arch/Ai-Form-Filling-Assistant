"""
Helper script to check if Poppler is installed and find its location.
Run this script to help configure Poppler for PDF processing.
"""
import os

def check_poppler():
    """Check for Poppler installation in common locations."""
    print("Checking for Poppler installation...\n")
    
    common_paths = [
        r"C:\poppler\Library\bin",
        r"C:\Program Files\poppler\bin",
        r"C:\Program Files (x86)\poppler\bin",
        r"C:\Users\{}\poppler\Library\bin".format(os.getenv('USERNAME', 'User')),
        r"C:\tools\poppler\bin",
    ]
    
    found_paths = []
    
    for path in common_paths:
        pdftoppm = os.path.join(path, "pdftoppm.exe")
        if os.path.exists(pdftoppm):
            found_paths.append(path)
            print(f"[OK] Found Poppler at: {path}")
            print(f"  pdftoppm.exe exists: {os.path.exists(pdftoppm)}\n")
    
    if not found_paths:
        print("X Poppler not found in common locations.\n")
        print("To install Poppler:")
        print("1. Download from: https://github.com/oschwartz10612/poppler-windows/releases")
        print("2. Extract to C:\\poppler (or another location)")
        print("3. Update backend/main.py with the path, or add to system PATH\n")
        return None
    
    if len(found_paths) == 1:
        print(f"\n[OK] Poppler found! Use this path in backend/main.py:")
        print(f"  POPPLER_PATH = r\"{found_paths[0]}\"")
        return found_paths[0]
    else:
        print(f"\n[OK] Multiple Poppler installations found. Using the first one:")
        print(f"  POPPLER_PATH = r\"{found_paths[0]}\"")
        return found_paths[0]

if __name__ == "__main__":
    path = check_poppler()
    if path:
        print(f"\nTo fix the error, add this line to backend/main.py (around line 61):")
        print(f"POPPLER_PATH = r\"{path}\"")

