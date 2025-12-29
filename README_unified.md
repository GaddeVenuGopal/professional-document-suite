# Professional Document Suite

A comprehensive, unified application that combines both PDF manipulation and image conversion capabilities in a single, professional interface. Deployable on Replicate for API access.

## Features

### PDF Tools
- **Document Tools:**
  - Merge multiple PDFs into a single document
  - Split PDFs by page range or individual pages
  - Rotate PDF pages (90°, 180°, 270°)
  - Compress PDFs to reduce file size
  - Extract specific pages from PDFs
  - Delete specific pages from PDFs

- **Security Tools:**
  - Unlock password-protected PDFs
  - Protect PDFs with password
  - Remove password protection from PDFs
  - Add digital signatures to PDFs

### Image Converter
- **Format Conversions:**
  - JPG ↔ PNG bidirectional conversion
  - WebP to JPG/PNG conversion
  - Convert multiple images to PDF
  - Batch processing capabilities

## Replicate Deployment

This application is configured for deployment on [Replicate](https://replicate.com). The following operations are available:

### PDF Operations
- `pdf_merge`: Merge multiple PDF files
- `pdf_split`: Split a PDF by page range or individual pages
- `pdf_rotate`: Rotate PDF pages
- `pdf_compress`: Compress a PDF file
- `pdf_unlock`: Unlock password-protected PDF
- `pdf_protect`: Protect PDF with password
- `pdf_remove_password`: Remove password from PDF
- `pdf_add_signature`: Add digital signature to PDF
- `pdf_extract_pages`: Extract specific pages
- `pdf_delete_pages`: Delete specific pages

### Image Operations
- `image_jpg_to_png`: Convert JPG to PNG
- `image_png_to_jpg`: Convert PNG to JPG
- `image_webp_to_jpg`: Convert WebP to JPG
- `image_webp_to_png`: Convert WebP to PNG
- `image_to_pdf`: Convert images to PDF

## Local Installation

To run locally:

1. Clone or download this repository
2. Navigate to the project directory
3. Install the required dependencies:
   ```
   pip install -r requirements_unified.txt
   ```

Run the application using:
```
streamlit run unified_app/app.py
```

## Architecture

The application follows a modular design with separate modules for different functionality:

- **Main Application**: `unified_app/app.py` - Contains the Streamlit UI and application logic
- **PDF Operations Module**: `unified_app/modules/pdf_operations.py` - Contains all PDF manipulation functions
- **Image Operations Module**: `unified_app/modules/image_operations.py` - Contains all image conversion functions
- **Replicate Interface**: `predict.py` - Provides API interface for Replicate deployment
- **Dependencies**: PyPDF2, PyMuPDF, endesive, Pillow, img2pdf for processing capabilities

All original functionality from both the PDF tools and image converter projects is preserved and accessible through a unified interface.

## Requirements

- Python 3.8+
- All dependencies listed in `requirements_unified.txt`

## Support

For issues or questions, please create an issue in this repository.