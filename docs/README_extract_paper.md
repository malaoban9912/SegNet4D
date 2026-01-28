# PDF 提取工具使用指南

本工具用于从 SegNet4D 论文 PDF 文件中提取文本和图片，并生成结构化的 Markdown 文档。

## 功能特性

- ✅ 自动提取 PDF 全文文本
- ✅ 识别章节结构（Abstract, Introduction, Method, Experiments, Conclusion 等）
- ✅ 提取所有图片并保存为 PNG 格式
- ✅ 生成带目录的 Markdown 文档
- ✅ 图片自动关联到对应章节
- ✅ 支持自定义输入输出路径
- ✅ 提供详细的处理日志

## 依赖项

本工具使用 **PyMuPDF** 库来解析 PDF 文件。

### 安装依赖

```bash
# 安装 PyMuPDF（推荐版本）
pip install PyMuPDF==1.22.0

# 或者安装项目所有依赖
pip install -r requirements.txt
```

**推荐版本**: PyMuPDF 1.22.0（也支持更高版本，但建议在 1.x 系列中）

## 使用方法

### 基本用法

在仓库根目录运行：

```bash
python tools/extract_paper.py
```

这将：
1. 读取根目录下的 `SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf`
2. 提取文本和图片
3. 在 `docs/` 目录下生成 `SegNet4D_paper_extracted.md`
4. 在 `docs/paper_images/` 目录下保存所有提取的图片

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--pdf-path` | 指定 PDF 文件路径 | `SegNet4D_Efficient_Instance-Aware_4D_Semantic_Segmentation_for_LiDAR_Point_Cloud.pdf` |
| `--out-md` | 指定输出 Markdown 文件路径 | `docs/SegNet4D_paper_extracted.md` |
| `--images-dir` | 指定图片输出目录 | `docs/paper_images/` |
| `--overwrite` | 覆盖已存在的输出文件 | False（不覆盖） |
| `--verbose` | 显示详细处理日志 | False（简洁输出） |

### 使用示例

#### 示例 1: 使用默认设置

```bash
python tools/extract_paper.py
```

#### 示例 2: 指定自定义 PDF 文件

```bash
python tools/extract_paper.py --pdf-path ./my_paper.pdf --out-md docs/my_paper.md
```

#### 示例 3: 覆盖已存在的输出文件

```bash
python tools/extract_paper.py --overwrite
```

#### 示例 4: 显示详细日志

```bash
python tools/extract_paper.py --verbose
```

#### 示例 5: 完整自定义参数

```bash
python tools/extract_paper.py \
  --pdf-path ./papers/segnet4d.pdf \
  --out-md docs/extracted/segnet4d.md \
  --images-dir docs/extracted/images/ \
  --overwrite \
  --verbose
```

## 输出文件结构

运行工具后，将生成以下文件结构：

```
SegNet4D/
├── docs/
│   ├── SegNet4D_paper_extracted.md     # 提取的 Markdown 文档
│   ├── paper_images/                    # 提取的图片目录
│   │   ├── page_01_img_1.png           # 第1页的第1张图片
│   │   ├── page_03_img_1.png           # 第3页的第1张图片
│   │   ├── page_05_img_1.png           # 第5页的第1张图片
│   │   └── ...
│   └── README_extract_paper.md         # 本说明文档
└── tools/
    └── extract_paper.py                 # PDF 提取脚本
```

### Markdown 文档结构

生成的 Markdown 文档包含以下部分：

1. **论文标题和元信息**：从 PDF 第一页提取
2. **目录**：带锚点链接的章节列表
3. **各章节内容**：
   - 章节标题
   - 页码范围
   - 提取的文本内容
   - 该章节相关的图片（带相对路径链接）
   - 解析说明占位符（供后续填写中文解析）
4. **附加图片**：未归类到具体章节的其他图片

## 章节识别

工具会自动识别以下常见章节标题（不区分大小写）：

- **英文**：Abstract, Introduction, Related Work, Method, Methodology, Approach, Experiments, Results, Discussion, Conclusion, Acknowledgment, References
- **中文**：摘要, 引言, 相关工作, 方法, 实验, 结果, 结论, 致谢, 参考文献

## 常见问题

### 1. 提示"未找到 PyMuPDF 库"

**问题**：运行脚本时显示缺少 PyMuPDF 依赖。

**解决方法**：
```bash
pip install PyMuPDF==1.22.0
```

### 2. 输出文件已存在

**问题**：运行脚本时提示"输出文件已存在"。

**解决方法**：
使用 `--overwrite` 参数强制覆盖：
```bash
python tools/extract_paper.py --overwrite
```

### 3. PDF 文件不存在

**问题**：显示"错误: PDF文件不存在"。

**解决方法**：
- 确认 PDF 文件路径正确
- 使用 `--pdf-path` 参数指定正确的路径：
```bash
python tools/extract_paper.py --pdf-path /path/to/your/paper.pdf
```

### 4. 某些图片无法提取

**问题**：部分图片在 Markdown 中显示为"无法提取"。

**原因**：某些 PDF 使用特殊编码或矢量格式，可能无法直接提取。

**解决方法**：
- 查看原 PDF 文件中的对应页面
- 对于关键图片，可以手动截图后添加到文档中

### 5. 章节识别不准确

**问题**：某些章节未被正确识别或分段。

**原因**：PDF 的文本布局可能不规则，或使用了非标准的章节标题。

**解决方法**：
- 生成的 Markdown 文档可以手动编辑和调整
- 查看 `--verbose` 模式下的详细日志了解识别过程

## 技术说明

### PDF 解析

- 使用 PyMuPDF (fitz) 库进行 PDF 解析
- 支持文本提取、图片提取、页面分析
- 对于加密或受保护的 PDF，需要先解除保护

### 图片提取

- 图片以 PNG 格式保存（保证兼容性和质量）
- 文件命名格式：`page_XX_img_Y.png`（XX=页码，Y=图片序号）
- 矢量图和内嵌图片都会尝试提取

### 文本编码

- 所有输出文件使用 UTF-8 编码
- 支持中英文混合内容
- Markdown 使用标准语法，兼容主流编辑器

## 后续使用建议

1. **人工审阅**：生成的 Markdown 文档建议人工审阅，确保章节划分和内容准确性
2. **补充解析**：在每个章节的"解析说明"部分填写中文解析和理解
3. **图片标注**：为重要图片添加详细的标题和说明
4. **格式调整**：根据需要调整 Markdown 格式和排版

## 脚本维护

- **位置**：`tools/extract_paper.py`
- **语言**：Python 3.6+
- **依赖**：PyMuPDF (fitz)
- **许可**：遵循仓库许可证

## 联系与反馈

如有问题或建议，请在仓库中提交 Issue。
