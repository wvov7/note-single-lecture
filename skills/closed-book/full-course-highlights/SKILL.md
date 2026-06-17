---
name: closed-book-full-course-highlights
description: >-
  Produce page-ordered highlight summaries for all lecture PDFs in a course,
  marking multi-page topics as high-priority. Use for closed-book full-course
  review, exam_lecture_stat Part 1, or complete slide coverage reports.
disable-model-invocation: true
metadata:
  author: Youhan Huang
  tool: Cursor Composer 2.5
---

# Closed-Book Full-Course Highlights

闭卷考试全课要点汇总。按课件原始顺序逐讲、逐页提取知识点，标注重复出现的高优先级主题。

## Applicability

- 闭卷复习第一阶段：建立全课知识覆盖清单
- 需对 `@lectureSlides` 全部 PDF 逐页处理
- 可与 `closed-book-exam-focus` 联用：本 skill 提供 Part 1 概括，后者提供考点权重

## Output Contract

默认输出 `exam_lecture_stat.md`（Part 1 部分）或独立文件：

```markdown
# <Course> Full-Course Highlights

## Lecture N: <title>
**Learning objectives**: …
**Topics by page range**:
1. P1–P3: … [priority marker]
2. P4–P8: …

Priority marker: repeated across multiple pages within or across lectures.
```

优先级标记规则：同一概念在多页出现须标注为高优先级；单页单次出现可简写但不得删除。

## Workflow

### 1. Slide extraction

- 逐页读取全部 PDF/PPT
- 图文并重：表格、示意图、截图须文字化
- 记录 `(lecture_file, page)` 供后续考点映射引用
- 扫描件或稀疏文本页须 OCR 或渲染后识别

### 2. Per-lecture summarization

- 按 PDF 文件名 / 讲次原始顺序组织
- 不按逻辑重排（逻辑重排见 `single-lecture-analysis`）
- 每讲包含：学习目标、按页码区间的要点列表

### 3. Priority annotation

- 统计各概念在课件中的出现页数
- 跨页重复：标注高优先级
- 单页单次：简要记录，保留完整性

### 4. Large-course execution

课件数量较大时：

1. 批量提取至 `_extracted/`（JSON 或 Markdown，含页码元数据）
2. 分批生成各讲 summary
3. 合并为单一报告

## Constraints

- 不得跳过任何页面
- 不得省略边缘知识点
- 页码区间须连续、无重叠遗漏
- 与 `single-lecture-analysis` 区分：本 skill 覆盖全课、按原序；后者深入单讲、按逻辑重组

## Invocation Examples

```text
使用 closed-book-full-course-highlights：@lectureSlides 逐页概括全部课件要点，多页出现的概念标注高优先级，输出 exam_lecture_stat.md。
```

## Attribution

- Author: Youhan Huang
- Tool: Cursor Composer 2.5
