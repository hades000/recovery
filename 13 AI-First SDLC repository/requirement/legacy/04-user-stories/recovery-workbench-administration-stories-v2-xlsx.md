<!-- source: 04 User stories/Recovery Workbench Administration Stories v2.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `04 User stories/Recovery Workbench Administration Stories v2.xlsx`  
> **Converted from:** XLSX

## Stories

| Administration stories |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 22 stories. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Key | Epic | Module | Module name | Title | Story | Priority | Depends on | Entities | Screens | Permission | Messages | Criteria | Test cases | Decision |
| RWB-AD-001 | E8 | P4 | Access and administration | Map Entra ID groups to Workbench roles | As a security administrator, I want each Entra ID group mapped to one Workbench role in each environment as a data row, so that a person gets their roles from the group the bank IAM grants, with no code change. | Must | RWB-E1-022 | decision_log_entry, role | Roles and access | Rules and parameters R; Rules and parameters C | MSG-P4-001, MSG-P4-004, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | 3 | 5 | DL40 |
| RWB-AD-002 | E8 | P4 | Access and administration | Permission matrix as a versioned load | As an application owner, I want the permission matrix of roles against the 14 capability areas loaded as a versioned file, so that a permission changes without a code release and every change has an approver. | Must | RWB-E1-037 | assignment, document, lov_value, role, permission | Rules and parameters; Reference data | Rules and parameters A; Reference data C | MSG-P4-002, MSG-P4-004, MSG-P4-001, MSG-GEN-001, MSG-P7-003 | 3 | 5 | None |
| RWB-AD-003 | E8 | P4 | Access and administration | Scope per role | As an application owner, I want each role given a scope of own cases, team, region or all as data, so that a person sees only the cases their role allows. | Must | RWB-E1-037 | recovery_case, assignment, decision_log_entry, role | Roles and access | Platform administration R | MSG-P4-003, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-004 | E8 | P4 | Access and administration | Masking profiles per role | As a Compliance and PDPA officer, I want a masking profile per role and personal field held as data, so that personal data is shown only to the roles allowed to see it. | Must | RWB-E1-037 | recovery_case, contact_point, document, decision_log_entry, role | Personal data; Roles and access | Rules and parameters C; Rules and parameters A | MSG-P4-003, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | 3 | 5 | DL26 |
| RWB-AD-005 | E8 | P4 | Access and administration | Separation of duty check at sign-in | As a security administrator, I want a session refused when a person's groups hold a conflicting role pair, so that no one holds two roles the separation of duty table forbids. | Must | RWB-E1-022 | role | Roles and access | Rules and parameters C; Rules and parameters A | MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-006 | E8 | P4 | Access and administration | Break-glass access | As a platform administrator, I want emergency access beyond my role, tied to an open incident, ending on its own, so that an incident can be fixed without a permanent grant. | Must | RWB-E1-039 | role | Roles and access | Platform administration R | MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | 3 | 5 | DL38 |
| RWB-AD-007 | E8 | P4 | Access and administration | Access log search and export | As an internal auditor, I want the access log searched by person, date, event and capability area, with export, so that I can show who accessed what without asking IT. | Must | RWB-E1-039 | document, decision_log_entry, role | Rules and parameters; Reference data | Platform administration R; Rules and parameters R | MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-008 | E8 | P4 | Access and administration | Access review list | As a role owner, I want a list of every holder of my roles each review cycle, to confirm or remove, so that access is recertified on schedule. | Must | RWB-E1-022 | assignment, decision_log_entry, role | Roles and access; Delegation of authority | Platform administration R | MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | 2 | 4 | DL38 |
| RWB-AD-009 | E8 | P4 | Access and administration | Load a list of values version | As a reference data administrator, I want a list of values loaded as a new version with a valid from date, so that a code list changes without a code release. | Must | RWB-E1-043 | recovery_case, assignment, document, lov_value | Rules and parameters; Reference data | Rules and parameters R; Rules and parameters A | MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-010 | E8 | P4 | Access and administration | Approve a reference data load | As a list owner, I want to approve or reject a loaded version before it takes effect, so that no reference data changes without its owner. | Must | RWB-AD-009 | assignment, decision_log_entry, lov_value | Rules and parameters; Reference data | Rules and parameters A; Reference data A | MSG-P4-002, MSG-P4-001, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-011 | E8 | P4 | Access and administration | Load a rule version | As a center of excellence analyst, I want a route set loaded as a new rule version where each row names its test case, so that rules change as data and every row is tested. | Must | RWB-E1-029 | recovery_case, document, rule_row | Rules and parameters; Personal data | Rules and parameters A; Rules and parameters R | MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001 | 2 | 3 | DL24 |
| RWB-AD-012 | E8 | P4 | Access and administration | Approve a rule version | As a risk and model risk officer, I want to approve a rule version that has passed its tests, with its valid from date, so that only tested and approved rules decide cases. | Must | RWB-AD-011 | recovery_case, rule_row | Rules and parameters; Personal data | Rules and parameters A; Rules and parameters R | MSG-P4-004, MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-013 | E8 | P4 | Access and administration | Roll back a rule or reference version | As a reference data administrator, I want the previous version restored through the same load, so that a bad change is undone in minutes. | Must | RWB-AD-012 | assignment, decision_log_entry, rule_row | Reference data | Rules and parameters C; Rules and parameters A | MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | 1 | 3 | None |
| RWB-AD-014 | E8 | P4 | Access and administration | Configure queues | As a reference data administrator, I want queues with their team, role, assignment method, caseload cap and overflow queue loaded as data, so that allocation follows the team set-up without a code change. | Must | RWB-E1-019 | queue, assignment, document, role | Queues and service levels | Rules and parameters R; Rules and parameters A | MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | 2 | 4 | DL23 |
| RWB-AD-015 | E8 | P4 | Access and administration | Configure service levels and timers | As a reference data administrator, I want the time allowed in each case state, its warning and its escalation point loaded as data, so that clocks and escalations follow the agreed service levels. | Must | RWB-E1-028 | recovery_case, timer, rule_row | Queues and service levels; Rules and parameters | Rules and parameters A; Rules and parameters C | MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | 2 | 4 | DL22 |
| RWB-AD-016 | E8 | P4 | Access and administration | Load the delegation of authority table | As a reference data administrator, I want approval levels, limits, holders and substitutes loaded as data with effective dates, so that approvals route by the regulation without a code change. | Must | RWB-E1-038 | delegation_limit | Delegation of authority; Rules and parameters | Rules and parameters A; Reference data C | MSG-P4-001, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-P7-003 | 2 | 4 | DL18 |
| RWB-AD-017 | E8 | P6 | Communications | Manage letter and notice templates | As a legal counsel, I want templates by type, product and language approved by Legal before use, and withdrawn when they change, so that every notice uses wording Legal has approved. | Must | RWB-E1-034 | task, legal_action, notice, template | Template approval | Litigation C; Litigation R | MSG-P6-003, MSG-P6-004, MSG-P6-001, MSG-GEN-001, MSG-P4-002, MSG-P7-003 | 2 | 4 | DL28 |
| RWB-AD-018 | E8 | P1 | Recovery data engine | Interface and job monitor | As a platform administrator, I want every load, file and job with its status, business date, checks and a rerun action, so that a failed load is found and rerun the same morning. | Must | RWB-E1-056 | document, decision_log_entry | Interface and job monitor; Data quality | Platform administration R; Platform administration U | MSG-P1-001, MSG-P1-002, MSG-GEN-001, MSG-P4-002, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-019 | E8 | P1 | Recovery data engine | Data quality and reconciliation console | As a data steward, I want load check exceptions, reconciliation breaks and stale data products on one screen, so that I fix data problems before they reach a decision. | Must | RWB-E1-011 | recovery_case, loan_account | Data quality | Platform administration R | MSG-P1-001, MSG-P1-002, MSG-GEN-001, MSG-P4-002, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-020 | E8 | P10 | Agent runtime | Autonomy level per decision step | As a risk and model risk officer, I want the autonomy level of each agent step held as data and changed only with committee approval, so that an agent never acts beyond what the committee approved. | Must | RWB-E1-063 | decision_log_entry | Agent monitor | Platform administration R | MSG-GEN-001, MSG-P4-002, MSG-P7-003 | 2 | 4 | None |
| RWB-AD-021 | E8 | P5 | Document hub | Retention classes and legal hold | As a Compliance and PDPA officer, I want retention classes by data product and document type, and legal holds that stop expiry, so that nothing is kept longer than its rule and nothing held is lost. | Must | RWB-E1-041 | document, rule_row | Document review queue; Document custody | Documents C; Documents R | MSG-P5-002, MSG-P5-003, MSG-P5-004, MSG-GEN-001, MSG-P4-002 | 2 | 3 | DL26 |
| RWB-AD-022 | E4 | S9 | Partner management | Partner firms and partner users | As a partner and agency manager, I want partner firms, their contracts and panel status held as data, and partner users requested for each firm, so that partners see only the work placed with their firm. | Must | RWB-E1-022 | partner, partner_instruction | Partner list; Partner home | Partner portal R | MSG-GEN-001, MSG-P4-002 | 2 | 3 | DL03 |

## Related backlog

| Administration already in the backlog |  |  |  |
|---|---|---|---|
| Stories already in the Epic 1 and Epic 2 backlog that this file builds on. They are not repeated here. |  |  |  |
| Key | Title | Module | Epic |
| RWB-E1-022 | Sign-on with SSO, MFA and the first roles | P4 | E1 |
| RWB-E1-029 | Rule load, validation and rollback | P3 | E1 |
| RWB-E1-034 | Letter template management | P6 | E1 |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | P4 | E1 |
| RWB-E1-038 | Delegation of authority table as reference data | P4 | E1 |
| RWB-E1-039 | Access log into the decision log and break-glass admin | P4,P7 | E1 |
| RWB-E1-041 | Retention classes and virus scan on intake | P5 | E1 |
| RWB-E1-043 | Reference data service with versioned tables | P3 | E1 |
| RWB-E1-048 | Rule change audit report | P3 | E1 |
| RWB-E1-056 | Run books and monitoring for every Epic 1 job | P2 | E1 |

## Acceptance criteria

| Acceptance criteria |  |  |
|---|---|---|
| Gherkin per story. |  |  |
| Key | Title | Gherkin |
| RWB-AD-001 | Map Entra ID groups to Workbench roles | Feature: Map Entra ID groups to Workbench roles<br><br>  Scenario: AC1 Group gives the role<br>    Given the group RWB-SIT-RW-CASEOWN mapped to RW-CASEOWN<br>    When a member of the group signs in to SIT<br>    Then the session holds the role RW-CASEOWN<br><br>  Scenario: AC2 Unmapped group<br>    Given a person whose only group has no mapping<br>    When they sign in<br>    Then the system refuses they with MSG-P4-001 and the refusal is in the access log<br><br>  Scenario: AC3 Mapping change<br>    Given a new mapping version with a valid from date<br>    When the date arrives<br>    Then sessions from that date use the new mapping |
| RWB-AD-002 | Permission matrix as a versioned load | Feature: Permission matrix as a versioned load<br><br>  Scenario: AC1 Load a matrix version<br>    Given a matrix file with every role and area<br>    When the reference data administrator loads it<br>    Then it passes the checks and waits for the application owner's approval<br><br>  Scenario: AC2 Incomplete matrix refused<br>    Given a file with a role missing<br>    When it is loaded<br>    Then the system refuses it in full with the missing role named<br><br>  Scenario: AC3 Takes effect on its date<br>    Given an approved version with a valid from date<br>    When the date arrives<br>    Then every endpoint checks against the new version |
| RWB-AD-003 | Scope per role | Feature: Scope per role<br><br>  Scenario: AC1 Own scope<br>    Given a case owner with scope Own<br>    When they list cases<br>    Then the system returns only cases they own<br><br>  Scenario: AC2 Out of scope<br>    Given a case owned by another team<br>    When a case owner with scope Team opens it<br>    Then the system does not find the response and the refusal is logged |
| RWB-AD-004 | Masking profiles per role | Feature: Masking profiles per role<br><br>  Scenario: AC1 Masked by default<br>    Given a role whose profile masks the phone number<br>    When it reads a case<br>    Then the system masks the phone number<br><br>  Scenario: AC2 Unmask is logged<br>    Given a role allowed to unmask the national ID token<br>    When it unmasks it on a record<br>    Then the system writes the read to the PII log<br><br>  Scenario: AC3 Profile change<br>    Given a new profile version approved by Compliance<br>    When its date arrives<br>    Then responses use the new profile |
| RWB-AD-005 | Separation of duty check at sign-in | Feature: Separation of duty check at sign-in<br><br>  Scenario: AC1 Conflict refused<br>    Given a person in the groups for RW-WRITEOFF and RW-WOCOMM<br>    When they sign in<br>    Then the system refuses the session and an incident goes to the security administrator<br><br>  Scenario: AC2 Table as data<br>    Given a new separation of duty version<br>    When it is approved<br>    Then the next sign-in checks against it |
| RWB-AD-006 | Break-glass access | Feature: Break-glass access<br><br>  Scenario: AC1 Granted with an incident<br>    Given an open incident and a reason of at least 20 characters<br>    When the security administrator approves the request<br>    Then the system grants access for the window and every action is marked break-glass<br><br>  Scenario: AC2 Refused without an incident<br>    Given no open incident<br>    When the request is made<br>    Then the system refuses it<br><br>  Scenario: AC3 Ends on its own<br>    Given an active grant<br>    When the window ends<br>    Then the grant ends with no action by anyone |
| RWB-AD-007 | Access log search and export | Feature: Access log search and export<br><br>  Scenario: AC1 Search<br>    Given sign-ins and refusals for a week<br>    When I search by person and date<br>    Then the matching entries show with the role and versions in force<br><br>  Scenario: AC2 Export<br>    Given a search result<br>    When I export it<br>    Then the file carries the same masking as the screen |
| RWB-AD-008 | Access review list | Feature: Access review list<br><br>  Scenario: AC1 List produced<br>    Given the review date<br>    When the review opens<br>    Then each role owner receives the holders of their roles<br><br>  Scenario: AC2 Not confirmed<br>    Given a holder not confirmed by the end of the review<br>    When the review closes<br>    Then the system requests removal through the bank IAM and logged |
| RWB-AD-009 | Load a list of values version | Feature: Load a list of values version<br><br>  Scenario: AC1 Valid load<br>    Given a file for LOV-ROUTE with codes and English labels<br>    When I load it<br>    Then it passes the checks and waits for the list owner's approval<br><br>  Scenario: AC2 Code in use removed<br>    Given a load that removes a code used by open cases<br>    When it is loaded<br>    Then the system refuses it with the count of records using the code |
| RWB-AD-010 | Approve a reference data load | Feature: Approve a reference data load<br><br>  Scenario: AC1 Approve<br>    Given a loaded version waiting for me<br>    When I approve it<br>    Then it takes effect from its valid from date and the approval is logged<br><br>  Scenario: AC2 Maker cannot approve<br>    Given a version I loaded<br>    When I try to approve it<br>    Then I am refused with MSG-P7-002 |
| RWB-AD-011 | Load a rule version | Feature: Load a rule version<br><br>  Scenario: AC1 Rule rows tested<br>    Given a route set file where every row has a test case ID<br>    When I load it<br>    Then the rule table tests run in SIT and the result is attached to the version<br><br>  Scenario: AC2 Row without a test<br>    Given a row with no test case ID<br>    When I load it<br>    Then the system refuses the version |
| RWB-AD-012 | Approve a rule version | Feature: Approve a rule version<br><br>  Scenario: AC1 Approve<br>    Given a version with every test passed<br>    When I approve it<br>    Then it applies to decisions from its valid from date<br><br>  Scenario: AC2 Open cases keep their version<br>    Given a case decided under the previous version<br>    When the new version takes effect<br>    Then the decided case keeps the version it was decided under (R-UNI-38) |
| RWB-AD-013 | Roll back a rule or reference version | Feature: Roll back a rule or reference version<br><br>  Scenario: AC1 Roll back<br>    Given a version in force that causes a breach<br>    When I load the previous version with an immediate date and the owner approves<br>    Then decisions from that time use the previous version and both changes are logged |
| RWB-AD-014 | Configure queues | Feature: Configure queues<br><br>  Scenario: AC1 Queue loaded<br>    Given a queue file<br>    When it is loaded and approved<br>    Then allocation uses the new method and cap from the valid from date<br><br>  Scenario: AC2 Overflow must exist<br>    Given a queue that names an overflow queue that does not exist<br>    When it is loaded<br>    Then the system refuses the load |
| RWB-AD-015 | Configure service levels and timers | Feature: Configure service levels and timers<br><br>  Scenario: AC1 Service level loaded<br>    Given a service level of 10 working days for state LIT_PACK with a warning at 8<br>    When it is approved<br>    Then new timers in that state use the values<br><br>  Scenario: AC2 Running timers<br>    Given a timer already running<br>    When a new version takes effect<br>    Then the running timer keeps its due date unless the rule says to recompute |
| RWB-AD-016 | Load the delegation of authority table | Feature: Load the delegation of authority table<br><br>  Scenario: AC1 Limits loaded<br>    Given limits by decision, level, product and amount<br>    When Risk approves the version<br>    Then approvals check against it from its date<br><br>  Scenario: AC2 Missing limit<br>    Given a decision with no limit at any level<br>    When it is submitted<br>    Then it goes to the next level up and an incident names the missing limit |
| RWB-AD-017 | Manage letter and notice templates | Feature: Manage letter and notice templates<br><br>  Scenario: AC1 Approve<br>    Given a new template version in Thai and English<br>    When Legal approves it<br>    Then notices generated from its date use it<br><br>  Scenario: AC2 Withdraw<br>    Given a template withdrawn<br>    When a notice of that type is due<br>    Then generation holds and a task goes to the litigation officer (R-LIT-04) |
| RWB-AD-018 | Interface and job monitor | Feature: Interface and job monitor<br><br>  Scenario: AC1 Status<br>    Given today's loads<br>    When I open the monitor<br>    Then each shows its business date, status and the result of each check<br><br>  Scenario: AC2 Rerun<br>    Given a failed load<br>    When I rerun it after the source is fixed<br>    Then the load runs again and both runs are logged |
| RWB-AD-019 | Data quality and reconciliation console | Feature: Data quality and reconciliation console<br><br>  Scenario: AC1 Breaks shown<br>    Given an account at 90 days past due with no case<br>    When the reconciliation runs<br>    Then the break shows with the account and the date<br><br>  Scenario: AC2 Stale product<br>    Given a data product past its expected business date<br>    When I open the console<br>    Then it shows as stale with its last good date |
| RWB-AD-020 | Autonomy level per decision step | Feature: Autonomy level per decision step<br><br>  Scenario: AC1 Level applied<br>    Given step D6.3 at level L1<br>    When the route agent answers<br>    Then the system shows the answer as a recommendation and a person decides<br><br>  Scenario: AC2 Step up recorded<br>    Given a committee approval for L2<br>    When the new version takes effect<br>    Then the change shows the approval reference in the version |
| RWB-AD-021 | Retention classes and legal hold | Feature: Retention classes and legal hold<br><br>  Scenario: AC1 Expiry<br>    Given a document past its retention period with no hold<br>    When the retention job runs<br>    Then the system proposes disposal and recorded, never silent<br><br>  Scenario: AC2 Hold<br>    Given a document under legal hold<br>    When its retention period ends<br>    Then the system keeps it and the hold is shown |
| RWB-AD-022 | Partner firms and partner users | Feature: Partner firms and partner users<br><br>  Scenario: AC1 Firm scope<br>    Given a law firm user<br>    When they open the partner portal<br>    Then only instructions placed with their firm show<br><br>  Scenario: AC2 Contract ends<br>    Given a firm whose contract ends today<br>    When the day ends<br>    Then the system disables its user accounts and open instructions are recalled |

## Test cases

| Test cases |  |  |  |
|---|---|---|---|
| 88 test cases. |  |  |  |
| Test case | Story | Covers | Test |
| TC-AD-001-01 | RWB-AD-001 | AC1 | Group gives the role |
| TC-AD-001-02 | RWB-AD-001 | AC2 | Unmapped group |
| TC-AD-001-03 | RWB-AD-001 | AC3 | Mapping change |
| TC-AD-001-04 | RWB-AD-001 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-001-05 | RWB-AD-001 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-002-01 | RWB-AD-002 | AC1 | Load a matrix version |
| TC-AD-002-02 | RWB-AD-002 | AC2 | Incomplete matrix refused |
| TC-AD-002-03 | RWB-AD-002 | AC3 | Takes effect on its date |
| TC-AD-002-04 | RWB-AD-002 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-002-05 | RWB-AD-002 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-003-01 | RWB-AD-003 | AC1 | Own scope |
| TC-AD-003-02 | RWB-AD-003 | AC2 | Out of scope |
| TC-AD-003-03 | RWB-AD-003 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-003-04 | RWB-AD-003 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-004-01 | RWB-AD-004 | AC1 | Masked by default |
| TC-AD-004-02 | RWB-AD-004 | AC2 | Unmask is logged |
| TC-AD-004-03 | RWB-AD-004 | AC3 | Profile change |
| TC-AD-004-04 | RWB-AD-004 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-004-05 | RWB-AD-004 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-005-01 | RWB-AD-005 | AC1 | Conflict refused |
| TC-AD-005-02 | RWB-AD-005 | AC2 | Table as data |
| TC-AD-005-03 | RWB-AD-005 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-005-04 | RWB-AD-005 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-006-01 | RWB-AD-006 | AC1 | Granted with an incident |
| TC-AD-006-02 | RWB-AD-006 | AC2 | Refused without an incident |
| TC-AD-006-03 | RWB-AD-006 | AC3 | Ends on its own |
| TC-AD-006-04 | RWB-AD-006 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-006-05 | RWB-AD-006 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-007-01 | RWB-AD-007 | AC1 | Search |
| TC-AD-007-02 | RWB-AD-007 | AC2 | Export |
| TC-AD-007-03 | RWB-AD-007 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-007-04 | RWB-AD-007 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-008-01 | RWB-AD-008 | AC1 | List produced |
| TC-AD-008-02 | RWB-AD-008 | AC2 | Not confirmed |
| TC-AD-008-03 | RWB-AD-008 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-008-04 | RWB-AD-008 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-009-01 | RWB-AD-009 | AC1 | Valid load |
| TC-AD-009-02 | RWB-AD-009 | AC2 | Code in use removed |
| TC-AD-009-03 | RWB-AD-009 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-009-04 | RWB-AD-009 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-010-01 | RWB-AD-010 | AC1 | Approve |
| TC-AD-010-02 | RWB-AD-010 | AC2 | Maker cannot approve |
| TC-AD-010-03 | RWB-AD-010 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-010-04 | RWB-AD-010 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-011-01 | RWB-AD-011 | AC1 | Rule rows tested |
| TC-AD-011-02 | RWB-AD-011 | AC2 | Row without a test |
| TC-AD-011-03 | RWB-AD-011 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-012-01 | RWB-AD-012 | AC1 | Approve |
| TC-AD-012-02 | RWB-AD-012 | AC2 | Open cases keep their version |
| TC-AD-012-03 | RWB-AD-012 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-012-04 | RWB-AD-012 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-013-01 | RWB-AD-013 | AC1 | Roll back |
| TC-AD-013-02 | RWB-AD-013 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-013-03 | RWB-AD-013 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-014-01 | RWB-AD-014 | AC1 | Queue loaded |
| TC-AD-014-02 | RWB-AD-014 | AC2 | Overflow must exist |
| TC-AD-014-03 | RWB-AD-014 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-014-04 | RWB-AD-014 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-015-01 | RWB-AD-015 | AC1 | Service level loaded |
| TC-AD-015-02 | RWB-AD-015 | AC2 | Running timers |
| TC-AD-015-03 | RWB-AD-015 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-015-04 | RWB-AD-015 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-016-01 | RWB-AD-016 | AC1 | Limits loaded |
| TC-AD-016-02 | RWB-AD-016 | AC2 | Missing limit |
| TC-AD-016-03 | RWB-AD-016 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-016-04 | RWB-AD-016 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-017-01 | RWB-AD-017 | AC1 | Approve |
| TC-AD-017-02 | RWB-AD-017 | AC2 | Withdraw |
| TC-AD-017-03 | RWB-AD-017 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-017-04 | RWB-AD-017 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-018-01 | RWB-AD-018 | AC1 | Status |
| TC-AD-018-02 | RWB-AD-018 | AC2 | Rerun |
| TC-AD-018-03 | RWB-AD-018 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-018-04 | RWB-AD-018 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-019-01 | RWB-AD-019 | AC1 | Breaks shown |
| TC-AD-019-02 | RWB-AD-019 | AC2 | Stale product |
| TC-AD-019-03 | RWB-AD-019 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-019-04 | RWB-AD-019 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-020-01 | RWB-AD-020 | AC1 | Level applied |
| TC-AD-020-02 | RWB-AD-020 | AC2 | Step up recorded |
| TC-AD-020-03 | RWB-AD-020 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-020-04 | RWB-AD-020 | Principle 5 | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-AD-021-01 | RWB-AD-021 | AC1 | Expiry |
| TC-AD-021-02 | RWB-AD-021 | AC2 | Hold |
| TC-AD-021-03 | RWB-AD-021 | Access | A role without the right is refused with MSG-P4-002 |
| TC-AD-022-01 | RWB-AD-022 | AC1 | Firm scope |
| TC-AD-022-02 | RWB-AD-022 | AC2 | Contract ends |
| TC-AD-022-03 | RWB-AD-022 | Access | A role without the right is refused with MSG-P4-002 |
