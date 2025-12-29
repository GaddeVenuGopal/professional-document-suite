"""
PDF Converter Module
Handles conversion from images to PDF documents.
"""

import os
from PIL import Image
import img2pdf


def images_to_pdf(image_paths: list[str], output_path: str) -> str:
    """
    Convert image files to a PDF document.
    
    Args:
        image_paths (list[str]): List of paths to image files
        output_path (str): Path for the output PDF file
        
    Returns:
        str: Path to the created PDF file
        
    Raises:
        FileNotFoundError: If any input file doesn't exist
        ValueError: If output path doesn't end with .pdf
    """
    # Validate input files
    for image_path in image_paths:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Input file {image_path} not found")
    
    # Check that output ends with .pdf
    if not output_path.lower().endswith('.pdf'):
        raise ValueError("Output file must have .pdf extension")
    
    # Save as PDF using img2pdf
    with open(output_path, 'wb') as f:
        f.write(img2pdf.convert(image_paths))
    
    print(f"Created PDF {output_path} from {len(image_paths)} image(s)")
    return output_path


def validate_image_files(image_paths: list[str]) -> bool:
    """
    Validate that all paths point to valid image files.
    
    Args:
        image_paths (list[str]): List of paths to validate
        
    Returns:
        bool: True if all files are valid images, False otherwise
    """
    for image_path in image_paths:
        if not os.path.exists(image_path):
            return False
        try:
            with Image.open(image_path):
                pass
        except Exception:
            return False
    return True


if __name__ == "__main__":
    # Example usage
    pass