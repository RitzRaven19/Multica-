Peer review of the six Group 2 submissions (Abhinav, Anil_Pradhan, Kartik_Sharma, Mrunmayee, Nibedita, Ritu_Dey) against the approved ground truth (`brd.json`, `business_rules.json` — 20 rules BR-001..BR-020, `open_questions.json` — OQ-001..OQ-004, `coverage_report.json`). Each document scored 0–5 on five rubric axes (see skill spec), total /25.

## BRD

| Contributor | Coverage | Scope accuracy | Open questions | Traceability | Clarity | Total /25 |
|---|---|---|---|---|---|---|
| **Ritu_Dey** | 4 | 5 | 5 | 5 | 4 | **23** |
| Mrunmayee | 4 | 5 | 4 | 3 | 4 | 20 |
| Kartik_Sharma | 3 | 5 | 5 | 4 | 4 | 21 |
| Nibedita | 3 | 5 | 5 | 3 | 4 | 20 |
| Abhinav | 2 | 4 | 4 | 3 | 3 | 16 |
| Anil_Pradhan | 0 | 1 | 1 | 2 | 1 | 5 |

**Winner: Ritu_Dey.** Her `BRD.docx` states 10 explicit `BR-XXX` business rules kept as a distinct layer from the `F#`/`NF#` requirement layer — the only submission besides Kartik's that preserves this separation, which is what lets a downstream FRD cite a rule instead of a requirement. Between the BR layer and the F/NF layer she states or clearly implies 19 of the 20 approved rules, including exact matches for the two hardest ones: BR-007 ("Only the Customer role may initiate a money transfer... Bank operations is explicitly barred") appears as her BR-005 + BR-004 + F12 ("System prevents Bank operations from initiating money transfers"), and BR-010 (statement view for *both* roles) appears as her BR-007. Scope accuracy is perfect — beneficiary management, notifications, service requests, real Aadhaar/PAN verification, and real money movement are all explicitly excluded. OQ-001 through OQ-004 are carried forward with wording nearly identical to the approved file, and her BR-010 explicitly states minimum balance and daily cap are "not yet defined and must be confirmed" rather than guessing values.

**Runner-up:** Mrunmayee's BRD is the most exhaustive — one requirement per in-scope action across both roles, covering essentially the full surface — but it reuses the ID `BR-001` for two different meanings (a functional-requirement numbering scheme in §8.3 and an unrelated business-rule numbering scheme in §8.4), which undermines traceability, and it omits an explicit "Bank operations cannot transfer" rule and a "Bank operations can view statements" rule.

## FRD

| Contributor | Req. fidelity | Coverage | Data/error specificity | Traceability | Clarity | Total /25 |
|---|---|---|---|---|---|---|
| **Ritu_Dey** | 5 | 4 | 5 | 5 | 4 | **23** |
| Kartik_Sharma | 4 | 4 | 4 | 4 | 4 | 20 |
| Nibedita | 4 | 4 | 4 | 4 | 4 | 20 |
| Mrunmayee | 5 | 4 | 1 | 5 | 3 | 18 |
| Abhinav | 3 | 3 | 4 | 3 | 3 | 16 |
| Anil_Pradhan | 1 | 1 | 0 | 2 | 1 | 5 |

**Winner: Ritu_Dey.** Her FRD is the only one that handles the two open numeric boundaries (minimum balance, daily transfer cap) the way the ground truth intends: her data spec defines `minimum_balance` and `daily_transfer_cap` fields explicitly `Blocked by OQ-002`/`OQ-003`, and gives a below/at/above boundary-triple table keyed to the literal placeholders `MIN_BALANCE` and `DAILY_CAP` rather than any invented number. Her error catalogue (16 entries, e.g. `ERR-011 BELOW_MINIMUM_BALANCE`) is tied to those same placeholders. Combined with full entity state-transition diagrams (Account: PENDING→ACTIVE→FROZEN→CLOSED, etc.) and clean `SA-#`/`BR-#` source citations on every FR, this is the most implementation-ready FRD of the six.

**Runner-up:** Kartik_Sharma's FRD (FR-001 through FR-030) is comparably thorough — it is the only other submission whose Bank-operations permission list explicitly includes "view the audit trail" (FR-013), closing a gap that Nibedita's FRD leaves open — but it resolves the minimum-balance question implicitly (any transfer exceeding the raw balance is rejected) instead of flagging it as pending, and never addresses the daily-cap boundary at all.

## UAT

| Contributor | Coverage (+/-) | Traceability | Concreteness | Boundary handling | Exclusion awareness | Total /25 |
|---|---|---|---|---|---|---|
| **Ritu_Dey** | 5 | 5 | 4 | 5 | 5 | **24** |
| Nibedita | 5 | 5 | 5 | 4 | 5 | 24 |
| Kartik_Sharma | 5 | 5 | 5 | 3 | 5 | 23 |
| Abhinav | 4 | 4 | 4 | 2 | 4 | 18 |
| Mrunmayee | 1 | 5 | 3 | 1 | 5 | 15 |
| Anil_Pradhan | 1 | 3 | 2 | 0 | 0 | 6 |

**Winner: Ritu_Dey** (tie-broken against Nibedita on traceability, axis 4/5 — see note below). Her UAT is the only one that tests the minimum-balance and daily-cap boundaries as true placeholders with explicit below/at/above triples: `AC-005.41/.42/.43` test `MIN_BALANCE - 0.01`, `MIN_BALANCE`, `MIN_BALANCE + 0.01`, and `AC-005.44/.45/.46` do the same for `DAILY_TRANSFER_CAP` — never guessing a number, exactly matching the rubric's intent. It has 49 acceptance criteria and matching cases with a full `rule_id → requirement_id → ac_id → uat_id → error_id` traceability table, positive and negative cases for every FR, and correctly tests no out-of-scope feature. Notably, its self-reported coverage summary honestly flags "Rule BR-006 has no downstream requirement" rather than hiding the gap — the kind of transparency the rubric rewards.

**Closest competitor:** Nibedita's UAT (46 cases, 12 scenarios) is comparably strong and also correctly refuses to invent OQ-002/OQ-003 values (marking those cases "cannot be executed to a definitive pass/fail until decided"), plus has the single most explicit exclusion-awareness statement of any submission ("Out-of-scope features... are excluded and no acknowledgements are given as in-scope"). It scores identically to Ritu_Dey pre-tiebreak; per the rubric's tie-break rule this was resolved on traceability (axis 4), where Ritu_Dey's UAT carries a single unbroken ID chain from rule through error code that Nibedita's matrix does not quite match in granularity.

## A serious rubric violation worth flagging

**Anil_Pradhan's ATP explicitly writes test cases against three out-of-scope items**: UAT-004 "Beneficiary Management - Add Beneficiary" (BR-015, excluded), UAT-007 "Notification Delivery - Transfer Confirmation" (BR-016, excluded), and UAT-008 "Service Request - Submit Request" (BR-017, excluded). This traces back to his BRD/SRS, which lists Beneficiaries, Notifications, and Service Requests as in-scope "business capabilities" — a direct contradiction of the approved `brd.json` out-of-scope list. This is the single clearest exclusion-scope failure across all 18 documents and is why Anil_Pradhan ranks last in every category.

## Known gaps (no submission covered well)

- **Bank-operations statement viewing**: two of six FRDs (Kartik_Sharma, Mrunmayee) omit an explicit "Bank operations can view any customer's statement" requirement even though BR-010 grants it to both roles.
- **"Reproducible" as a distinct governance quality** (part of BR-019/approved objective #4) is folded into "schema-valid/source-linked" language in most submissions rather than stated as its own testable condition; only Mrunmayee's FRD (FR-022) states all five qualities verbatim.
- **KYC-before-account-opening sequencing** (BR-001's precise ordering) is implied by section order in every BRD but never stated as an explicit precedence rule ("KYC must complete before an account can exist") outside of Nibedita's and Kartik's FRDs.
- Genuinely correct boundary-placeholder testing (MIN_BALANCE/DAILY_TRANSFER_CAP as symbols, not numbers) appears fully only in Ritu_Dey's and, less rigorously, Nibedita's UAT — the other four either skip the daily-cap boundary entirely or implicitly resolve it to a specific value.

*This is a peer-review recommendation, not a final grade — status and picks should be treated accordingly.*
