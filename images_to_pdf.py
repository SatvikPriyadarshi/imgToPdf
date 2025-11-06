from PIL import Image
import os
from pathlib import Path

def create_pdf_from_images(input_folder, output_pdf, images_per_page=8):
    """
    Convert images to PDF with multiple images per page.
    
    Args:
        input_folder: Folder containing images
        output_pdf: Output PDF filename
        images_per_page: Number of images per page (default 8)
    """
    # Get all image files
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    image_files = sorted([
        os.path.join(input_folder, f) 
        for f in os.listdir(input_folder) 
        if f.lower().endswith(image_extensions)
    ])
    
    if not image_files:
        print("No images found in the folder!")
        return
    
    print(f"Found {len(image_files)} images")
    
    # PDF page size (A4 in pixels at 72 DPI)
    page_width = 2480  # A4 width at 300 DPI
    page_height = 3508  # A4 height at 300 DPI
    
    # Grid layout (4 rows x 2 columns for 8 images)
    rows = 4
    cols = 2
    border = 2  # 2px white border
    
    # Calculate image dimensions
    img_width = page_width // cols
    img_height = page_height // rows
    
    pdf_pages = []
    
    # Process images in batches
    for page_num in range(0, len(image_files), images_per_page):
        batch = image_files[page_num:page_num + images_per_page]
        
        # Create blank white page
        page = Image.new('RGB', (page_width, page_height), 'white')
        
        # Place images on the page
        for idx, img_path in enumerate(batch):
            try:
                img = Image.open(img_path)
                
                # Calculate position
                row = idx // cols
                col = idx % cols
                x = col * img_width
                y = row * img_height
                
                # Resize image to fit cell (with border consideration)
                cell_w = img_width - border
                cell_h = img_height - border
                img = img.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
                
                # Paste image (leaving border space)
                paste_x = x + (border if col > 0 else 0)
                paste_y = y + (border if row > 0 else 0)
                page.paste(img, (paste_x, paste_y))
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        # Convert to RGB if needed
        if page.mode != 'RGB':
            page = page.convert('RGB')
        
        pdf_pages.append(page)
        print(f"Created page {len(pdf_pages)} with {len(batch)} images")
    
    # Save as PDF
    if pdf_pages:
        pdf_pages[0].save(
            output_pdf, 
            save_all=True, 
            append_images=pdf_pages[1:],
            resolution=300.0
        )
        print(f"\nPDF created successfully: {output_pdf}")
        print(f"Total pages: {len(pdf_pages)}")
    else:
        print("No pages created!")

if __name__ == "__main__":
    input_folder = "images"
    output_pdf = "screenshots.pdf"
    
    create_pdf_from_images(input_folder, output_pdf)
