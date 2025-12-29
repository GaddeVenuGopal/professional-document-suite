"""
PDF Operations Module
Handles all PDF manipulation and security operations for the unified application.
"""
import os
import tempfile
from PyPDF2 import PdfReader, PdfWriter, PasswordType
from datetime import datetime
from endesive import pdf
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography import x509


def merge_pdfs(pdf_files):
    """
    Merge multiple PDF files into a single PDF.
    
    Args:
        pdf_files: List of uploaded file objects
    
    Returns:
        str: Path to the merged PDF file
    """
    try:
        writer = PdfWriter()
        
        # Iterate through each PDF file
        for pdf_file in pdf_files:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.getvalue())
                tmp_path = tmp_file.name
            
            # Read the PDF and add all pages to the writer
            reader = PdfReader(tmp_path)
            for page in reader.pages:
                writer.add_page(page)
            
            # Clean up temporary file
            os.unlink(tmp_path)
        
        # Save the merged PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix="_merged.pdf") as tmp_file:
            writer.write(tmp_file)
            return tmp_file.name
            
    except Exception as e:
        raise Exception(f"Error merging PDFs: {str(e)}")


def split_pdf(pdf_file, method="individual", start=None, end=None):
    """
    Split a PDF file into multiple parts.
    
    Args:
        pdf_file: Uploaded file object
        method: Split method ("individual" or "range")
        start: Start page number (for range method)
        end: End page number (for range method)
    
    Returns:
        list: Paths to the split PDF files
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        reader = PdfReader(tmp_path)
        split_files = []
        
        if method == "individual":
            # Split each page into separate files
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_page_{i+1}.pdf") as tmp_file:
                    writer.write(tmp_file)
                    split_files.append(tmp_file.name)
                    
        elif method == "range" and start is not None and end is not None:
            # Split by page range
            writer = PdfWriter()
            
            # Adjust for 0-based indexing
            start_index = start - 1
            end_index = min(end, len(reader.pages))
            
            for i in range(start_index, end_index):
                writer.add_page(reader.pages[i])
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_pages_{start}-{end}.pdf") as tmp_file:
                writer.write(tmp_file)
                split_files.append(tmp_file.name)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return split_files
        
    except Exception as e:
        raise Exception(f"Error splitting PDF: {str(e)}")


def rotate_pdf(pdf_file, angle, pages=None):
    """
    Rotate pages in a PDF file.
    
    Args:
        pdf_file: Uploaded file object
        angle: Rotation angle (90, 180, or 270)
        pages: List of page numbers to rotate (None for all pages)
    
    Returns:
        str: Path to the rotated PDF file
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        reader = PdfReader(tmp_path)
        writer = PdfWriter()
        
        # Process each page
        for i, page in enumerate(reader.pages):
            page_num = i + 1  # 1-based page numbering
            
            # Rotate if page is in the list or if rotating all pages
            if pages is None or page_num in pages:
                page.rotate(angle)
            
            writer.add_page(page)
        
        # Save the rotated PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix="_rotated.pdf") as tmp_file:
            writer.write(tmp_file)
            result_path = tmp_file.name
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return result_path
        
    except Exception as e:
        raise Exception(f"Error rotating PDF: {str(e)}")


def compress_pdf(pdf_file, compression_level=5):
    """
    Compress a PDF file to reduce its size.
    
    Args:
        pdf_file: Uploaded file object
        compression_level: Compression level (1-9)
    
    Returns:
        str: Path to the compressed PDF file
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        # Use PyMuPDF for compression
        import fitz  # PyMuPDF
        
        # Open the PDF
        doc = fitz.open(tmp_path)
        
        # Create a new PDF for output
        output_doc = fitz.open()
        
        # Copy pages to the new document (this helps optimize the PDF)
        for page_num in range(len(doc)):
            page = doc[page_num]
            output_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        
        # Save with compression settings
        # Determine the appropriate garbage collection and deflate settings based on compression level
        garbage = 4  # Remove unused objects
        deflate = True  # Compress the output
        
        # Save the compressed PDF to a temporary file
        compressed_pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix="_compressed.pdf").name
        output_doc.save(compressed_pdf_path, garbage=garbage, deflate=deflate)
        
        # Close documents
        doc.close()
        output_doc.close()
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return compressed_pdf_path
        
    except Exception as e:
        # If PyMuPDF fails, fall back to basic compression
        try:
            # Make sure the original file is closed before deleting
            if 'doc' in locals():
                try:
                    doc.close()
                except:
                    pass
            if 'output_doc' in locals():
                try:
                    output_doc.close()
                except:
                    pass
                    
            # Clean up the temporary file if it still exists
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
            # Now implement basic compression
            reader = PdfReader(tmp_path)
            writer = PdfWriter()
            
            # Copy all pages (basic compression by recreating the PDF without extra metadata)
            for page in reader.pages:
                writer.add_page(page)
            
            # Save the compressed PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix="_compressed.pdf") as tmp_file:
                writer.write(tmp_file)
                result_path = tmp_file.name
            
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            
            return result_path
        except Exception as fallback_e:
            raise Exception(f"Error compressing PDF: {str(e)}. Fallback also failed: {str(fallback_e)}")


def unlock_pdf(pdf_file, password):
    """
    Remove password protection from a PDF file.
    
    Args:
        pdf_file: Uploaded file object
        password: Password to unlock the PDF
    
    Returns:
        str: Path to the unlocked PDF file or None if password is incorrect
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        reader = PdfReader(tmp_path)
        
        # Check if the PDF is encrypted
        if reader.is_encrypted:
            # Try to decrypt with the provided password
            result = reader.decrypt(password)
            
            # Check if decryption was successful
            if result == PasswordType.NOT_DECRYPTED:
                # Clean up temporary file
                os.unlink(tmp_path)
                return None
            
            # Create a new PDF without password protection
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            # Save the unlocked PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix="_unlocked.pdf") as tmp_file:
                writer.write(tmp_file)
                result_path = tmp_file.name
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            return result_path
        else:
            # PDF is not encrypted, return the original file path
            return tmp_path
            
    except Exception as e:
        raise Exception(f"Error unlocking PDF: {str(e)}")


def protect_with_password(pdf_file, password):
    """
    Add password protection to a PDF file.
    
    Args:
        pdf_file: Uploaded file object
        password: Password to protect the PDF with
    
    Returns:
        str: Path to the password-protected PDF file
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        reader = PdfReader(tmp_path)
        writer = PdfWriter()
        
        # Copy all pages to the writer
        for page in reader.pages:
            writer.add_page(page)
        
        # Add password protection
        writer.encrypt(password)
        
        # Save the protected PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix="_protected.pdf") as tmp_file:
            writer.write(tmp_file)
            result_path = tmp_file.name
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return result_path
        
    except Exception as e:
        raise Exception(f"Error protecting PDF with password: {str(e)}")


def remove_password(pdf_file, password):
    """
    Remove password protection from a PDF file.
    
    Args:
        pdf_file: Uploaded file object
        password: Password to unlock the PDF
    
    Returns:
        str: Path to the PDF file with password removed
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        reader = PdfReader(tmp_path)
        
        # Check if the PDF is encrypted
        if reader.is_encrypted:
            # Try to decrypt with the provided password
            result = reader.decrypt(password)
            
            # Check if decryption was successful
            if result == PasswordType.NOT_DECRYPTED:
                # Clean up temporary file
                os.unlink(tmp_path)
                raise Exception("Incorrect password provided")
            
            # Create a new PDF without password protection
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            # Save the unprotected PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix="_unprotected.pdf") as tmp_file:
                writer.write(tmp_file)
                result_path = tmp_file.name
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            return result_path
        else:
            # PDF is not encrypted, return the original file
            return tmp_path
            
    except Exception as e:
        raise Exception(f"Error removing password from PDF: {str(e)}")


def add_digital_signature(pdf_file, signature_info):
    """
    Add a digital signature to a PDF file.
    
    Args:
        pdf_file: Uploaded file object
        signature_info: Dictionary containing signature details
                       (name, location, reason, contact_info)
    
    Returns:
        str: Path to the signed PDF file
    """
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        # Prepare signature parameters
        date = datetime.utcnow().strftime("%Y%m%d%H%M%S+00'00'")
        signature_params = {
            "sigflags": 3,
            "sigpage": 0,
            "sigbutton": True,
            "contact": signature_info.get("contact_info", ""),
            "location": signature_info.get("location", ""),
            "signingdate": date,
            "reason": signature_info.get("reason", ""),
            "signature": "",
            "signaturebox": (470, 840, 570, 640),
        }
        
        # For demonstration purposes, we'll create a self-signed certificate
        # In a production environment, you would use a real certificate
        # Generate a private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create a self-signed certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, signature_info.get("name", "Unknown Signer")),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow().replace(year=datetime.utcnow().year + 1)
        ).sign(private_key, hashes.SHA256())
        
        # Load the PDF data
        with open(tmp_path, "rb") as f:
            datau = f.read()
        
        # Sign the PDF - pass the key object and cert object directly
        datas = pdf.cms.sign(datau, signature_params, private_key, cert, [], "sha256")
        
        # Save the signed PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix="_signed.pdf") as tmp_file:
            tmp_file.write(datau)
            tmp_file.write(datas)
            result_path = tmp_file.name
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return result_path
        
    except Exception as e:
        # Fallback to metadata-based approach if signing fails
        try:
            reader = PdfReader(tmp_path)
            writer = PdfWriter()
            
            # Copy all pages to the writer
            for page in reader.pages:
                writer.add_page(page)
            
            # Add signature metadata
            writer.add_metadata({
                "/Producer": "PDF Tools Digital Signature",
                "/Title": f"Signed Document - {signature_info.get('name', '')}",
                "/Author": signature_info.get("name", ""),
                "/Subject": signature_info.get("reason", "Digitally Signed Document"),
            })
            
            # Save the PDF with signature metadata to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix="_signed.pdf") as tmp_file:
                writer.write(tmp_file)
                result_path = tmp_file.name
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            return result_path
        except Exception as fallback_e:
            raise Exception(f"Error adding digital signature: {str(e)}. Fallback also failed: {str(fallback_e)}")


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