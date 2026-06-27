# Docket Intelligence Workbench

**Monitor court cases, preserve historical docket snapshots, detect meaningful changes, organize filings, and analyze case records with source-grounded AI.**

> Status: public architecture and MVP foundation. The repository is being built as a portfolio-grade, self-hostable workbench with a sanitized demonstration environment.

## What works now

- FastAPI health, case, parser, and snapshot-comparison endpoints
- Domain models for cases, docket entries, snapshots, and detected changes
- Deterministic SHA-256 snapshot hashing
- Added, removed, and modified entry detection
- Parser-first Cuyahoga County Common Pleas adapter
- Sanitized docket fixture and automated tests

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn docket_workbench.api.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive API.

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

## Product boundaries

This project is **case-monitoring, document-analysis, compliance, and communication infrastructure**. It is not a law firm and does not provide legal representation.

The platform may explain source records, surface inconsistencies, generate timelines, and help users organize information. It should not automatically file documents, make legal decisions, contact judges or probation officers on a user's behalf, or present inferred intent as established fact.

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

The public workbench contains the reusable application, source-adapter contract, reference connector, tests, synthetic fixtures, and local deployment. Customer data, production credentials, private deployments, and customer-specific integrations remain outside this repository.

## Documentation

See [Foundation](docs/FOUNDATION.md) for the product vision, source-repository inventory, target architecture, domain model, security boundaries, and MVP backlog.

## Public demo principles

The public demonstration will use synthetic, redacted, or clearly public records. It will not expose private case documents, customer information, production credentials, or personal legal strategy.

Detected differences are described neutrally—for example:

- Historical snapshot difference
- Missing-entry candidate
- Record-integrity warning
- Potential anomaly requiring human review

The software can show that records differ. It should not claim that a difference proves intent.

## Roadmap

1. Persist cases, monitoring runs, raw captures, and snapshots in PostgreSQL.
2. Port authorized-case Playwright acquisition from the private Cuyahoga scraper.
3. Add the Next.js case dashboard and historical comparison view.
4. Ingest filings and provide source-cited search and Q&A.
5. Add alerts, audit history, Docker deployment, and a public demo.

## Author

Designed and built by [Giorgiy Shepov](https://github.com/george-shepov), focusing on software architecture, court-data acquisition, document pipelines, AI retrieval, workflow automation, infrastructure, and deployment.

## License

No open-source license has been selected yet. Until a license is added, the source is publicly viewable but remains all rights reserved.
