BUSINESS REQUIREMENTS DOCUMENT
Online Banking Simulation — v1
Status: DRAFT (agent-generated, pending human review/approval)
Source inputs: charter.md, scope_agreement.md (v1.0)

1. Introduction
1.1 Purpose
This BRD defines the business requirements for v1 of the Online Banking Simulation, translating the approved scope agreement into requirements that can be designed, built, tested, and traced through to defect resolution.
1.2 Audience
Business Analysis (Ritu & Team), Architecture/Development (Mohit & Team), QA/Testing (Mandeep & Team), Defect RCA (Adiba & Team).
1.3 References
charter.md; scope_agreement.md v1.0; BRD_template.txt.
1.4 Acronyms and Glossary
KYC — Know Your Customer. PAN — Permanent Account Number (India, format-checked only in v1). Aadhaar — Indian identity number (format-checked only in v1). UAT — User Acceptance Testing.

2. Project Drivers
2.1 Business Problem
Customers expect secure digital access to core banking functions. A student-built simulation must demonstrate a traceable path from approved business rule to evidence record, not just a working UI.
2.2 Business Objectives
Deliver a coherent v1 banking simulation covering onboarding, login, transfers, and statements; demonstrate role-based, auditable journeys; produce reviewable, schema-consistent, human-approved artifacts at each SDLC stage.
2.3 Stakeholders
Customer (end user, synthetic identity). Bank operations (reviews KYC, manages account state). Business Analysis persona (Ritu & Team) — owns this BRD. Architecture/Dev persona (Mohit & Team) — consumes this BRD. QA persona (Mandeep & Team) — derives UAT from this BRD. Defect RCA persona (Adiba & Team) — triages against this BRD's business rules.

3. Constraints, Assumptions and Dependencies
Constraints: No real KYC verification (Aadhaar/PAN are format-checked only, mocked); no real money movement (synthetic only).
Assumptions: Test data is synthetic and does not represent real identities or accounts. UAT execution owner is not yet confirmed (see OQ-001).
Dependencies: Account activation depends on KYC review by Bank operations. Statement download depends on statement view being available.

4. Current State
No existing system. This is a greenfield v1 build with no legacy data or process to migrate.

5. Scope of Work
5.1 In Scope
1. Customer onboarding with KYC (Aadhaar, PAN — format check only, mocked)
2. Account onboarding and activation
3. Login
4. Logout
5. Money transfer
6. Money receive
7. Statement view
8. Statement download

5.2 Out of Scope
Beneficiary management, notifications, service requests (not on v1 build list). Real Aadhaar/PAN verification (format check only). Real money movement (synthetic only, no actual funds).

5.3 Roles
Customer — registers, completes KYC, logs in, transfers money, views/downloads statements. Cannot review KYC or freeze accounts.
Bank operations — reviews KYC submissions, activates/freezes accounts, views audit trail. Cannot initiate transfers.

6. Business Rules
BR-001: An account cannot be activated until KYC (Aadhaar + PAN) passes format validation.
BR-002: Aadhaar and PAN values are validated for format only in v1; no external/real verification is performed.
BR-003: A Customer cannot transfer money from an account that is not in an Activated state.
BR-004: A Bank operations user can freeze an Activated account, which blocks further transfers until unfrozen.
BR-005: A Bank operations user cannot initiate, approve, or reverse a money transfer.
BR-006: All money movement is synthetic; no integration with real payment rails exists in v1.
BR-007: Every state change (KYC review, activation, freeze, transfer, login/logout) must be recorded in an auditable trail visible to Bank operations.
BR-008: A Customer can only view and download statements for accounts they own.

7. Requirements
7.1 Requirements Organisation
Functional requirements are grouped by the eight in-scope capabilities (Section 5.1) and numbered F1–F8. Non-functional requirements are numbered NF1+.
7.2 Priority Key
1 = Must, 2 = Should, 3 = Could, F = Future, BP = Business Process

7.3 Functional Requirements
F1 (1, BP) — Customer Onboarding with KYC: The system shall allow a Customer to register with a synthetic identity and submit Aadhaar and PAN values for format validation (BR-001, BR-002).
F2 (1, BP) — Account Onboarding and Activation: The system shall allow Bank operations to review a submitted KYC record and activate or reject the associated account (BR-001, BR-007).
F3 (1) — Login: The system shall allow a Customer or Bank operations user to authenticate with role-appropriate credentials and receive role-scoped access (BR-007).
F4 (1) — Logout: The system shall allow an authenticated user to terminate their session (BR-007).
F5 (1, BP) — Money Transfer: The system shall allow a Customer to transfer synthetic funds from their own Activated account to another account (BR-003, BR-005, BR-006).
F6 (1) — Money Receive: The system shall credit a receiving account's synthetic balance when a transfer targeting it completes (BR-006).
F7 (1) — Statement View: The system shall allow a Customer to view a transaction statement for accounts they own, and allow Bank operations to view any account's statement for audit purposes (BR-008).
F8 (2) — Statement Download: The system shall allow a Customer to download a statement for an account they own in a durable file format (BR-008).

7.4 Non-Functional Requirements
NF1 (1) — Security: Role-based access control shall prevent a Customer from accessing another Customer's accounts or Bank operations functions.
NF2 (1) — Auditability: Every write action (BR-007) shall be logged with actor, timestamp, and before/after state.
NF3 (2) — Testability: Every functional requirement (F1–F8) shall have at least one traceable UAT test case.
NF4 (2) — Data integrity: Synthetic account balances shall never go negative as a result of a transfer (subject to OQ-002/OQ-003 resolution).
NF5 (3) — Accessibility: Core Customer journeys (F1, F3, F5, F7, F8) should meet basic keyboard-navigable, screen-reader-friendly interaction patterns.

8. Business Implementation Requirements
Bank operations users require a review queue for pending KYC submissions (supports F2). Audit trail (NF2) must be queryable by Bank operations without direct database access.

9. Issues
OQ-001: Who executes UAT? (owner unresolved — see scope_agreement.md)
OQ-002: What is the minimum balance policy, if any?
OQ-003: Is there a daily transfer cap, and if so, what value?
OQ-004: Is the data-testid convention for UI test automation confirmed?

10. Handover
This BRD is handed to Architecture/Development (Mohit & Team) for technical design, and to QA (Mandeep & Team) as the basis for the FRD and UAT plan. Open issues (Section 9) should be resolved or explicitly accepted as risks before design sign-off.
