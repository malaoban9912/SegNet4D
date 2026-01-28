# PDF Paper Extraction Tool

This document describes how to use the `extract_paper.py` utility to extract text and images from academic PDF papers and convert them to structured Markdown format.

## Overview

The `extract_paper.py` script uses PyMuPDF (also known as `fitz`) to:
- Extract all text from PDF pages
- Detect and segment common academic paper sections (Abstract, Introduction, Method, etc.)
- Extract all images from the PDF
- Generate a structured Markdown file with:
  - Title and authors
  - Table of contents with section links
  - Organized sections with headings
  - All extracted images with captions

## Dependencies

The script requires PyMuPDF to be installed:

```bash
pip install PyMuPDF==1.24.0
```

Or install all project dependencies:

```bash
pip install -r requirements.txt
```

If PyMuPDF is not installed, the script will display a clear error message with installation instructions.

## Usage

### Basic Usage

Extract the default SegNet4D paper from the repository root:

```bash
python tools/extract_paper.py
```

This will:
- Read `SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf` from the repo root
- Save extracted Markdown to `docs/SegNet4D_paper_extracted.md`
- Save all images to `docs/paper_images/`

### Extract a Custom PDF

```bash
python tools/extract_paper.py --pdf-path /path/to/your/paper.pdf
```

### Specify Custom Output Paths

```bash
python tools/extract_paper.py --output custom_output.md --images-dir custom_images/
```

### Overwrite Existing Files

By default, the script will not overwrite existing output files. To overwrite:

```bash
python tools/extract_paper.py --overwrite
```

### Verbose Logging

Enable detailed logging to see extraction progress:

```bash
python tools/extract_paper.py --verbose
```

### Combined Options

```bash
python tools/extract_paper.py --pdf-path papers/custom.pdf --output output/extracted.md --overwrite --verbose
```

## Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--pdf-path` | Path to the PDF file to extract | `SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf` |
| `--output` | Output Markdown file path | `docs/SegNet4D_paper_extracted.md` |
| `--images-dir` | Directory to save extracted images | `docs/paper_images` |
| `--overwrite` | Overwrite existing output files | False |
| `-v`, `--verbose` | Enable verbose output | False |
| `-h`, `--help` | Show help message and exit | - |

## Output Format

### Markdown File Structure

The generated Markdown file includes:

1. **Title and Authors** - Extracted from the first page
2. **Table of Contents** - Clickable links to all detected sections
3. **Sections** - Organized by detected headings:
   - Abstract
   - Introduction
   - Related Work
   - Method/Methodology/Approach
   - Experiments/Results
   - Discussion
   - Conclusion
   - Acknowledgments
   - References
4. **Extracted Images** - All images organized by page number with captions

### Image Files

Images are saved with the naming convention:
```
page_XX_img_Y.{ext}
```

Where:
- `XX` is the page number (zero-padded)
- `Y` is the image index on that page
- `{ext}` is the original image format (png, jpg, etc.)

Example: `page_03_img_1.png` is the first image from page 3.

## Expected Output

When run successfully from the repository root, the script creates:

```
docs/
├── SegNet4D_paper_extracted.md     # Main output Markdown file
└── paper_images/                    # Directory containing extracted images
    ├── page_01_img_1.png
    ├── page_02_img_1.png
    ├── page_03_img_1.png
    └── ...
```

The Markdown file can be viewed directly on GitHub and will display images using relative links.

## Section Detection

The script automatically detects common academic paper section headings (case-insensitive):
- Abstract
- Introduction
- Related Work
- Method / Methodology / Approach
- Experiments / Results
- Discussion
- Conclusion
- Acknowledgments / Acknowledgements
- References

Sections are detected when these words appear as standalone headings (typically at the start of a line).

## Error Handling

The script provides clear error messages for common issues:

- **Missing PyMuPDF**: Instructions to install the dependency
- **Missing PDF file**: Clear message indicating the file path that was not found
- **Existing output files**: Prevents accidental overwriting unless `--overwrite` is specified
- **Image extraction failures**: Continues processing and logs warnings for individual image failures

## Viewing the Output

The generated Markdown file is designed to be viewed on GitHub. Simply navigate to `docs/SegNet4D_paper_extracted.md` in the repository browser.

Images are embedded using relative paths, so they will display correctly when viewing the Markdown file on GitHub.

## Troubleshooting

### PyMuPDF Import Error

If you see an error about missing `fitz` module:

```bash
pip install PyMuPDF==1.24.0
```

### Permission Errors

Ensure you have write permissions to the output directories (`docs/` and `docs/paper_images/`).

### No Sections Detected

If no sections are detected, the script will create a single "Full Text" section with all content. This may happen with:
- Non-standard paper formats
- PDFs with poor text extraction
- Papers without clear section headings

### Poor Text Extraction Quality

If the extracted text quality is poor:
- The PDF may use images instead of text
- The PDF may have complex layouts that confuse text extraction
- Consider using a different PDF source or tool for complex documents

## Integration with CI/CD

The script can be integrated into CI/CD pipelines:

```bash
# In your CI script
python tools/extract_paper.py --verbose --overwrite
```

The script exits with status code 0 on success and 1 on failure, making it suitable for automated workflows.

## Contributing

When modifying this tool:
1. Test with various PDF formats
2. Ensure error messages are clear and actionable
3. Maintain backward compatibility with existing command-line arguments
4. Update this documentation with any new features or changes
