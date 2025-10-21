"""
Historical Snapshot Manager
Captures and stores monthly SEO performance snapshots for trend analysis
"""

import sqlite3
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional, Any
import json


class SnapshotManager:
    """
    Manages monthly SEO performance snapshots

    Features:
    - Captures GSC metrics (clicks, impressions, CTR, position)
    - Captures GA4 metrics (users, sessions, engagement)
    - Stores monthly snapshots for historical comparison
    - Retrieves historical data for trend analysis
    """

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / 'database' / 'seo_data.db'
        self.db_path = str(db_path)
        self._ensure_snapshot_table()

    def _ensure_snapshot_table(self):
        """Create monthly_snapshots table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                snapshot_date DATE NOT NULL,
                snapshot_month TEXT NOT NULL,

                -- GSC Metrics
                total_clicks INTEGER DEFAULT 0,
                total_impressions INTEGER DEFAULT 0,
                avg_ctr REAL DEFAULT 0.0,
                avg_position REAL DEFAULT 0.0,
                total_queries INTEGER DEFAULT 0,

                -- GA4 Metrics
                total_users INTEGER DEFAULT 0,
                total_sessions INTEGER DEFAULT 0,
                total_pageviews INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0.0,
                bounce_rate REAL DEFAULT 0.0,
                avg_session_duration REAL DEFAULT 0.0,

                -- Calculated Changes (vs previous month)
                clicks_change_percent REAL,
                impressions_change_percent REAL,
                ctr_change_percent REAL,
                position_change REAL,
                users_change_percent REAL,

                -- Metadata
                snapshot_source TEXT DEFAULT 'manual',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (client_id) REFERENCES clients(id),
                UNIQUE(client_id, snapshot_month)
            )
        ''')

        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_snapshots_client_date
            ON monthly_snapshots(client_id, snapshot_date)
        ''')

        conn.commit()
        conn.close()

    def capture_snapshot(self,
                        client_id: int,
                        gsc_data: Dict[str, Any],
                        ga4_data: Dict[str, Any] = None,
                        snapshot_date: date = None,
                        source: str = 'manual') -> int:
        """
        Capture a monthly snapshot of SEO performance

        Args:
            client_id: Client ID
            gsc_data: Dictionary with GSC metrics
            ga4_data: Dictionary with GA4 metrics (optional)
            snapshot_date: Date of snapshot (defaults to today)
            source: Source of snapshot (manual, automated, import)

        Returns:
            Snapshot ID
        """
        if snapshot_date is None:
            snapshot_date = date.today()

        snapshot_month = snapshot_date.strftime('%Y-%m')

        # Extract GSC metrics from normalized data
        # The data_normalizer returns nested structure: gsc_data['kpis']['total_clicks']['value']
        kpis = gsc_data.get('kpis', {})
        total_clicks = kpis.get('total_clicks', {}).get('value', 0)
        total_impressions = kpis.get('impressions', {}).get('value', 0)
        avg_ctr = kpis.get('ctr', {}).get('value', 0.0)
        avg_position = kpis.get('avg_position', {}).get('value', 0.0)
        total_queries = len(gsc_data.get('top_queries', []))

        # Extract GA4 metrics (if provided)
        # The data_normalizer returns flat structure for GA4 data
        if ga4_data:
            total_users = ga4_data.get('total_users', 0)
            total_sessions = ga4_data.get('total_sessions', 0)
            total_pageviews = ga4_data.get('total_page_views', 0)  # Note: field name is 'total_page_views' in normalizer
            engagement_rate = ga4_data.get('avg_engagement_rate', 0.0)
            bounce_rate = ga4_data.get('avg_bounce_rate', 0.0)
            avg_session_duration = ga4_data.get('avg_session_duration', 0.0)
        else:
            total_users = 0
            total_sessions = 0
            total_pageviews = 0
            engagement_rate = 0.0
            bounce_rate = 0.0
            avg_session_duration = 0.0

        # Get previous month's snapshot for change calculations
        previous_snapshot = self.get_previous_snapshot(client_id, snapshot_month)

        if previous_snapshot:
            clicks_change = self._calculate_change_percent(
                total_clicks, previous_snapshot['total_clicks']
            )
            impressions_change = self._calculate_change_percent(
                total_impressions, previous_snapshot['total_impressions']
            )
            ctr_change = self._calculate_change_percent(
                avg_ctr, previous_snapshot['avg_ctr']
            )
            position_change = avg_position - previous_snapshot['avg_position']
            users_change = self._calculate_change_percent(
                total_users, previous_snapshot['total_users']
            )
        else:
            clicks_change = None
            impressions_change = None
            ctr_change = None
            position_change = None
            users_change = None

        # Insert or update snapshot
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO monthly_snapshots (
                client_id, snapshot_date, snapshot_month,
                total_clicks, total_impressions, avg_ctr, avg_position, total_queries,
                total_users, total_sessions, total_pageviews,
                engagement_rate, bounce_rate, avg_session_duration,
                clicks_change_percent, impressions_change_percent,
                ctr_change_percent, position_change, users_change_percent,
                snapshot_source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            client_id, snapshot_date, snapshot_month,
            total_clicks, total_impressions, avg_ctr, avg_position, total_queries,
            total_users, total_sessions, total_pageviews,
            engagement_rate, bounce_rate, avg_session_duration,
            clicks_change, impressions_change, ctr_change, position_change, users_change,
            source
        ))

        snapshot_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return snapshot_id

    def get_previous_snapshot(self, client_id: int, current_month: str) -> Optional[Dict]:
        """Get the previous month's snapshot for comparison"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM monthly_snapshots
            WHERE client_id = ? AND snapshot_month < ?
            ORDER BY snapshot_month DESC
            LIMIT 1
        ''', (client_id, current_month))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_snapshots(self, client_id: int, months: int = 6) -> List[Dict]:
        """
        Get recent snapshots for a client

        Args:
            client_id: Client ID
            months: Number of months to retrieve (default: 6)

        Returns:
            List of snapshot dictionaries, ordered by date (newest first)
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM monthly_snapshots
            WHERE client_id = ?
            ORDER BY snapshot_date DESC
            LIMIT ?
        ''', (client_id, months))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_trend_data(self, client_id: int, metric: str, months: int = 12) -> Dict:
        """
        Get trend data for a specific metric

        Args:
            client_id: Client ID
            metric: Metric name (total_clicks, total_impressions, etc.)
            months: Number of months to retrieve

        Returns:
            Dictionary with labels and values for charting
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(f'''
            SELECT snapshot_month, {metric}
            FROM monthly_snapshots
            WHERE client_id = ?
            ORDER BY snapshot_month ASC
            LIMIT ?
        ''', (client_id, months))

        rows = cursor.fetchall()
        conn.close()

        labels = [row['snapshot_month'] for row in rows]
        values = [row[metric] for row in rows]

        return {
            'labels': labels,
            'values': values,
            'metric': metric
        }

    def get_latest_snapshot(self, client_id: int) -> Optional[Dict]:
        """Get the most recent snapshot for a client"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM monthly_snapshots
            WHERE client_id = ?
            ORDER BY snapshot_date DESC
            LIMIT 1
        ''', (client_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def has_historical_data(self, client_id: int) -> bool:
        """Check if client has any historical snapshots"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) as count
            FROM monthly_snapshots
            WHERE client_id = ?
        ''', (client_id,))

        count = cursor.fetchone()[0]
        conn.close()

        return count > 0

    def get_snapshot_count(self, client_id: int) -> int:
        """Get number of snapshots for a client"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) as count
            FROM monthly_snapshots
            WHERE client_id = ?
        ''', (client_id,))

        count = cursor.fetchone()[0]
        conn.close()

        return count

    @staticmethod
    def _calculate_change_percent(current: float, previous: float) -> Optional[float]:
        """Calculate percentage change between two values"""
        if previous == 0:
            return None

        change = ((current - previous) / previous) * 100
        return round(change, 2)


# Create global instance
snapshot_manager = SnapshotManager()
