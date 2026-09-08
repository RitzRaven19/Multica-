FUNCTIONAL / SOFTWARE REQUIREMENTS SPECIFICATION
Online Banking Simulation — v1
Status: DRAFT (agent-generated, pending human review/approval)
Source inputs: BRD_online_banking_v1.md (F1–F8, NF1–NF5), SRS_template.txt

1. Introduction
This FRD elaborates the functional requirements F1–F8 and non-functional requirements NF1–NF5 from BRD_online_banking_v1.md into implementation-ready specifications for Architecture/Development (Mohit & Team).

2. Overall Description
2.1 Product Perspective
Standalone web simulation with two roles (Customer, Bank operations), a synthetic ledger, and no external payment or identity-verification integrations.
2.2 Product Functions
Onboarding + KYC review, account activation, authentication, money transfer/receive, statement view/download, audit logging.
2.3 Constraints
No real Aadhaar/PAN verification (format check only, per BR-002). No real money movement (BR-006). No beneficiary management, notifications, or service requests in v1 (out of scope per scope_agreement.md).

3. System Features
3.1 Description
Eight features map 1:1 to BRD functional requirements F1–F8.
3.2 Functional Requirements (detailed)

FR-1 (traces F1 — Customer Onboarding with KYC)
Input: full name, synthetic Aadhaar (12-digit numeric format), synthetic PAN (5 letters + 4 digits + 1 letter format).
Processing: system validates both fields against format regex only; no external verification call is made (BR-002).
Output: KYC record created with status PENDING_REVIEW; account created with status UNACTIVATED.
Error handling: malformed Aadhaar/PAN is rejected with a field-level format error before submission.

FR-2 (traces F2 — Account Onboarding and Activation)
Input: Bank operations selects a PENDING_REVIEW KYC record.
Processing: Bank operations approves (account → ACTIVATED) or rejects (account → REJECTED, reason required).
Output: Account status change is written to the audit trail (BR-007).

FR-3 (traces F3 — Login)
Input: username/email + password.
Processing: system authenticates credentials and resolves role (Customer or Bank operations); a Customer session is scoped to their own account IDs only (NF1).
Output: session token; role-appropriate landing view.

FR-4 (traces F4 — Logout)
Input: authenticated session.
Processing: session token invalidated server-side.
Output: user returned to unauthenticated state.

FR-5 (traces F5 — Money Transfer)
Preconditions: source account status = ACTIVATED (BR-003); actor role = Customer and owns the source account; actor role ≠ Bank operations (BR-005).
Input: source account, destination account, amount.
Processing: system debits source, credits destination in a single atomic operation; balance must not go negative (NF4, pending OQ-002/OQ-003).
Output: transaction record on both accounts; audit trail entry (BR-007).

FR-6 (traces F6 — Money Receive)
Processing: receiving account balance is credited as the counterpart of FR-5's atomic transfer; no separate "accept" action exists in v1.
Output: transaction record visible in the receiving Customer's statement (F7).

FR-7 (traces F7 — Statement View)
Input: account ID, optional date range.
Processing: Customer may only query accounts they own; Bank operations may query any account (BR-008, NF1).
Output: chronological transaction list (transfers in/out, balance after each entry).

FR-8 (traces F8 — Statement Download)
Input: account ID, optional date range (same access rule as FR-7).
Processing: statement is rendered to a durable file (e.g., CSV or PDF).
Output: downloadable file; download event is optionally logged (see NF2).

4. Requirements
4.1–4.3 Organizational / Business / User
Organizational: two personas only (Customer, Bank operations) in v1; no admin/superuser role defined yet.
Business: all rules per BRD Section 6 (BR-001–BR-008) apply unconditionally.
User: Customer-facing flows (FR-1, FR-3–FR-5, FR-7, FR-8) should require no banking-domain training to complete.

4.4 External Interfaces
None in v1. Aadhaar/PAN format validation is local logic, not an external identity-verification API call (BR-002).

4.5 System Features
See Section 3.2 (FR-1 through FR-8).

4.6 Performance
No hard SLA defined for v1 (simulation/student project). Suggested target: core actions (login, transfer, statement view) complete within 2 seconds under single-user test load — informal, not contractually binding.

4.7 Acceptance Criteria
Each FR-1–FR-8 is acceptance-tested via a corresponding UAT case in UAT_online_banking_v1.md; a feature is accepted only when its linked UAT case(s) pass and its audit trail entry (where applicable) is verified.

4.8 Database Requirements
Minimum entities: Customer, Account (status: UNACTIVATED/ACTIVATED/REJECTED/FROZEN), KYCRecord (status: PENDING_REVIEW/APPROVED/REJECTED), Transaction, AuditLogEntry. Referential integrity: a Transaction must reference two existing Accounts; an AuditLogEntry must reference an actor and an entity.

4.9 Design Constraints
Must support BR-004 (freeze blocks transfers) and BR-005 (Bank operations cannot transfer) at the authorization layer, not just the UI layer.

4.12 System Attributes
Auditability (NF2), role-based access control (NF1), testability (NF3) are first-class attributes, not add-ons — every write path must produce an audit entry and be reachable by an automated test.

5. Other Requirements
Open items inherited from BRD Section 9 (OQ-001–OQ-004) are not yet resolved; NF4 (non-negative balance) and any transfer cap are provisional pending OQ-002/OQ-003.
