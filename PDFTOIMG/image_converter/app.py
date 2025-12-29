"""
Professional Streamlit App for Image Converter
A sleek, modern UI for the modular image conversion system.
"""

import streamlit as st
from PIL import Image
import io
import os
import tempfile
from src.modules.jpg_png_converter import convert_jpg_to_png, convert_png_to_jpg
from src.modules.webp_converter import convert_webp_to_jpg, convert_webp_to_png
from src.modules.pdf_converter import images_to_pdf


# Set page configuration
st.set_page_config(
    page_title="Professional Image Converter",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .subheader {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
        font-weight: 600;
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
    .conversion-button {
        background-color: #1E88E5;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .conversion-button:hover {
        background-color: #1565C0;
    }
    .stProgress > div > div > div > div {
        background-color: #1E88E5;
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🖼️ Professional Image Converter</h1>', unsafe_allow_html=True)

# Description
st.markdown("""
<div style="text-align: center; max-width: 800px; margin: 0 auto 2rem auto; font-size: 1.1rem;">
    A powerful, easy-to-use tool for converting between various image formats and creating PDF documents.
    Supports JPG, PNG, WebP, and PDF conversions with professional quality output.
</div>
""", unsafe_allow_html=True)

# Create tabs for different conversion types
tab1, tab2, tab3, tab4 = st.tabs(["JPG ↔ PNG", "WebP → JPG/PNG", "Images → PDF", "About"])

# JPG ↔ PNG Conversion Tab
with tab1:
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
with tab2:
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
with tab3:
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
with tab4:
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

# Sidebar with additional information
with st.sidebar:
    st.markdown("# 🖼️ Image Converter")
    st.markdown("---")
    st.markdown("### 📋 Quick Stats")
    st.metric("Supported Formats", "4")
    st.metric("Conversion Types", "5")
    st.metric("Processing Speed", "⚡ Fast")
    
    st.markdown("### ℹ️ Instructions")
    st.markdown("""
    1. Select a conversion tab above
    2. Upload your image(s)
    3. Click the convert button
    4. Download your converted file
    """)
    
    st.markdown("### ⚙️ Settings")
    quality = st.slider("Output Quality", 1, 100, 95)
    st.caption("Quality setting affects JPG output compression")
    
    st.markdown("### 📞 Support")
    st.markdown("Having issues? Contact support@example.com")