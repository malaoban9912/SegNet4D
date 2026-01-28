#!/usr/bin/env python3
"""
PDF Paper Extraction Utility

This script extracts text and images from academic PDF papers and converts them
to structured Markdown format with section headers and table of contents.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


def check_dependencies():
    """Check if PyMuPDF is available and provide installation instructions if not."""
    try:
        import fitz  # PyMuPDF
        return True
    except ImportError:
        print("ERROR: PyMuPDF is not installed.")
        print("\nTo install PyMuPDF, run:")
        print("    pip install PyMuPDF==1.24.0")
        print("\nOr install all project dependencies:")
        print("    pip install -r requirements.txt")
        return False


def extract_images_from_page(page, page_num: int, output_dir: Path, verbose: bool = False) -> List[Tuple[str, int]]:
    """
    Extract all images from a PDF page and save them to files.
    
    Args:
        page: PyMuPDF page object
        page_num: Page number (1-indexed)
        output_dir: Directory to save images
        verbose: Whether to print verbose logging
        
    Returns:
        List of tuples (image_path, image_index) for images extracted from this page
    """
    images = []
    image_list = page.get_images(full=True)
    
    for img_index, img_info in enumerate(image_list, start=1):
        xref = img_info[0]
        
        try:
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Create filename with page and image index
            image_filename = f"page_{page_num:02d}_img_{img_index}.{image_ext}"
            image_path = output_dir / image_filename
            
            # Save image
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            
            if verbose:
                print(f"  Extracted image: {image_filename}")
            
            images.append((str(image_path.relative_to(image_path.parent.parent)), img_index))
        except Exception as e:
            if verbose:
                print(f"  Warning: Could not extract image {img_index} from page {page_num}: {e}")
    
    return images


def detect_section_headings(text: str) -> List[Tuple[str, int]]:
    """
    Detect section headings in the text.
    
    Args:
        text: Full text from the PDF
        
    Returns:
        List of tuples (section_name, position_in_text)
    """
    # Common section headings in academic papers
    section_patterns = [
        r'\bAbstract\b',
        r'\bIntroduction\b',
        r'\bRelated\s+Work\b',
        r'\bMethod\b',
        r'\bMethodology\b',
        r'\bApproach\b',
        r'\bExperiments?\b',
        r'\bResults?\b',
        r'\bDiscussion\b',
        r'\bConclusion\b',
        r'\bAcknowledgments?\b',
        r'\bReferences?\b'
    ]
    
    sections = []
    
    for pattern in section_patterns:
        # Search case-insensitive
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Check if this is likely a heading (not in middle of sentence)
            start = match.start()
            end = match.end()
            
            # Check context - headings usually have newlines before them
            # or are at the start
            if start == 0 or (start > 0 and text[start-1] in '\n\r'):
                # Check if followed by newline or end of text
                if end >= len(text) or text[end] in '\n\r. ':
                    section_name = match.group(0).strip()
                    sections.append((section_name, start))
    
    # Remove duplicates and sort by position
    sections = list(dict.fromkeys(sections))  # Remove duplicates while preserving order
    sections.sort(key=lambda x: x[1])
    
    return sections


def split_text_into_sections(text: str, sections: List[Tuple[str, int]]) -> Dict[str, str]:
    """
    Split text into sections based on detected headings.
    
    Args:
        text: Full text from the PDF
        sections: List of (section_name, position) tuples
        
    Returns:
        Dictionary mapping section names to their content
    """
    section_dict = {}
    
    if not sections:
        section_dict["Full Text"] = text
        return section_dict
    
    for i, (section_name, start_pos) in enumerate(sections):
        # Find end position (start of next section or end of text)
        if i + 1 < len(sections):
            end_pos = sections[i + 1][1]
        else:
            end_pos = len(text)
        
        # Extract section content
        section_content = text[start_pos:end_pos].strip()
        
        # Remove the section heading from content (it's already the key)
        section_content = re.sub(f'^{re.escape(section_name)}', '', section_content, count=1, flags=re.IGNORECASE).strip()
        
        section_dict[section_name] = section_content
    
    return section_dict


def extract_title_and_authors(first_page_text: str) -> Tuple[str, str]:
    """
    Try to extract title and authors from the first page.
    
    Args:
        first_page_text: Text from the first page
        
    Returns:
        Tuple of (title, authors)
    """
    lines = first_page_text.split('\n')
    
    # Simple heuristic: title is often the first few lines in larger font
    # For simplicity, we'll take the first non-empty line as title
    # and next few lines as authors
    title = ""
    authors = ""
    
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    if non_empty_lines:
        # First line is likely the title
        title = non_empty_lines[0]
        
        # Next 1-3 lines might be authors (before Abstract or other sections)
        author_lines = []
        for line in non_empty_lines[1:4]:
            # Stop if we hit a common section header
            if re.search(r'\b(Abstract|Introduction|Keywords)\b', line, re.IGNORECASE):
                break
            author_lines.append(line)
        
        authors = ' '.join(author_lines)
    
    return title, authors


def extract_pdf_to_markdown(pdf_path: str, output_md: str, images_dir: str, verbose: bool = False, overwrite: bool = False) -> bool:
    """
    Extract text and images from PDF and create a structured Markdown file.
    
    Args:
        pdf_path: Path to input PDF file
        output_md: Path to output Markdown file
        images_dir: Directory to save extracted images
        verbose: Whether to print verbose logging
        overwrite: Whether to overwrite existing output files
        
    Returns:
        True if extraction successful, False otherwise
    """
    import fitz  # PyMuPDF
    
    # Check if output exists
    if os.path.exists(output_md) and not overwrite:
        print(f"ERROR: Output file '{output_md}' already exists.")
        print("Use --overwrite to overwrite existing files.")
        return False
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file '{pdf_path}' not found.")
        return False
    
    # Create output directories
    os.makedirs(os.path.dirname(output_md), exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    if verbose:
        print(f"Opening PDF: {pdf_path}")
    
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"ERROR: Could not open PDF file: {e}")
        return False
    
    # Extract text from all pages
    full_text = ""
    page_texts = []
    all_images = []  # List of (page_num, image_path, img_index)
    
    if verbose:
        print(f"Extracting text and images from {len(doc)} pages...")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()
        page_texts.append((page_num + 1, page_text))
        full_text += page_text + "\n"
        
        # Extract images from this page
        images = extract_images_from_page(page, page_num + 1, Path(images_dir), verbose=verbose)
        for img_path, img_idx in images:
            all_images.append((page_num + 1, img_path, img_idx))
    
    doc.close()
    
    if verbose:
        print(f"Extracted {len(page_texts)} pages and {len(all_images)} images")
    
    # Extract title and authors from first page
    title, authors = extract_title_and_authors(page_texts[0][1] if page_texts else "")
    
    # Detect section headings
    sections = detect_section_headings(full_text)
    
    if verbose:
        print(f"Detected {len(sections)} sections: {[s[0] for s in sections]}")
    
    # Split text into sections
    section_dict = split_text_into_sections(full_text, sections)
    
    # Generate Markdown output
    if verbose:
        print(f"Writing output to: {output_md}")
    
    with open(output_md, 'w', encoding='utf-8') as f:
        # Write title and authors
        if title:
            f.write(f"# {title}\n\n")
        else:
            f.write(f"# Extracted Paper Content\n\n")
        
        if authors:
            f.write(f"**Authors:** {authors}\n\n")
        
        f.write("---\n\n")
        
        # Write table of contents
        f.write("## Table of Contents\n\n")
        for section_name, _ in sections:
            # Create anchor link (lowercase, replace spaces with hyphens)
            anchor = section_name.lower().replace(' ', '-').replace('.', '')
            f.write(f"- [{section_name}](#{anchor})\n")
        
        f.write("\n---\n\n")
        
        # Write sections
        for section_name, content in section_dict.items():
            f.write(f"## {section_name}\n\n")
            f.write(f"{content}\n\n")
        
        # Write extracted images section
        if all_images:
            f.write("---\n\n")
            f.write("## Extracted Images\n\n")
            f.write("Below are all images extracted from the PDF, organized by page number.\n\n")
            
            current_page = None
            for page_num, img_path, img_idx in all_images:
                if current_page != page_num:
                    if current_page is not None:
                        f.write("\n")
                    f.write(f"### Page {page_num}\n\n")
                    current_page = page_num
                
                f.write(f"![Image {img_idx} from page {page_num}]({img_path})\n\n")
                f.write(f"*Image {img_idx} from page {page_num}*\n\n")
    
    if verbose:
        print(f"SUCCESS: Extraction complete!")
        print(f"  - Markdown output: {output_md}")
        print(f"  - Images saved to: {images_dir}")
        print(f"  - Total sections: {len(section_dict)}")
        print(f"  - Total images: {len(all_images)}")
    
    return True


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Extract text and images from academic PDF papers to structured Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract the default paper from repo root
  python tools/extract_paper.py
  
  # Extract a custom PDF file
  python tools/extract_paper.py --pdf-path /path/to/paper.pdf
  
  # Overwrite existing output files
  python tools/extract_paper.py --overwrite
  
  # Verbose output
  python tools/extract_paper.py --verbose
        """
    )
    
    parser.add_argument(
        '--pdf-path',
        type=str,
        default='SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf',
        help='Path to the PDF file to extract (default: SegNet4D paper in repo root)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='docs/SegNet4D_paper_extracted.md',
        help='Output Markdown file path (default: docs/SegNet4D_paper_extracted.md)'
    )
    
    parser.add_argument(
        '--images-dir',
        type=str,
        default='docs/paper_images',
        help='Directory to save extracted images (default: docs/paper_images)'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing output files'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    # Perform extraction
    success = extract_pdf_to_markdown(
        pdf_path=args.pdf_path,
        output_md=args.output,
        images_dir=args.images_dir,
        verbose=args.verbose,
        overwrite=args.overwrite
    )
    
    if not success:
        sys.exit(1)
    
    print(f"\nExtraction complete! Output saved to: {args.output}")


if __name__ == '__main__':
    main()
