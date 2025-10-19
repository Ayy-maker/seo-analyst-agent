# Technical Report

**Generated**: October 18, 2025

## Performance Overview

This module shows 3 critical issues requiring immediate attention. Total of 5 findings identified with actionable recommendations.

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Findings | 5 |
| High Severity | 3 |
| Medium Severity | 2 |
| Low Severity | 0 |


## Insights

### 1. Found 2 pages with errors

**Severity**: HIGH

**Metrics**:
- 4Xx Errors: 1
- 5Xx Errors: 1
- Total Errors: 2

**Recommendation**: Fix 404 errors with redirects or restore content. Resolve 5xx server errors immediately as they impact crawling.

---

### 2. 1 important pages are non-indexable

**Severity**: HIGH

**Metrics**:
- Count: 1

**Recommendation**: Review robots.txt, meta robots, and X-Robots-Tag headers. Ensure important content is indexable.

---

### 3. 6 pages failing Core Web Vitals

**Severity**: HIGH

**Metrics**:
- Poor Lcp: 6
- Poor Fid: 0
- Poor Cls: 5
- Total: 6

**Recommendation**: Optimize images, reduce JavaScript, improve server response time. Focus on LCP, FID, and CLS improvements.

---

### 4. 1 pages with slow load times

**Severity**: MEDIUM

**Metrics**:
- Count: 1
- Avg Load Time: 3.2

**Recommendation**: Implement caching, compress images, minify CSS/JS. Target load time under 3 seconds.

---

### 5. 2 pages with deep crawl depth (>3 clicks)

**Severity**: MEDIUM

**Metrics**:
- Count: 2
- Avg Depth: 4.5

**Recommendation**: Improve internal linking structure. Important pages should be within 3 clicks from homepage.

---

