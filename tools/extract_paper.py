#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Extraction Utility for SegNet4D Paper

This script extracts text and images from PDF files, particularly designed for
the SegNet4D paper. It uses PyMuPDF (fitz) to parse PDFs and extract content.

Usage:
    python tools/extract_paper.py --pdf-path path/to/paper.pdf
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Check if PyMuPDF is available
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is not installed.", file=sys.stderr)
    print("Please install it using: pip install PyMuPDF==1.22.0", file=sys.stderr)
    sys.exit(1)

# Check if Pillow is available (optional for image conversion)
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


# Common section headings to detect (English and Chinese)
SECTION_PATTERNS = [
    (r'^\s*abstract\s*$', 'Abstract'),
    (r'^\s*摘\s*要\s*$', '摘要'),
    (r'^\s*introduction\s*$', 'Introduction'),
    (r'^\s*引\s*言\s*$', '引言'),
    (r'^\s*related\s+work\s*$', 'Related Work'),
    (r'^\s*相\s*关\s*工\s*作\s*$', '相关工作'),
    (r'^\s*method\s*$', 'Method'),
    (r'^\s*方\s*法\s*$', '方法'),
    (r'^\s*methodology\s*$', 'Methodology'),
    (r'^\s*experiments?\s*$', 'Experiments'),
    (r'^\s*实\s*验\s*$', '实验'),
    (r'^\s*results?\s*$', 'Results'),
    (r'^\s*结\s*果\s*$', '结果'),
    (r'^\s*discussion\s*$', 'Discussion'),
    (r'^\s*讨\s*论\s*$', '讨论'),
    (r'^\s*conclusions?\s*$', 'Conclusion'),
    (r'^\s*结\s*论\s*$', '结论'),
    (r'^\s*acknowledgments?\s*$', 'Acknowledgment'),
    (r'^\s*致\s*谢\s*$', '致谢'),
    (r'^\s*references?\s*$', 'References'),
    (r'^\s*参\s*考\s*文\s*献\s*$', '参考文献'),
]


def extract_title_and_authors(text):
    """
    Heuristically extract title and authors from the text.
    
    Args:
        text: Full text from the PDF
        
    Returns:
        tuple: (title, authors) where both are strings
    """
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    # Simple heuristic: title is usually the first significant line
    title = non_empty_lines[0] if non_empty_lines else "Unknown Title"
    
    # Authors are usually on the next few lines
    authors = "Unknown Authors"
    if len(non_empty_lines) > 1:
        # Look for lines that might contain author names (before Abstract/Introduction)
        author_lines = []
        for i, line in enumerate(non_empty_lines[1:6], 1):  # Check first 5 lines after title
            lower_line = line.lower()
            # Stop if we hit common section headers
            if any(keyword in lower_line for keyword in ['abstract', 'introduction', '摘要', '引言']):
                break
            author_lines.append(line)
        
        if author_lines:
            authors = ', '.join(author_lines[:3])  # Take up to 3 lines
    
    return title, authors


def detect_sections(text):
    """
    Detect sections in the text based on common headings.
    
    Args:
        text: Full text from the PDF
        
    Returns:
        dict: Dictionary mapping section names to their content
    """
    lines = text.split('\n')
    sections = {}
    current_section = "Introduction"
    section_content = []
    
    for line in lines:
        # Check if this line matches any section pattern
        matched = False
        for pattern, section_name in SECTION_PATTERNS:
            if re.match(pattern, line.strip(), re.IGNORECASE):
                # Save previous section
                if section_content:
                    sections[current_section] = '\n'.join(section_content).strip()
                
                # Start new section
                current_section = section_name
                section_content = []
                matched = True
                break
        
        if not matched:
            section_content.append(line)
    
    # Save the last section
    if section_content:
        sections[current_section] = '\n'.join(section_content).strip()
    
    return sections


def extract_images_from_pdf(pdf_path, images_dir, verbose=False):
    """
    Extract all images from the PDF and save them to the images directory.
    
    Args:
        pdf_path: Path to the PDF file
        images_dir: Directory to save extracted images
        verbose: Whether to print verbose output
        
    Returns:
        list: List of tuples (page_num, image_index, image_path)
    """
    extracted_images = []
    
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            if verbose:
                print(f"Page {page_num + 1}: Found {len(image_list)} images")
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Generate image filename (sanitize to prevent directory traversal)
                image_filename = f"page_{page_num + 1:02d}_img_{img_index + 1}.{image_ext}"
                # Ensure the path stays within images_dir
                image_path = os.path.abspath(os.path.join(images_dir, image_filename))
                if not image_path.startswith(os.path.abspath(images_dir)):
                    if verbose:
                        print(f"  Warning: Skipping potentially unsafe path: {image_filename}")
                    continue
                
                # Save the image
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                # Try to convert to PNG if Pillow is available and it's not already PNG
                if PILLOW_AVAILABLE and image_ext.lower() != 'png':
                    try:
                        img_obj = Image.open(image_path)
                        png_filename = f"page_{page_num + 1:02d}_img_{img_index + 1}.png"
                        png_path = os.path.abspath(os.path.join(images_dir, png_filename))
                        if not png_path.startswith(os.path.abspath(images_dir)):
                            if verbose:
                                print(f"  Warning: Skipping potentially unsafe PNG path: {png_filename}")
                            continue
                        
                        img_obj.save(png_path, 'PNG')
                        
                        # Remove the original if conversion was successful
                        os.remove(image_path)
                        image_path = png_path
                        
                        if verbose:
                            print(f"  Converted {image_filename} to PNG")
                    except Exception as e:
                        if verbose:
                            print(f"  Warning: Could not convert {image_filename} to PNG: {e}")
                
                extracted_images.append((page_num + 1, img_index + 1, image_path))
                
                if verbose:
                    print(f"  Saved: {os.path.basename(image_path)}")
    
    return extracted_images


def extract_text_from_pdf(pdf_path, verbose=False):
    """
    Extract all text from the PDF.
    
    Args:
        pdf_path: Path to the PDF file
        verbose: Whether to print verbose output
        
    Returns:
        str: Extracted text from all pages
    """
    full_text = []
    
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            full_text.append(text)
            
            if verbose:
                print(f"Page {page_num + 1}: Extracted {len(text)} characters")
    
    return '\n'.join(full_text)


def generate_markdown(title, authors, sections, extracted_images, images_dir, out_md, verbose=False):
    """
    Generate a Markdown file with extracted content.
    
    Args:
        title: Paper title
        authors: Paper authors
        sections: Dictionary of sections
        extracted_images: List of extracted images
        images_dir: Directory where images are saved
        out_md: Output markdown file path
        verbose: Whether to print verbose output
    """
    with open(out_md, 'w', encoding='utf-8') as f:
        # Write title and authors
        f.write(f"# {title}\n\n")
        f.write(f"**Authors:** {authors}\n\n")
        f.write("---\n\n")
        
        # Write table of contents
        f.write("## Table of Contents\n\n")
        for section_name in sections.keys():
            # Create anchor link (lowercase, replace spaces with hyphens)
            anchor = section_name.lower().replace(' ', '-')
            f.write(f"- [{section_name}](#{anchor})\n")
        f.write("\n---\n\n")
        
        # Write sections
        for section_name, content in sections.items():
            f.write(f"## {section_name}\n\n")
            f.write(f"{content}\n\n")
            f.write("<!-- 待后续进行更详细的中文解析 -->\n\n")
            f.write("---\n\n")
        
        # Write extracted images section
        if extracted_images:
            f.write("## Extracted Images\n\n")
            
            # Group images by page
            images_by_page = {}
            for page_num, img_index, img_path in extracted_images:
                if page_num not in images_by_page:
                    images_by_page[page_num] = []
                images_by_page[page_num].append((img_index, img_path))
            
            for page_num in sorted(images_by_page.keys()):
                f.write(f"### Page {page_num}\n\n")
                for img_index, img_path in images_by_page[page_num]:
                    # Create relative path for markdown
                    rel_path = os.path.relpath(img_path, os.path.dirname(out_md))
                    f.write(f"![Page {page_num} Image {img_index}]({rel_path})\n\n")
            
            f.write("---\n\n")
    
    if verbose:
        print(f"Markdown file generated: {out_md}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Extract text and images from SegNet4D paper PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from default PDF
  python tools/extract_paper.py
  
  # Extract from custom PDF
  python tools/extract_paper.py --pdf-path path/to/paper.pdf
  
  # Specify custom output paths
  python tools/extract_paper.py --out-md docs/custom.md --images-dir docs/my_images/
  
  # Overwrite existing files with verbose output
  python tools/extract_paper.py --overwrite --verbose
        """
    )
    
    parser.add_argument(
        '--pdf-path',
        default='SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf',
        help='Path to the PDF file (default: SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf)'
    )
    parser.add_argument(
        '--out-md',
        default='docs/SegNet4D_paper_extracted.md',
        help='Output Markdown file path (default: docs/SegNet4D_paper_extracted.md)'
    )
    parser.add_argument(
        '--images-dir',
        default='docs/paper_images',
        help='Directory to save extracted images (default: docs/paper_images)'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing output files'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print verbose output'
    )
    
    args = parser.parse_args()
    
    # Check if PDF exists
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)
    
    # Check if output file exists and overwrite flag is not set
    if os.path.exists(args.out_md) and not args.overwrite:
        print(f"Error: Output file already exists: {args.out_md}", file=sys.stderr)
        print("Use --overwrite to overwrite existing files", file=sys.stderr)
        sys.exit(1)
    
    # Create output directories if they don't exist
    os.makedirs(os.path.dirname(args.out_md), exist_ok=True)
    os.makedirs(args.images_dir, exist_ok=True)
    
    if args.verbose:
        print(f"PDF Path: {args.pdf_path}")
        print(f"Output Markdown: {args.out_md}")
        print(f"Images Directory: {args.images_dir}")
        print(f"Pillow available: {PILLOW_AVAILABLE}")
        print()
    
    # Extract text
    if args.verbose:
        print("Extracting text from PDF...")
    full_text = extract_text_from_pdf(args.pdf_path, args.verbose)
    
    # Extract title and authors
    title, authors = extract_title_and_authors(full_text)
    if args.verbose:
        print(f"\nTitle: {title}")
        print(f"Authors: {authors}")
        print()
    
    # Detect sections
    if args.verbose:
        print("Detecting sections...")
    sections = detect_sections(full_text)
    if args.verbose:
        print(f"Found {len(sections)} sections: {', '.join(sections.keys())}")
        print()
    
    # Extract images
    if args.verbose:
        print("Extracting images from PDF...")
    extracted_images = extract_images_from_pdf(args.pdf_path, args.images_dir, args.verbose)
    if args.verbose:
        print(f"\nExtracted {len(extracted_images)} images")
        print()
    
    # Generate markdown
    if args.verbose:
        print("Generating Markdown file...")
    generate_markdown(title, authors, sections, extracted_images, args.images_dir, args.out_md, args.verbose)
    
    print(f"✓ Successfully extracted PDF content to {args.out_md}")
    print(f"✓ Extracted {len(extracted_images)} images to {args.images_dir}")


if __name__ == '__main__':
    main()
