---
name: closed-book-single-lecture-analysis
description: >-
  Perform in-depth analysis of one or more lecture PDFs with logic reordering
  and tiered depth by topic frequency. Use for closed-book single-lecture study,
  conceptual deep dives, or batch continuation across lecture numbers.
disable-model-invocation: true
metadata:
  author: Youhan Huang
  tool: Cursor Composer 2.5
---

# Closed-Book Single-Lecture Analysis

闭卷考试单课件深入分析。对指定 lecture 进行完整覆盖、逻辑重组与分级深度阐述。

## Applicability

- 闭卷复习中对单讲或多讲进行系统性学习
- 课件含公式、推导、图示，需图文联合解析
- 支持分批执行：完成指定讲次后，按用户指令继续后续讲次

## Output Contract

默认输出 Markdown，命名由用户指定，推荐 `<Course>_L<n>_analysis.md`。

结构模板：

```markdown
## 1. Overview
- Core problem statement
- Reordered logic flow: A → B → C

## 2. Topic Analysis

### [Core] Topic name
- Source definitions and key terms (verbatim from slides)
- Conceptual explanation
- Formulas and symbol definitions (if applicable)
- Prerequisite and successor relations
- Typical exam applications

### [Auxiliary] Topic name
- Brief definition
- Role within the lecture scope

## 3. Review questions
（3 items）
```

英方课程：关键术语保留英文，格式 `中文（English）`。

## Depth Rules

| Occurrence in slides | Treatment |
|---------------------|-----------|
| Multiple pages, repeated, with derivations | Full analysis |
| Single page, mentioned once | Concise summary |

零遗漏：辅助知识点可短，但不得删除。

## Workflow

### 1. Slide inspection

- 读取用户指定的 PDF/PPT
- 稀疏页、图示页、公式页须渲染或 OCR，不得仅依赖文本层
- 统计各概念页码跨度与出现频次

### 2. Logic reordering

- 打破原始 Slide 页序
- 按由浅入深、因果链或架构层次重组
- 正文不得按 `Slide 1 / Slide 2` 组织（页码仅作溯源注释）

### 3. Tiered writing

- 核心主题：完整定义、解释、公式、考点
- 辅助主题：简要定义与定位

### 4. Batch continuation

用户指定后续讲次时：

- 仅处理新指定范围
- 保持与前序批次一致的结构与术语规范

## Constraints

- 图示内容须转写为文字，不得使用「见图」类占位
- PDF 图像层与文本层同等重要
- 不得输出与课件矛盾的通用知识

## Invocation Examples

```text
使用 closed-book-single-lecture-analysis：@lectureSlides 分析 L1。多页概念完整展开，单页概念简要概括。
```

```text
使用 closed-book-single-lecture-analysis，继续 L7–L8，须包含 PDF 图示内容。
```

## Relation to Root Skill

根目录 `note-single-lecture` 面向单讲笔记产物（思维导图 → 提示词 → 课程笔记）。本 skill 面向闭卷理解的深度分析正文，二者可配合使用。

## Attribution

- Author: Youhan Huang
- Tool: Cursor Composer 2.5
