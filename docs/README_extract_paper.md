# PDF Extraction Utility Documentation

This document explains how to use the PDF extraction utility for the SegNet4D paper.

## Overview

The `extract_paper.py` script extracts text and images from PDF files, particularly designed for academic papers. It uses PyMuPDF (fitz) to parse PDFs and extract content, then organizes the content into a structured Markdown file.

## Features

- **Text Extraction**: Extracts all text from the PDF and organizes it by detected sections
- **Image Extraction**: Extracts all embedded images from the PDF
- **Image Conversion**: Automatically converts images to PNG format when Pillow is available
- **Section Detection**: Automatically detects common paper sections (Abstract, Introduction, Method, etc.) in both English and Chinese
- **Markdown Output**: Generates a well-structured Markdown file with:
  - Title and authors (heuristically extracted)
  - Table of contents with clickable links
  - Organized sections with content
  - Placeholder comments for future detailed parsing
  - Embedded image references with relative paths
- **Robust Error Handling**: Clear error messages and non-zero exit codes for missing dependencies

## Dependencies

The script requires the following Python packages:

- **PyMuPDF (fitz)** - Required for PDF parsing
  ```bash
  pip install PyMuPDF==1.22.0
  ```

- **Pillow** - Optional, for image format conversion to PNG
  ```bash
  pip install Pillow
  ```

If PyMuPDF is not installed, the script will exit with a clear error message and instructions.

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Verify the installation:
   ```bash
   python -c "import fitz; print('PyMuPDF installed successfully')"
   ```

## Usage

### Basic Usage

Extract content from the default SegNet4D paper:

```bash
python tools/extract_paper.py
```

This will:
- Read `SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf`
- Extract text and images
- Save images to `docs/paper_images/`
- Generate `docs/SegNet4D_paper_extracted.md`

### Custom PDF Path

Extract content from a different PDF file:

```bash
python tools/extract_paper.py --pdf-path path/to/your/paper.pdf
```

### Custom Output Paths

Specify custom output locations:

```bash
python tools/extract_paper.py \
  --out-md docs/custom_output.md \
  --images-dir docs/custom_images/
```

### Overwrite Existing Files

By default, the script will not overwrite existing output files. To allow overwriting:

```bash
python tools/extract_paper.py --overwrite
```

### Verbose Output

Get detailed information about the extraction process:

```bash
python tools/extract_paper.py --verbose
```

This will display:
- Configuration settings
- Number of characters extracted per page
- Number of images found per page
- Image conversion status
- Section detection results

### Combined Example

Extract with all options:

```bash
python tools/extract_paper.py \
  --pdf-path path/to/paper.pdf \
  --out-md docs/output.md \
  --images-dir docs/images/ \
  --overwrite \
  --verbose
```

## Command-Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--pdf-path` | `SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf` | Path to the input PDF file |
| `--out-md` | `docs/SegNet4D_paper_extracted.md` | Path for the output Markdown file |
| `--images-dir` | `docs/paper_images` | Directory to save extracted images |
| `--overwrite` | False | Allow overwriting existing output files |
| `--verbose` | False | Enable verbose output with detailed progress information |

## Output Structure

### Markdown File

The generated Markdown file includes:

1. **Header**: Title and authors (heuristically extracted from the first page)
2. **Table of Contents**: Clickable links to all detected sections
3. **Sections**: Each detected section with its content, including:
   - Section heading
   - Extracted text content
   - Placeholder comment: `<!-- 待后续进行更详细的中文解析 -->`
4. **Extracted Images**: Gallery of all extracted images, organized by page

### Image Files

Images are saved with the following naming convention:
- Format: `page_XX_img_Y.ext`
- `XX`: Two-digit page number (e.g., 01, 02, 03)
- `Y`: Image index on that page (starting from 1)
- `ext`: Original image extension (or `png` if converted)

Examples:
- `page_01_img_1.png` - First image from page 1
- `page_03_img_2.png` - Second image from page 3

## Section Detection

The script automatically detects common paper sections in both English and Chinese:

| English | Chinese |
|---------|---------|
| Abstract | 摘要 |
| Introduction | 引言 |
| Related Work | 相关工作 |
| Method / Methodology | 方法 |
| Experiments | 实验 |
| Results | 结果 |
| Discussion | 讨论 |
| Conclusion | 结论 |
| Acknowledgment | 致谢 |
| References | 参考文献 |

The detection is case-insensitive and uses regular expressions to match section headings.

## Troubleshooting

### PyMuPDF Not Found

**Error**: `Error: PyMuPDF is not installed.`

**Solution**: Install PyMuPDF:
```bash
pip install PyMuPDF==1.22.0
```

### PDF File Not Found

**Error**: `Error: PDF file not found: <path>`

**Solution**: Check that the PDF path is correct and the file exists:
```bash
ls -l SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf
```

### Output File Already Exists

**Error**: `Error: Output file already exists: <path>`

**Solution**: Use the `--overwrite` flag to allow overwriting:
```bash
python tools/extract_paper.py --overwrite
```

### Image Conversion Failed

**Warning**: `Warning: Could not convert <filename> to PNG: <error>`

**Note**: This is just a warning. The image is still extracted in its original format. To enable PNG conversion, install Pillow:
```bash
pip install Pillow
```

## Examples

### Example 1: First-time extraction

```bash
# Extract the SegNet4D paper for the first time
python tools/extract_paper.py --verbose
```

Output:
```
PDF Path: SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf
Output Markdown: docs/SegNet4D_paper_extracted.md
Images Directory: docs/paper_images
Pillow available: True

Extracting text from PDF...
Page 1: Extracted 2045 characters
...

✓ Successfully extracted PDF content to docs/SegNet4D_paper_extracted.md
✓ Extracted 15 images to docs/paper_images
```

### Example 2: Re-extract with updates

```bash
# Re-extract after making changes or updates
python tools/extract_paper.py --overwrite
```

### Example 3: Extract different paper

```bash
# Extract a different paper to a different location
python tools/extract_paper.py \
  --pdf-path papers/another_paper.pdf \
  --out-md docs/another_paper.md \
  --images-dir docs/another_paper_images/
```

## Advanced Usage

### Batch Processing

Extract multiple PDFs:

```bash
#!/bin/bash
for pdf in papers/*.pdf; do
  basename=$(basename "$pdf" .pdf)
  python tools/extract_paper.py \
    --pdf-path "$pdf" \
    --out-md "docs/${basename}.md" \
    --images-dir "docs/${basename}_images/" \
    --overwrite
done
```

### Integration with Other Tools

The generated Markdown can be used with other tools:

```bash
# Convert to HTML
pandoc docs/SegNet4D_paper_extracted.md -o docs/SegNet4D_paper_extracted.html

# View in a Markdown viewer
grip docs/SegNet4D_paper_extracted.md
```

## Notes

- The title and author extraction is heuristic and may not be perfect for all PDFs
- Section detection relies on common heading patterns and may miss unconventional section names
- Image quality depends on the original PDF embedding
- The script creates directories automatically if they don't exist
- All output is UTF-8 encoded to support international characters

## Contributing

If you encounter issues or have suggestions for improvements, please open an issue in the repository.

## License

This utility is part of the SegNet4D project and follows the same license.
