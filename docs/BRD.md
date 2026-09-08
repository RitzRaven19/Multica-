# Business Requirements Document — Online Banking Simulation v1

**Status: DRAFT — pending human approval**

## 1. Introduction

### 1.1 Purpose
This document defines the business rules and requirements for the Online Banking Simulation v1, so that an approved business rule can be traced through requirement, design, implementation, test, and defect-decision records. It is derived from `charter.md` and `scope_agreement.md` using the section structure of `BRD_template.txt`.

### 1.2 Audience
Technical design/coding/unit-test agent, system-test/automation agent, defect root-cause-analysis agent, and human reviewers (Business Analysis, Architecture, QA, Defect RCA teams named in the charter).

### 1.3 References
- `charter.md` — Online Banking Application, end-to-end student project charter
- `scope_agreement.md` v1.0 (DRAFT) — Scope Agreement, Online Banking Simulation v1
- `BRD_template.txt` — required BRD section structure

### 1.4 Acronyms and Glossary
- **KYC** — Know Your Customer, identity-verification process
- **PAN** — Permanent Account Number (India tax ID)
- **Aadhaar** — Indian national identity number
- **UAT** — User Acceptance Testing
- **BR** — Business Rule
- **F** — Functional Requirement
- **NF** — Non-Functional Requirement
- **OQ** — Open Question
- **BP** — Business Process (priority tag; see 7.2)

## 2. Project Drivers

### 2.1 Business Problem
Customers expect secure digital access to onboarding, accounts, beneficiaries, transfers, statements, notifications, and service requests. Building even a simplified version requires coordinated business analysis, architecture, engineering, testing, evidence management, and defect triage. Student projects often treat these as isolated activities, causing ambiguous requirements, untestable designs, weak handoffs, and disagreement over whether failures are defects or new requests. (charter.md 1.1)

### 2.2 Business Objectives
- Deliver a coherent banking simulation using synthetic identities, accounts, balances, beneficiaries, and payments.
- Demonstrate customer and bank-operations journeys with role-based access and auditable state changes.
- Build four agent families: BRD; technical design/coding/unit testing; system-test/automation; and defect root-cause analysis.
- Make agent output reviewable, reproducible, schema-valid, source-linked, and subject to human approval.
- Use security, privacy, accessibility, reliability, and testability as acceptance conditions — not optional polish.
- Practice governance: baselines, versioning, change control, traceability, evidence, risk management, and retrospectives.
(charter.md 1.2)

### 2.3 Stakeholders
- Business Analysis persona — Ritu & Team (this BRD's authors)
- Architecture & Build and Unit Test (Development) persona — Mohit & Team
- Quality Assurance & Testing persona — Mandeep & Team
- Defect Root Cause Analysis persona — Adiba & Team
- End-user roles: Customer, Bank operations (see 5.3)

## 3. Constraints, Assumptions and Dependencies

**Constraints**
- Aadhaar/PAN verification is format-check only and mocked — no real government verification integration (scope_agreement.md, Out of scope).
- All money movement is synthetic only; no real funds are transferred (scope_agreement.md, Out of scope).
- Beneficiary management, notifications, and service requests are not on the v1 build list (scope_agreement.md, Out of scope).

**Assumptions**
- Only two roles exist in v1: Customer and Bank operations (scope_agreement.md, Roles).
- Identities, accounts, and balances are synthetic test data, not real customer data.

**Dependencies**
- This BRD depends on `charter.md` and `scope_agreement.md` as its sole source inputs.
- Downstream design, build, test, and defect-RCA agent work depends on this BRD and must not proceed past unresolved open questions (see Section 9) without human resolution.

## 4. Current State
Greenfield project — no pre-existing system. Online Banking Simulation v1 is a new build; there is no legacy system to migrate from or integrate with.

## 5. Scope of Work

### 5.1 In Scope
1. Customer on-boarding with KYC (Aadhaar, PAN) — Customer, Bank operations
2. Account on-boarding and activation — Customer, Bank operations
3. Login — Customer, Bank operations
4. Logout — Customer, Bank operations
5. Money transfer — Customer
6. Money receive — Customer
7. Statement view — Customer, Bank operations
8. Statement download — Customer

### 5.2 Out of Scope
- Beneficiary management, notifications, service requests — not on build list
- Real Aadhaar/PAN verification — format check only, mocked
- Real money movement — synthetic only

### 5.3 Roles
- **Customer** — registers, KYC, logs in, transfers, views/downloads statements
- **Bank operations** — reviews KYC, activates/freezes accounts, views audit trail, cannot transfer

## 6. Business Rules

| ID | Rule | Trace |
|---|---|---|
| BR-001 | KYC submissions (Aadhaar, PAN) are validated by format check only; no real government verification is performed. | Scope 5.1 item 1; Scope 5.2 (mocked verification) |
| BR-002 | Only the Bank operations role may review KYC submissions and activate or freeze accounts; the Customer role cannot self-activate or self-freeze its own account. | Scope 5.1 item 2; Scope 5.3 Roles |
| BR-003 | The Bank operations role cannot execute money transfers. | Scope 5.3 Roles; Scope 5.1 item 5 |
| BR-004 | All money movement is synthetic; no rule, screen, or integration may execute a real transfer of funds. | Scope 5.2 Out of scope |
| BR-005 | A Customer or Bank operations user must be logged in (authenticated session) before accessing account, transfer, or statement functions; logout terminates that session. | Scope 5.1 items 3, 4 |
| BR-006 | An account must be in an activated state before money transfer or money receive functionality is available on it. | Scope 5.1 items 2, 5, 6 |
| BR-007 | Statement download is available to the Customer role; statement view is available to both Customer and Bank operations roles. | Scope 5.1 items 7, 8; Scope 5.3 Roles |
| BR-008 | Money transfer must enforce a minimum account balance and a daily transfer cap; the specific threshold values are unresolved. | Scope 5.1 item 5; see OQ-002, OQ-003 in Section 9 |

## 7. Requirements

### 7.1 Requirements Organisation
Requirements are grouped by the in-scope capability areas listed in Section 5.1 (onboarding/KYC, account activation, login/logout, transfer, receive, statement view, statement download), and are traced to a scope-agreement item and/or a business rule from Section 6.

### 7.2 Priority Key
1 = Must, 2 = Should, 3 = Could, F = Future, BP = Business Process

### 7.3 Functional Requirements

| ID | Requirement | Priority | Trace |
|---|---|---|---|
| F1 | The Customer shall be able to submit on-boarding details including Aadhaar and PAN for KYC. | 1 | Scope 5.1 item 1 |
| F2 | The system shall perform a format-only validation of Aadhaar and PAN values submitted for KYC (mocked; no external verification call). | 1 | Scope 5.1 item 1; BR-001 |
| F3 | Bank operations shall review a submitted KYC record and approve or reject it. | BP | Scope 5.1 item 1; Scope 5.3 Roles; BR-002 |
| F4 | The system shall create an account on-boarding request upon KYC approval. | 1 | Scope 5.1 item 2 |
| F5 | Bank operations shall be able to activate or freeze a Customer account. | BP | Scope 5.1 item 2; Scope 5.3 Roles; BR-002 |
| F6 | The Customer shall be able to log in with registered credentials. | 1 | Scope 5.1 item 3 |
| F7 | Bank operations shall be able to log in with their credentials. | 1 | Scope 5.1 item 3; Scope 5.3 Roles |
| F8 | The system shall terminate the authenticated session when a Customer or Bank operations user logs out. | 1 | Scope 5.1 item 4; BR-005 |
| F9 | The Customer shall be able to initiate a money transfer from an activated account. | 1 | Scope 5.1 item 5; BR-003, BR-006 |
| F10 | The system shall reject a money transfer if the source account is not activated. | 1 | Scope 5.1 items 2, 5; BR-006 |
| F11 | The system shall credit a receiving account with a synthetic money-receive transaction. | 1 | Scope 5.1 item 6; BR-004 |
| F12 | The Customer shall be able to view an account statement (transaction history). | 1 | Scope 5.1 item 7 |
| F13 | Bank operations shall be able to view a Customer's account statement. | 1 | Scope 5.1 item 7; Scope 5.3 Roles |
| F14 | The Customer shall be able to download an account statement. | 1 | Scope 5.1 item 8; BR-007 |
| F15 | Bank operations shall be able to view an audit trail of KYC and account actions. | 1 | Scope 5.3 Roles |
| F16 | The system shall enforce a minimum balance and a daily transfer cap on money transfers; threshold values are pending resolution. | 2 | BR-008; see OQ-002, OQ-003 |

### 7.4 Non-Functional Requirements

| ID | Requirement | Priority | Trace |
|---|---|---|---|
| NF1 | Authentication credentials shall be stored and transmitted securely (e.g., hashed at rest, encrypted in transit). | 1 | charter.md 1.2 (security) |
| NF2 | KYC identifiers (Aadhaar, PAN) shall be treated as sensitive data with access restricted to authorized roles. | 1 | charter.md 1.2 (privacy); BR-002 |
| NF3 | The system shall enforce role-based access control consistent with the Customer and Bank operations role definitions. | 1 | charter.md 1.2; Scope 5.3 Roles |
| NF4 | KYC decisions, account activation/freeze actions, and transfers shall be recorded as auditable, traceable state changes (actor, action, timestamp). | 1 | charter.md 1.2 (auditable state changes) |
| NF5 | UI elements shall expose stable identifiers to support automated testing; the naming convention is pending confirmation. | 1 | charter.md 1.2 (testability); see OQ-004 |
| NF6 | Customer-facing journeys (onboarding, login, transfer, statement) shall meet accessibility standards as an acceptance condition, not optional polish. | 1 | charter.md 1.2 (accessibility) |
| NF7 | The system shall reliably record synthetic transfer and receive transactions without data loss. | 1 | charter.md 1.2 (reliability) |

## 8. Business Implementation Requirements
- All identities, accounts, balances, and transactions are synthetic test data; no production or real customer data migration is required.
- KYC verification must be implemented as a mocked, format-only check (no real Aadhaar/PAN verification integration) per Scope 5.2.
- No real payment rails or money-movement integration are to be implemented; transfer/receive must remain synthetic per BR-004.

## 9. Issues
The following open questions from `scope_agreement.md` are unresolved and are carried forward without an assumed answer. Downstream agents and reviewers should treat any requirement or business rule that depends on them (BR-008, F16, NF5) as provisional until resolved.

- **OQ-001**: Who executes UAT?
- **OQ-002**: What is the minimum account balance (referenced by BR-008, F16)?
- **OQ-003**: What is the daily transfer cap (referenced by BR-008, F16)?
- **OQ-004**: Is the data-testid convention confirmed (referenced by NF5)?

## 10. Handover
This BRD is a **DRAFT** and must not be treated as approved input for design, build, test, or defect-RCA work until a human explicitly approves it. Once approved, downstream agents should treat Sections 6 and 7 as the source of traceable business rules and requirements, and should flag any design or implementation decision that depends on an unresolved item in Section 9 rather than assuming a value.
