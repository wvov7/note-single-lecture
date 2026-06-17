# Skills Catalog

英方课复习 skill 索引。`skills/` 按考试形式分为两层目录；根目录 [`SKILL.md`](../SKILL.md) 为单讲笔记 workflow（`note-single-lecture`）。

## Directory Structure

```text
skills/
├── open-book/
│   └── layered-index/          # 开卷：分层索引
└── closed-book/
    ├── exam-focus/               # 闭卷：考试重点
    ├── full-course-highlights/   # 闭卷：全部课件重点
    └── single-lecture-analysis/  # 闭卷：单课件深入分析
```

## Skill Reference

| Category | Skill | Purpose | Default output |
|----------|-------|---------|----------------|
| Open-book | [layered-index](open-book/layered-index/SKILL.md) | 分层索引：Block → 课件 → Topic/Page | `revision_exam.md` |
| Closed-book | [exam-focus](closed-book/exam-focus/SKILL.md) | 历年试题与课件交叉分析，考点权重 | `exam_lecture_summary.md` |
| Closed-book | [full-course-highlights](closed-book/full-course-highlights/SKILL.md) | 全部课件逐页要点汇总 | `exam_lecture_stat.md` |
| Closed-book | [single-lecture-analysis](closed-book/single-lecture-analysis/SKILL.md) | 单讲逻辑重组与分级深度分析 | `<Course>_L<n>_analysis.md` |
| Root | [note-single-lecture](../SKILL.md) | 单讲笔记：思维导图 → 提示词 → 笔记 | `note-single-lecture/<stem>_课程笔记.md` |

## Selection Guide

| Requirement | Skill |
|-------------|-------|
| 开卷考试，需 Topic → PDF 页码检索 | `open-book/layered-index` |
| 闭卷考试，需确定复习优先级 | `closed-book/exam-focus` |
| 闭卷考试，需全课覆盖清单 | `closed-book/full-course-highlights` |
| 闭卷考试，需深入理解单讲 | `closed-book/single-lecture-analysis` |
| 单讲结构化中文笔记 | `note-single-lecture`（根目录） |

## Installation (Cursor)

将所需 skill 子目录复制至 Cursor skills 路径：

```powershell
Copy-Item -Recurse "<repo>\skills\closed-book\exam-focus" `
  "$env:USERPROFILE\.cursor\skills\closed-book-exam-focus"
```

根 skill 安装方式见 [README.md](../README.md)。

## Attribution

| Field | Value |
|-------|-------|
| Author | Youhan Huang |
| Tool | Cursor Composer 2.5 |
