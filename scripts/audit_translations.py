#!/usr/bin/env python3
"""Audit bilingual translation coverage for note-single-lecture outputs.

The script checks two things:
1. translation_units.json has complete source, translation, and explanation fields.
2. Final Markdown notes do not contain English source quote/list blocks unless
   the same block also contains Chinese translation text.

Usage:
  python audit_translations.py translation_units.json notes.md report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
ENGLISH_RE = re.compile(r"[A-Za-z]")
FENCE_RE = re.compile(r"^\s*```")


def has_chinese(text: str) -> bool:
    return bool(CHINESE_RE.search(text or ""))


def has_english(text: str) -> bool:
    return bool(ENGLISH_RE.search(text or ""))


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def searchable_markdown(text: str) -> str:
    text = re.sub(r"(?m)^\s*>\s?", "", text or "")
    text = re.sub(r"(?m)^\s*[-*]\s+", "", text)
    return normalize_space(text)


def searchable_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in (text or "").splitlines():
        cleaned = searchable_markdown(raw)
        if cleaned:
            lines.append(cleaned)
    return lines


def missing_units(text: str, normalized_notes: str, min_len: int = 12) -> list[str]:
    compact = searchable_markdown(text)
    if not compact:
        return []
    if len(compact) >= 30 and compact in normalized_notes:
        return []
    missing: list[str] = []
    for line in searchable_lines(text):
        if len(line) >= min_len and line not in normalized_notes:
            missing.append(line)
    return missing


def load_units(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    problems: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        units = data.get("units")
    else:
        units = data
    if not isinstance(units, list):
        return [], ["translation_units.json must be a list or an object with a 'units' list."]
    normalized: list[dict[str, Any]] = []
    required = ["id", "slide", "type", "source", "translation", "explanation"]
    for idx, unit in enumerate(units, 1):
        if not isinstance(unit, dict):
            problems.append(f"Unit {idx} is not an object.")
            continue
        normalized.append(unit)
        label = str(unit.get("id") or f"#{idx}")
        for field in required:
            if not str(unit.get(field, "")).strip():
                problems.append(f"{label}: missing required field '{field}'.")
        source = str(unit.get("source", ""))
        translation = str(unit.get("translation", ""))
        explanation = str(unit.get("explanation", ""))
        if source and not has_english(source):
            problems.append(f"{label}: source should preserve English original text.")
        if translation and not has_chinese(translation):
            problems.append(f"{label}: translation must contain Chinese.")
        if explanation and not has_chinese(explanation):
            problems.append(f"{label}: explanation must contain Chinese.")
    return normalized, problems


def iter_note_blocks(text: str) -> list[dict[str, Any]]:
    """Return English quote/list blocks that do not include inline Chinese."""
    blocks: list[dict[str, Any]] = []
    lines = text.splitlines()
    in_code = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if FENCE_RE.match(line):
            in_code = not in_code
            i += 1
            continue
        if in_code or not line.strip():
            i += 1
            continue

        stripped = line.strip()
        starts_quote = stripped.startswith(">")
        starts_list = bool(re.match(r"^[-*]\s+", stripped))
        if starts_quote or starts_list:
            block_lines = [stripped]
            start = i + 1
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    break
                if starts_quote and nxt.startswith(">"):
                    block_lines.append(nxt)
                    i += 1
                    continue
                if starts_list and re.match(r"^[-*]\s+", nxt):
                    block_lines.append(nxt)
                    i += 1
                    continue
                break
            end = i
            raw = "\n".join(block_lines)
            cleaned = re.sub(r"(^|\n)\s*(>|[-*])\s*", " ", raw)
            if has_english(cleaned) and not has_chinese(cleaned):
                blocks.append({"line": start, "end_line": end, "text": normalize_space(cleaned)})
            continue
        i += 1
    return blocks


def audit_notes(notes_path: Path, units: list[dict[str, Any]], lookahead: int) -> list[dict[str, Any]]:
    text = notes_path.read_text(encoding="utf-8-sig")
    issues: list[dict[str, Any]] = []

    for block in iter_note_blocks(text):
        issues.append(
            {
                "kind": "missing_inline_translation",
                "line": block["line"],
                "text": block["text"][:220],
                "message": "English source block must include Chinese translation inside the same quote/list block.",
            }
        )

    normalized_notes = searchable_markdown(text)
    for unit in units:
        source_raw = str(unit.get("source", ""))
        translation_raw = str(unit.get("translation", ""))
        explanation_raw = str(unit.get("explanation", ""))
        if not searchable_markdown(source_raw):
            continue
        missing_source = missing_units(source_raw, normalized_notes, min_len=12)
        if missing_source:
            issues.append(
                {
                    "kind": "unit_not_found_in_notes",
                    "unit_id": unit.get("id"),
                    "source_preview": missing_source[:5],
                    "message": "translation_units.json source does not appear in final notes.",
                }
            )
        missing_translation = missing_units(translation_raw, normalized_notes, min_len=6)
        if missing_translation:
            issues.append(
                {
                    "kind": "translation_not_found_in_notes",
                    "unit_id": unit.get("id"),
                    "translation_preview": missing_translation[:5],
                    "message": "translation_units.json translation does not appear in final notes.",
                }
            )
        missing_explanation = missing_units(explanation_raw, normalized_notes, min_len=12)
        if missing_explanation:
            issues.append(
                {
                    "kind": "explanation_not_found_in_notes",
                    "unit_id": unit.get("id"),
                    "explanation_preview": missing_explanation[:5],
                    "message": "translation_units.json explanation does not appear in final notes.",
                }
            )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("units", type=Path)
    parser.add_argument("notes", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--lookahead", type=int, default=6)
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args()

    units, unit_problems = load_units(args.units)
    note_issues = audit_notes(args.notes, units, args.lookahead)
    report = {
        "translation_units": str(args.units),
        "notes": str(args.notes),
        "unit_count": len(units),
        "unit_problems": unit_problems,
        "note_issues": note_issues,
        "ok": not unit_problems and not note_issues,
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["ok"] or args.warn_only:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
