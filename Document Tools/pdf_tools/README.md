# Professional PDF Toolkit

A comprehensive solution for all your PDF manipulation needs, built with Python and Streamlit.

## Features

This toolkit provides the following PDF manipulation capabilities:

1. **Merge PDFs**: Combine multiple PDF files into a single document
2. **Split PDF**: Divide a PDF file into multiple documents
3. **Rotate PDF**: Rotate pages in a PDF document
4. **Compress PDF**: Reduce the file size of your PDF document (basic compression by recreating the PDF structure)
5. **Extract Pages**: Extract specific pages from a PDF document
6. **Delete Pages**: Remove specific pages from a PDF document
7. **Unlock PDF**: Remove password protection from a PDF document
8. **Protect with Password**: Add password protection to a PDF document
9. **Remove Password**: Remove password protection from a PDF document
10. **Digital Signature**: Add digital signature to a PDF document

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```
   python -m venv pdf_tools_env
   ```
4. Activate the virtual environment:
   - On Windows: `pdf_tools_env\Scripts\activate`
   - On macOS/Linux: `source pdf_tools_env/bin/activate`
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```
streamlit run pdf_tools/app.py
```

Then open your browser to the URL provided in the terminal (typically http://localhost:8501).

## Modules

- `pdf_operations.py`: Core PDF operations (merge, split, rotate, compress, unlock, password protection, digital signatures)
- `page_operations.py`: Page-specific operations (extract, delete)

## Security

- All file processing happens locally in your browser
- No files are uploaded to any server
- Temporary files are automatically cleaned up after processing
- Password protection uses industry-standard encryption
- Digital signatures use cryptographic libraries for secure signing

## License

This project is licensed under the MIT License - see the LICENSE file for details.