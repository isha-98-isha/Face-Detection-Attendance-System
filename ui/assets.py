"""
Asset management helpers.
"""
import os
from pathlib import Path
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "Images_GUI"

def get_image_path(filename):
    """Returns the absolute path to an image in the Images_GUI directory."""
    return str(IMAGES_DIR / filename)

def load_image(filename, size=None):
    """Loads an image from the Images_GUI directory and optionally resizes it."""
    try:
        path = get_image_path(filename)
        if not os.path.exists(path):
            return None
            
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {filename}: {e}")
        return None
