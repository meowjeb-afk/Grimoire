"""
Optical Scrying Module
Handles OCR text extraction and screen capture operations.
"""
import os
import mss
import pytesseract
from PIL import Image

class OpticalScrying:
    def __init__(self):
        """
        Initializes the Optical Scrying engine.
        Note: Requires Tesseract OCR installed on the system.
        """
        # Set Tesseract path for Windows (adjust if installed elsewhere)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        print("[OpticalScrying] Engine initialized.")

    def extract_text_from_image(self, image_path):
        """
        Reads text from an image file using Tesseract OCR.
        Returns the extracted text as a string.
        """
        print(f"[Processing] Extracting text from: {image_path}")
        try:
            img = Image.open(image_path)
            # Use PSM 6 for uniform block of text
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(img, config=custom_config)
            print(f"[Success] Extracted {len(text)} characters.")
            return text.strip()
        except Exception as e:
            error_msg = f"[Scrying Failed] {e}"
            print(error_msg)
            return error_msg

    def capture_region(self, monitor_index=1):
        """
        Captures a screenshot of the specified monitor.
        Returns the path to the saved temporary image.
        """
        print(f"[Processing] Capturing monitor {monitor_index}...")
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[monitor_index]
                sct_img = sct.grab(monitor)
                # Convert to PIL Image (BGRX to RGB)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                
                # Save to temp directory
                temp_dir = os.getenv('TEMP', os.path.expanduser('~'))
                temp_path = os.path.join(temp_dir, "grimoire_scry.png")
                img.save(temp_path)
                print(f"[Success] Screenshot saved to: {temp_path}")
                return temp_path
        except Exception as e:
            error_msg = f"[Capture Failed] {e}"
            print(error_msg)
            return error_msg
