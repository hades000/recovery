<!-- source: 01 Decisions and governance/Recovery Workbench Admin and Access Model v4.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `01 Decisions and governance/Recovery Workbench Admin and Access Model v4.docx`  
> **Converted from:** DOCX

Recovery Workbench

Admin and access model

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench admin and access model |
| Version | 3 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Standard | NIST role based access control model (ANSI/INCITS 359) |

# 1. The model on one page

The Recovery Workbench is a module of ACE: one service, one repository and one front end. Access to the Workbench therefore uses what ACE already runs in production: Entra ID sign-in with multi-factor authentication, the bank IAM integration, role based access control, the audit log, the PII log through PII Kafka and the SOC log. The Workbench adds its own roles, permissions, scope rules and masking rules, held as versioned data.

| Question | Position in this model | Reason | Status |
|---|---|---|---|
| Who grants access | The application owner's organization. A role owner approves each grant and an access administrator carries it out in the bank IAM. | SCB administers enterprise tools such as Jira centrally, and business applications through their application owner. | Assumed, G1 |
| Who the application owner is | The Tribe Lead of the Collections and Recovery Tribe, for ACE as a whole. Recovery roles are delegated to recovery role owners. The ACE team is the technical custodian. | ACE holds the collection and the recovery modules in one service, so one application owner covers both. | Assumed, G2 |
| Where identity is held | Entra ID. The Workbench holds no password and no local account. | ACE runs Entra ID sign-in with IAM integration in production. | Settled |
| How a person holds a role | Membership of one Entra ID group per Workbench role per environment, granted through a bank IAM request. The Workbench reads the membership at sign-in. | ACE grants roles through the bank IAM and Entra ID today. | Settled; group names G7 |
| What a role may do | A permission matrix of 54 roles across 14 capability areas, using the letters C, R, U, D and A, held as versioned data. | Every role and permission is a data row with a version, so a change needs no code release. | Settled |
| Authority levels | Four administration levels decide who may grant access. Six approval levels from the bank approval authority regulation decide who may approve a recovery decision. | Access authority and approval authority are separate. Approval authority follows Regulation กกค.540031. | Assumed, G1 and G4 |
| Partners | No partner reaches the Workbench until the architecture team approves external access. Partners use the existing channels until then. | Access from outside the bank makes the application internet facing, which needs an architecture change with a lead time of one to three months. | Gap G3 |
| Non-human actors | Each runs under its own service identity, holds a role in the same roles table, and is checked and logged the same way as a person. | ACE runs services under managed identities. | Settled |

Settled: agreed by the bank or already in production. Assumed: the position the build uses until the bank answers. Gap: an answer needed from the bank, listed with its owner and date in section 11. Each gap is also held in the Recovery Workbench decision log under the ID shown beside it.

# 2. Terms

Each element of the NIST role based access control model has one name in the Workbench.

| NIST element | Meaning | In the Workbench |
|---|---|---|
| User | A person or a service identity that acts in the system | A bank employee, a partner user or a service identity, identified by Entra ID |
| Role | A job function with the permissions it needs | One row in the roles table, for example RW-CASEOWN, case owner |
| Permission | Approval to perform an operation on an object | A letter C, R, U, D or A in one of 14 capability areas, with a scope and a masking position |
| Session | The roles a user has active at one time | Created at sign-in. Carries the roles, the scope and the masking position until it ends |
| User assignment | Which users hold which roles | Entra ID group membership, granted through the bank IAM |
| Permission assignment | Which roles hold which permissions | The permission matrix version in force |
| Role hierarchy | One role inheriting the permissions of another | Not used. A person who needs two roles holds both, and the permissions of both apply |
| Static separation of duty | Role pairs that one user may never hold together | The conflict table in section 6.1 |
| Dynamic separation of duty | Actions one user may not combine in one session or on one record | The maker and checker rules in section 6.2 |

# 3. Administration

## 3.1 Central administration or application owner administration

|  | Central administration | Application owner administration |
|---|---|---|
| Who decides a grant | A central IAM or IT security team, on the request and the line manager's approval | The role owner for the role requested, under the application owner |
| Who carries out the grant | The central team | The access administrator in the business, or the IAM fulfillment team on the role owner's approval |
| Who reviews access | The central team runs the review; managers confirm | Role owners recertify their roles; the application owner signs the result |
| Where SCB uses it today | Enterprise tools, for example Jira licenses | Business applications |
| What the Workbench builds | Entra ID groups mapped to roles, the permission matrix as data, the access log | The same |
| Effect on the Epic 1 build | None. Changes who is trained and who signs the access tests | None |

Both options grant access in the same place, Entra ID through the bank IAM, so the build does not wait for the answer. The answer changes who holds administration levels 2 and 3 in section 3.2. This model uses application owner administration, because SCB administers business applications that way.

## 3.2 Administration levels

| Level | Position | Held by | May | May not |
|---|---|---|---|---|
| 1 | Application owner | Tribe Lead, Collections and Recovery Tribe (assumed, G2) | Approve the roles table and each permission matrix version. Appoint role owners and access administrators. Sign each access review. Accept the remaining access risk | Approve their own access. Load a matrix version |
| 2 | Role owner | The head of the unit whose staff hold the role: case operations, restructuring, legal and litigation, NPA and asset liquidity, debt sale, credit administration and write-off, control functions | Approve or reject each grant of a role they own. Confirm the separation of duty check. Recertify the holders of their roles at each review | Grant a role they do not own. Carry out a grant |
| 3 | Access administrator | Chief Debt Recovery Management Office (assumed, G1) | Carry out approved grants and removals in the bank IAM. Run the review cycle. Follow up leavers | Approve a grant. Hold a role owner position for the same roles |
| 4 | Line manager | The person's manager | Request a role for a team member. Confirm movers and leavers | Approve the request they raised |

Four technical positions support the business levels and decide no business grant.

| Position | Role code | Held by | Does |
|---|---|---|---|
| Security administrator | RW-SECADM | SCB IT security | Maintains the Entra ID groups and the IAM link. Approves and reviews break-glass use |
| Platform administrator | RW-PLATADM | ACE team and TechX platform | Runs the environments. Holds no permanent access to case data. Takes break-glass access only under an open incident |
| Reference data administrator | RW-REFADM | Center of excellence | Loads an approved roles, permission matrix, scope or masking version. Approves none of them |
| Internal audit | RW-AUDIT | Internal audit | Reads the access log and every version in force on any date. Changes nothing |

## 3.3 Who does what

| Action | App owner | Role owner | Access admin | Line manager | Security admin | Platform admin | Ref data admin | Compliance | Audit |
|---|---|---|---|---|---|---|---|---|---|
| Add or change a role in the roles table | A | R |  |  |  |  | D |  | V |
| Change the permission matrix | A | R |  |  | V |  | D |  | V |
| Change a masking rule | V |  |  |  |  |  | D | A | V |
| Map an Entra ID group to a role | A |  |  |  | D |  |  |  | V |
| Grant a role to a person |  | A | D | R |  |  |  |  | V |
| Move a person between roles |  | A | D | R |  |  |  |  | V |
| Remove a leaver |  |  | D | R |  |  |  |  | V |
| Recertify the holders of a role | A | D | D |  |  |  |  |  | V |
| Take break-glass access |  |  |  |  | A | R |  |  | V |
| Review break-glass use | V |  |  |  | D |  |  | V | V |
| Read the access log | V | V | V |  | V |  |  | V | V |

A approves. D does the work. R requests. V views. A blank cell means no part in the action. A role owner views the access log for their own roles only.

## 3.4 If the bank chooses central administration

- Level 3 moves from the Chief Debt Recovery Management Office to the bank's central IAM team.

- Role owners still approve each grant, because only the unit head can judge who needs a recovery role.

- The application owner still signs each access review.

- Nothing in the Workbench build changes. Training and the access tests in section 10 move to the central team.

# 4. Roles and permissions

## 4.1 Role classes

| Class | Roles | Signs in to the Workbench | Identity |
|---|---|---|---|
| Bank user | 37 | Yes | Entra ID, bank account |
| Partner user | 7 | Not until external access is approved (G3) | A partner identity through an external gateway |
| Customer party | 4 | No. Customers, guarantors, heirs and bidders are parties on a case and reach the bank through the existing channels | None in the Workbench |
| Non-human actor | 6 | Acts under a service identity | Managed identity |
| Total | 54 |  |  |

The six non-human actors are the case workflow module, the rules component, the data load from COLLINS, the OCR and extraction pipeline, the decision log writer and the agent platform. Every role with its permissions is listed in the Users, roles and permissions workbook.

## 4.2 Role rules

- A role is named for a job, never for a person.

- Every role has one role owner and a default scope: own, team, region or all.

- No role inherits from another. A person who needs two roles holds both, and the permissions of both apply.

- A role, a permission, a scope rule and a masking rule are each a data row with a version and an effective date. A change is a validated load, not a code release.

- A capability area with no letter for a role refuses every action in that area.

- Masking is applied before data reaches a screen or an agent. A role sees a personal data field unmasked only where its masking rule allows it.

- There is one Entra ID group per role per environment. Membership of the group is the only way to hold the role.

- A session keeps the versions it resolved at sign-in until it ends. The next session uses the versions then in force.

## 4.3 The parts of a permission

| Part | Values | Held in | Owner |
|---|---|---|---|
| Operation | C create, R read, U update, D delete, A approve | Permission matrix | Application owner |
| Capability area | Case record; queue and allocation; treatment and offer; litigation; asset and disposal; debt sale; write-off and posting; documents; rules and parameters; reference data; decision log; partner portal; reporting; platform administration | Permission matrix | Application owner |
| Scope | Own, team, region, all | Scope rules | Role owner |
| Masking | Masked or unmasked, per personal data field | Masking rules | Compliance |
| Approval limit | Decision type and amount per approval level | Delegation of authority table | Risk with the product heads |

Scope filters the records first and the permission is checked second. A record outside a person's scope is never returned, and the count of records excluded is never shown.

## 4.4 Roles with real users at each release

Epic 1, released on 30 November 2026, delivers the foundation with no business screens. At that release only the administration roles hold real users: security administrator, platform administrator, reference data administrator, center of excellence analyst, data steward, Compliance and internal audit. Each business role has named test users in SIT and UAT. Business roles receive real users from the release that gives them a screen, starting with Epic 2 in December 2026. This position is assumed until the business lead confirms the list (G6).

# 5. Request, grant and removal

## 5.1 Joiner

| Step | Who | Action | Where | Record |
|---|---|---|---|---|
| 1 | Line manager | Raises a request naming the person, the role and the reason | Bank IAM | IAM request |
| 2 | Role owner | Approves or rejects, after checking the conflict table in section 6.1 | Bank IAM | IAM approval |
| 3 | Access administrator | Adds the person to the Entra ID group for the role in each environment requested | Bank IAM to Entra ID | Group change |
| 4 | The person | Signs in with multi-factor authentication | Workbench | Sign-in in the access log |
| 5 | Workbench | Resolves the roles, scope and masking. The first screen names the roles and the scope in one line | Workbench | Session in the access log |

## 5.2 Mover, leaver and review

| Event | What happens | Control |
|---|---|---|
| Mover | One request removes the previous roles and adds the new ones in the same change. The owners of both the old and the new roles approve. | A mover never holds both sets of roles |
| Leaver | The line manager or the HR leaver record starts removal from every Workbench group. The open session ends at the next request and no new session can start. | Removal within the leaver response time (G5) |
| Periodic review | Each role owner recertifies every holder of their roles. A holder who is not recertified is removed. The application owner signs the result. | At the review interval (G5) |
| No role | A person who signs in with no role is refused with the message: You have no Recovery Workbench role. Ask your team manager to request one. | The refusal is written to the access log |

## 5.3 Break-glass

- A platform administrator requests access beyond their role, naming the open incident, the capability area, the scope and the reason in at least 20 characters.

- The security administrator approves. A request with no open incident is refused.

- The grant ends when its window ends, with no action by anyone. The screen shows that break-glass is active and the time remaining.

- Every action under break-glass is marked as break-glass in the access log with the incident reference.

- The security administrator reviews the use inside the review window (G5). An unreviewed use goes to the head of SCB IT security and to Compliance.

# 6. Separation of duty

## 6.1 Role pairs one person may not hold

| Role | May not also hold | Reason |
|---|---|---|
| Security administrator | Any business role | The person who maps groups to roles could grant themselves business access |
| Platform administrator | Any business role | Technical access combined with business access passes around scope and masking |
| Access administrator | Role owner for the same roles | One person would approve and carry out the same grant |
| Reference data administrator | Risk and model risk officer | Loading a delegation or rule version and approving it are separate steps |
| Center of excellence analyst | Risk and model risk officer | Writing a rule and approving it are separate steps |
| Restructuring officer | Credit approval committee member | Proposing a restructure and approving it are separate steps |
| Write-off team member | Write-off committee member | Proposing a write-off and approving it are separate steps |
| Internal audit | Any other role | Audit reads and changes nothing |

The role owner checks the table at step 2 of every grant. The Workbench checks it again at sign-in: a session that would hold a conflicting pair is refused, an incident is raised to the security administrator and the refusal is logged.

## 6.2 Maker and checker

- A person may not approve a decision they proposed or prepared, whatever their approval level.

- A person may not approve their own access request or review their own break-glass use.

- The person who requests a grant and the person who approves it are two different people.

- An agent may recommend. A person approves wherever the autonomy level of the step requires it.

# 7. Approval levels for recovery decisions

The bank sets approval authority for problem loans and for assets held for sale in Regulation กกค.540031, amended by กกค.690070: chapter 2 for problem loans and chapter 3 for assets held for sale. Chapter 2 does not cover credit cards, unsecured loans or auto loans. Those follow chapter 8 of credit approval regulation รบ.-กส.450032, amended by กกค.690085, or the product regulation. The Workbench covers hire purchase, so both regulations apply.

| Level | Problem loans, chapter 2 | Assets held for sale, chapter 3 |
|---|---|---|
| 1 | Board of Directors | Board of Directors |
| 2 | Executive Committee | Executive Committee |
| 3 | Problem Asset Resolution Committee | Management Committee |
| 4 | Head of Recovery, function level | Problem Asset Resolution Committee |
| 5 | Recovery executive, division level | Head of Recovery, function level, or Recovery executive, division level |
| 6 | Recovery executive, department level | No level 6 |

Problem Asset Resolution Committee is คณะกรรมการแก้ไขสินทรัพย์ที่มีปัญหา. Management Committee is คณะกรรมการจัดการ.

Chapter 2 sets limits for each of these decisions: debt restructuring; partial release of collateral; delay of legal action; the auction price; release of a guarantor; delay of seizure where the bank holds a preferential right; extension of the repayment period; cancellation of legal action; delay or suspension of an auction; write-off; recovery of written-off debt; new credit to a problem loan; transfer of claims to a third party; and release of a Thai Credit Guarantee Corporation guarantee. Chapter 3 sets limits for sale, lease, extension of a sale contract, and legal action on assets held for sale.

## 7.1 How an approval level attaches to a person

- The A letter in the permission matrix says a role may approve. The approval level and the delegation of authority table say which decision and up to what amount.

- An approval level belongs to a person in a position. It is held as data with effective dates, and it is not a role. A person who changes position changes level in the same change.

- Limits are held in the delegation of authority table exactly as the regulation states them: principal amount, loss as a percentage, and sale price against fair market value. A limit change is a data load approved by Risk.

- Committee levels approve by resolution. The Workbench records the decision once, with the resolution reference, the date and the members present.

- Each level names a substitute for when the holder is absent, with effective dates (G4).

- A decision that no limit covers goes to the next level up, and an incident records the missing limit.

- A decision already approved keeps the delegation version it was approved under.

# 8. Partners, customers and service identities

## 8.1 Partners

Seven partner roles exist: collection agencies, law firms, valuers, auction vendors, debt buyers and asset management companies, RAMC, and the Legal Execution Department. Opening the Workbench to users outside the bank makes it internet facing. That needs a change approved by the architecture team, with a lead time of one to three months. Law firms are first needed at Epic 5, litigation, in March 2027. A request made in November gives an answer between December 2026 and February 2027, so the request has to be raised in November.

Until external access is approved, partners keep the channels they use today: the LIT lawyer web for law firms, the OA portal for collection agencies, SVAF for valuers, HOME.SCB for asset buyers, and file exchange by SFTP.

Once approved, a partner user holds a partner identity separate from bank identities, signs in with multi-factor authentication, and is limited to the cases placed with their firm. The partner and agency manager requests partner users. The role owner approves. A partner account ends when the firm's contract ends. The permission matrix, masking and access log apply to partner users in the same way as to bank users.

## 8.2 Customers

Customers, guarantors, heirs and bidders do not sign in to the Workbench. They act through SCB Easy, LINE OA, branches and the contact center. A data subject request follows the bank's PDPA process.

## 8.3 Service identities

- Each non-human actor has its own managed identity, a role in the roles table and a named owner.

- Credentials are held in Key Vault. No identity is shared between actors.

- An agent identity holds only the permissions that the autonomy level of its step allows.

- Every action by a service identity is checked against the matrix and written to the access log, as for a person.

# 9. Access records

| Record | Holds | Read by |
|---|---|---|
| Workbench access log, inside the decision log | Sign-ins, refusals, grants and removals, the versions in force, break-glass use, every read of the case store, the document store and the recovery data. Append only | Application owner; role owners for their roles; security administrator; Compliance; internal audit |
| ACE audit log | Every change made through the service | Security administrator; internal audit |
| PII log through PII Kafka | Every read of a personal data field | Compliance; internal audit |
| SOC log | Security events for monitoring | SCB security operations |

Retention of each record follows the bank retention schedule, set in the records retention and archiving document.

# 10. How access is tested before each release

| Test | How | Passes when | Signed by |
|---|---|---|---|
| Sign-in | A test user for each role in the release signs in with multi-factor authentication | The session shows the right roles, scope and masking | Role owner |
| No role | A user with an Entra ID account and no Workbench group signs in | Refused with the message in 5.2; refusal in the access log | Security administrator |
| Scope | A case owner test user opens a case owned by another team | Nothing is returned; refusal in the access log | Role owner |
| Masking | Test users of three roles open the same case | Each sees personal data fields masked as the masking rules state | Compliance |
| Conflict | A test user is placed in two groups listed in 6.1 | The session is refused and an incident is raised | Security administrator |
| Leaver | A group is removed during an open session | The next request ends the session | Access administrator |
| Break-glass | One request with an open incident and one without | The first is granted for its window with every action marked; the second is refused | Security administrator |
| Matrix change | A new matrix version changes one permission | The change applies from its effective date with no code release | Application owner |

Test users exist in SIT and UAT only. The application owner accepts the access tests as part of the release sign-off.

# 11. Assumptions and gaps

| ID | Needed from the bank | Owner | By | Position used until answered | If the answer differs |
|---|---|---|---|---|---|
| G1 DL01 | Whether access is granted centrally or by the application owner | K. Tee | 28 Oct | Application owner administration, with the Chief Debt Recovery Management Office as access administrator | Level 3 moves to the central IAM team. No build change |
| G2 DL02 | Who the application owner is | K. Tee with K. Bell | 28 Oct | Tribe Lead, Collections and Recovery Tribe, for ACE as a whole; ACE team as technical custodian | Level 1 and the review sign-off move. No build change |
| G3 DL03 | Who makes the architecture change for external partner access | K. Book with the architecture team | 29 Oct | Partners stay on their existing channels | Each month of delay moves partner access in the Workbench one release later |
| G4 DL18 | Which person holds each approval level, and the substitute for each | Risk with the product heads | 30 Nov | The delegation of authority table is loaded with the regulation's levels and limits and no names | Approval routing in Epic 2 cannot pass user acceptance testing |
| G5 DL38 | The access review interval, the leaver response time and the break-glass review window | SCB IT security | 20 Nov | Review every six months; leaver within the same working day; break-glass reviewed within one working day. Each is a parameter | The parameter values change by data load. No build change |
| G6 DL39 | Which roles receive real users at each release | Business lead, Collections and Recovery Tribe | 20 Nov | Administration roles at Epic 1; business roles from Epic 2 | The provisioning list for each release changes |
| G7 DL40 | The Entra ID group names and the IAM entry for the Workbench roles | SCB IT security | 6 Nov | One group per role per environment, named to the bank standard | Group mapping is a data load. No build change |
