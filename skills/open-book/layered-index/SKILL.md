---
name: open-book-layered-index
description: >-
  Construct hierarchical open-book exam indexes that map topics to lecture PDF
  file names and page numbers. Use for open-book revision, revision_exam.md,
  course map, or slide page lookup without explanatory prose.
disable-model-invocation: true
metadata:
  author: Youhan Huang
  tool: Cursor Composer 2.5
---

# Open-Book Layered Index

开卷考试复习索引。输出分层检索结构，将知识点映射至课件文件名与页码；默认不包含知识点解释性正文。

## Applicability

- 开卷考试复习资料编制
- 需快速定位：某主题对应哪份 PDF、哪几页
- 输入为全套 lecture PDF/PPT；可选历年试题目录用于附录权重表

## Design Principles

1. 覆盖完整优先于篇幅压缩
2. 知识结构优先于课件原始页序
3. 索引职责与解释职责分离：本 skill 仅负责索引
4. 图示、UML、流程图、表格须转写为可检索文字条目，不得使用「见图」类占位表述

## Output Contract

默认输出 `revision_exam.md`，推荐结构：

```markdown
# <Course> Open-Book Index

## Layer 1 — Course Blocks
Mermaid 概览：Block → 课件文件列表

## Layer 2 — Per-Lecture Index Tables
### <PDF filename>
| Topic（缩写首次附全称） | Pages |
|--------|-------|

## Layer 3 — Figure / Diagram Index（可选）
| Figure / Diagram | PDF | Pages | Related topics |

## Appendix — Exam Topic Pointers（可选，需 oldResource）
| Topic | Frequency | Priority | PDF | Pages |
```

英方课程：英文术语及缩写首次出现须附全称。

## Workflow

### 1. Corpus ingestion

读取全部 PDF/PPT，同时处理：

- 正文、图片、UML、架构图、时序图、状态图、活动图、表格、公式
- 图中箭头、标注及其逻辑关系

对每张关键图示提取：核心概念、组成单元、单元关系、说明的问题、关联知识点。

### 2. Layer 1 — Course blocks

按主题将课程划分为若干 Block；每 Block 映射一组课件文件。输出 Mermaid 分层概览。

### 3. Layer 2 — Lecture index tables

对每份 PDF 生成完整「Topic → Pages」表。页码为 PDF 内页序；若课件含 printed slide number，可同时标注。

### 4. Layer 3 — Figure index

汇总关键图表索引，支持考场按图名检索。

### 5. Appendix — Exam pointers（可选）

若提供 `@oldResource`：

- 统计历年试题考点频率
- 输出单一 Master Table，合并频率、优先级与页码指向
- 不得重复生成多张同义排序表

## Constraints

- 页码必须对应工作区中真实文件名
- Layer 2 须覆盖全部课件，不得遗漏章节
- 缩写首次出现须含全称
- 合并或删除旧版中间文件前须经用户确认

## Invocation Examples

```text
使用 open-book-layered-index：@lectureSlides 生成 revision_exam.md。Layer 1–3 为分层索引，不包含知识点解释。
```

```text
使用 open-book-layered-index，结合 @oldResource 在 Appendix 中追加考点频率与页码指向表。
```

## Attribution

- Author: Youhan Huang
- Tool: Cursor Composer 2.5
