**Business Requirements Document — Online Banking Simulation v1**
Version: 0.1.0-DRAFT | Status: **DRAFT — pending human approval**

## 1. Introduction

### 1.1 Purpose
This document defines the business requirements for v1 of the Online Banking Application student project: a synthetic banking simulation plus a traceable, agent-driven SDLC. It is produced by brd-agent from `charter.md` and `scope_agreement.md` only, and is a draft pending human review and approval.

### 1.2 Audience
Business Analysis (Ritu & Team), Architecture/Development (Mohit & Team), QA & Testing (Mandeep & Team), Defect Root-Cause Analysis (Adiba & Team), and downstream agents in the Group 2 SDLC pipeline (technical design/coding, system-test/automation, defect root-cause analysis).

### 1.3 References
- `charter.md` — project charter (problem statement, objectives).
- `scope_agreement.md` v1.0 DRAFT — in-scope/out-of-scope items, roles, open questions.
- `BRD_template.txt` — section structure used for this document.

### 1.4 Acronyms and Glossary
| Term | Meaning |
|---|---|
| BRD | Business Requirements Document |
| KYC | Know Your Customer |
| PAN | Permanent Account Number (India tax ID) |
| Aadhaar | Indian national identity number |
| UAT | User Acceptance Testing |
| SDLC | Software Development Life Cycle |
| RCA | Root-Cause Analysis |
| F*, NF* | Functional / Non-Functional requirement IDs |
| BR-xxx | Business Rule ID |
| OQ-xxx | Open Question ID |

## 2. Project Drivers

### 2.1 Business Problem
Customers expect secure digital access to onboarding, accounts, beneficiaries, transfers, statements, notifications, and service requests. Building even a simplified version requires coordinated business analysis, architecture, engineering, testing, evidence management, and defect triage. Student projects often treat these as isolated activities, causing ambiguous requirements, untestable designs, weak handoffs, and disagreement over whether failures are defects or new requests. This project asks four groups to build both a banking simulation and specialized agents that support a traceable SDLC, so that an approved business rule can be shown to become a requirement, design element, implementation, test, defect decision, and evidence record end to end.

### 2.2 Business Objectives
1. Deliver a coherent banking simulation using synthetic identities, accounts, balances, beneficiaries, and payments.
2. Demonstrate customer and bank-operations' journeys with role-based access and auditable state changes.
3. Build four agent families: BRD; technical design/coding/unit testing; system-test/automation; and defect root-cause analysis.
4. Make agent output reviewable, reproducible, schema-valid, source-linked, and subject to human approval.
5. Use security, privacy, accessibility, reliability, and testability as acceptance conditions — not optional polish.
6. Practice governance: baselines, versioning, change control, traceability, evidence, risk management, and retrospectives.
7. Leverage AI agents to perform tasks and drive results, with human validation of agent-produced results.

### 2.3 Stakeholders
| Stakeholder | Persona |
|---|---|
| Business Analysis | Ritu & Team |
| Architecture & Build/Unit Test (Development) | Mohit & Team |
| Quality Assurance & Testing | Mandeep & Team |
| Defect Root-Cause Analysis | Adiba & Team |
| Customer | End user of the banking simulation |
| Bank operations | End user / internal staff role |

## 3. Constraints, Assumptions and Dependencies
**Constraints:** all identities, accounts, and money movement are synthetic (BR-003); KYC checks are format-only, not real verification (BR-001).

**Assumptions:**
- All identities, accounts, balances, and transactions are synthetic/test data; no real customer PII or real financial rails are involved.
- KYC document checks (Aadhaar, PAN) validate format only and do not call external government verification services.
- Values for minimum balance and daily transfer cap are not yet defined (OQ-002, OQ-003) and are excluded from this BRD's requirements until resolved.
- The UAT-executing party is not yet defined (OQ-001); acceptance testing is assumed to occur but the responsible party is pending confirmation.
- The data-testid selector convention for test automation is not yet confirmed (OQ-004) and is assumed to be settled before detailed system-test design begins.

**Dependencies:** this BRD is the sole input (via approval) to the next SDLC stage (technical design/coding/unit-test agent); it depends only on `charter.md` and `scope_agreement.md` — there is no `approved/` predecessor for this stage.

## 4. Current State
Greenfield build. There is no pre-existing online-banking system for this student project; v1 is a new synthetic simulation built from the charter and scope agreement.

## 5. Scope of Work

### 5.1 In Scope
| # | Item | Roles |
|---|---|---|
| 1 | Customer on-boarding with KYC (Aadhaar, PAN) | Customer, Bank operations |
| 2 | Account on-boarding and activation | Customer, Bank operations |
| 3 | Login | Customer, Bank operations |
| 4 | Logout | Customer, Bank operations |
| 5 | Money transfer | Customer |
| 6 | Money receive | Customer |
| 7 | Statement view | Customer, Bank operations |
| 8 | Statement download | Customer |

### 5.2 Out of Scope
| Item | Reason |
|---|---|
| Beneficiary management, notifications, service requests | Not on build list for v1 |
| Real Aadhaar/PAN verification | Format check only; verification is mocked |
| Real money movement | Synthetic only |

### 5.3 Roles
| Role | Description |
|---|---|
| Customer | Registers, completes KYC, logs in, transfers funds, and views/downloads statements. |
| Bank operations | Reviews KYC, activates/freezes accounts, views the audit trail; cannot transfer funds. |

## 6. Business Rules
| Rule ID | Statement | Priority | Roles | Source |
|---|---|---|---|---|
| BR-001 | Customer onboarding requires KYC using Aadhaar and PAN identity documents, validated by format only; no real government verification is performed. | Must | Customer, Bank operations | SA-1, SA-OOS-2 |
| BR-002 | An account must be reviewed and activated by Bank operations before it can be used for transactions. | Must | Customer, Bank operations | SA-2, SA-ROLE-OPS |
| BR-003 | All money transfers and receipts are synthetic; no integration with real payment rails or real fund movement is performed. | Must | Customer | SA-OOS-3 |
| BR-004 | The Customer role may register, complete KYC, log in, transfer funds, and view/download statements. | Must | Customer | SA-ROLE-CUST |
| BR-005 | The Bank operations role may review KYC, activate or freeze accounts, and view the audit trail, but may not initiate money transfers. | Must | Bank operations | SA-ROLE-OPS |
| BR-006 | Beneficiary management, notifications, and service requests are excluded from the v1 build. | Must | — | SA-OOS-1 |
| BR-007 | All account, KYC, and transfer state changes must be recorded with actor, action, and timestamp to support the Bank operations audit trail and defect root-cause analysis. | Must | Bank operations | SA-ROLE-OPS, CH-OBJ-2, CH-OBJ-6 |
| BR-008 | Agent-produced SDLC artifacts must be reviewable, reproducible, schema-valid, source-linked, and subject to human approval before being treated as approved. | Must | — | CH-OBJ-4 |
| BR-009 | Login and logout must be available to both Customer and Bank operations users, with role-based access control enforced. | Must | Customer, Bank operations | SA-3, SA-4, CH-OBJ-2 |
| BR-010 | Statement view is available to Customer and Bank operations; statement download is available to Customer only, in v1. | Must | Customer, Bank operations | SA-7, SA-8, SA-ROLE-CUST, SA-ROLE-OPS |
| BR-011 | Security, privacy, accessibility, reliability, and testability apply as acceptance conditions to every in-scope Customer and Bank operations journey. | Must | — | CH-OBJ-5 |

All rules are **status: Draft**, pending human approval. Full detail (rationale) is in `business_rules.json`.

## 7. Requirements

### 7.1 Requirements Organisation
Functional requirements are numbered F1–F10; non-functional requirements are numbered NF1–NF7. Each requirement lists its priority and the source_ids (business rules and/or scope_agreement.md items) it traces to. Full machine-readable detail is in `brd.json`.

### 7.2 Priority Key
1 = Must, 2 = Should, 3 = Could, F = Future, BP = Business Process. All requirements below are priority 1 (Must), reflecting that every item in section 5.1 is in scope for v1.

### 7.3 Functional Requirements
| ID | Statement | Priority | Source |
|---|---|---|---|
| F1 | The system shall allow a Customer to register and complete KYC using Aadhaar and PAN identity documents, with format validation only (mocked verification). | 1 | SA-1, BR-001 |
| F2 | The system shall allow a Customer to onboard an account, and shall allow Bank operations to review and activate it before the account can be used. | 1 | SA-2, BR-002, SA-ROLE-OPS |
| F3 | The system shall allow Customer and Bank operations users to log in, with role-based access control applied. | 1 | SA-3, BR-009 |
| F4 | The system shall allow Customer and Bank operations users to log out, terminating their authenticated session. | 1 | SA-4, BR-009 |
| F5 | The system shall allow a Customer to initiate a synthetic money transfer to another account. | 1 | SA-5, BR-003, BR-004 |
| F6 | The system shall allow a Customer's account to receive a synthetic money transfer. | 1 | SA-6, BR-003 |
| F7 | The system shall allow Customer and Bank operations users to view account statements according to their role permissions. | 1 | SA-7, BR-010 |
| F8 | The system shall allow a Customer to download their account statement. | 1 | SA-8, BR-010, SA-ROLE-CUST |
| F9 | The system shall allow Bank operations to view the audit trail of account and KYC state changes. | 1 | SA-ROLE-OPS, BR-007 |
| F10 | The system shall prevent Bank operations users from initiating money transfers. | 1 | SA-ROLE-OPS, BR-005 |

### 7.4 Non-Functional Requirements
| ID | Statement | Priority | Source |
|---|---|---|---|
| NF1 | The system shall require authentication for every Customer and Bank operations action, protecting account and identity data appropriate to a banking simulation. | 1 | BR-011, CH-OBJ-5, BR-009 |
| NF2 | The system shall treat KYC and account data as sensitive and restrict access to it by role. | 1 | BR-011, SA-ROLE-OPS |
| NF3 | Customer- and Bank-operations-facing interfaces shall meet accessibility requirements as an acceptance condition. | 1 | BR-011, CH-OBJ-5 |
| NF4 | The system shall reliably persist account, KYC, and transaction state changes without data loss. | 1 | BR-011, CH-OBJ-5 |
| NF5 | The system shall be built to be testable, including deterministic synthetic data and stable UI selectors for test automation. | 1 | BR-011, OQ-004 |
| NF6 | All account, KYC, and transfer state changes shall be recorded with actor, action, and timestamp to support audit-trail viewing and defect root-cause analysis. | 1 | CH-OBJ-2, CH-OBJ-6, BR-007 |
| NF7 | Every approved business rule shall be traceable through requirement, design, implementation, test, and evidence record, and all agent-produced artifacts shall be reviewable, reproducible, schema-valid, source-linked, and subject to human approval. | 1 | CH-PROB-2, CH-OBJ-4, CH-OBJ-6, BR-008 |

## 8. Business Implementation Requirements
Not yet defined. Implementation-level decisions (data model, screen flows, API/service boundaries, environment/config) are owned by the technical design/coding stage and are out of scope for this BRD; they must trace back to the business rules and requirements in sections 6–7.

## 9. Issues
Open questions carried forward verbatim from `scope_agreement.md` — no answers are assumed:

| ID | Question | Owner | Blocks |
|---|---|---|---|
| OQ-001 | Who executes UAT? | TBD | Acceptance sign-off / UAT execution for all in-scope journeys |
| OQ-002 | Minimum balance? | TBD | Account activation and money-transfer validation rules (minimum balance enforcement) — F2, F5 |
| OQ-003 | Daily cap? | TBD | Money-transfer limit business rule and validation — F5 |
| OQ-004 | data-testid convention confirmed? | TBD | System-test/automation agent's selector strategy — NF5 (testability) |

## 10. Handover
This BRD, `brd.json`, `business_rules.json`, and `open_questions.json` are all **DRAFT**, pending human approval — nothing in this package should be treated as approved. Once approved, this package is the input to the next Group 2 SDLC stage (technical design/coding/unit-test agent). The four open questions above should be resolved, or explicitly deferred with owner and target date, before or during that handover.

---
*Source ID key: `SA-1`…`SA-8` = scope_agreement.md in-scope items 1–8; `SA-OOS-1`…`SA-OOS-3` = scope_agreement.md out-of-scope items 1–3; `SA-ROLE-CUST` / `SA-ROLE-OPS` = scope_agreement.md role definitions; `CH-PROB-1`/`CH-PROB-2` = charter.md §1.1 problem statement paragraphs 1–2; `CH-OBJ-1`…`CH-OBJ-7` = charter.md §1.2 objectives 1–7; `OQ-xxx` = open_questions.json; `BR-xxx` = business_rules.json.*
