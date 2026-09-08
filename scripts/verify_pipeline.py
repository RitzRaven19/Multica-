#!/usr/bin/env python3
"""Structural + referential-integrity gate for the Group 2 JSON pipeline.

Validates shared_outputs/{brd,business_rules,open_questions,frd,data_spec,
error_catalogue,acceptance_criteria,uat_cases,coverage_report}.json and
shared_outputs/traceability_matrix.csv against the schemas fixed in the
Group 2 agent instructions (brd-agent / frd-agent / uat-generator).

Hard failures (exit 1): missing files, broken JSON, missing required
fields, dangling id references, duplicate ids, requirements with no
acceptance criteria or no UAT case.

Warnings only: a business rule with no downstream FRD requirement. That
can be a real gap or a deliberate exclusion rule (e.g. "X is out of
scope") -- telling the two apart is a judgement call this script can't
make, so it's surfaced for a human/agent to read, not auto-failed.
"""
import csv
import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "shared_outputs"

REQUIRED_FILES = [
    "brd.json", "business_rules.json", "open_questions.json", "BRD.md",
    "frd.json", "data_spec.json", "error_catalogue.json",
    "acceptance_criteria.json", "uat_cases.json",
    "traceability_matrix.csv", "coverage_report.json",
]


def load_json(name):
    p = OUT / name
    if not p.exists():
        return None
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)


def main():
    errors = []
    warnings = []

    missing = [f for f in REQUIRED_FILES if not (OUT / f).exists()]
    if missing:
        errors.append(f"Missing file(s): {', '.join(missing)}")
        print("=== Pipeline verification ===")
        for e in errors:
            print(f"FAIL  {e}")
        sys.exit(1)

    try:
        brd = load_json("brd.json")
        br = load_json("business_rules.json")
        oq = load_json("open_questions.json")
        frd = load_json("frd.json")
        data_spec = load_json("data_spec.json")
        errcat = load_json("error_catalogue.json")
        ac = load_json("acceptance_criteria.json")
        uat = load_json("uat_cases.json")
        cov = load_json("coverage_report.json")
    except json.JSONDecodeError as e:
        print("=== Pipeline verification ===")
        print(f"FAIL  Invalid JSON: {e}")
        sys.exit(1)

    # ---- brd.json ----
    for key in ["document", "version", "objectives", "stakeholders", "roles",
                "in_scope", "out_of_scope", "assumptions", "open_question_ids",
                "requirements_functional", "requirements_nonfunctional"]:
        if key not in brd:
            errors.append(f"brd.json missing top-level key: {key}")

    all_reqs = brd.get("requirements_functional", []) + brd.get("requirements_nonfunctional", [])
    req_ids = [r["id"] for r in all_reqs]
    dupes = [x for x in set(req_ids) if req_ids.count(x) > 1]
    if dupes:
        errors.append(f"brd.json duplicate requirement id(s): {dupes}")
    all_req_id_set = set(req_ids)

    # ---- business_rules.json ----
    br_ids = set()
    for r in br:
        for field in ["rule_id", "statement", "rationale", "source_ids", "roles", "priority", "status"]:
            if field not in r:
                errors.append(f"business_rules.json {r.get('rule_id','?')} missing field: {field}")
        br_ids.add(r.get("rule_id"))
    if len(br_ids) != len(br):
        errors.append("business_rules.json has duplicate rule_id(s)")

    # ---- open_questions.json ----
    oq_ids = {q["id"] for q in oq}
    for qid in brd.get("open_question_ids", []):
        if qid not in oq_ids:
            errors.append(f"brd.json open_question_ids references {qid} not in open_questions.json")

    # brd.json source_ids -> business_rules.json (where they look like BR-xxx)
    for req in all_reqs:
        for sid in req.get("source_ids", []):
            if re.match(r"^BR-\d+$", sid) and sid not in br_ids:
                errors.append(f"brd.json {req['id']} source_ids references {sid} not in business_rules.json")

    # ---- frd.json ----
    frd_req_ids = set()
    official_ids = []
    for f in frd:
        for field in ["requirement_id", "official_id", "title", "statement", "epic", "source_ids",
                      "roles", "preconditions", "postconditions", "error_ids", "assumptions",
                      "open_question_ids", "priority", "priority_code", "status", "version"]:
            if field not in f:
                errors.append(f"frd.json {f.get('requirement_id','?')} missing field: {field}")
        frd_req_ids.add(f.get("requirement_id"))
        official_ids.append(f.get("official_id"))

    if len(frd_req_ids) != len(frd):
        errors.append("frd.json has duplicate requirement_id(s)")

    id_dupes = [x for x in set(official_ids) if official_ids.count(x) > 1]
    if id_dupes:
        errors.append(f"frd.json duplicate official_id: {id_dupes}")
    uncovered = all_req_id_set - set(official_ids)
    if uncovered:
        errors.append(f"BRD requirement(s) with no FRD entry: {sorted(uncovered)}")
    extra = set(official_ids) - all_req_id_set
    if extra:
        errors.append(f"frd.json official_id(s) not in brd.json: {sorted(extra)}")

    err_ids = {e.get("error_id") for e in errcat}
    for f in frd:
        for eid in f.get("error_ids") or []:
            if eid not in err_ids:
                errors.append(f"frd.json {f['requirement_id']} references error_id {eid} not in error_catalogue.json")
        for sid in f.get("source_ids") or []:
            if re.match(r"^BR-\d+$", sid) and sid not in br_ids:
                errors.append(f"frd.json {f['requirement_id']} source_ids references {sid} not in business_rules.json")

    # business rules with no downstream FRD requirement -- warning, not error
    # (could be a deliberate exclusion rule; a human/agent judgement call)
    covered_source_ids = set()
    for f in frd:
        covered_source_ids.update(sid for sid in (f.get("source_ids") or []) if sid.startswith("BR-"))
    uncovered_rules = br_ids - covered_source_ids
    if uncovered_rules:
        warnings.append(f"Business rule(s) with no downstream FRD requirement (verify intentional): {sorted(uncovered_rules)}")

    # ---- data_spec.json ----
    for key in ["fields", "state_transitions", "fixtures"]:
        if key not in data_spec:
            errors.append(f"data_spec.json missing top-level key: {key}")

    # ---- error_catalogue.json ----
    for e in errcat:
        for field in ["error_id", "name", "http_status", "user_message", "notes"]:
            if field not in e:
                errors.append(f"error_catalogue.json {e.get('error_id','?')} missing field: {field}")
        if e.get("http_status") is not None and not (100 <= e["http_status"] < 600):
            errors.append(f"error_catalogue.json {e['error_id']} implausible http_status {e['http_status']}")
    if len(err_ids) != len(errcat):
        errors.append("error_catalogue.json has duplicate error_id(s)")

    # ---- acceptance_criteria.json ----
    ac_ids = set()
    by_req = {}
    for a in ac:
        for field in ["ac_id", "requirement_id", "type", "fixture_ids", "given", "when", "then"]:
            if field not in a:
                errors.append(f"acceptance_criteria.json {a.get('ac_id','?')} missing field: {field}")
        ac_ids.add(a.get("ac_id"))
        if a.get("requirement_id") not in frd_req_ids:
            errors.append(f"acceptance_criteria.json {a.get('ac_id')} requirement_id not in frd.json")
        if a.get("type") not in ("positive", "negative", "boundary"):
            errors.append(f"acceptance_criteria.json {a.get('ac_id')} invalid type {a.get('type')}")
        by_req.setdefault(a.get("requirement_id"), []).append(a.get("type"))
    if len(ac_ids) != len(ac):
        errors.append("acceptance_criteria.json has duplicate ac_id(s)")

    for rid in frd_req_ids:
        types = by_req.get(rid, [])
        if "positive" not in types:
            errors.append(f"{rid} has no positive acceptance criterion")
        if "negative" not in types:
            errors.append(f"{rid} has no negative acceptance criterion")

    # ---- uat_cases.json ----
    uat_ids = set()
    covered_reqs = set()
    for u in uat:
        for field in ["uat_id", "title", "requirement_ids", "role", "preconditions", "steps"]:
            if field not in u:
                errors.append(f"uat_cases.json {u.get('uat_id','?')} missing field: {field}")
        uat_ids.add(u.get("uat_id"))
        for rid in u.get("requirement_ids") or []:
            covered_reqs.add(rid)
            if rid not in frd_req_ids:
                errors.append(f"uat_cases.json {u.get('uat_id')} requirement_ids references {rid} not in frd.json")
        for field in ["actual_result", "status", "evidence_ref", "tester", "date"]:
            val = u.get(field)
            if val not in (None, "", "null"):
                errors.append(f"uat_cases.json {u.get('uat_id')}.{field} should be blank pre-execution, got {val!r}")
    if len(uat_ids) != len(uat):
        errors.append("uat_cases.json has duplicate uat_id(s)")

    uncovered_fr = frd_req_ids - covered_reqs
    if uncovered_fr:
        errors.append(f"FRD requirement(s) with no UAT case: {sorted(uncovered_fr)}")

    # ---- traceability_matrix.csv ----
    with open(OUT / "traceability_matrix.csv", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    expected_header = ["rule_id", "requirement_id", "ac_id", "uat_id", "error_id", "roles", "status"]
    if not rows or rows[0] != expected_header:
        errors.append(f"traceability_matrix.csv header mismatch: got {rows[0] if rows else None}")
    else:
        matrix_rule_ids = {r[0] for r in rows[1:] if r and r[0]}
        missing_from_matrix = br_ids - matrix_rule_ids
        if missing_from_matrix:
            errors.append(f"business_rules.json rule(s) absent from traceability_matrix.csv entirely: {sorted(missing_from_matrix)}")

    # ---- coverage_report.json ----
    for key in ["status", "counts", "acceptance_rate", "issues"]:
        if key not in cov:
            errors.append(f"coverage_report.json missing key: {key}")
    if cov.get("status") == "PASS" and cov.get("issues"):
        errors.append("coverage_report.json status is PASS but issues[] is non-empty")
    if cov.get("status") == "FAIL" and not cov.get("issues"):
        errors.append("coverage_report.json status is FAIL but issues[] is empty")

    print("=== Pipeline verification ===")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")

    if errors:
        print(f"\n{len(errors)} check(s) failed.")
        sys.exit(1)

    print("\nAll structural and referential-integrity checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
