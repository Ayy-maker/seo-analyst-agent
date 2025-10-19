# Sample Data Files

This directory contains sample SEO report data for testing the SEO Analyst Agent.

## Files

### 1. search-console-keywords.csv
Sample Google Search Console keyword performance data.

**Columns:**
- `query`: Search query
- `position`: Average ranking position
- `impressions`: Number of impressions
- `clicks`: Number of clicks
- `ctr`: Click-through rate (%)
- `url`: Landing page URL

**Use case**: Test keyword analysis, CTR optimization, ranking monitoring

### 2. technical-audit.csv
Sample technical SEO audit data (Screaming Frog style).

**Columns:**
- `url`: Page URL
- `status_code`: HTTP status code
- `indexability`: Whether page is indexable
- `crawl_depth`: Clicks from homepage
- `load_time`: Page load time (seconds)
- `lcp`: Largest Contentful Paint (seconds)
- `fid`: First Input Delay (milliseconds)
- `cls`: Cumulative Layout Shift
- `mobile_friendly`: Mobile usability

**Use case**: Test technical SEO analysis, Core Web Vitals, crawl errors

## Testing

Run analysis on sample data:

```bash
# Test with keyword data
python main.py analyze --reports data/samples/search-console-keywords.csv

# Test with technical data
python main.py analyze --reports data/samples/technical-audit.csv

# Test with both
python main.py analyze --reports data/samples/*.csv
```

## Expected Insights

### Keyword Data
- Top performers: "meta tags", "seo tools", "seo strategy"
- Low CTR opportunities: "link building", "core web vitals"
- High impressions, low clicks: "backlink checker", "competitor analysis"

### Technical Data
- 1 404 error (/blog/post-3)
- 1 500 error (/test-page)
- 2 non-indexable pages (/products, /old-page)
- Core Web Vitals issues: /blog/post-2 (poor LCP, FID, CLS)
- Deep pages: /deep/nested/page (5 clicks from home)
- Mobile issues: /blog/post-2 not mobile-friendly

## Creating Your Own Sample Data

To create test data from real reports:

1. Export from Google Search Console (Queries report)
2. Export from Screaming Frog (Internal HTML)
3. Place in `data/samples/`
4. Run analysis

**Note**: Sample data is anonymized and for testing only.
