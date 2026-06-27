# Foundation

## Product vision

Court records are usually organized for publication, not for sustained monitoring. Users repeatedly check the same pages, download filings into unrelated folders, reconstruct timelines manually, and have no reliable way to see how a public docket changed over time.

Docket Intelligence Workbench converts a public case record into a monitored, searchable workspace:

- preserve what the source showed at each capture;
- distinguish source evidence from system analysis;
- detect meaningful additions, removals, and modifications;
- organize filings and generated timelines;
- answer questions with traceable citations;
- notify users according to a case-specific schedule.

## Porting inventory

This repository is a curated destination, not a wholesale copy of earlier experiments.

| Source repository | Reusable capability | Porting decision |
|---|---|---|
| `professional_legal_tax_assistant` | FastAPI/Next.js shell, case management, document ingestion, RAG, authentication, operations | Port selected patterns and cleaned modules; exclude private data, credentials, legacy UI, and unrelated agents |
| `cuyahoga_cp_scraper` | Cuyahoga acquisition, scheduled jobs, PDF retrieval, operational scripts | Implement behind the `CourtSourceAdapter` boundary; start with deterministic parsing and fixtures |
| `docket-pro` | Hashing, normalization, historical comparison, anomaly surfacing | Port record-integrity concepts with neutral terminology and tests |
| `docket-tracker` | Monitoring workflow experiments | Review for scheduling and alert behavior |
| `court-document-dev` | Document-processing experiments | Review for ingestion and citation components |
| `AI-Law-Firm` | Legal workflow experiments | Treat as research; do not import broad legal-agent claims into the MVP |

### Porting rules

- No private case files, customer data, logs, database dumps, or generated evidence.
- No committed credentials, browser profiles, cookies, or copied `.env` files.
- No raw Git history import from private repositories.
- Prefer clean implementation with provenance explained in pull requests.
- Add sanitized fixtures and tests before enabling live acquisition.
- Keep broad courthouse analytics separate from hosted user-authorized monitoring.

## Target architecture

```text
Next.js web application
        │
        ▼
FastAPI application API
├── identity and organizations
├── cases and watchlists
├── timelines and change history
├── documents and cited questions
└── monitoring configuration
        │
        ├── PostgreSQL: durable relational state
        ├── object storage: immutable captures and documents
        ├── vector store: document retrieval
        └── queue/scheduler
                 │
                 ▼
          monitoring workers
          ├── CourtSourceAdapter registry
          ├── source acquisition
          ├── parsing and normalization
          ├── snapshot comparison
          ├── document ingestion
          └── alerts and audit events
```

Each court connector separates two operations:

1. **Capture** the source with an appropriate client, such as Playwright.
2. **Parse** already captured bytes without network access.

This keeps parsing deterministic and allows sanitized regression fixtures.

## Domain model

- **Organization** — tenant boundary for users, cases, policies, and billing.
- **User** — authenticated person with an organization role.
- **Case** — monitored legal matter identified by court and case number.
- **CourtSource** — adapter definition for a public record system.
- **CaseSourceSubscription** — source URL plus monitoring schedule.
- **MonitoringRun** — one acquisition attempt with status and diagnostics.
- **RawCapture** — immutable bytes plus SHA-256 hash.
- **DocketSnapshot** — normalized docket state derived from a capture.
- **DocketEntry** — one published docket row.
- **DetectedChange** — added, removed, or modified entry requiring review.
- **DocumentVersion** — immutable filing plus provenance and extraction state.
- **TimelineEvent** — normalized event derived from a source entry or document.
- **Alert** — delivery record for a meaningful event.
- **AuditEvent** — security and operational history.

Every derived object must retain provenance to the source that supports it. Analysis cannot silently replace evidence.

## Security and privacy

Never commit credentials, private case documents, customer information, authenticated browser state, database dumps, logs, uploads, or backups.

Hosted monitoring is intended for cases explicitly added by a user, party, or authorized attorney. Raw captures and downloaded documents receive integrity hashes and immutable metadata. AI answers about case content require source references and are labeled as generated analysis.

## MVP backlog

### Completed in the foundation branch

- [x] Public product positioning
- [x] Domain models for cases, entries, snapshots, and changes
- [x] Deterministic snapshot hashing
- [x] Added/removed/modified comparison
- [x] Parser-first Cuyahoga adapter
- [x] Sanitized HTML fixture
- [x] Minimal FastAPI case and comparison endpoints
- [x] Unit and API tests

### Next

- [ ] PostgreSQL models and migrations
- [ ] Organization and user ownership
- [ ] Immutable raw-capture metadata
- [ ] Monitoring-run state and diagnostics
- [ ] Port authorized-case Playwright capture from `cuyahoga_cp_scraper`
- [ ] Rate limits, retries, backoff, and source-health diagnostics
- [ ] Filing download queue
- [ ] Next.js case dashboard
- [ ] Documents, search, and cited Q&A
- [ ] Alerts, audit history, Docker stack, and public synthetic demo
