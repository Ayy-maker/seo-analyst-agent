# PRD: SEO Analyst Agent

## 1. Overview

We need an AI SEO Analyst that ingests SEO reports (CSV, XLSX, PDF, JSON), interprets them, and generates structured insights, recommendations, and monthly reviews. This replaces manual analysis, speeds up reporting, and ensures consistent SEO advice.

## 2. Goals

- Automate intake of SEO reports.
- Standardize data across keywords, technical, backlinks, on-page, and traffic.
- Produce actionable insights prioritized by impact.
- Deliver client-friendly summaries and technical action logs.
- Track historical performance and trends.

## 3. Inputs

- Google Search Console exports
- SEMrush / Ahrefs / Moz reports
- Google Analytics reports
- Technical SEO audit exports (Screaming Frog, Sitebulb, etc.)
- Backlink reports
- Content inventory CSVs

## 4. Outputs

- **Executive Summary** (plain language, client-friendly).
- **Action Plan** (prioritized fixes: high, medium, low).
- **Module Reports**:
  - Keyword performance (rankings, CTR, wins/losses).
  - Technical SEO (crawl/indexation, Core Web Vitals).
  - On-page SEO (metadata, schema, content gaps).
  - Backlinks (toxic, new, lost, competitor).
  - Traffic & conversions (landing page trends).
- **Dashboard Data** (exportable to Google Sheets/Notion).
- **Alerts** (critical issues: ranking drops, 404 spikes).

## 5. Roles

- **Analyst Agent**: Reads reports, extracts insights.
- **Critic Agent**: Reviews recommendations for accuracy.
- **Reporter Agent**: Formats into summaries + action plans.
- **Notifier Agent** (Phase 3): Sends alerts.

## 6. Workflow

### Report Intake
- Manual upload → parse and store.
- Map source type to correct module.

### Analysis
- Keyword trends.
- Technical health.
- Content & on-page.
- Backlinks.
- Traffic performance.

### Report Generation
- Executive summary.
- Action plan with priorities.
- Trend comparison vs last report.

### Delivery
- Export to Google Docs/Sheets/Notion.
- Client-ready PDF.
- Internal task log (CSV/JSON).

## 7. Phases & Acceptance Criteria

### Phase 1 (MVP) – Manual Reports

**Features:**
- ✓ Input: User uploads 2–3 types of reports.
- ✓ Analyst Agent parses and extracts insights.
- ✓ Reporter Agent outputs summary + action plan.
- ✓ Outputs accurate and client-readable.

**Acceptance Criteria:**
- Analyst correctly recognizes top/worst keywords from Search Console CSV.
- Generates at least 5 actionable recommendations.
- Summaries are less than 300 words and non-technical.

### Phase 2 – Automated Data Pipeline

**Features:**
- ✓ Integrate with APIs (GSC, Analytics, Ahrefs).
- ✓ Store historical data in Notion/Sheets.
- ✓ Enable comparisons (month-over-month trends).

**Acceptance Criteria:**
- API pull works reliably.
- Trends are displayed side-by-side.
- Dashboard updates automatically.

### Phase 3 – Notifications & Dashboards

**Features:**
- ✓ Slack/Email alerts for major SEO issues.
- ✓ Notion/Sheets dashboards for KPIs.

**Acceptance Criteria:**
- Alerts triggered within 24h of issue detection.
- Dashboard shows current month and last 2 months.

### Phase 4 – Advanced Intelligence

**Features:**
- ✓ Forecast traffic based on ranking changes.
- ✓ Competitor intelligence (SERP scrape, keyword gap).
- ✓ Integration with WordPress/Astro to suggest live improvements.

**Acceptance Criteria:**
- Forecast accuracy within 15% of actual next-month traffic.
- Competitor gap analysis identifies at least 10 missing keywords per audit.

## 8. Environment & File Structure

```
seo-analyst/
  ├── data/                # Uploaded & parsed reports
  ├── agents/
  │     ├── analyst/       # Extract insights
  │     ├── critic/        # Validate
  │     ├── reporter/      # Format output
  │     └── notifier/      # Alerts (later)
  ├── outputs/
  │     ├── summaries/
  │     ├── action-plans/
  │     ├── dashboards/
  │     └── alerts/
  ├── config/
  │     ├── env.json       # API keys, thresholds
  │     └── prompts/       # Master & module prompts
```

## 9. Test Plan

- Feed past reports → validate insights match human analyst conclusions.
- Cross-check technical SEO recommendations with Screaming Frog output.
- Test formatting for client-ready summaries.
- Simulate ranking drop → check if alerts trigger.

## 10. Risks & Mitigation

- **Parsing issues with PDFs** → prefer CSV/XLSX where possible.
- **Overload of recommendations** → enforce top 5 priorities per section.
- **False positives in backlinks** → require Critic Agent review.
