# MVP Requirements

## Owner And Recipient

Primary user and owner:

- Sherry George
- sherry.george@doceree.com
- Role: Owner/Admin

Daily PDF brief recipient:

- Sherry George only

## MVP Statement

The MVP is a local-first autonomous competitive intelligence command center that monitors the approved Day-1 competitor source cohort, creates evidence-backed findings, routes high-risk findings to review, generates a daily PDF brief, emails it to Sherry, and displays all activity in a dashboard-first UI.

## Must-Have Capabilities

1. Local application setup
2. Local PostgreSQL database
3. Sherry admin login
4. Product Spine seed
5. Competitor and Source Registry seed
6. 50-source MVP monitoring cohort
7. Source policy enforcement
8. Day-1 baseline crawl
9. Static and browser crawler
10. Diff and boilerplate suppression
11. Evidence Vault
12. Source health tracking
13. Evidence analysis queue
14. Core OpenAI agent runtime
15. Specialist research agents for MVP source types
16. Governance agents
17. Market Intelligence Orchestrator
18. Findings workflow
19. Human review workflow
20. Battlecard candidate workflow
21. Alert candidate workflow
22. Daily autonomous run
23. Daily brief generation
24. PDF generation
25. Email delivery to Sherry
26. Dashboard-first UI
27. Source Registry UI
28. Evidence Vault UI
29. Findings UI
30. Review queue UI
31. Daily Briefs UI
32. Agent Runs UI
33. Security and permissions
34. Audit logs
35. Safe mode
36. Backup and restore
37. Core test suite
38. Golden eval scaffold

## Daily Journey

1. System runs daily at 6:00 AM America/New_York.
2. System checks approved Day-1 sources.
3. System creates snapshots and diffs.
4. System creates evidence for meaningful changes.
5. System routes evidence to specialist agents.
6. Governance agents validate interpretation.
7. Orchestrator creates final findings or review items.
8. Daily Brief Agent creates report data.
9. PDF is generated.
10. Email is sent to Sherry.
11. Sherry opens dashboard.
12. Sherry reviews findings, warnings, and source failures.
13. Sherry approves, rejects, edits, or requests more evidence.

## Evidence Requirements

Every evidence record must include:

- Source URL
- Captured timestamp
- Source type
- Collection method
- Excerpt

Raw evidence must be immutable. Final findings must link to evidence.

## Finding Requirements

Every final finding must include:

- Linked evidence
- Severity score
- Confidence score
- Product mapping or unmapped/category-level reason
- Source caveats where needed
- Review status where required

Low-confidence findings must remain visibly labeled.

## Review And Approval Requirements

- Severity 4 and 5 findings route to Sherry review.
- CEO alerts require Sherry approval.
- Sales alerts require Sherry approval.
- Battlecard publication requires Sherry approval.
- Specialist agents cannot create final findings directly.

## Security Requirements

- Password-protected app
- Admin-only settings
- Server-side permissions
- Secrets in environment variables only
- No secrets in logs
- No public PDF links
- Storage folder not exposed directly
- Audit logs for important actions

## Local Operations Requirements

- Safe mode
- Backups
- Restore workflow
- Health checks
- Source failure visibility
- Worker heartbeat visibility

## Milestone 0 Status

Milestone 0 creates this documentation only. The capabilities above are requirements for later milestones, not completed implementation.
