"""
Database Manager - Handle all database operations
Provides CRUD operations for clients, reports, metrics, and insights
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from contextlib import contextmanager


class DatabaseManager:
    """Manages SQLite database operations for historical data"""
    
    def __init__(self, db_path: str = "database/seo_data.db"):
        self.db_path = db_path
        self._ensure_database()
    
    def _ensure_database(self):
        """Create database and tables if they don't exist"""
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database with schema
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            with self.get_connection() as conn:
                conn.executescript(schema_sql)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    # ==================== CLIENT OPERATIONS ====================
    
    def create_client(self, name: str, domain: str = None, industry: str = None, config: Dict = None) -> int:
        """Create a new client"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO clients (name, domain, industry, config_json)
                   VALUES (?, ?, ?, ?)""",
                (name, domain, industry, json.dumps(config) if config else None)
            )
            return cursor.lastrowid
    
    def get_client(self, client_id: int = None, name: str = None) -> Optional[Dict]:
        """Get client by ID or name"""
        with self.get_connection() as conn:
            if client_id:
                cursor = conn.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            elif name:
                cursor = conn.execute("SELECT * FROM clients WHERE name = ?", (name,))
            else:
                return None
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_clients(self) -> List[Dict]:
        """Get all clients"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM clients ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_client(self, client_id: int, **kwargs):
        """Update client information"""
        allowed_fields = ['name', 'domain', 'industry', 'config_json']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return
        
        if 'config_json' in updates and isinstance(updates['config_json'], dict):
            updates['config_json'] = json.dumps(updates['config_json'])
        
        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        set_clause += ", updated_at = ?"
        
        with self.get_connection() as conn:
            conn.execute(
                f"UPDATE clients SET {set_clause} WHERE id = ?",
                (*updates.values(), datetime.now(), client_id)
            )
    
    # ==================== REPORT OPERATIONS ====================
    
    def create_report(self, client_id: int, report_date: date, **kwargs) -> int:
        """Create a new report entry"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO reports 
                   (client_id, report_date, report_period, report_type, file_path, 
                    insights_count, health_score)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    client_id,
                    report_date,
                    kwargs.get('report_period'),
                    kwargs.get('report_type'),
                    kwargs.get('file_path'),
                    kwargs.get('insights_count', 0),
                    kwargs.get('health_score')
                )
            )
            return cursor.lastrowid
    
    def get_reports(self, client_id: int = None, limit: int = 10) -> List[Dict]:
        """Get reports for a client or all reports if client_id is None"""
        with self.get_connection() as conn:
            if client_id is not None:
                cursor = conn.execute(
                    """SELECT * FROM reports 
                       WHERE client_id = ? 
                       ORDER BY report_date DESC 
                       LIMIT ?""",
                    (client_id, limit)
                )
            else:
                cursor = conn.execute(
                    """SELECT * FROM reports 
                       ORDER BY report_date DESC 
                       LIMIT ?""",
                    (limit,)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    def get_latest_report(self, client_id: int) -> Optional[Dict]:
        """Get most recent report for a client"""
        reports = self.get_reports(client_id, limit=1)
        return reports[0] if reports else None
    
    def update_report(self, report_id: int, **kwargs):
        """Update report information"""
        allowed_fields = ['file_path', 'status', 'insights_count', 'health_score', 'report_period']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return
        
        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        
        with self.get_connection() as conn:
            conn.execute(
                f"UPDATE reports SET {set_clause} WHERE id = ?",
                (*updates.values(), report_id)
            )
    
    # ==================== METRICS OPERATIONS ====================
    
    def save_metrics(self, report_id: int, client_id: int, metrics: List[Dict]):
        """Save multiple metrics at once"""
        with self.get_connection() as conn:
            conn.executemany(
                """INSERT INTO metrics 
                   (report_id, client_id, metric_name, metric_value, metric_unit,
                    metric_change_percent, metric_date, module)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        report_id,
                        client_id,
                        m['name'],
                        m['value'],
                        m.get('unit'),
                        m.get('change_percent'),
                        m.get('date', date.today()),
                        m.get('module')
                    )
                    for m in metrics
                ]
            )
    
    def get_metrics(self, client_id: int, metric_name: str = None, 
                   start_date: date = None, end_date: date = None) -> List[Dict]:
        """Get metrics with optional filters"""
        query = "SELECT * FROM metrics WHERE client_id = ?"
        params = [client_id]
        
        if metric_name:
            query += " AND metric_name = ?"
            params.append(metric_name)
        
        if start_date:
            query += " AND metric_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND metric_date <= ?"
            params.append(end_date)
        
        query += " ORDER BY metric_date DESC"
        
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_metric_trend(self, client_id: int, metric_name: str, months: int = 6) -> List[Dict]:
        """Get metric trend for the last N months"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """SELECT metric_date, metric_value, metric_change_percent
                   FROM metrics
                   WHERE client_id = ? AND metric_name = ?
                   AND metric_date >= date('now', ? || ' months')
                   ORDER BY metric_date ASC""",
                (client_id, metric_name, f'-{months}')
            )
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== KEYWORDS OPERATIONS ====================
    
    def save_keywords(self, report_id: int, client_id: int, keywords: List[Dict]):
        """Save keyword data"""
        with self.get_connection() as conn:
            conn.executemany(
                """INSERT INTO keywords 
                   (report_id, client_id, keyword, position, previous_position,
                    position_change, impressions, clicks, ctr, date, url)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        report_id,
                        client_id,
                        k['keyword'],
                        k.get('position'),
                        k.get('previous_position'),
                        k.get('position_change'),
                        k.get('impressions', 0),
                        k.get('clicks', 0),
                        k.get('ctr', 0.0),
                        k.get('date', date.today()),
                        k.get('url')
                    )
                    for k in keywords
                ]
            )
    
    def get_keyword_history(self, client_id: int, keyword: str) -> List[Dict]:
        """Get historical data for a specific keyword"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """SELECT * FROM keywords
                   WHERE client_id = ? AND keyword = ?
                   ORDER BY date ASC""",
                (client_id, keyword)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def get_top_keywords(self, client_id: int, limit: int = 50) -> List[Dict]:
        """Get top performing keywords from latest report"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """SELECT keyword, position, impressions, clicks, ctr, position_change
                   FROM keywords
                   WHERE client_id = ? 
                   AND date = (SELECT MAX(date) FROM keywords WHERE client_id = ?)
                   ORDER BY clicks DESC
                   LIMIT ?""",
                (client_id, client_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== INSIGHTS OPERATIONS ====================
    
    def save_insights(self, report_id: int, client_id: int, insights: List[Dict]):
        """Save insights"""
        with self.get_connection() as conn:
            conn.executemany(
                """INSERT INTO insights 
                   (report_id, client_id, module, insight_text, insight_type,
                    severity, metric_impact, priority)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        report_id,
                        client_id,
                        i.get('module', 'general'),
                        i.get('insight') or i.get('insight_text') or 'No insight provided',
                        i.get('type', 'insight'),
                        i.get('severity', 'medium'),
                        i.get('metric_value', 0),
                        i.get('priority', 3)
                    )
                    for i in insights
                ]
            )
    
    def get_insights(self, report_id: int = None, client_id: int = None) -> List[Dict]:
        """Get insights for a specific report or client"""
        query = "SELECT * FROM insights WHERE 1=1"
        params = []
        
        if report_id:
            query += " AND report_id = ?"
            params.append(report_id)
        
        if client_id:
            query += " AND client_id = ?"
            params.append(client_id)
        
        query += " ORDER BY created_at DESC"
        
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_open_insights(self, client_id: int = None) -> List[Dict]:
        """Get all open (unresolved) insights"""
        query = "SELECT * FROM v_open_issues"
        params = []
        
        if client_id:
            query += " WHERE client_id = ?"
            params.append(client_id)
        
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def resolve_insight(self, insight_id: int):
        """Mark an insight as resolved"""
        with self.get_connection() as conn:
            conn.execute(
                """UPDATE insights 
                   SET status = 'resolved', resolved_at = ?
                   WHERE id = ?""",
                (datetime.now(), insight_id)
            )
    
    # ==================== TRAFFIC OPERATIONS ====================
    
    def save_traffic(self, report_id: int, client_id: int, traffic_data: List[Dict]):
        """Save traffic metrics"""
        with self.get_connection() as conn:
            conn.executemany(
                """INSERT INTO traffic 
                   (report_id, client_id, date, sessions, users, pageviews,
                    bounce_rate, avg_session_duration, source, device)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        report_id,
                        client_id,
                        t.get('date', date.today()),
                        t.get('sessions', 0),
                        t.get('users', 0),
                        t.get('pageviews', 0),
                        t.get('bounce_rate'),
                        t.get('avg_session_duration'),
                        t.get('source'),
                        t.get('device')
                    )
                    for t in traffic_data
                ]
            )
    
    def get_traffic_trend(self, client_id: int, days: int = 30) -> List[Dict]:
        """Get traffic trend for last N days"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """SELECT date, SUM(sessions) as total_sessions,
                   SUM(users) as total_users, SUM(pageviews) as total_pageviews
                   FROM traffic
                   WHERE client_id = ?
                   AND date >= date('now', ? || ' days')
                   GROUP BY date
                   ORDER BY date ASC""",
                (client_id, f'-{days}')
            )
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== FORECASTS & ANOMALIES ====================
    
    def save_forecast(self, client_id: int, metric_name: str, forecasts: List[Dict]):
        """Save forecast data"""
        with self.get_connection() as conn:
            conn.executemany(
                """INSERT INTO forecasts 
                   (client_id, metric_name, forecast_date, predicted_value,
                    confidence_low, confidence_high, model_type)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        client_id,
                        metric_name,
                        f['date'],
                        f['predicted_value'],
                        f.get('confidence_low'),
                        f.get('confidence_high'),
                        f.get('model_type', 'linear')
                    )
                    for f in forecasts
                ]
            )
    
    def get_forecasts(self, client_id: int, metric_name: str) -> List[Dict]:
        """Get latest forecasts for a metric"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """SELECT * FROM forecasts
                   WHERE client_id = ? AND metric_name = ?
                   ORDER BY forecast_date ASC""",
                (client_id, metric_name)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def save_anomaly(self, client_id: int, metric_name: str, date: date, 
                    expected: float, actual: float, severity: str):
        """Record an anomaly"""
        deviation = ((actual - expected) / expected * 100) if expected != 0 else 0
        
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO anomalies 
                   (client_id, metric_name, date, expected_value, actual_value,
                    deviation_percent, severity)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (client_id, metric_name, date, expected, actual, deviation, severity)
            )
    
    def get_recent_anomalies(self, client_id: int, days: int = 7) -> List[Dict]:
        """Get recent anomalies"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """SELECT * FROM anomalies
                   WHERE client_id = ?
                   AND date >= date('now', ? || ' days')
                   ORDER BY date DESC, ABS(deviation_percent) DESC""",
                (client_id, f'-{days}')
            )
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== STATISTICS ====================
    
    def get_client_stats(self, client_id: int) -> Dict:
        """Get overview statistics for a client"""
        with self.get_connection() as conn:
            # Total reports
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM reports WHERE client_id = ?",
                (client_id,)
            )
            total_reports = cursor.fetchone()['count']
            
            # Open insights
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM insights WHERE client_id = ? AND status = 'open'",
                (client_id,)
            )
            open_insights = cursor.fetchone()['count']
            
            # Latest health score
            cursor = conn.execute(
                """SELECT health_score FROM reports 
                   WHERE client_id = ? AND health_score IS NOT NULL
                   ORDER BY report_date DESC LIMIT 1""",
                (client_id,)
            )
            row = cursor.fetchone()
            health_score = row['health_score'] if row else None
            
            # Top keywords count
            cursor = conn.execute(
                """SELECT COUNT(DISTINCT keyword) as count FROM keywords 
                   WHERE client_id = ?""",
                (client_id,)
            )
            keyword_count = cursor.fetchone()['count']
            
            return {
                'total_reports': total_reports,
                'open_insights': open_insights,
                'health_score': health_score,
                'tracked_keywords': keyword_count
            }
