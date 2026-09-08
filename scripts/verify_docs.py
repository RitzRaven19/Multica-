#!/usr/bin/env python3
"""Traceability gate for docs/BRD.md, docs/FRD.md, docs/UAT.md.

Checks the chain business-rule -> functional requirement -> functional
spec -> test case actually holds:
  1. Every BRD F-id is referenced by at least one FRD requirement block.
  2. Every FRD requirement block's references (F-id/BR-id) exist in the BRD.
  3. Every FRD FR-id is referenced by at least one UAT test case.
  4. Every UAT test case's references (FR-id/BR-id) exist upstream.

Exits non-zero if any check fails, so it can gate a CI job. Open
questions (OQ-xxx) are reported for visibility only -- they are not a
failure, they are the known-unresolved items the docs already flag.
"""
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

ID_BR = re.compile(r"\bBR-\d{3}\b")
ID_F = re.compile(r"\bF\d{1,3}\b")
ID_NF = re.compile(r"\bNF\d{1,2}\b")
ID_FR = re.compile(r"\bFR-\d{1,3}\b")
ID_TC = re.compile(r"\bTC-\d{1,3}\b")
ID_OQ = re.compile(r"\bOQ-\d{3}\b")

FRD_HEADING = re.compile(r"^#{1,4}\s*(FR-\d{1,3})\b.*$", re.MULTILINE)
UAT_TC_LINE = re.compile(r"^\*\*(TC-\d{1,3})\*\*\s*\|(.*)$", re.MULTILINE)


def read(name):
    p = DOCS / name
    return p.read_text(encoding="utf-8") if p.exists() else None


def declared_ids(text, pattern):
    return set(pattern.findall(text))


def frd_trace_map(text):
    """FR-id -> set of F-ids/BR-ids referenced in that FR's section (heading to next heading)."""
    headings = list(FRD_HEADING.finditer(text))
    out = {}
    for i, m in enumerate(headings):
        fr_id = m.group(1)
        start = m.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        block = text[start:end]
        out.setdefault(fr_id, set()).update(ID_F.findall(block))
        out[fr_id].update(ID_BR.findall(block))
    return out


def uat_trace_map(text):
    """TC-id -> set of FR-ids/BR-ids declared on that test case's own line."""
    out = {}
    for m in UAT_TC_LINE.finditer(text):
        tc_id, rest = m.group(1), m.group(2)
        refs = set(ID_FR.findall(rest)) | set(ID_BR.findall(rest))
        out.setdefault(tc_id, set()).update(refs)
    return out


def main():
    errors = []
    warnings = []

    brd = read("BRD.md")
    frd = read("FRD.md")
    uat = read("UAT.md")

    if brd is None:
        errors.append("docs/BRD.md is missing -- no BRD to trace against.")
    if frd is None:
        errors.append("docs/FRD.md is missing -- no FRD to trace against.")
    if uat is None:
        warnings.append("docs/UAT.md is missing -- UAT coverage cannot be checked yet.")

    if brd and frd:
        brd_f_ids = declared_ids(brd, ID_F) - declared_ids(brd, ID_NF)
        brd_br_ids = declared_ids(brd, ID_BR)
        frd_map = frd_trace_map(frd)

        covered_f = set()
        dangling_frd_refs = set()
        for fr_id, refs in frd_map.items():
            for r in refs:
                if r in brd_f_ids:
                    covered_f.add(r)
                elif r in brd_br_ids:
                    pass
                else:
                    dangling_frd_refs.add(f"{fr_id} -> {r}")

        uncovered_f = sorted(brd_f_ids - covered_f, key=lambda s: int(re.sub(r"\D", "", s)))

        if not frd_map:
            warnings.append("FRD.md has no '#### FR-x' style headings -- could not build a trace map.")
        if uncovered_f:
            errors.append(
                "BRD functional requirement(s) with no FRD coverage: "
                + ", ".join(uncovered_f)
            )
        if dangling_frd_refs:
            errors.append(
                "FRD section(s) reference id(s) that do not exist in BRD.md: "
                + ", ".join(sorted(dangling_frd_refs))
            )

    if frd and uat:
        frd_fr_ids = set(frd_trace_map(frd).keys()) or declared_ids(frd, ID_FR)
        brd_br_ids = declared_ids(brd, ID_BR) if brd else set()
        uat_map = uat_trace_map(uat)

        covered_fr = set()
        dangling_uat_refs = set()
        for tc_id, refs in uat_map.items():
            for r in refs:
                if r in frd_fr_ids:
                    covered_fr.add(r)
                elif r in brd_br_ids:
                    pass
                else:
                    dangling_uat_refs.add(f"{tc_id} -> {r}")

        uncovered_fr = sorted(frd_fr_ids - covered_fr)
        if not uat_map:
            warnings.append("UAT.md has no '**TC-xx** | FR-x | BR-xxx | ...' style lines -- could not build a trace map.")
        if uncovered_fr:
            errors.append(
                "FRD requirement(s) with no UAT test case: " + ", ".join(uncovered_fr)
            )
        if dangling_uat_refs:
            errors.append(
                "UAT test case(s) reference id(s) that do not exist upstream: "
                + ", ".join(sorted(dangling_uat_refs))
            )

    for name, text in (("BRD.md", brd), ("FRD.md", frd), ("UAT.md", uat)):
        if text:
            oqs = sorted(declared_ids(text, ID_OQ))
            if oqs:
                warnings.append(f"{name} carries open question(s): {', '.join(oqs)}")

    print("=== Document verification ===")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")

    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        sys.exit(1)

    print("\nAll traceability checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
