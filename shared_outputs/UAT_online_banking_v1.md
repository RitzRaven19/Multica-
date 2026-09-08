USER ACCEPTANCE TEST PLAN
Online Banking Simulation — v1
Status: DRAFT (agent-generated, pending human review/approval)
Source inputs: BRD_online_banking_v1.md, FRD_online_banking_v1.md
Note: UAT execution owner is unresolved (OQ-001 in BRD Section 9) — this plan assumes QA (Mandeep & Team) executes, pending confirmation.

1. Purpose
Verify that each functional requirement (F1–F8 / FR-1–FR-8) and its underlying business rules (BR-001–BR-008) behave as specified, from the perspective of the Customer and Bank operations roles.

2. Scope
In scope: the eight v1 capabilities per scope_agreement.md. Out of scope: beneficiary management, notifications, service requests, real KYC/payment verification (none exist to test in v1).

3. Entry / Exit Criteria
Entry: FRD approved; test environment seeded with at least one synthetic Customer and one Bank operations account.
Exit: all Priority-1 test cases (TC-01–TC-11) pass; any failing case is logged as a defect and routed to Defect RCA (Adiba & Team).

4. Test Cases

TC-01 (traces FR-1 / BR-001, BR-002) — Valid KYC submission
Steps: Register new Customer; submit well-formed Aadhaar (12 digits) and PAN (5 letters+4 digits+1 letter).
Expected: KYC record created, status PENDING_REVIEW; account created, status UNACTIVATED.

TC-02 (traces FR-1 / BR-002) — Malformed KYC rejected
Steps: Submit Aadhaar with 11 digits.
Expected: Field-level format error; no KYC record is created.

TC-03 (traces FR-2 / BR-001, BR-007) — KYC approval activates account
Steps: Bank operations reviews PENDING_REVIEW KYC and approves it.
Expected: Account status → ACTIVATED; audit trail shows actor, timestamp, before/after state.

TC-04 (traces FR-2) — KYC rejection blocks activation
Steps: Bank operations rejects a KYC record with a reason.
Expected: Account status → REJECTED; Customer cannot log in to a transacting session for that account.

TC-05 (traces FR-3, NF1) — Role-scoped login
Steps: Log in as Customer A.
Expected: Customer A sees only their own account(s); no access to Customer B's accounts or Bank operations screens.

TC-06 (traces FR-4) — Logout terminates session
Steps: Log out, then attempt to reuse the prior session token/URL.
Expected: Access is denied; user is redirected to login.

TC-07 (traces FR-5 / BR-003) — Transfer from Activated account succeeds
Steps: Customer A (ACTIVATED account) transfers a valid amount to Customer B's ACTIVATED account.
Expected: Source debited, destination credited atomically; transaction recorded on both sides; audit entry created.

TC-08 (traces FR-5 / BR-003) — Transfer from non-Activated account blocked
Steps: Attempt a transfer from an UNACTIVATED or FROZEN account.
Expected: Transfer is rejected; no balance change on either account.

TC-09 (traces FR-5 / BR-005) — Bank operations cannot transfer
Steps: Attempt to invoke the transfer action as a Bank operations user (via UI and, if feasible, direct API call).
Expected: Action is denied at the authorization layer, not just hidden in the UI.

TC-10 (traces FR-7 / BR-008) — Statement view is owner-scoped
Steps: Customer A requests a statement for Customer B's account.
Expected: Access denied. Customer A requests their own account's statement: transaction history displayed correctly, including the TC-07 transfer.

TC-11 (traces FR-8 / BR-008) — Statement download
Steps: Customer A downloads their own account statement.
Expected: File downloads in the specified format and matches the on-screen statement (TC-10) for the same date range.

TC-12 (traces BR-004, Priority 2) — Freeze blocks transfer
Steps: Bank operations freezes Customer A's ACTIVATED account; Customer A attempts a transfer.
Expected: Account status → FROZEN; transfer is rejected, same as TC-08.

5. Traceability Summary
Every test case above maps to exactly one FRD requirement and at least one BRD business rule, satisfying NF3 (testability) from the BRD. Any requirement without a corresponding test case here should be flagged before exit.

6. Defect Handling
A failed test case is logged with: TC ID, requirement traced, actual vs. expected result, and environment/data state. Defect RCA (Adiba & Team) determines whether a failure is a build defect, a requirements gap, or a new-request-in-disguise — per the charter's goal of avoiding ambiguity between the three.

7. Sign-off
Pending: UAT execution owner (OQ-001), minimum balance policy (OQ-002), transfer cap (OQ-003), and data-testid convention (OQ-004) should be resolved before this plan is finalized and approved.
