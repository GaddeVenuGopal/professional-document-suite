"""
JPG ↔ PNG Converter Module
Handles conversion between JPEG and PNG image formats.
"""

import os
from PIL import Image
from pathlib import Path


def convert_jpg_to_png(input_path: str) -> str:
    """
    Convert a JPEG image to PNG format.
    
    Args:
        input_path (str): Path to the input JPEG file
        
    Returns:
        str: Path to the converted PNG file
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input file is not a JPEG
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found")
    
    # Verify it's a JPEG file
    try:
        with Image.open(input_path) as img:
            if img.format.lower() not in ['jpeg', 'jpg']:
                raise ValueError(f"Input file {input_path} is not a JPEG image")
    except Exception as e:
        raise ValueError(f"Unable to open image file: {e}")
    
    # Convert JPEG to PNG
    with Image.open(input_path) as img:
        # Handle transparency for PNG
        if img.mode in ('RGBA', 'LA'):
            # Already has transparency, keep as is
            pass
        elif img.mode == 'P':
            # Convert palette images to RGBA to preserve transparency
            img = img.convert('RGBA')
        else:
            # Convert to RGB for JPEG or RGBA for PNG
            img = img.convert('RGB')
        
        # Determine output filename
        input_stem = Path(input_path).stem
        output_filename = f"{input_stem}.png"
        
        # Save as PNG
        img.save(output_filename, 'PNG')
        
        print(f"Converted {input_path} to {output_filename}")
        return output_filename


def convert_png_to_jpg(input_path: str) -> str:
    """
    Convert a PNG image to JPEG format.
    
    Args:
        input_path (str): Path to the input PNG file
        
    Returns:
        str: Path to the converted JPEG file
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input file is not a PNG
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found")
    
    # Verify it's a PNG file
    try:
        with Image.open(input_path) as img:
            if img.format.lower() not in ['png']:
                raise ValueError(f"Input file {input_path} is not a PNG image")
    except Exception as e:
        raise ValueError(f"Unable to open image file: {e}")
    
    # Convert PNG to JPEG
    with Image.open(input_path) as img:
        # JPEG doesn't support transparency, convert to RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background for transparent images
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        else:
            img = img.convert('RGB')
        
        # Determine output filename
        input_stem = Path(input_path).stem
        output_filename = f"{input_stem}.jpg"
        
        # Save as JPEG
        img.save(output_filename, 'JPEG', quality=95)
        
        print(f"Converted {input_path} to {output_filename}")
        return output_filename


def get_image_format(file_path: str) -> str:
    """
    Determine the format of an image file.
    
    Args:
        file_path (str): Path to the image file
        
    Returns:
        str: Image format (jpg, png, etc.)
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a valid image
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
        
    try:
        with Image.open(file_path) as img:
            return img.format.lower()
    except Exception as e:
        raise ValueError(f"Unable to determine format of {file_path}: {e}")


if __name__ == "__main__":
    # Example usage
    pass