import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter

def extract_pages(pdf_file, start_page, end_page):
    """
    Extract specific pages from a PDF file.
    
    Args:
        pdf_file: Uploaded file object
        start_page: Starting page number (1-based)
        end_page: Ending page number (1-based)
    
    Returns:
        str: Path to the PDF file containing extracted pages
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        reader = PdfReader(tmp_path)
        writer = PdfWriter()
        
        # Validate page numbers
        total_pages = len(reader.pages)
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            raise ValueError(f"Invalid page range. Document has {total_pages} pages.")
        
        # Adjust for 0-based indexing
        start_index = start_page - 1
        end_index = end_page
        
        # Extract pages in the specified range
        for i in range(start_index, end_index):
            writer.add_page(reader.pages[i])
        
        # Save the extracted pages to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix="_extracted.pdf") as tmp_file:
            writer.write(tmp_file)
            result_path = tmp_file.name
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return result_path
        
    except Exception as e:
        raise Exception(f"Error extracting pages: {str(e)}")

def delete_pages(pdf_file, pages_to_delete):
    """
    Delete specific pages from a PDF file.
    
    Args:
        pdf_file: Uploaded file object
        pages_to_delete: List of page numbers to delete (1-based)
    
    Returns:
        str: Path to the PDF file with pages deleted
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        reader = PdfReader(tmp_path)
        writer = PdfWriter()
        
        # Validate page numbers
        total_pages = len(reader.pages)
        for page_num in pages_to_delete:
            if page_num < 1 or page_num > total_pages:
                raise ValueError(f"Page {page_num} is invalid. Document has {total_pages} pages.")
        
        # Add pages that are not in the deletion list
        for i, page in enumerate(reader.pages):
            page_num = i + 1  # 1-based page numbering
            if page_num not in pages_to_delete:
                writer.add_page(page)
        
        # Save the modified PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix="_deleted.pdf") as tmp_file:
            writer.write(tmp_file)
            result_path = tmp_file.name
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return result_path
        
    except Exception as e:
        raise Exception(f"Error deleting pages: {str(e)}")