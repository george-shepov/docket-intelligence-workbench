# Docket Intelligence Workbench

**Monitor court cases, preserve historical docket snapshots, detect meaningful changes, organize filings, and analyze case records with source-grounded AI.**

> Status: architecture and MVP foundation. The public repository is being built as a portfolio-grade, self-hostable workbench with a sanitized demonstration environment.

## Why this exists

Court dockets and filings are often scattered across court websites, downloaded documents, email notices, and local folders. Legal professionals and self-represented litigants may repeatedly check the same pages, reconstruct timelines manually, and compare records by eye.

Docket Intelligence Workbench is designed to turn that repetitive work into a monitored workflow:

1. Add a case and its public court source.
2. Schedule monitoring by case.
3. Preserve each retrieved docket as an immutable snapshot.
4. Normalize entries and compare them with earlier snapshots.
5. Identify new, changed, removed, or reclassified entries.
6. Download and hash available filings.
7. Build a searchable case timeline.
8. Ask questions and receive answers with citations to source documents.
9. Deliver alerts when a meaningful event occurs.

## Intended users

- Law firms and legal operations teams
- Litigation-support and compliance professionals
- Journalists and public-record researchers
- Self-represented litigants organizing their own records
- Developers building court-data connectors and document workflows

## Product boundaries

This project is **case-monitoring, document-analysis, compliance, and communication infrastructure**. It is not a law firm and does not provide legal representation.

The platform may explain source records, surface inconsistencies, generate timelines, and help users organize information. It should not automatically file documents, make legal decisions, contact judges or probation officers on a user's behalf, or present inferred intent as established fact.

## MVP

The first complete vertical slice will support:

- Case creation and watchlists
- Per-case monitoring schedules
- A Cuyahoga County Common Pleas source adapter
- Immutable docket snapshots
- Entry normalization and historical comparison
- Meaningful-event detection
- Filing download, hashing, and indexing
- Timeline and change-history views
- Email alerts and digests
- Source-cited document questions and answers
- Audit history for monitoring runs and analysis

## Architecture direction

```text
Web application
├── Accounts, organizations, and cases
├── Timeline, documents, and cited Q&A
├── Monitoring settings and alerts
└── Administration and audit history
        │
        ├── Monitoring scheduler and workers
        ├── CourtSourceAdapter interface
        │      ├── Cuyahoga Common Pleas adapter
        │      └── Future court adapters
        ├── Snapshot and comparison engine
        ├── Document ingestion and retrieval
        └── Notification services
```

The public workbench will contain the reusable application, source-adapter contract, reference connector, tests, synthetic fixtures, and local deployment. Customer data, production credentials, private deployments, and customer-specific integrations remain outside this repository.

## Documentation

- [Product vision](docs/PRODUCT_VISION.md)
- [Current repository inventory](docs/CURRENT_REPOSITORY_INVENTORY.md)
- [Target architecture](docs/TARGET_ARCHITECTURE.md)
- [Domain model](docs/DOMAIN_MODEL.md)
- [MVP backlog](docs/MVP_BACKLOG.md)
- [Security and privacy](docs/SECURITY_AND_PRIVACY.md)
- [Architecture decisions](docs/adr/)

## Public demo principles

The public demonstration will use synthetic, redacted, or clearly public records. It will not expose private case documents, customer information, production credentials, or personal legal strategy.

Detected differences will be described neutrally—for example:

- Historical snapshot difference
- Missing-entry candidate
- Record-integrity warning
- Potential anomaly requiring human review

The software can show that records differ. It should not claim that a difference proves intent.

## Technology direction

The initial implementation will reuse proven components from related private projects while establishing a clean public history:

- FastAPI API and background services
- PostgreSQL for durable application state
- Redis-backed scheduling/worker execution when required
- Next.js web application
- Docker Compose for local evaluation
- Playwright-based court connectors
- Pluggable AI and embedding providers
- Automated tests and fixture-based connector validation

## Roadmap

1. Architecture and domain foundation
2. Case and monitoring-run API
3. Source-adapter contract and reference connector
4. Immutable snapshots and docket comparison
5. Documents, timeline, and cited Q&A
6. Alerts, audit history, and hosted demonstration
7. Private deployment and organization features

## Author

Designed and built by [Giorgiy Shepov](https://github.com/george-shepov), focusing on software architecture, court-data acquisition, document pipelines, AI retrieval, workflow automation, infrastructure, and deployment.

## License

No open-source license has been selected yet. Until a license is added, the source is publicly viewable but remains all rights reserved.