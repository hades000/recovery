# Source documents consulted

Every source document that an AISDLC stage cited while building Build Sequence v6 orders 1 to 10.

- The documents are not copied into this repository. They are in the programme document set v14,
  and every path below is relative to that set's root.
- To check a citation, hash the file with SHA-256 and compare it with the value below.
- `evidence/document-set-baseline.sha256` holds the hash of every file in the set as it was before
  delivery started. Hashing the set again at the end shows it was not changed.
- The converted copies in `17 AI-First SDLC Repository v2/requirement/legacy/` are the Markdown text
  the agents read. Each one names the original `.docx` or `.xlsx` it was converted from.

| Document (name, version) | Path in the document set | SHA-256 | Cited by |
|---|---|---|---|
| Decision Log v10 | `01 Decisions and governance/Recovery Workbench Decision Log v10.xlsx` | `b83e1fb3878053ab10991d6195288f6377b08d181d2eb9b23898e71340365c49` | All four (D-RCV-28, -35, -36, -50 and others) |
| Squad decision register (AISDLC v2 workspace) | `17 AI-First SDLC Repository v2/docs/decisions/decision-register.md` | `3e7e77e06edbeba3a1fbd116327ee9d7f3d292e6cb7be885be422ff185aeff5f` | All four |
| AGENTS.md v2 (AISDLC v2 workspace) | `17 AI-First SDLC Repository v2/AGENTS.md` | `1e481e0f19dc2180df3c32bd5686e9baef44315099511ca99d1426b27080722c` | All four; copied to this repo root |
| Backend standards (AISDLC v2 context) | `17 AI-First SDLC Repository v2/.github/contexts/backend-standards.md` | `dc46e8f61956eab2467692ca4196eddfa4c483f090b658b9ced96d7edf40f71c` | RWB-E1-044, RWB-E1-042 |
| Architecture Decision Records v3 | `05 Technical architecture/Recovery Workbench Architecture Decision Records v3.md` | `1b37f4439404a02cec1e57bdf0794d21d6630aa9954d8932a22b5cbf660b9829` | RWB-E1-044, RWB-TE-001, RWB-TE-002 |
| ACE Architecture Decision v3 | `05 Technical architecture/Recovery Workbench ACE Architecture Decision v3.docx` | `f93515f99e85b1284550a2878c0c885a4017f3564987d04984ca32ca44472728` | RWB-E1-044 (ADR-010 boundary) |
| Epic 1 story files v7 (archive) | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip` | `501b20bf00f1160f4a77df8dee53b4108d3008919ca20cc3d1f08e33fca8b160` | All four |
| RWB-E1-044 story file v7 | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 044 Database migrations versioned with parameterized schema names v1.md` | `0adbd6bdf8256e6456afb2179b6cd216117f409ebc7703d21c2634d508bc547b` | RWB-E1-044 |
| RWB-TE-001 story file v7 | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB TE 001 Recovery module folder and boundary test v1.md` | `475c3f31daab244e8e05a7124ee27a9dd4aa03db00754a6ca1624696f1e19a65` | RWB-TE-001 |
| RWB-E1-042 story file v7 | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 042 Central configuration service and parameter catalog v1.md` | `f1fc36e7d400283dbc9967282109b914cf8d013c5eab706150b0be76fc1f4f9a` | RWB-E1-042 |
| RWB-TE-002 story file v7 | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB TE 002 Code owners for the recovery module v1.md` | `2cfdccfcc5bf387a337a82badc1e25f503e2e55507787b63fce585fc0f745ff6` | RWB-TE-002 |
| RWB-E1-043 story file v7 | `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 043 Reference data service with versioned tables v2.md` | `ce0e905f1b015e38f6c3dbd300e7079a126e36f23e3dc1ae621e911683b06587` | RWB-E1-042 (split of work); next story |
| ACE Team Stories v1 | `04 User stories/Recovery Workbench ACE Team Stories v1.md` | `01b03b596429ab9ff792714dc18f78727ed2a953b8685797d5146359923b98da` | RWB-E1-044 (RWB-ACE-001) |
| Build Sequence Epic 1 and Epic 2 v6 | `11 Delivery and operations/Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx` | `9b0b6fe8e491fc10509b5ae7a390b2c1f5cc8896a13ef6dd193640fb693837c0` | All four (order 1 to 4) |
| Physical Schema v6 | `06 Data/Recovery Workbench Physical Schema v6.sql` | `76cbfb835be6135a4f0d55cf3f6a7fda81910f31fd6045cabbef3a9b8e7bce5a` | RWB-E1-042, RWB-E1-044 |
| Data Classification and Personal Data Inventory v4 | `06 Data/Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx` | `f0fca0a1f0c67f74e4c8c689b3ccc83da3382a46fa4d7b56065445cee1a70077` | RWB-E1-042 |
| API Specification v4 (YAML) | `05 Technical architecture/Recovery Workbench API Specification v4.yaml` | `535cb46594190f0bf535a2ad3f034e9f50f987a92fe19c0524a2755f5923b891` | RWB-E1-042 |
| Event and Messaging Design v4 | `05 Technical architecture/Recovery Workbench Event and Messaging Design v4.md` | `cc57cec8b1a37f22a195a070387ec98598644e3b8d57f697d5ffb7f8f0cadb51` | RWB-E1-042 |
| Environment and Deployment Design v4 | `05 Technical architecture/Recovery Workbench Environment and Deployment Design v4.docx` | `6d6b0badead669b182c00b8d7973bb7053241421dc3b73700e9587750a093ac0` | RWB-E1-044 |
| Audit and Logging Design v2 | `05 Technical architecture/Recovery Workbench Audit and Logging Design v2.docx` | `a713e215bfa422fe57bf342723e644dedbc58fab28348be3c3768be1e1f5bd1a` | RWB-TE-001 (trace ID) |
| Error and Message Standard v4 | `07 Screens and experience/Recovery Workbench Error and Message Standard v4.docx` | `2d81e1371f6aa7114bc9b2689a74fa04248e383140077d88122a38d4d623d1e6` | RWB-E1-042 |
| Users, Roles and Permissions v4 | `02 Business architecture and process/Recovery Workbench Users Roles and Permissions v4.xlsx` | `2acfb36d0da4294c50026efa535ec6a3c91c9f01f54dfb92c256d7d8bf25fc08` | RWB-E1-042 |
| Engineering Practices v5 | `11 Delivery and operations/Recovery Workbench Engineering Practices v5.docx` | `da2b4aed5f59f7d030274041621ad17aa88de65e2c8e7a23b5f615665eeb263c` | RWB-TE-002 |
| AI Assisted Development Approach v1 | `08 AI and agents/Recovery Workbench AI Assisted Development Approach v1.md` | `d34f69c01981fa886e0879979a8e09624318c8135da2493d4bac70d2b1ad0ca2` | RWB-TE-002; AGENTS.md section 7 and 9 |
| Test Cases v7 | `09 Testing and quality/Recovery Workbench Test Cases v7.xlsx` | `dd09e80a2d25bf9079a1172493f77c9d2393aaf6efaad13927387ae27ef19e28` | All four |
| Non Functional Specification v3 | `03 Requirements and specifications/Recovery Workbench Non Functional Specification v3.docx` | `189474be4e9ae1ffbbbc1d9d56958d224d597df2be68f17aad09a839767a44db` | RWB-E1-042 |
| RWB-E1-042 Clarification Pack | `E1-042 Migration and Clarifications/RWB-E1-042 Clarification Pack.md` | `2bb9a2d08682cc9df5ffbc387d35c46f981f6b38ec825970fd3d145f5af9c5fa` | RWB-E1-042 |
| RWB-E1-042 parameter catalog (clarification) | `E1-042 Migration and Clarifications/config/parameter-catalog.csv` | `0e2b00d61dca35e69315524de633573ec801bccc15795709c6d7478bb2d42fbf` | RWB-E1-042 |
| RWB-E1-042 messages (clarification) | `E1-042 Migration and Clarifications/config/messages-e1-042.csv` | `c2073c9f55a4263d48cf8bae0415f09772a07a35706d3ff96a16c003b84c53cc` | RWB-E1-042 |

These are the principal documents the four built stories (RWB-E1-044, RWB-TE-001, RWB-E1-042, RWB-TE-002)
cite. Each stage's own artefacts name further sections and rows. The hashes are from
`evidence/document-set-baseline.sha256` (17 Nov 2026 23:03). The re-hash on 19 Nov 2026 gave the same value
for every file listed here (`evidence/docset-integrity.md`).
