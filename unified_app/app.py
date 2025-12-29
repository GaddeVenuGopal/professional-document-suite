import streamlit as st
from modules.pdf_operations import (
    merge_pdfs, split_pdf, rotate_pdf, compress_pdf, unlock_pdf, 
    protect_with_password, remove_password, add_digital_signature,
    extract_pages, delete_pages
)
from modules.image_operations import (
    convert_jpg_to_png, convert_png_to_jpg, convert_webp_to_jpg, 
    convert_webp_to_png, images_to_pdf, validate_image_files
)
import os
import tempfile
from PIL import Image


# Set page configuration
st.set_page_config(
    page_title="Professional Document Suite",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #2D3748;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .operation-card {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .result-box {
        background-color: #F7FAFC;
        border-left: 4px solid #3182CE;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-top: 1rem;
    }
    .feature-card {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-header'>📁 Professional Document Suite</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; margin-bottom: 2rem;'>A comprehensive solution for all your PDF manipulation and image conversion needs</div>", unsafe_allow_html=True)

# Create tabs for different toolsets
tab1, tab2 = st.tabs(["PDF Tools", "Image Converter"])

# Initialize session state variables
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "PDF Tools"

# PDF TOOLS TAB
with tab1:
    st.session_state.current_tab = "PDF Tools"
    
    # Create sub-tabs for PDF tools using radio buttons to track selection
    pdf_tool_selected = st.radio("Select PDF Tool", ["Document Tools", "Security Tools"], key="pdf_tool_selector")
    
    if pdf_tool_selected == "Document Tools":
        st.header("Document Tools")
        
        # Sidebar navigation for Document Tools
        st.sidebar.title("PDF Tools")
        operation = st.sidebar.selectbox(
            "Select PDF Operation",
            [
                "Merge PDFs",
                "Split PDF",
                "Rotate PDF",
                "Compress PDF",
                "Extract Pages",
                "Delete Pages"
            ],
            key="document_operation"
        )
        
        # File upload section
        st.sidebar.subheader("Upload Files")
        uploaded_files = st.sidebar.file_uploader(
            "Choose PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            key="document_uploader"
        )
        
        # Main content area based on selected operation
        if operation == "Merge PDFs":
            st.markdown("<h2 class='subheader'>Merge Multiple PDFs</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Combine multiple PDF files into a single document</div>", unsafe_allow_html=True)
            
            if uploaded_files and len(uploaded_files) > 1:
                if st.button("Merge PDFs"):
                    with st.spinner("Merging PDFs..."):
                        try:
                            merged_file_path = merge_pdfs(uploaded_files)
                            if merged_file_path:
                                st.success("PDFs merged successfully!")
                                with open(merged_file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Merged PDF",
                                        data=file,
                                        file_name="merged_document.pdf",
                                        mime="application/pdf"
                                    )
                                
                                # Clean up temporary file
                                if os.path.exists(merged_file_path):
                                    os.remove(merged_file_path)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            elif uploaded_files and len(uploaded_files) == 1:
                st.info("Please upload at least two PDF files to merge.")
            else:
                st.info("Please upload PDF files to get started.")

        elif operation == "Split PDF":
            st.markdown("<h2 class='subheader'>Split PDF</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Divide a PDF file into multiple documents</div>", unsafe_allow_html=True)
            
            if uploaded_files and len(uploaded_files) == 1:
                split_method = st.radio("Split Method", ["By Page Range", "Each Page as Separate File"])
                
                if split_method == "By Page Range":
                    col1, col2 = st.columns(2)
                    with col1:
                        start_page = st.number_input("Start Page", min_value=1, value=1)
                    with col2:
                        end_page = st.number_input("End Page", min_value=start_page, value=start_page+1)
                        
                    if st.button("Split PDF"):
                        with st.spinner("Splitting PDF..."):
                            try:
                                split_files = split_pdf(uploaded_files[0], method="range", start=start_page, end=end_page)
                                if split_files:
                                    st.success("PDF split successfully!")
                                    for i, file_path in enumerate(split_files):
                                        with open(file_path, "rb") as file:
                                            st.download_button(
                                                label=f"Download Split Part {i+1}",
                                                data=file,
                                                file_name=f"split_part_{i+1}.pdf",
                                                mime="application/pdf"
                                            )
                                            
                                        # Clean up temporary file
                                        if os.path.exists(file_path):
                                            os.remove(file_path)
                            except Exception as e:
                                st.error(f"An error occurred: {str(e)}")
                else:  # Each Page as Separate File
                    if st.button("Split PDF"):
                        with st.spinner("Splitting PDF..."):
                            try:
                                split_files = split_pdf(uploaded_files[0], method="individual")
                                if split_files:
                                    st.success("PDF split successfully!")
                                    for i, file_path in enumerate(split_files):
                                        with open(file_path, "rb") as file:
                                            st.download_button(
                                                label=f"Download Page {i+1}",
                                                data=file,
                                                file_name=f"page_{i+1}.pdf",
                                                mime="application/pdf"
                                            )
                                            
                                        # Clean up temporary file
                                        if os.path.exists(file_path):
                                            os.remove(file_path)
                            except Exception as e:
                                st.error(f"An error occurred: {str(e)}")
            elif uploaded_files and len(uploaded_files) > 1:
                st.info("Please upload only one PDF file for splitting.")
            else:
                st.info("Please upload a PDF file to get started.")

        elif operation == "Rotate PDF":
            st.markdown("<h2 class='subheader'>Rotate PDF</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Rotate pages in a PDF document</div>", unsafe_allow_html=True)
            
            if uploaded_files and len(uploaded_files) == 1:
                rotation_angle = st.selectbox("Rotation Angle", [90, 180, 270])
                page_option = st.radio("Pages to Rotate", ["All Pages", "Specific Pages"])
                
                pages_to_rotate = None
                if page_option == "Specific Pages":
                    pages_input = st.text_input("Enter page numbers (comma separated)", "1,2,3")
                    try:
                        pages_to_rotate = [int(x.strip()) for x in pages_input.split(",")]
                    except ValueError:
                        st.error("Please enter valid page numbers separated by commas.")
                
                if st.button("Rotate PDF"):
                    with st.spinner("Rotating PDF..."):
                        try:
                            rotated_file_path = rotate_pdf(uploaded_files[0], rotation_angle, pages_to_rotate)
                            if rotated_file_path:
                                st.success("PDF rotated successfully!")
                                with open(rotated_file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Rotated PDF",
                                        data=file,
                                        file_name="rotated_document.pdf",
                                        mime="application/pdf"
                                    )
                                
                                # Clean up temporary file
                                if os.path.exists(rotated_file_path):
                                    os.remove(rotated_file_path)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            elif uploaded_files and len(uploaded_files) > 1:
                st.info("Please upload only one PDF file for rotation.")
            else:
                st.info("Please upload a PDF file to get started.")

        elif operation == "Compress PDF":
            st.markdown("<h2 class='subheader'>Compress PDF</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Reduce the file size of your PDF document</div>", unsafe_allow_html=True)
            
            if uploaded_files and len(uploaded_files) == 1:
                compression_level = st.slider("Compression Level", 1, 9, 5)
                
                if st.button("Compress PDF"):
                    with st.spinner("Compressing PDF..."):
                        try:
                            compressed_file_path = compress_pdf(uploaded_files[0], compression_level)
                            if compressed_file_path:
                                st.success("PDF compressed successfully!")
                                original_size = uploaded_files[0].size
                                compressed_size = os.path.getsize(compressed_file_path)
                                st.info(f"Original size: {original_size} bytes | Compressed size: {compressed_size} bytes | Saved: {original_size - compressed_size} bytes ({((original_size - compressed_size) / original_size * 100):.1f}%)")
                                
                                with open(compressed_file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Compressed PDF",
                                        data=file,
                                        file_name="compressed_document.pdf",
                                        mime="application/pdf"
                                    )
                                
                                # Clean up temporary file
                                if os.path.exists(compressed_file_path):
                                    os.remove(compressed_file_path)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            elif uploaded_files and len(uploaded_files) > 1:
                st.info("Please upload only one PDF file for compression.")
            else:
                st.info("Please upload a PDF file to get started.")

        elif operation == "Extract Pages":
            st.markdown("<h2 class='subheader'>Extract Pages</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Extract specific pages from a PDF document</div>", unsafe_allow_html=True)
            
            if uploaded_files and len(uploaded_files) == 1:
                col1, col2 = st.columns(2)
                with col1:
                    start_page = st.number_input("Start Page", min_value=1, value=1)
                with col2:
                    end_page = st.number_input("End Page", min_value=start_page, value=start_page)
                
                if st.button("Extract Pages"):
                    with st.spinner("Extracting pages..."):
                        try:
                            extracted_file_path = extract_pages(uploaded_files[0], start_page, end_page)
                            if extracted_file_path:
                                st.success("Pages extracted successfully!")
                                with open(extracted_file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Extracted Pages",
                                        data=file,
                                        file_name="extracted_pages.pdf",
                                        mime="application/pdf"
                                    )
                                
                                # Clean up temporary file
                                if os.path.exists(extracted_file_path):
                                    os.remove(extracted_file_path)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            elif uploaded_files and len(uploaded_files) > 1:
                st.info("Please upload only one PDF file for page extraction.")
            else:
                st.info("Please upload a PDF file to get started.")

        elif operation == "Delete Pages":
            st.markdown("<h2 class='subheader'>Delete Pages</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Remove specific pages from a PDF document</div>", unsafe_allow_html=True)
            
            if uploaded_files and len(uploaded_files) == 1:
                pages_to_delete = st.text_input("Enter page numbers to delete (comma separated)", "1,2")
                try:
                    pages_list = [int(x.strip()) for x in pages_to_delete.split(",")]
                except ValueError:
                    st.error("Please enter valid page numbers separated by commas.")
                    pages_list = []
                
                if st.button("Delete Pages") and pages_list:
                    with st.spinner("Deleting pages..."):
                        try:
                            deleted_file_path = delete_pages(uploaded_files[0], pages_list)
                            if deleted_file_path:
                                st.success("Pages deleted successfully!")
                                with open(deleted_file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Modified PDF",
                                        data=file,
                                        file_name="modified_document.pdf",
                                        mime="application/pdf"
                                    )
                                
                                # Clean up temporary file
                                if os.path.exists(deleted_file_path):
                                    os.remove(deleted_file_path)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            elif uploaded_files and len(uploaded_files) > 1:
                st.info("Please upload only one PDF file for page deletion.")
            else:
                st.info("Please upload a PDF file to get started.")

    elif pdf_tool_selected == "Security Tools":
        st.header("Security Tools")
        
        # Sidebar navigation for Security Tools
        security_operation = st.sidebar.selectbox(
            "Select Security Operation",
            [
                "Unlock PDF",
                "Protect with Password",
                "Remove Password",
                "Digital Signature"
            ],
            key="security_operation"
        )
        
        # File upload section for Security Tools
        security_uploaded_files = st.sidebar.file_uploader(
            "Choose PDF files for security operations",
            type=["pdf"],
            accept_multiple_files=True,
            key="security_uploader"
        )
        
        # Main content area based on selected security operation
        if security_operation == "Unlock PDF":
            st.markdown("<h2 class='subheader'>Unlock PDF</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Remove password protection from a PDF document</div>", unsafe_allow_html=True)
            
            if security_uploaded_files and len(security_uploaded_files) == 1:
                password = st.text_input("Enter PDF Password", type="password")
                
                if st.button("Unlock PDF") and password:
                    with st.spinner("Unlocking PDF..."):
                        try:
                            unlocked_file_path = unlock_pdf(security_uploaded_files[0], password)
                            if unlocked_file_path:
                                st.success("PDF unlocked successfully!")
                                with open(unlocked_file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Unlocked PDF",
                                        data=file,
                                        file_name="unlocked_document.pdf",
                                        mime="application/pdf"
                                    )
                                
                                # Clean up temporary file
                                if os.path.exists(unlocked_file_path):
                                    os.remove(unlocked_file_path)
                            else:
                                st.error("Failed to unlock PDF. Please check the password.")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            elif security_uploaded_files and len(security_uploaded_files) > 1:
                st.info("Please upload only one PDF file for unlocking.")
            else:
                st.info("Please upload a PDF file to get started.")

        elif security_operation == "Protect with Password":
            st.markdown("<h2 class='subheader'>Protect PDF with Password</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Add password protection to your PDF document</div>", unsafe_allow_html=True)
            
            if security_uploaded_files and len(security_uploaded_files) == 1:
                password = st.text_input("Enter Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                if password and confirm_password:
                    if password != confirm_password:
                        st.error("Passwords do not match!")
                    else:
                        if st.button("Protect PDF"):
                            with st.spinner("Protecting PDF with password..."):
                                try:
                                    protected_file_path = protect_with_password(security_uploaded_files[0], password)
                                    if protected_file_path:
                                        st.success("PDF protected successfully!")
                                        with open(protected_file_path, "rb") as file:
                                            st.download_button(
                                                label="Download Protected PDF",
                                                data=file,
                                                file_name="protected_document.pdf",
                                                mime="application/pdf"
                                            )
                                        
                                        # Clean up temporary file
                                        if os.path.exists(protected_file_path):
                                            os.remove(protected_file_path)
                                except Exception as e:
                                    st.error(f"An error occurred: {str(e)}")
                elif password or confirm_password:
                    st.info("Please enter and confirm your password.")
            elif security_uploaded_files and len(security_uploaded_files) > 1:
                st.info("Please upload only one PDF file for password protection.")
            else:
                st.info("Please upload a PDF file to get started.")

        elif security_operation == "Remove Password":
            st.markdown("<h2 class='subheader'>Remove Password from PDF</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Remove password protection from your PDF document</div>", unsafe_allow_html=True)
            
            if security_uploaded_files and len(security_uploaded_files) == 1:
                password = st.text_input("Enter PDF Password", type="password")
                
                if st.button("Remove Password") and password:
                    with st.spinner("Removing password from PDF..."):
                        try:
                            unprotected_file_path = remove_password(security_uploaded_files[0], password)
                            if unprotected_file_path:
                                st.success("Password removed successfully!")
                                with open(unprotected_file_path, "rb") as file:
                                    st.download_button(
                                        label="Download Unprotected PDF",
                                        data=file,
                                        file_name="unprotected_document.pdf",
                                        mime="application/pdf"
                                    )
                                
                                # Clean up temporary file
                                if os.path.exists(unprotected_file_path):
                                    os.remove(unprotected_file_path)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            elif security_uploaded_files and len(security_uploaded_files) > 1:
                st.info("Please upload only one PDF file for password removal.")
            else:
                st.info("Please upload a PDF file to get started.")

        elif security_operation == "Digital Signature":
            st.markdown("<h2 class='subheader'>Add Digital Signature</h2>", unsafe_allow_html=True)
            st.markdown("<div class='operation-card'>Add digital signature to your PDF document</div>", unsafe_allow_html=True)
            
            if security_uploaded_files and len(security_uploaded_files) == 1:
                st.info("Note: This tool creates a digital signature using a self-signed certificate for demonstration. For legally binding signatures, use a certified digital ID from a trusted certificate authority.")
                
                col1, col2 = st.columns(2)
                with col1:
                    signer_name = st.text_input("Signer Name")
                    signer_location = st.text_input("Location")
                with col2:
                    signature_reason = st.text_input("Reason for Signing")
                    contact_info = st.text_input("Contact Information")
                
                signature_type = st.radio("Signature Type", ["Visual Signature (with signature field)", "Document Catalog Signature"])
                
                if st.button("Add Digital Signature"):
                    if signer_name:
                        with st.spinner("Adding digital signature..."):
                            try:
                                signature_info = {
                                    "name": signer_name,
                                    "location": signer_location,
                                    "reason": signature_reason,
                                    "contact_info": contact_info
                                }
                                signed_file_path = add_digital_signature(security_uploaded_files[0], signature_info)
                                if signed_file_path:
                                    st.success("Digital signature added successfully!")
                                    st.info("The document has been digitally signed. You can verify the signature by opening the PDF in Adobe Reader or another PDF viewer that supports signature verification.")
                                    with open(signed_file_path, "rb") as file:
                                        st.download_button(
                                            label="Download Signed PDF",
                                            data=file,
                                            file_name="signed_document.pdf",
                                            mime="application/pdf"
                                        )
                                    
                                    # Clean up temporary file
                                    if os.path.exists(signed_file_path):
                                        os.remove(signed_file_path)
                            except Exception as e:
                                st.error(f"An error occurred: {str(e)}")
                                st.info("Note: Some PDF viewers may not display self-signed certificates as valid. For production use, please use certificates from a trusted Certificate Authority.")
                    else:
                        st.error("Please enter the signer's name.")

# IMAGE CONVERTER TAB
with tab2:
    st.session_state.current_tab = "Image Converter"
    
    # Create tabs for different conversion types
    img_tab1, img_tab2, img_tab3, img_tab4 = st.tabs(["JPG ↔ PNG", "WebP → JPG/PNG", "Images → PDF", "About"])
    
    # JPG ↔ PNG Conversion Tab
    with img_tab1:
        st.markdown('<h2 class="subheader">JPG ↔ PNG Converter</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("JPG to PNG")
            jpg_file = st.file_uploader("Upload JPG Image", type=["jpg", "jpeg"], key="jpg_uploader")
            
            if jpg_file is not None:
                # Display original image
                st.image(jpg_file, caption="Original JPG Image", use_container_width=True)
                
                # Convert button
                if st.button("Convert to PNG", key="jpg_to_png_btn"):
                    with st.spinner("Converting..."):
                        try:
                            # Save uploaded file temporarily
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                                tmp_file.write(jpg_file.getvalue())
                                tmp_file_path = tmp_file.name
                            
                            # Convert
                            output_path = convert_jpg_to_png(tmp_file_path)
                            
                            # Read converted file
                            with open(output_path, "rb") as file:
                                converted_data = file.read()
                            
                            # Display converted image
                            st.image(converted_data, caption="Converted PNG Image", use_container_width=True)
                            
                            # Download button
                            st.download_button(
                                label="Download PNG",
                                data=converted_data,
                                file_name=output_path,
                                mime="image/png"
                            )
                            
                            # Clean up temporary files
                            os.unlink(tmp_file_path)
                            os.unlink(output_path)
                            
                            st.success("Conversion successful!")
                        except Exception as e:
                            st.error(f"Error during conversion: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("PNG to JPG")
            png_file = st.file_uploader("Upload PNG Image", type=["png"], key="png_uploader")
            
            if png_file is not None:
                # Display original image
                st.image(png_file, caption="Original PNG Image", use_container_width=True)
                
                # Convert button
                if st.button("Convert to JPG", key="png_to_jpg_btn"):
                    with st.spinner("Converting..."):
                        try:
                            # Save uploaded file temporarily
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                                tmp_file.write(png_file.getvalue())
                                tmp_file_path = tmp_file.name
                            
                            # Convert
                            output_path = convert_png_to_jpg(tmp_file_path)
                            
                            # Read converted file
                            with open(output_path, "rb") as file:
                                converted_data = file.read()
                            
                            # Display converted image
                            st.image(converted_data, caption="Converted JPG Image", use_container_width=True)
                            
                            # Download button
                            st.download_button(
                                label="Download JPG",
                                data=converted_data,
                                file_name=output_path,
                                mime="image/jpeg"
                            )
                            
                            # Clean up temporary files
                            os.unlink(tmp_file_path)
                            os.unlink(output_path)
                            
                            st.success("Conversion successful!")
                        except Exception as e:
                            st.error(f"Error during conversion: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)

    # WebP Conversion Tab
    with img_tab2:
        st.markdown('<h2 class="subheader">WebP Converter</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("WebP to JPG")
            webp_file_jpg = st.file_uploader("Upload WebP Image", type=["webp"], key="webp_jpg_uploader")
            
            if webp_file_jpg is not None:
                # Display original image
                st.image(webp_file_jpg, caption="Original WebP Image", use_container_width=True)
                
                # Convert button
                if st.button("Convert to JPG", key="webp_to_jpg_btn"):
                    with st.spinner("Converting..."):
                        try:
                            # Save uploaded file temporarily
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as tmp_file:
                                tmp_file.write(webp_file_jpg.getvalue())
                                tmp_file_path = tmp_file.name
                            
                            # Convert
                            output_path = convert_webp_to_jpg(tmp_file_path)
                            
                            # Read converted file
                            with open(output_path, "rb") as file:
                                converted_data = file.read()
                            
                            # Display converted image
                            st.image(converted_data, caption="Converted JPG Image", use_container_width=True)
                            
                            # Download button
                            st.download_button(
                                label="Download JPG",
                                data=converted_data,
                                file_name=output_path,
                                mime="image/jpeg"
                            )
                            
                            # Clean up temporary files
                            os.unlink(tmp_file_path)
                            os.unlink(output_path)
                            
                            st.success("Conversion successful!")
                        except Exception as e:
                            st.error(f"Error during conversion: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("WebP to PNG")
            webp_file_png = st.file_uploader("Upload WebP Image", type=["webp"], key="webp_png_uploader")
            
            if webp_file_png is not None:
                # Display original image
                st.image(webp_file_png, caption="Original WebP Image", use_container_width=True)
                
                # Convert button
                if st.button("Convert to PNG", key="webp_to_png_btn"):
                    with st.spinner("Converting..."):
                        try:
                            # Save uploaded file temporarily
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as tmp_file:
                                tmp_file.write(webp_file_png.getvalue())
                                tmp_file_path = tmp_file.name
                            
                            # Convert
                            output_path = convert_webp_to_png(tmp_file_path)
                            
                            # Read converted file
                            with open(output_path, "rb") as file:
                                converted_data = file.read()
                            
                            # Display converted image
                            st.image(converted_data, caption="Converted PNG Image", use_container_width=True)
                            
                            # Download button
                            st.download_button(
                                label="Download PNG",
                                data=converted_data,
                                file_name=output_path,
                                mime="image/png"
                            )
                            
                            # Clean up temporary files
                            os.unlink(tmp_file_path)
                            os.unlink(output_path)
                            
                            st.success("Conversion successful!")
                        except Exception as e:
                            st.error(f"Error during conversion: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)

    # Images to PDF Conversion Tab
    with img_tab3:
        st.markdown('<h2 class="subheader">Images to PDF Converter</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("Convert Multiple Images to PDF")
        
        # Multiple file uploader
        image_files = st.file_uploader(
            "Upload Images", 
            type=["jpg", "jpeg", "png", "webp"], 
            accept_multiple_files=True,
            key="pdf_uploader"
        )
        
        if image_files:
            # Display uploaded images
            st.subheader("Uploaded Images")
            cols = st.columns(min(len(image_files), 4))
            for i, file in enumerate(image_files):
                with cols[i % 4]:
                    st.image(file, caption=f"Image {i+1}", use_container_width=True)
            
            # Convert button
            if st.button("Convert to PDF", key="images_to_pdf_btn"):
                with st.spinner("Converting images to PDF..."):
                    try:
                        # Save uploaded files temporarily
                        temp_paths = []
                        for file in image_files:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
                                tmp_file.write(file.getvalue())
                                temp_paths.append(tmp_file.name)
                        
                        # Create output PDF path
                        output_pdf = "converted_document.pdf"
                        
                        # Convert to PDF
                        images_to_pdf(temp_paths, output_pdf)
                        
                        # Read PDF file
                        with open(output_pdf, "rb") as file:
                            pdf_data = file.read()
                        
                        # Display PDF preview (as download button since we can't embed PDFs easily)
                        st.subheader("Conversion Successful!")
                        st.download_button(
                            label="📥 Download PDF Document",
                            data=pdf_data,
                            file_name=output_pdf,
                            mime="application/pdf",
                            key="pdf_download"
                        )
                        
                        # Clean up temporary files
                        for path in temp_paths:
                            os.unlink(path)
                        os.unlink(output_pdf)
                        
                        st.success("PDF conversion completed successfully!")
                    except Exception as e:
                        st.error(f"Error during conversion: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

    # About Tab
    with img_tab4:
        st.markdown('<h2 class="subheader">About This Tool</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🛠️ Features
        
        This professional image converter offers:
        
        - **JPG ↔ PNG Conversion**: Convert between JPEG and PNG formats while preserving quality
        - **WebP Support**: Convert modern WebP images to traditional formats
        - **PDF Creation**: Combine multiple images into a single PDF document
        - **Lossless Processing**: Maintain image quality throughout conversions
        - **Batch Processing**: Convert multiple images at once
        
        ### 🔧 Technical Details
        
        - Built with Python and Streamlit for a responsive web interface
        - Uses Pillow for image processing
        - Utilizes img2pdf for high-quality PDF generation
        - Modular architecture for easy maintenance and extensibility
        
        ### 💡 Tips
        
        - PNG format is ideal for images with transparency or sharp graphics
        - JPG format is better for photographs and images with many colors
        - WebP offers excellent compression while maintaining quality
        - PDFs are perfect for sharing documents and combining multiple images
        
        ### 📄 Supported Formats
        
        | Input Format | Output Formats |
        |--------------|----------------|
        | JPG/JPEG     | PNG, PDF       |
        | PNG          | JPG, PDF       |
        | WebP         | JPG, PNG       |
        | Multiple Images | PDF         |
        
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: #f5f5f5; border-radius: 10px;">
            <p style="margin: 0; font-size: 0.9rem; color: #666;">
                Professional Image Converter v1.0 | Made with ❤️ using Streamlit
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #718096;'>Professional Document Suite &copy; 2025 | Secure and Reliable PDF & Image Processing</div>", unsafe_allow_html=True)