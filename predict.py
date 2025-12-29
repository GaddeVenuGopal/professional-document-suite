"""
Replicate prediction script for Professional Document Suite
This script provides a simple interface to run the PDF and image tools via Replicate
"""
import os
import tempfile
from pathlib import Path
from typing import List, Optional
import mimetypes

# Import our modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from unified_app.modules.pdf_operations import (
    merge_pdfs, split_pdf, rotate_pdf, compress_pdf, 
    unlock_pdf, protect_with_password, remove_password, 
    add_digital_signature, extract_pages, delete_pages
)
from unified_app.modules.image_operations import (
    convert_jpg_to_png, convert_png_to_jpg, 
    convert_webp_to_jpg, convert_webp_to_png, 
    images_to_pdf
)

# Try to import replicate
try:
    from replicate import create
except ImportError:
    create = None

# Try to import PIL for image handling
try:
    from PIL import Image
except ImportError:
    Image = None

def predict(
    input_files: List[Path],
    operation: str = "merge_pdfs",
    output_format: str = "pdf",
    **kwargs
) -> List[Path]:
    """
    Main prediction function for Replicate deployment
    
    Args:
        input_files: List of input files to process
        operation: Which operation to perform
        output_format: Desired output format
        **kwargs: Additional parameters for specific operations
    
    Returns:
        List of output file paths
    """
    
    # Create a temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Copy input files to temp directory so we can work with them
        temp_input_paths = []
        for i, input_file in enumerate(input_files):
            temp_input_path = os.path.join(temp_dir, f"input_{i}_{input_file.name}")
            with open(temp_input_path, 'wb') as f:
                f.write(input_file.read())
            temp_input_paths.append(temp_input_path)
        
        # Process based on operation type
        if operation.startswith("pdf_"):
            # PDF operations
            if operation == "pdf_merge":
                return [merge_pdfs([open(p, 'rb') for p in temp_input_paths])]
            elif operation == "pdf_split":
                method = kwargs.get("method", "range")
                start = kwargs.get("start_page", 1)
                end = kwargs.get("end_page", 2)
                return [split_pdf(open(temp_input_paths[0], 'rb'), method, start, end)]
            elif operation == "pdf_rotate":
                angle = kwargs.get("angle", 90)
                pages = kwargs.get("pages", None)
                return [rotate_pdf(open(temp_input_paths[0], 'rb'), angle, pages)]
            elif operation == "pdf_compress":
                return [compress_pdf(open(temp_input_paths[0], 'rb'))]
            elif operation == "pdf_unlock":
                password = kwargs.get("password", "")
                result = unlock_pdf(open(temp_input_paths[0], 'rb'), password)
                if result is None:
                    raise ValueError("Incorrect password or unable to unlock PDF")
                return [result]
            elif operation == "pdf_protect":
                password = kwargs.get("password", "password")
                return [protect_with_password(open(temp_input_paths[0], 'rb'), password)]
            elif operation == "pdf_remove_password":
                password = kwargs.get("password", "")
                return [remove_password(open(temp_input_paths[0], 'rb'), password)]
            elif operation == "pdf_add_signature":
                signature_info = {
                    "name": kwargs.get("name", "Replicate User"),
                    "location": kwargs.get("location", "Cloud"),
                    "reason": kwargs.get("reason", "Digitally signed via Replicate"),
                    "contact_info": kwargs.get("contact_info", "user@replicate.com")
                }
                return [add_digital_signature(open(temp_input_paths[0], 'rb'), signature_info)]
            elif operation == "pdf_extract_pages":
                start_page = kwargs.get("start_page", 1)
                end_page = kwargs.get("end_page", 1)
                return [extract_pages(open(temp_input_paths[0], 'rb'), start_page, end_page)]
            elif operation == "pdf_delete_pages":
                pages_to_delete = kwargs.get("pages_to_delete", [1])
                return [delete_pages(open(temp_input_paths[0], 'rb'), pages_to_delete)]
        
        elif operation.startswith("image_"):
            # Image operations
            if operation == "image_jpg_to_png":
                return [convert_jpg_to_png(temp_input_paths[0])]
            elif operation == "image_png_to_jpg":
                return [convert_png_to_jpg(temp_input_paths[0])]
            elif operation == "image_webp_to_jpg":
                return [convert_webp_to_jpg(temp_input_paths[0])]
            elif operation == "image_webp_to_png":
                return [convert_webp_to_png(temp_input_paths[0])]
            elif operation == "image_to_pdf":
                output_pdf_path = os.path.join(temp_dir, "output.pdf")
                return [images_to_pdf(temp_input_paths, output_pdf_path)]
        
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    
    return []


# If run directly for testing
if __name__ == "__main__":
    import sys
    print("Professional Document Suite - Replicate Interface")
    print("This module provides PDF and image processing capabilities for Replicate deployment")
    print("Available operations: pdf_merge, pdf_split, pdf_rotate, pdf_compress, pdf_unlock, pdf_protect,")
    print("                        pdf_remove_password, pdf_add_signature, pdf_extract_pages, pdf_delete_pages,")
    print("                        image_jpg_to_png, image_png_to_jpg, image_webp_to_jpg, image_webp_to_png, image_to_pdf")