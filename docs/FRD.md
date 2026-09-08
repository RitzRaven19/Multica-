FUNCTIONAL REQUIREMENTS SPECIFICATION
Online Banking Simulation — v1
Status: DRAFT (agent-generated, pending human review/approval)
Source: BRD_online_banking_v1.md (v1), SRS_template.txt

## 1. Introduction

This FRD translates the approved BRD for Online Banking Simulation v1 into a Software Requirements Specification. Every FR-x traces to one or more BRD functional requirements (F1–F8) and the business rules (BR-001 through BR-008) cited by the BRD. Non-functional requirements NF1–NF5 are reflected as cross-cutting constraints in the relevant FR specs.

The eight in-scope capabilities from BRD Section 5.1 are:

1. Customer Onboarding with KYC
2. Account Onboarding and Activation
3. Login
4. Logout
5. Money Transfer
6. Money Receive
7. Statement View
8. Statement Download

Two roles exist (BRD Section 5.3):
- Customer — registers, completes KYC, logs in, transfers money, views/downloads statements. Cannot review KYC or freeze accounts.
- Bank operations — reviews KYC submissions, activates/freezes accounts, views audit trail. Cannot initiate transfers.

Open questions (BRD Section 9) that affect downstream design:
- OQ-002: Minimum balance policy, if any. Affects FR-5 (transfer validation) and NF-4 (data integrity).
- OQ-003: Daily transfer cap, if any. Affects FR-5.
- OQ-001: UAT execution owner unresolved. Affects NF-3 (testability).
- OQ-004: data-testid convention unresolved. Affects NF-5 (accessibility).

**No features beyond BRD Section 5.1 are introduced. Ambiguities are flagged, not resolved.**

## 2. Overall Description

### 2.1 Product Perspective

Online Banking Simulation v1 is a greenfield, synthetic-money simulation with no real payment rails, no real KYC verification, and no legacy data. It demonstrates a traceable path from approved business rule to evidence record.

### 2.2 Product Functions

| Function | FR Ref | BRD Ref | Description |
|---|---|---|---|
| Customer Onboarding with KYC | FR-1 | F1 | Register with synthetic identity, submit Aadhaar + PAN, format validation |
| Account Onboarding and Activation | FR-2 | F2 | Bank ops review KYC, activate or reject account |
| Login | FR-3 | F3 | Authenticate with role-appropriate credentials |
| Logout | FR-4 | F4 | Terminate active session |
| Money Transfer | FR-5 | F5 | Transfer synthetic funds from own Activated account |
| Money Receive | FR-6 | F6 | Credit receiving account on completed transfer |
| Statement View | FR-7 | F7 | View transaction statement (Customer: own; Bank ops: any) |
| Statement Download | FR-8 | F8 | Download statement in durable file format |

### 2.3 Constraints

- No real KYC verification (Aadhaar/PAN format-check only, mocked) — BR-001, BR-002
- No real money movement (synthetic only) — BR-006
- No beneficiary management, notifications, or service requests in v1
- Account activation depends on KYC review by Bank operations
- Statement download depends on statement view being available

## 3. System Features

### 3.1 Description

The system provides two user roles with role-scoped access. Customer-facing journeys are onboarding, login, transfer, and statements. Bank operations journeys are KYC review, activation, freeze, and audit trail viewing. All state changes are audit-logged.

### 3.2 Functional Requirements

#### FR-1: Customer Onboarding with KYC

**Traces to:** F1 (BRD §7.3) · BR-001, BR-002
**Priority:** 1 (Must) · Business Process

**Input:**
- Customer name (string)
- Email address (string, valid format)
- Phone number (string, valid format)
- Aadhaar number (string, 12-digit numeric)
- PAN (string, alphanumeric, valid PAN format)
- Password (string, meets complexity policy)

**Processing / Business Logic:**
1. System accepts registration form with all required fields.
2. Aadhaar is validated for format: exactly 12 digits, no leading zeros (BR-002).
3. PAN is validated for format: 5 uppercase letters + 4 digits + 1 uppercase letter (e.g., ABCDE1234F) (BR-002).
4. No external/real verification of Aadhaar or PAN is performed (BR-002).
5. On successful validation, a synthetic Customer record and an associated Account are created in a Pending-KYC state.
6. The KYC submission is placed in a queue visible to Bank operations for review (BRD §8).
7. All actions (registration, validation result, KYC submission) are audit-logged (BR-007).

**Output:**
- Customer account created with status Pending-KYC
- Confirmation message to Customer with submission reference

**Error Handling:**
- Invalid Aadhaar format → reject with specific error: "Aadhaar must be exactly 12 digits"
- Invalid PAN format → reject with specific error: "PAN must be in format ABCDE1234F"
- Duplicate email or phone → reject with specific error: "An account with this email/phone already exists"
- Missing required fields → reject with error listing each missing field

**Open Items:**
- Password complexity policy not specified in BRD — flag for resolution.

---

#### FR-2: Account Onboarding and Activation

**Traces to:** F2 (BRD §7.3) · BR-001, BR-007
**Priority:** 1 (Must) · Business Process

**Input:**
- Bank operations user authenticated with Bank operations role
- KYC submission reference
- Review decision: Activate or Reject
- Rejection reason (string, required when rejecting)

**Processing / Business Logic:**
1. Bank operations user accesses a review queue of pending KYC submissions (BRD §8).
2. User views the submitted KYC details (Customer name, Aadhaar, PAN — format-validated only).
3. User selects Activate or Reject.
4. If Activate: Account state transitions from Pending-KYC to Activated. Customer is notified.
5. If Reject: Account state transitions to Rejected. Customer is notified with rejection reason.
6. An account cannot be activated until KYC passes format validation (BR-001) — this is already satisfied at submission time; the review confirms the record is complete.
7. All actions (review open, decision, state transition) are audit-logged with actor, timestamp, and before/after state (BR-007).

**Output:**
- Account state updated to Activated or Rejected
- Notification to Customer of decision

**Error Handling:**
- Submission already reviewed → reject with error: "This KYC submission has already been processed"
- Missing rejection reason → reject with error: "Rejection reason is required"
- Attempting to activate an account already in Activated state → reject with error: "Account is already activated"

---

#### FR-3: Login

**Traces to:** F3 (BRD §7.3) · BR-007
**Priority:** 1 (Must)

**Input:**
- Email address (string)
- Password (string)
- Expected role: Customer or Bank operations

**Processing / Business Logic:**
1. System authenticates the user against stored credentials.
2. On success, system establishes a session with role-scoped access:
   - Customer role: access to own account(s), transfers, statements
   - Bank operations role: access to KYC review queue, audit trail, account management
3. Role-based access control prevents cross-role access (NF-1): a Customer cannot access Bank operations functions and vice versa.
4. Login event is audit-logged with actor, timestamp, and IP/session ID (BR-007).

**Output:**
- Authenticated session token
- Role-appropriate landing page/dashboard

**Error Handling:**
- Invalid credentials → reject with generic error: "Invalid email or password" (no disclosure of which field is wrong)
- Account not activated (Pending-KYC or Rejected state) → reject with error: "Your account has not been activated. Please complete KYC verification."
- Account frozen → reject with error: "Your account is frozen. Please contact support."
- Too many failed attempts → (specify lockout policy — **flag: not defined in BRD**)

---

#### FR-4: Logout

**Traces to:** F4 (BRD §7.3) · BR-007
**Priority:** 1 (Must)

**Input:**
- Authenticated user (any role)

**Processing / Business Logic:**
1. System terminates the active session.
2. Session token is invalidated server-side.
3. Logout event is audit-logged with actor, timestamp, and session ID (BR-007).

**Output:**
- Session terminated
- Redirect to login page

**Error Handling:**
- Session already expired → silently redirect to login (no error needed)
- Logout request with no active session → treat as no-op

---

#### FR-5: Money Transfer

**Traces to:** F5 (BRD §7.3) · BR-003, BR-005, BR-006
**Priority:** 1 (Must) · Business Process

**Input:**
- Authenticated Customer user
- Source account ID (must be owned by the Customer)
- Destination account ID
- Transfer amount (positive decimal)

**Processing / Business Logic:**
1. System verifies the source account is in Activated state (BR-003). Transfer is blocked otherwise.
2. System verifies the initiating user is a Customer role (BR-005 — Bank operations cannot initiate transfers).
3. System verifies the source account is owned by the initiating Customer (BR-008 implicit — can only act on own accounts).
4. System verifies the destination account exists and is in an Activated state.
5. System checks the source account has sufficient balance (NF-4: balance shall never go negative). Balance validation rules pending OQ-002 (minimum balance) and OQ-003 (daily transfer cap).
6. On validation pass: source account balance is debited, destination account balance is credited. Amounts are synthetic only (BR-006).
7. A transfer record is created with: source account, destination account, amount, timestamp, initiating actor.
8. All actions are audit-logged (BR-007).

**Output:**
- Transfer confirmation with reference ID
- Updated source and destination balances

**Error Handling:**
- Source account not Activated → reject with error: "Transfers are only allowed from activated accounts" (BR-003)
- Source account frozen → reject with error: "This account is frozen and cannot make transfers"
- Destination account not found → reject with error: "Destination account not found"
- Destination account not Activated → reject with error: "Destination account is not activated"
- Insufficient balance → reject with error: "Insufficient balance"
- User is Bank operations role → reject with error: "Bank operations users cannot initiate transfers" (BR-005)
- User does not own source account → reject with error: "You can only transfer from your own accounts"
- Transfer amount ≤ 0 → reject with error: "Transfer amount must be greater than zero"
- Open: daily transfer cap exceeded (pending OQ-003) → reject with error if cap defined

---

#### FR-6: Money Receive

**Traces to:** F6 (BRD §7.3) · BR-006
**Priority:** 1 (Must)

**Input:**
- Completed transfer event from FR-5 (source account, destination account, amount)

**Processing / Business Logic:**
1. When a transfer initiated via FR-5 completes validation, the system credits the destination account's balance.
2. The credit is recorded as a transaction entry on the destination account.
3. All amounts are synthetic (BR-006) — no real money movement.
4. The receive event is part of the same audit-logged transfer record (BR-007).

**Output:**
- Destination account balance updated
- Transaction entry visible in destination account's statement (FR-7)

**Error Handling:**
- Destination account deleted or frozen after transfer validation but before credit → (edge case) system should either complete the atomic transaction or reject and reverse. **Flag: transaction atomicity not specified in BRD — flag for resolution.**
- Duplicate receive for same transfer ID → reject, idempotency check on transfer ID

---

#### FR-7: Statement View

**Traces to:** F7 (BRD §7.3) · BR-008
**Priority:** 1 (Must)

**Input:**
- Authenticated user (Customer or Bank operations)
- Account ID
- Optional: date range filter (from, to)

**Processing / Business Logic:**
1. If user is Customer: system verifies the account is owned by the user (BR-008).
2. If user is Bank operations: system allows viewing any account's statement for audit purposes (BRD §7.3 F7).
3. System retrieves transaction history for the specified account and optional date range.
4. Statement is displayed in the UI with: date, transaction type (debit/credit/transfer), amount, counterparty account, running balance.

**Output:**
- Transaction list displayed in UI
- No file download in this function (see FR-8)

**Error Handling:**
- Customer requests statement for account they do not own → reject with error: "You can only view statements for your own accounts" (BR-008)
- Account not found → reject with error: "Account not found"
- No transactions in date range → display empty statement with message "No transactions found for the selected period"

---

#### FR-8: Statement Download

**Traces to:** F8 (BRD §7.3) · BR-008
**Priority:** 2 (Should)

**Input:**
- Authenticated Customer user
- Account ID
- Optional: date range filter (from, to)
- Preferred file format (e.g., PDF, CSV — **flag: format not specified in BRD**)

**Processing / Business Logic:**
1. System verifies the account is owned by the Customer (BR-008).
2. System retrieves transaction history (same logic as FR-7).
3. System generates a downloadable file in the specified format.
4. Download event is audit-logged (BR-007).
5. FR-8 depends on FR-7 being available (BRD §3 constraint).

**Output:**
- Downloadable file (PDF/CSV) containing the statement

**Error Handling:**
- Customer requests statement for account they do not own → reject with error: "You can only download statements for your own accounts" (BR-008)
- Account not found → reject with error: "Account not found"
- Unsupported file format → reject with error listing supported formats
- Statement generation failure (timeout or system error) → retry or report error to user

---

### 3.3 Non-Functional Requirements (Cross-Cutting)

#### NF-1: Security — Role-Based Access Control
**Traces to:** NF1 (BRD §7.4) · BR-005, BR-008

- Every API endpoint must verify the authenticated user's role before granting access.
- Customer users cannot access Bank operations endpoints (KYC review, account activation, freeze, audit trail).
- Bank operations users cannot access Customer-only endpoints (money transfer initiation).
- Customer users cannot access other Customers' data (account details, statements, transfers).

#### NF-2: Auditability
**Traces to:** NF2 (BRD §7.4) · BR-007

- Every write action (state change, transfer, login/logout) must be logged with: actor ID, timestamp, action type, before state, after state.
- Audit trail is queryable by Bank operations via UI without direct database access (BRD §8).
- Audit logs are append-only; no modification or deletion is permitted through the application.

#### NF-3: Testability
**Traces to:** NF3 (BRD §7.4)

- Every FR-1 through FR-8 must have at least one traceable UAT test case.
- UAT execution owner is unresolved (OQ-001) — test cases should be written but execution plan deferred until OQ-001 is resolved.

#### NF-4: Data Integrity — Balance Integrity
**Traces to:** NF4 (BRD §7.4)

- Synthetic account balances shall never go negative as a result of a transfer.
- Minimum balance policy (OQ-002) and daily transfer cap (OQ-003) are pending resolution; FR-5 must incorporate these rules once defined.

#### NF-5: Accessibility
**Traces to:** NF5 (BRD §7.4)

- Core Customer journeys (FR-1, FR-3, FR-5, FR-7, FR-8) should meet basic keyboard-navigable, screen-reader-friendly interaction patterns.
- data-testid convention for UI test automation is pending confirmation (OQ-004).

## 4. Requirements

### 4.1 Organizational Requirements
- All development must follow traceability: every code change must link to a BRD requirement (F-number or BR-number).
- Architecture/Dev team (Mohit & Team) consumes this FRD as the basis for technical design.

### 4.2 Business Requirements
- BR-001 through BR-008 are non-negotiable constraints for v1.
- Open questions (OQ-001 through OQ-004) must be resolved or explicitly accepted as risks before design sign-off (BRD §10).

### 4.3 User Requirements
- Customer: Can register, complete KYC, log in, transfer money, view/download statements for own accounts only.
- Bank operations: Can review KYC, activate/freeze accounts, view audit trail, view any account statement. Cannot initiate transfers.

### 4.4 External Interfaces
- No external payment rails (BR-006).
- No external KYC verification services (BR-002).
- All interfaces are internal to the simulation.

### 4.5 System Features
- Two-role system (Customer, Bank operations) with role-scoped access.
- State machine for accounts: Pending-KYC → Activated → Frozen (reversible).

### 4.6 Performance
- **Not specified in BRD v1.** Flag for future consideration.

### 4.7 Acceptance Criteria
- Every FR-1 through FR-8 is testable via at least one UAT test case (NF-3).
- All BRD business rules (BR-001 through BR-008) are demonstrably enforced.
- Audit trail (NF-2) is queryable and shows all required state changes.

### 4.8 Database Requirements
- **Not specified in BRD v1.** Schema design is deferred to Architecture/Dev phase.

### 4.9 Design Constraints
- Greenfield v1 — no legacy data or process to migrate (BRD §4).
- Synthetic data only — no real identities or funds (BRD §3).

### 4.12 System Attributes
- Security (NF-1): Role-based access control.
- Auditability (NF-2): Append-only audit logs.
- Testability (NF-3): UAT traceable to FRs.
- Data Integrity (NF-4): Non-negative balances.
- Accessibility (NF-5): Keyboard navigation, screen reader support.

## 5. Other Requirements

### Ambiguities and Flags (Not Resolved — Pending Human Review)

| ID | Description | Affects | Action Required |
|---|---|---|---|
| OQ-001 | UAT execution owner unresolved | NF-3 (testability) | Resolve before design sign-off |
| OQ-002 | Minimum balance policy undefined | FR-5, NF-4 | Define: is there a floor? What value? |
| OQ-003 | Daily transfer cap undefined | FR-5, NF-4 | Define: is there a cap? What value? |
| OQ-004 | data-testid convention unconfirmed | NF-5, UI test automation | Confirm convention |
| FLAG-001 | Password complexity policy not in BRD | FR-3 | Define password requirements |
| FLAG-002 | Account lockout policy (failed logins) not in BRD | FR-3 | Define lockout threshold and duration |
| FLAG-003 | Statement download file format not specified | FR-8 | Define: PDF, CSV, or both? |
| FLAG-004 | Transaction atomicity for FR-6 not specified | FR-6 | Define: what happens if credit fails after debit? |
| FLAG-005 | Performance requirements not specified | NF (all) | Defer to v2 or define baseline |

---

**End of FRD v1 — Status: DRAFT**
**Awaiting human review and approval. No implementation should proceed until this document is explicitly approved.**