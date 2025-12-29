#!/usr/bin/env python3
"""
Main Entry Point for Image Converter
Command-line interface for the modular image conversion system.
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.modules.jpg_png_converter import convert_jpg_to_png, convert_png_to_jpg, get_image_format
from src.modules.webp_converter import convert_webp_to_jpg, convert_webp_to_png
from src.modules.pdf_converter import images_to_pdf


def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="Modular Image Converter")
    parser.add_argument("command", 
                        choices=["jpg-png", "png-jpg", "webp-jpg", "webp-png", "img-pdf"],
                        help="Conversion command to execute")
    parser.add_argument("inputs", nargs="+", help="Input file(s)")
    
    args = parser.parse_args()
    
    try:
        if args.command == "jpg-png":
            if len(args.inputs) != 1:
                print("Error: jpg-png conversion requires exactly one input file")
                return 1
            
            input_file = args.inputs[0]
            if not os.path.exists(input_file):
                print(f"Error: File {input_file} not found")
                return 1
                
            file_format = get_image_format(input_file)
            if file_format not in ['jpeg', 'jpg']:
                print(f"Error: File {input_file} is not a JPEG image")
                return 1
                
            convert_jpg_to_png(input_file)
            
        elif args.command == "png-jpg":
            if len(args.inputs) != 1:
                print("Error: png-jpg conversion requires exactly one input file")
                return 1
            
            input_file = args.inputs[0]
            if not os.path.exists(input_file):
                print(f"Error: File {input_file} not found")
                return 1
                
            file_format = get_image_format(input_file)
            if file_format not in ['png']:
                print(f"Error: File {input_file} is not a PNG image")
                return 1
                
            convert_png_to_jpg(input_file)
            
        elif args.command == "webp-jpg":
            if len(args.inputs) != 1:
                print("Error: webp-jpg conversion requires exactly one input file")
                return 1
            
            input_file = args.inputs[0]
            if not os.path.exists(input_file):
                print(f"Error: File {input_file} not found")
                return 1
                
            file_format = get_image_format(input_file)
            if file_format not in ['webp']:
                print(f"Error: File {input_file} is not a WebP image")
                return 1
                
            convert_webp_to_jpg(input_file)
            
        elif args.command == "webp-png":
            if len(args.inputs) != 1:
                print("Error: webp-png conversion requires exactly one input file")
                return 1
            
            input_file = args.inputs[0]
            if not os.path.exists(input_file):
                print(f"Error: File {input_file} not found")
                return 1
                
            file_format = get_image_format(input_file)
            if file_format not in ['webp']:
                print(f"Error: File {input_file} is not a WebP image")
                return 1
                
            convert_webp_to_png(input_file)
            
        elif args.command == "img-pdf":
            if len(args.inputs) < 2:
                print("Error: img-pdf conversion requires at least one input file and one output file")
                return 1
            
            image_files = args.inputs[:-1]
            output_pdf = args.inputs[-1]
            
            # Validate input files
            for img_file in image_files:
                if not os.path.exists(img_file):
                    print(f"Error: File {img_file} not found")
                    return 1
            
            # Check that output ends with .pdf
            if not output_pdf.lower().endswith('.pdf'):
                print("Error: Output file must have .pdf extension")
                return 1
                
            images_to_pdf(image_files, output_pdf)
            
        else:
            print(f"Unknown command: {args.command}")
            print("Available commands:")
            print("  jpg-png: Convert JPEG to PNG")
            print("  png-jpg: Convert PNG to JPEG")
            print("  webp-jpg: Convert WebP to JPEG")
            print("  webp-png: Convert WebP to PNG")
            print("  img-pdf: Convert images to PDF")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())