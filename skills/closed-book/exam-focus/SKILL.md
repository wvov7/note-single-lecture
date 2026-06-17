---
name: closed-book-exam-focus
description: >-
  Derive weighted exam topic priorities by cross-referencing past papers with
  lecture slide indexes. Use for closed-book exam preparation, exam_lecture_summary,
  or prioritization from oldResource and lectureSlides.
disable-model-invocation: true
metadata:
  author: Youhan Huang
  tool: Cursor Composer 2.5
---

# Closed-Book Exam Focus

闭卷考试考点优先级分析。基于历年试题与课件索引，输出加权考点表及复习优先级。

## Applicability

- 闭卷考试前的考点筛选与排序
- 输入需同时包含 `@lectureSlides` 与 `@oldResource`（或等价路径）
- 可结合 `full-course-highlights` 产出的页码索引作为交叉引用基础

## Output Contract

默认输出 `exam_lecture_summary.md` 或用户指定文件名：

```markdown
# <Course> Exam Focus Analysis

## Weighting Method
（说明权重公式与假设）

## Master Topic Table
| Topic | Weight | Past papers | Lecture PDF | Pages | Priority |
|-------|--------|-------------|-------------|-------|----------|

## Review Priority List
1. …
```

## Weighting Rules

须在报告中显式声明所采用的权重规则。推荐信号如下：

| Signal | Weight tier |
|--------|-------------|
| 往年试题高分值 / 大题 | Highest |
| 课件内多页且跨多讲出现 | Highest |
| 任意年份试题出现过 | High |
| 课件内重复出现 | Medium |
| 年份越近 | 累加权重 |

## Workflow

### 1. Resource inventory

- 枚举 `lectureSlides/` 全部 PDF/PPT
- 枚举 `oldResource/` 历年卷、quiz、样题
- 扫描件须经 OCR；中间产物存放于 `_extracted/`

### 2. Past-paper extraction

- 按年份记录题型结构、分值分布、覆盖知识点
- 为每份试卷分配基础权重（近期年份权重更高）

### 3. Topic normalization

- 从试题中提取考点短语
- 归一化至统一 taxonomy
- 映射至 `(lecture_pdf, page)` 索引

### 4. Master table synthesis

- 合并频率、权重、页码指向为单一总表
- 按权重降序排列
- 不确定匹配须标注 `pending verification`

### 5. Slide-grounded Q&A（可选扩展）

若用户要求根据课件作答试题或复核答案：

- 结论须附 `(PDF filename, page)` 引用
- 答案须严格基于课件；课件未涵盖的内容须标注为推断
- 批量输出默认写入 `answer.md`

## Constraints

- 不得虚构试题中未出现的考点
- 每条考点须可回溯至具体 PDF 与页码
- 仅保留一张 Master Topic Table，避免重复排序表

## Invocation Examples

```text
使用 closed-book-exam-focus：@oldResource @lectureSlides 生成 exam_lecture_summary.md，按权重降序列出考点及对应页码。
```

```text
使用 closed-book-exam-focus，根据课件回答 @期末考试 全部题目并写入 answer.md，每题附 PDF 页码依据。
```

## Attribution

- Author: Youhan Huang
- Tool: Cursor Composer 2.5
