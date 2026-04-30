# Scope Lock

## MVP Definition

The MVP is a local-first autonomous competitive intelligence command center for Sherry. It monitors the approved Day-1 competitor source cohort, creates evidence-backed findings, routes high-risk findings to review, generates a daily PDF brief, emails it to Sherry, and displays activity in a dashboard-first UI.

## MVP Must Prove

- The system can run independently.
- The system can collect evidence safely.
- The system can detect meaningful competitor change.
- The system can analyze evidence with agents.
- The system can create source-backed findings.
- The system can keep low-confidence and high-risk findings reviewable.
- The system can generate and email a useful daily brief.
- The system can expose failures instead of hiding them.
- The system can be backed up and restored.
- The system can be tested and trusted.

## Included Source Scope

MVP automation may use only approved Day-1 source registry rows, including approved public:

- Competitor websites
- Official homepages
- Product pages
- Solution pages
- Newsroom pages
- Press release pages
- Blogs
- Careers pages
- Public docs or release notes included in the Day-1 registry
- Public case study pages included in the Day-1 registry
- Public partner or integration pages included in the Day-1 registry

Manual uploads are allowed only when access basis is recorded.

## Day-1 50-Source Cohort Rule

Only the 50-source MVP cohort is scheduled by default. All post-MVP sources remain inactive unless Sherry manually promotes them.

## Excluded Automated Source Scope

MVP automation must not collect from:

- LinkedIn company pages
- Executive LinkedIn profiles
- Private social platforms
- Restricted social platforms without approved API, vendor, or manual export
- Analyst reports through automation
- Gated webinars through automation
- Paid reports through automation
- Login-required portals
- Paywalled sources with unknown access basis
- CAPTCHA-gated sources
- Private groups
- Contact databases
- Review sites unless specifically approved
- Patent databases
- Trademark databases
- Podcast or video sources
- Ad libraries

## Competitor Scope

MVP includes competitors present in the Product Spine / Competitor and Source Registry seed and included in the 50-source MVP monitoring cohort.

Post-MVP competitors may appear as inactive, backlog, or discovery records. They must not appear in the daily crawl plan, scheduler active cohort, or daily brief as monitored competitors unless promoted by Sherry.

## Product Spine Scope

The MVP includes Product Spine seeding for:

- Doceree product registry
- Journey stages
- Confirmed claims
- Inferred claims
- Needs confirmation claims
- Product keywords
- Negative keywords
- Competitive signal mapping rules
- Battlecard triggers
- Severity guidance
- Confidence guidance
- Open questions

## Product Claim Rules

- Confirmed claims may be reused as approved Doceree messaging.
- Inferred claims must remain labeled as inferred.
- Needs confirmation claims must not be used as approved Doceree positioning.
- Competitor findings must cite external source URL and access date.
- Doceree product truth must stay separate from competitor descriptions.

## Agent Scope

MVP active agents may include:

- Website Change Hunter
- News / PR Agent
- Docs / Release Notes Agent
- Jobs Signal Agent
- Partnership / Integration Agent
- Case Study / Proof Point Agent
- Manual Upload Classifier
- Evidence Validator
- Source Compliance Guardrail
- Product Mapper
- Severity Scorer
- Confidence Scorer
- Overclaiming Guardrail
- Duplicate Detector
- Prompt Injection Guardrail
- Market Intelligence Orchestrator
- Daily Brief Agent
- PDF Report Agent
- Source Health Agent
- Ask War Room Agent

Agents listed for later source types or integrations must stay inactive unless the milestone explicitly activates them inside MVP scope.

## Explicit Scope Stop Conditions

Stop before implementation if a requested task would:

- Activate post-MVP sources.
- Crawl forbidden sources.
- Treat manual uploads as crawler targets.
- Send CEO/Sales alerts without Sherry approval.
- Publish battlecards without Sherry approval.
- Create final findings without evidence.
- Hide source failures.
- Hide low-confidence labels.
- Commit secrets, raw HTML, PDFs, screenshots, backups, logs, or database dumps.
