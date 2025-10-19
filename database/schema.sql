-- SEO Analyst Agent - Database Schema
-- Phase 4: Historical Intelligence System

-- Clients table (multi-client support)
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    domain TEXT,
    industry TEXT,
    config_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reports table (main metadata)
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    report_date DATE NOT NULL,
    report_period TEXT,
    report_type TEXT,
    file_path TEXT,
    status TEXT DEFAULT 'completed',
    insights_count INTEGER DEFAULT 0,
    health_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Metrics table (time-series data for KPIs)
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    metric_unit TEXT,
    metric_change_percent REAL,
    metric_date DATE NOT NULL,
    module TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Keywords table (keyword tracking over time)
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    position REAL,
    previous_position REAL,
    position_change REAL,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    ctr REAL DEFAULT 0.0,
    date DATE NOT NULL,
    url TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Insights table (historical insights tracking)
CREATE TABLE IF NOT EXISTS insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    module TEXT NOT NULL,
    insight_text TEXT NOT NULL,
    insight_type TEXT,
    severity TEXT,
    metric_impact REAL,
    priority INTEGER DEFAULT 3,
    status TEXT DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Traffic table (traffic metrics over time)
CREATE TABLE IF NOT EXISTS traffic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    date DATE NOT NULL,
    sessions INTEGER DEFAULT 0,
    users INTEGER DEFAULT 0,
    pageviews INTEGER DEFAULT 0,
    bounce_rate REAL,
    avg_session_duration REAL,
    source TEXT,
    device TEXT,
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Technical issues table (track technical SEO problems)
CREATE TABLE IF NOT EXISTS technical_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    issue_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    url TEXT,
    description TEXT,
    date_found DATE NOT NULL,
    date_resolved DATE,
    status TEXT DEFAULT 'open',
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Backlinks table (backlink tracking)
CREATE TABLE IF NOT EXISTS backlinks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    source_url TEXT NOT NULL,
    target_url TEXT NOT NULL,
    anchor_text TEXT,
    domain_authority REAL,
    spam_score REAL,
    first_seen DATE NOT NULL,
    last_seen DATE,
    status TEXT DEFAULT 'active',
    FOREIGN KEY (report_id) REFERENCES reports(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Competitors table (competitor tracking)
CREATE TABLE IF NOT EXISTS competitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    competitor_domain TEXT NOT NULL,
    competitor_name TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    UNIQUE(client_id, competitor_domain)
);

-- Competitor rankings table (track competitor positions)
CREATE TABLE IF NOT EXISTS competitor_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    position REAL,
    date DATE NOT NULL,
    FOREIGN KEY (competitor_id) REFERENCES competitors(id)
);

-- Forecasts table (store predictions)
CREATE TABLE IF NOT EXISTS forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    forecast_date DATE NOT NULL,
    predicted_value REAL,
    confidence_low REAL,
    confidence_high REAL,
    model_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Anomalies table (track detected anomalies)
CREATE TABLE IF NOT EXISTS anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    date DATE NOT NULL,
    expected_value REAL,
    actual_value REAL,
    deviation_percent REAL,
    severity TEXT,
    alert_sent BOOLEAN DEFAULT 0,
    acknowledged BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_metrics_client_date ON metrics(client_id, metric_date);
CREATE INDEX IF NOT EXISTS idx_keywords_client_date ON keywords(client_id, date);
CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_traffic_client_date ON traffic(client_id, date);
CREATE INDEX IF NOT EXISTS idx_insights_client_module ON insights(client_id, module);
CREATE INDEX IF NOT EXISTS idx_insights_status ON insights(status);
CREATE INDEX IF NOT EXISTS idx_technical_issues_status ON technical_issues(status);
CREATE INDEX IF NOT EXISTS idx_backlinks_client ON backlinks(client_id);
CREATE INDEX IF NOT EXISTS idx_forecasts_client_date ON forecasts(client_id, forecast_date);
CREATE INDEX IF NOT EXISTS idx_anomalies_client_date ON anomalies(client_id, date);

-- Create views for common queries
CREATE VIEW IF NOT EXISTS v_latest_metrics AS
SELECT 
    c.name as client_name,
    m.metric_name,
    m.metric_value,
    m.metric_unit,
    m.metric_change_percent,
    m.metric_date,
    m.module
FROM metrics m
JOIN clients c ON m.client_id = c.id
WHERE m.metric_date = (
    SELECT MAX(metric_date) 
    FROM metrics m2 
    WHERE m2.client_id = m.client_id 
    AND m2.metric_name = m.metric_name
);

CREATE VIEW IF NOT EXISTS v_keyword_trends AS
SELECT 
    c.name as client_name,
    k.keyword,
    k.position,
    k.previous_position,
    k.position_change,
    k.impressions,
    k.clicks,
    k.ctr,
    k.date
FROM keywords k
JOIN clients c ON k.client_id = c.id
ORDER BY k.date DESC, k.position ASC;

CREATE VIEW IF NOT EXISTS v_open_issues AS
SELECT 
    c.name as client_name,
    i.module,
    i.insight_text,
    i.severity,
    i.created_at,
    CAST((julianday('now') - julianday(i.created_at)) as INTEGER) as days_open
FROM insights i
JOIN clients c ON i.client_id = c.id
WHERE i.status = 'open'
ORDER BY i.priority ASC, i.created_at ASC;
