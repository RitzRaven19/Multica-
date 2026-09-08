# Online Banking Simulation — Group 2 (Business Analysis)

End-to-end student SDLC project. This repo holds Group 2's slice: a three-agent
pipeline that turns `charter.md` + `scope_agreement.md` into an approved BRD,
FRD, and UAT plan — as machine-readable JSON/CSV, human-readable `.docx`, and
a traceability chain that's actually checked, not just claimed.

## Pipeline

```
charter.md + scope_agreement.md
        |
        v
   brd-agent  -->  raw/  -->  HUMAN REVIEW  -->  approved/
        |
        v
   frd-agent  -->  raw/  -->  HUMAN REVIEW  -->  approved/
        |
        v
 uat-generator -->  raw/  -->  HUMAN REVIEW  -->  approved/
        |
        v
      shared_outputs/  -->  CI verification  -->  Groups 3, 4, 5
```

Each agent reads **only** the `approved/` output of the stage before it —
never `raw/`. `uat-generator` is the join point: it's the only stage that
sees all five approved files from both prior stages at once, which makes it
the only place the full chain (business rule → requirement → criterion →
test case → error) can actually be cross-checked.

The three agents run in [Multica](https://multica.ai), workspace **Online
Banking BA**, one per runtime:

| Agent | Runtime | Reads | Writes |
|---|---|---|---|
| `brd-agent` | Claude | `charter.md`, `scope_agreement.md`, `BRD_template.txt` | `brd.json`, `business_rules.json`, `open_questions.json`, `BRD.md`, `BRD.docx` |
| `frd-agent` | OpenCode | `approved/brd.json`, `approved/business_rules.json`, `SRS_template.txt` | `frd.json`, `data_spec.json`, `error_catalogue.json`, `FRD.docx` |
| `uat-generator` | Codex | all 5 approved files above | `acceptance_criteria.json`, `uat_cases.json`, `traceability_matrix.csv`, `coverage_report.json`, `UAT.docx` |

Each agent's full task spec — schemas, required fields, the rules above —
lives in a bound Multica **Skill** (`brd-agent-skill`, `frd-agent-skill`,
`uat-generator-skill`), not pasted into the agent's `instructions` field.
That's the platform's own convention: instructions own per-turn workflow,
skills own the durable domain contract.

### Each agent generates its own `.docx`

`brd-agent`, `frd-agent`, and `uat-generator` each run a small Python script
(`render_*_docx.py`, attached as an issue input) at the end of their own run,
converting the JSON/Markdown they just wrote into a Word document — and
verify the file actually exists before delivering it. Nothing downstream
regenerates these independently, so the `.docx` can never drift from what was
actually approved.

## Schemas

Fixed field-for-field in each agent's bound skill. The one non-obvious rule:
every `business_rules.json` entry has a `type` — `"requirement-generating"`
or `"exclusion"`. A rule like "beneficiary management is out of scope for v1"
is an **exclusion**: it correctly has no downstream FRD requirement, and
`uat-generator` lists it in `coverage_report.json`'s `excluded_rules[]`
instead of flagging it as a gap. Everything else is expected to trace all the
way to a test case.

## Repo layout

```
shared_outputs/     the 11 approved deliverables + 3 .docx (what Groups 3/4/5 consume)
scripts/
  verify_pipeline.py   CI gate: schema + referential-integrity checks over shared_outputs/
  render_docx.py       manual fallback renderer (the agents now self-generate their own
                        .docx; this exists for re-rendering shared_outputs/ by hand if needed)
.github/workflows/
  verify-docs.yml      runs verify_pipeline.py on every push touching shared_outputs/,
                        opens a GitHub issue on failure, renders .docx as build artifacts
presentations/       (Group 2 deliverable, not yet populated)
```

`ba-artifacts/` (outside this repo, in the user's home directory) holds the
working `raw/` → `approved/` staging area and the two templates
(`BRD_template.txt`, `SRS_template.txt`) — that's where the human-review gate
actually happens before anything lands in `shared_outputs/`.

## Re-running a stage

Each agent only runs when a Multica issue is assigned to it — creating the
issue with the right attachments is what triggers it:

```bash
multica issue create --title "..." \
  --assignee-id <agent-id> \
  --attachment <input-file> [--attachment <input-file> ...] \
  --allow-external-file
```

Poll `multica issue runs <issue-key> --output json` until `status` leaves
`running`, then pull the agent's delivered files from its attachment list (or
its local workdir under `~/multica_workspaces/`). Move reviewed output into
`ba-artifacts/approved/`, copy into `shared_outputs/`, then commit and push —
CI re-verifies automatically.

## Known open questions

Carried forward verbatim from `scope_agreement.md`, unresolved by design
rather than guessed at:

- **OQ-001** — who executes UAT?
- **OQ-002** — minimum account balance?
- **OQ-003** — daily transfer cap?
- **OQ-004** — is the `data-testid` UI test-automation convention confirmed?

`FR-005`'s boundary test cases already cover both limits with the threshold
left as a named placeholder (`MIN_BALANCE`, `DAILY_TRANSFER_CAP`), so
resolving OQ-002/OQ-003 later is a value substitution, not a redesign.

## Handoff (Groups 3, 4, 5)

Per the Group 2 spec: Group 3 (build) needs `frd.json`, `data_spec.json`,
`error_catalogue.json` and must implement `error_catalogue.json`'s
`user_message` text exactly as written. Group 4 (test) needs
`acceptance_criteria.json`, `uat_cases.json`, and asserts against the error
catalogue literally. Group 5 (defect RCA) uses everything as a lookup index
via `traceability_matrix.csv`.
