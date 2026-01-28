#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF提取工具 - 从论文PDF中提取文本和图片并生成Markdown文档

该脚本使用PyMuPDF (fitz)从PDF文件中提取文本和图片，
并生成结构化的Markdown文档，包含章节标题、正文和图片链接。
"""

import argparse
import os
import re
import sys
from pathlib import Path


def check_dependencies():
    """检查PyMuPDF依赖是否已安装"""
    try:
        import fitz
        return True
    except ImportError:
        print("=" * 60)
        print("错误: 未找到PyMuPDF库")
        print("=" * 60)
        print("请使用以下命令安装PyMuPDF:")
        print("  pip install PyMuPDF==1.22.0")
        print("\n或安装所有依赖:")
        print("  pip install -r requirements.txt")
        print("=" * 60)
        return False


def extract_images_from_page(page, page_num, images_dir, verbose=False):
    """
    从单个PDF页面提取所有图片
    
    Args:
        page: PyMuPDF页面对象
        page_num: 页码（从1开始）
        images_dir: 图片保存目录
        verbose: 是否显示详细日志
        
    Returns:
        提取的图片信息列表 [(文件名, 相对路径), ...]
    """
    image_list = []
    img_list = page.get_images(full=True)
    
    for img_index, img in enumerate(img_list, start=1):
        xref = img[0]
        try:
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # 生成文件名: page_XX_img_Y.png
            filename = f"page_{page_num:02d}_img_{img_index}.png"
            filepath = images_dir / filename
            
            # 保存图片
            with open(filepath, "wb") as img_file:
                img_file.write(image_bytes)
            
            # 返回相对路径（相对于docs目录）
            relative_path = f"paper_images/{filename}"
            image_list.append((filename, relative_path))
            
            if verbose:
                print(f"  提取图片: {filename} (原格式: {image_ext})")
                
        except Exception as e:
            if verbose:
                print(f"  警告: 无法提取图片 {img_index} (xref={xref}): {e}")
            # 添加占位符
            filename = f"page_{page_num:02d}_img_{img_index}_failed"
            image_list.append((filename, None))
    
    return image_list


def detect_section_title(text_line):
    """
    检测文本行是否为章节标题
    
    支持的章节标题（不区分大小写）：
    Abstract, 摘要, Introduction, 引言, Related Work, 相关工作,
    Method, 方法, Methodology, Approach, Experiments, Results,
    实验, 结果, Discussion, Conclusion, 结论, Acknowledgment, 
    致谢, References, 参考文献
    
    Returns:
        如果是章节标题，返回标题文本；否则返回None
    """
    # 清理文本并检查是否为标题
    cleaned = text_line.strip()
    
    # 章节标题关键词（不区分大小写）
    section_keywords = [
        r'\b(abstract)\b',
        r'摘要',
        r'\b(introduction)\b',
        r'引言',
        r'\b(related\s+work)\b',
        r'相关工作',
        r'\b(method)\b',
        r'方法',
        r'\b(methodology)\b',
        r'\b(approach)\b',
        r'\b(experiments?)\b',
        r'\b(results?)\b',
        r'实验',
        r'结果',
        r'\b(discussion)\b',
        r'\b(conclusions?)\b',
        r'结论',
        r'\b(acknowledgments?)\b',
        r'致谢',
        r'\b(references)\b',
        r'参考文献',
    ]
    
    # 检查是否匹配任何章节关键词
    for pattern in section_keywords:
        if re.search(pattern, cleaned, re.IGNORECASE):
            # 额外验证：标题通常不会太长
            if len(cleaned) < 100:
                return cleaned
    
    # 检查编号章节标题，如 "1. Introduction" 或 "1 Introduction"
    numbered_pattern = r'^\s*\d+\.?\s+([A-Z][a-zA-Z\s]+)$'
    match = re.match(numbered_pattern, cleaned)
    if match and len(cleaned) < 100:
        return cleaned
    
    return None


def extract_text_and_structure(pdf_path, verbose=False):
    """
    从PDF提取文本并识别章节结构
    
    Returns:
        (title, sections) 其中 sections 是 [(section_name, text, page_num, images), ...]
    """
    import fitz
    
    doc = fitz.open(pdf_path)
    title = None
    current_section = "引言"  # 默认章节
    sections = []
    section_text = []
    section_start_page = 1
    section_images = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        # 从第一页尝试提取标题
        if page_num == 0 and title is None:
            lines = text.split('\n')
            # 通常标题在前几行
            for i, line in enumerate(lines[:10]):
                if line.strip() and len(line.strip()) > 10:
                    title = line.strip()
                    break
        
        # 分行处理文本
        lines = text.split('\n')
        for line in lines:
            # 检查是否为章节标题
            section_title = detect_section_title(line)
            if section_title:
                # 保存之前的章节
                if section_text:
                    sections.append((
                        current_section,
                        '\n'.join(section_text),
                        section_start_page,
                        section_images
                    ))
                
                # 开始新章节
                current_section = section_title
                section_text = []
                section_start_page = page_num + 1
                section_images = []
                
                if verbose:
                    print(f"检测到章节: {section_title} (第 {page_num + 1} 页)")
            else:
                # 添加到当前章节
                if line.strip():
                    section_text.append(line)
    
    # 保存最后一个章节
    if section_text:
        sections.append((
            current_section,
            '\n'.join(section_text),
            section_start_page,
            section_images
        ))
    
    doc.close()
    
    return title, sections


def extract_all_images(pdf_path, images_dir, verbose=False):
    """
    从PDF的所有页面提取图片
    
    Returns:
        {page_num: [(filename, relative_path), ...], ...}
    """
    import fitz
    
    doc = fitz.open(pdf_path)
    all_images = {}
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = extract_images_from_page(page, page_num + 1, images_dir, verbose)
        if images:
            all_images[page_num + 1] = images
    
    doc.close()
    return all_images


def generate_markdown(title, sections, all_images, output_path, verbose=False):
    """
    生成Markdown文档
    
    Args:
        title: 论文标题
        sections: 章节列表 [(section_name, text, page_num, images), ...]
        all_images: 所有页面的图片 {page_num: [(filename, relative_path), ...], ...}
        output_path: 输出文件路径
        verbose: 是否显示详细日志
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        # 写入标题
        if title:
            f.write(f"# {title}\n\n")
        else:
            f.write("# SegNet4D 论文提取\n\n")
        
        f.write("*本文档由自动化工具从PDF提取生成*\n\n")
        f.write("---\n\n")
        
        # 生成目录
        f.write("## 目录\n\n")
        for i, (section_name, _, _, _) in enumerate(sections, start=1):
            # 创建锚点链接（转换为小写，替换空格和特殊字符）
            anchor = re.sub(r'[^\w\u4e00-\u9fff]+', '-', section_name.lower())
            anchor = anchor.strip('-')
            f.write(f"{i}. [{section_name}](#{anchor})\n")
        f.write("\n---\n\n")
        
        # 写入各章节
        for section_name, text, start_page, _ in sections:
            # 章节标题
            anchor = re.sub(r'[^\w\u4e00-\u9fff]+', '-', section_name.lower())
            anchor = anchor.strip('-')
            f.write(f"## {section_name}\n\n")
            f.write(f"*页码范围: 第 {start_page} 页开始*\n\n")
            
            # 章节正文
            f.write(text)
            f.write("\n\n")
            
            # 插入该页面的图片
            # 注意：这里简单处理，插入起始页的图片
            if start_page in all_images:
                f.write(f"### 图片 (第 {start_page} 页)\n\n")
                for filename, relative_path in all_images[start_page]:
                    if relative_path:
                        f.write(f"![{filename}]({relative_path})\n\n")
                        f.write(f"*图片来源: PDF 第 {start_page} 页, 文件名: {filename}*\n\n")
                    else:
                        f.write(f"*[无法提取图片: {filename}，请查看原PDF第 {start_page} 页]*\n\n")
            
            # 添加解析占位符
            f.write("### 解析说明\n\n")
            f.write("[待解析：在此处填写对本节的中文解析]\n\n")
            f.write("---\n\n")
        
        # 添加所有其他页面的图片（不在章节范围内的）
        f.write("## 附加图片\n\n")
        f.write("*以下是其他页面提取的图片*\n\n")
        
        section_pages = {start_page for _, _, start_page, _ in sections}
        for page_num in sorted(all_images.keys()):
            if page_num not in section_pages:
                f.write(f"### 第 {page_num} 页图片\n\n")
                for filename, relative_path in all_images[page_num]:
                    if relative_path:
                        f.write(f"![{filename}]({relative_path})\n\n")
                    else:
                        f.write(f"*[无法提取图片: {filename}]*\n\n")
                f.write("\n")
    
    if verbose:
        print(f"✓ Markdown文档已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='从PDF提取文本和图片并生成Markdown文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认设置
  python tools/extract_paper.py
  
  # 指定自定义PDF和输出路径
  python tools/extract_paper.py --pdf-path ./my_paper.pdf --out-md docs/my_paper.md
  
  # 覆盖已存在的输出文件
  python tools/extract_paper.py --overwrite
  
  # 显示详细处理日志
  python tools/extract_paper.py --verbose
        """
    )
    
    parser.add_argument(
        '--pdf-path',
        type=str,
        default='SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf',
        help='PDF文件路径（默认: 仓库根目录的论文PDF）'
    )
    parser.add_argument(
        '--out-md',
        type=str,
        default='docs/SegNet4D_paper_extracted.md',
        help='输出Markdown文件路径（默认: docs/SegNet4D_paper_extracted.md）'
    )
    parser.add_argument(
        '--images-dir',
        type=str,
        default='docs/paper_images/',
        help='图片输出目录（默认: docs/paper_images/）'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='如果输出文件已存在，则覆盖'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细处理日志'
    )
    
    args = parser.parse_args()
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    import fitz  # 只有在依赖检查通过后才导入
    
    # 转换路径为绝对路径
    script_dir = Path(__file__).parent.parent  # 仓库根目录
    pdf_path = Path(args.pdf_path)
    if not pdf_path.is_absolute():
        pdf_path = script_dir / pdf_path
    
    output_md = Path(args.out_md)
    if not output_md.is_absolute():
        output_md = script_dir / output_md
    
    images_dir = Path(args.images_dir)
    if not images_dir.is_absolute():
        images_dir = script_dir / images_dir
    
    # 检查PDF文件是否存在
    if not pdf_path.exists():
        print(f"错误: PDF文件不存在: {pdf_path}")
        sys.exit(1)
    
    # 检查输出文件是否已存在
    if output_md.exists() and not args.overwrite:
        print(f"错误: 输出文件已存在: {output_md}")
        print("使用 --overwrite 参数来覆盖现有文件")
        sys.exit(1)
    
    # 创建输出目录
    try:
        output_md.parent.mkdir(parents=True, exist_ok=True)
        images_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"错误: 无法创建目录: {e}")
        sys.exit(1)
    
    print("=" * 60)
    print("PDF提取工具")
    print("=" * 60)
    print(f"PDF文件: {pdf_path}")
    print(f"输出Markdown: {output_md}")
    print(f"图片目录: {images_dir}")
    print("=" * 60)
    
    try:
        # 提取文本和结构
        if args.verbose:
            print("\n[1/3] 提取文本和章节结构...")
        title, sections = extract_text_and_structure(pdf_path, args.verbose)
        
        if args.verbose:
            print(f"\n提取到 {len(sections)} 个章节")
            if title:
                print(f"论文标题: {title}")
        
        # 提取所有图片
        if args.verbose:
            print("\n[2/3] 提取图片...")
        all_images = extract_all_images(pdf_path, images_dir, args.verbose)
        
        total_images = sum(len(imgs) for imgs in all_images.values())
        if args.verbose:
            print(f"\n共提取 {total_images} 张图片")
        
        # 生成Markdown
        if args.verbose:
            print("\n[3/3] 生成Markdown文档...")
        generate_markdown(title, sections, all_images, output_md, args.verbose)
        
        print("\n" + "=" * 60)
        print("✓ 提取完成!")
        print("=" * 60)
        print(f"章节数量: {len(sections)}")
        print(f"图片数量: {total_images}")
        print(f"输出文件: {output_md}")
        print(f"图片目录: {images_dir}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: 处理过程中出现异常: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
