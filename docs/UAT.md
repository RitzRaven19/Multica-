USER ACCEPTANCE TEST PLAN
Online Banking Simulation — v1
Status: DRAFT (agent-generated, pending human review/approval)
Source inputs: FRD_online_banking_v1.md (FR-1–FR-8), BRD_online_banking_v1.md (BR-001–BR-008)

## 1. Purpose and Traceability Rule

Every test case below cites exactly one FR-x (from the FRD) and at least one BR-xxx (from the BRD's Section 6 business rules). Coverage spans both in-scope roles: Customer and Bank operations. Per NF3, every functional requirement FR-1–FR-8 must have at least one traceable UAT case; that condition is satisfied below (see Section 3 for exceptions/notes).

Legend: Role = Customer (C) or Bank operations (BO).

## 2. Test Cases

### FR-1 — Customer Onboarding with KYC

**TC-01** | FR-1 | BR-001, BR-002 | Role: C
- Precondition: Customer is on the onboarding form, unauthenticated/new.
- Steps: 1) Enter full name. 2) Enter a syntactically valid 12-digit numeric Aadhaar. 3) Enter a syntactically valid PAN (5 letters + 4 digits + 1 letter). 4) Submit.
- Expected: No external verification call is made. A KYC record is created with status PENDING_REVIEW; the associated account is created with status UNACTIVATED.

**TC-02** | FR-1 | BR-002 | Role: C
- Precondition: Customer is on the onboarding form.
- Steps: 1) Enter a malformed Aadhaar (e.g., 11 digits, or contains letters). 2) Attempt to submit.
- Expected: Field-level format error is shown before submission; no KYC record or account is created.

**TC-03** | FR-1 | BR-002 | Role: C
- Precondition: Customer is on the onboarding form.
- Steps: 1) Enter a malformed PAN (e.g., wrong letter/digit pattern). 2) Attempt to submit.
- Expected: Field-level format error is shown before submission; no KYC record or account is created.

### FR-2 — Account Onboarding and Activation

**TC-04** | FR-2 | BR-001, BR-007 | Role: BO
- Precondition: A KYC record exists with status PENDING_REVIEW (from TC-01).
- Steps: 1) Bank operations opens the KYC review queue. 2) Selects the PENDING_REVIEW record. 3) Approves it.
- Expected: Account status transitions to ACTIVATED. An audit trail entry is written recording actor, timestamp, and before/after state.

**TC-05** | FR-2 | BR-007 | Role: BO
- Precondition: A KYC record exists with status PENDING_REVIEW.
- Steps: 1) Bank operations selects the record. 2) Rejects it, supplying a reason.
- Expected: Account status transitions to REJECTED. An audit trail entry is written with the rejection reason, actor, and timestamp.

**TC-06** | FR-2 | BR-007 | Role: BO
- Precondition: A KYC record exists with status PENDING_REVIEW.
- Steps: 1) Bank operations attempts to reject the record without entering a reason.
- Expected: Submission is blocked with a validation error requiring a reason; account status is unchanged and no audit entry is written.

**TC-07** | FR-2 | BR-004, BR-007 | Role: BO
- Precondition: An account exists with status ACTIVATED.
- Steps: 1) Bank operations selects the ACTIVATED account. 2) Applies a freeze action.
- Expected: Account status transitions to FROZEN. An audit trail entry is written recording actor, timestamp, and before/after state. (See Section 3, Note A on FR mapping for the freeze action.)

### FR-3 — Login

**TC-08** | FR-3 | BR-007 | Role: C
- Precondition: A Customer account exists with status ACTIVATED and valid credentials.
- Steps: 1) Enter valid username/email and password. 2) Submit.
- Expected: A session token is issued; the Customer lands on a view scoped only to their own account IDs. Login is recorded in the audit trail.

**TC-09** | FR-3 | BR-007 | Role: BO
- Precondition: A Bank operations account exists with valid credentials.
- Steps: 1) Enter valid username/email and password. 2) Submit.
- Expected: A session token is issued; the user lands on the Bank operations view. Login is recorded in the audit trail.

**TC-10** | FR-3 | BR-007 | Role: C
- Precondition: A Customer account exists.
- Steps: 1) Enter a valid username with an incorrect password. 2) Submit.
- Expected: Authentication is rejected; no session token is issued. The failed attempt is recorded in the audit trail.

### FR-4 — Logout

**TC-11** | FR-4 | BR-007 | Role: C
- Precondition: Customer holds an authenticated session (from TC-08).
- Steps: 1) Trigger logout.
- Expected: Session token is invalidated server-side; user is returned to the unauthenticated state. Logout is recorded in the audit trail.

**TC-12** | FR-4 | BR-007 | Role: BO
- Precondition: Bank operations user holds an authenticated session (from TC-09).
- Steps: 1) Trigger logout.
- Expected: Session token is invalidated server-side; user is returned to the unauthenticated state. Logout is recorded in the audit trail.

### FR-5 — Money Transfer

**TC-13** | FR-5 | BR-003, BR-006, BR-007 | Role: C
- Precondition: Customer owns a source account with status ACTIVATED and sufficient balance; a valid destination account exists.
- Steps: 1) Customer initiates a transfer specifying source account, destination account, and an amount not exceeding the source balance. 2) Confirms.
- Expected: Source is debited and destination is credited atomically; a transaction record appears on both accounts; an audit trail entry is written; source balance does not go negative.

**TC-14** | FR-5 | BR-003 | Role: C
- Precondition: Customer owns a source account with status UNACTIVATED.
- Steps: 1) Customer attempts to initiate a transfer from the UNACTIVATED account.
- Expected: Transfer is blocked at the authorization layer; no debit/credit occurs; no transaction record is created.

**TC-15** | FR-5 | BR-003, BR-004 | Role: C
- Precondition: Customer owns a source account previously ACTIVATED, now FROZEN (from TC-07).
- Steps: 1) Customer attempts to initiate a transfer from the FROZEN account.
- Expected: Transfer is blocked at the authorization layer; no debit/credit occurs; no transaction record is created.

**TC-16** | FR-5 | BR-005 | Role: BO
- Precondition: Bank operations user is authenticated.
- Steps: 1) Bank operations attempts to initiate, approve, or reverse a money transfer via any available interface/API.
- Expected: Action is rejected at the authorization layer regardless of UI restrictions; no transaction record is created.

**TC-17** | FR-5 | BR-006 | Role: C
- Precondition: Customer owns a source account with status ACTIVATED and a known balance.
- Steps: 1) Customer attempts to transfer an amount exceeding the current source balance.
- Expected: Transfer is rejected; source balance does not go negative; no transaction record is created. (See Section 3, Note B — this case exercises NF4, which has no dedicated BR and is provisional pending OQ-002/OQ-003.)

### FR-6 — Money Receive

**TC-18** | FR-6 | BR-006, BR-007 | Role: C
- Precondition: A completed transfer targets the Customer's account (counterpart of TC-13).
- Steps: 1) Recipient Customer logs in and opens their statement/balance view.
- Expected: Receiving account balance reflects the credit immediately upon the transfer's completion, with no separate accept step; the transaction is visible in the recipient's statement (FR-7) and recorded in the audit trail.

**TC-19** | FR-6 | BR-006 | Role: C
- Precondition: A transfer targeting the Customer's account has completed.
- Steps: 1) Recipient Customer checks their account for any pending/"accept transfer" action.
- Expected: No pending or accept-style action exists or is required; the credit is already final.

### FR-7 — Statement View

**TC-20** | FR-7 | BR-008 | Role: C
- Precondition: Customer owns an account with transaction history.
- Steps: 1) Customer requests a statement for their own account, optionally with a date range.
- Expected: A chronological transaction list (transfers in/out, balance after each entry) is returned.

**TC-21** | FR-7 | BR-008 | Role: C
- Precondition: Customer A and Customer B each own separate accounts.
- Steps: 1) Customer A attempts to request a statement for Customer B's account (e.g., by ID manipulation).
- Expected: Access is denied; no statement data for the other Customer's account is returned.

**TC-22** | FR-7 | BR-008 | Role: BO
- Precondition: Any Customer account with transaction history exists.
- Steps: 1) Bank operations requests a statement for that account for audit purposes.
- Expected: Statement is returned regardless of ownership, since Bank operations may query any account.

### FR-8 — Statement Download

**TC-23** | FR-8 | BR-008 | Role: C
- Precondition: Customer owns an account with transaction history.
- Steps: 1) Customer requests a statement download for their own account, optionally with a date range.
- Expected: A downloadable file (CSV or PDF) is generated in a durable format matching the on-screen statement (FR-7) data.

**TC-24** | FR-8 | BR-008 | Role: C
- Precondition: Customer A and Customer B each own separate accounts.
- Steps: 1) Customer A attempts to download a statement for Customer B's account.
- Expected: Access is denied; no file is generated.

**TC-25** | FR-8 | BR-008 | Role: BO
- Precondition: Any Customer account with transaction history exists.
- Steps: 1) Bank operations requests a statement download for that account.
- Expected: Download succeeds, per the FRD's "same access rule as FR-7." (See Section 3, Note C — the BRD's F8 wording names only the Customer role; confirm this is intended before treating TC-25 as a Must-pass case.)

## 3. Coverage Summary and Notes

All eight functional requirements (FR-1–FR-8) have at least one traceable test case; there is no FR-x gap to report.

The following traceability observations are surfaced for Business Analysis / Architecture sign-off, not resolved here (outside this agent's role):

- **Note A (TC-07):** BR-004 requires that Bank operations can freeze an ACTIVATED account, and FRD Section 4.9 requires BR-004 be enforced at the authorization layer. However, no FR explicitly describes a "freeze" action — FR-2's text only covers KYC approve/reject. TC-07 is mapped to FR-2 as the nearest fit (Bank-operations-driven account status change). Recommend the FRD be updated to explicitly scope freeze/unfreeze under FR-2 (or a new FR) so this traceability is unambiguous.
- **Note B (TC-17):** NF4 (non-negative balance) has no dedicated business rule in BRD Section 6, and is explicitly marked provisional pending OQ-002 (minimum balance policy) and OQ-003 (daily transfer cap). TC-17 cites BR-006 as the closest applicable rule; this mapping should be revisited once OQ-002/OQ-003 are resolved.
- **Note C (TC-25):** BRD F8 describes statement download only for the Customer role, while FRD FR-8 says download uses "the same access rule as FR-7" (which includes Bank operations). TC-25 tests the FRD's broader reading; confirm with Business Analysis whether Bank operations download access is in scope for v1.
- **OQ-001 (UAT execution owner)** is still unresolved per BRD Section 9. This plan is produced per the FRD's acceptance-criteria requirement (Section 4.7) but stays DRAFT until a human owner reviews and approves it, and until OQ-001 is settled for who executes it.

Any test case that fails during execution is to be handed to Defect RCA (Adiba & Team) — this plan does not attempt root-cause analysis or remediation.
