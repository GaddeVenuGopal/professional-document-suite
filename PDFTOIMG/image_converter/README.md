# Modular Image Converter

A modular Python package for converting between various image formats and creating PDF documents from images.

## Features

1. **JPG ↔ PNG** - Convert between JPEG and PNG formats
2. **WebP → JPG/PNG** - Convert WebP images to traditional formats
3. **Image → PDF** - Create PDF documents from image files
4. **Streamlit Web Interface** - Professional web UI for easy conversions

## Installation

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### As a Package

```bash
pip install -e .
```

### Streamlit Web Interface

```bash
streamlit run app.py
```

## Usage

### As a Module

```python
from src.modules.jpg_png_converter import convert_jpg_to_png, convert_png_to_jpg
from src.modules.webp_converter import convert_webp_to_jpg, convert_webp_to_png
from src.modules.pdf_converter import images_to_pdf

# Convert JPG to PNG
convert_jpg_to_png("input.jpg")

# Convert PNG to JPG
convert_png_to_jpg("input.png")

# Convert WebP to JPG
convert_webp_to_jpg("input.webp")

# Convert WebP to PNG
convert_webp_to_png("input.webp")

# Convert images to PDF
images_to_pdf(["image1.jpg", "image2.png"], "output.pdf")
```

### Command Line

```bash
# After installing as package:
image-converter jpg-png input.jpg
image-converter png-jpg input.png
image-converter webp-jpg input.webp
image-converter webp-png input.webp
image-converter img-pdf image1.jpg image2.png output.pdf
```

## API Reference

### JPG/PNG Converter
- `convert_jpg_to_png(input_path: str) -> str`: Convert JPEG to PNG
- `convert_png_to_jpg(input_path: str) -> str`: Convert PNG to JPEG

### WebP Converter
- `convert_webp_to_jpg(input_path: str) -> str`: Convert WebP to JPEG
- `convert_webp_to_png(input_path: str) -> str`: Convert WebP to PNG

### PDF Converter
- `images_to_pdf(image_paths: list[str], output_path: str) -> str`: Convert images to PDF

### Streamlit Web Interface
- `app.py`: Professional web UI with tabbed interface for all conversion types

## Supported Formats

- **Input Formats**: JPG/JPEG, PNG, WebP
- **Output Formats**: JPG, PNG, PDF

## Notes

- When converting from transparent formats (PNG, WebP) to JPEG, transparent areas will be filled with white
- When creating PDFs, all images will be converted to RGB color mode
- Output files are saved in the same directory as the input files