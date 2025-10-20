"""
Google Analytics 4 API Client
Automatically fetches user behavior data using Google Analytics Data API
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json

# Google API imports
try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest,
        DateRange,
        Dimension,
        Metric
    )
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    GOOGLE_APIS_AVAILABLE = False


class GA4APIClient:
    """Google Analytics 4 API client for automated data fetching"""

    # OAuth 2.0 scopes
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

    def __init__(self, credentials_dir: str = None, property_id: str = None, service_account_file: str = None):
        """
        Initialize GA4 API client

        Args:
            credentials_dir: Directory to store OAuth credentials
            property_id: GA4 property ID (e.g., "properties/123456789")
            service_account_file: Path to service account JSON key file (optional)
        """
        if not GOOGLE_APIS_AVAILABLE:
            raise ImportError(
                "Google Analytics API libraries not installed. "
                "Run: pip install google-analytics-data google-auth-oauthlib"
            )

        self.credentials_dir = Path(credentials_dir or 'config/credentials')
        self.credentials_dir.mkdir(parents=True, exist_ok=True)

        self.token_path = self.credentials_dir / 'ga4_token.json'
        self.config_path = self.credentials_dir / 'ga4_config.json'
        self.service_account_path = Path(service_account_file) if service_account_file else (self.credentials_dir / 'service_account.json')

        self.property_id = property_id or self._load_property_id()
        self.credentials = None
        self.client = None
        self.auth_method = None  # 'oauth' or 'service_account'

    def _load_property_id(self) -> Optional[str]:
        """Load saved property ID"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    return config.get('property_id')
            except:
                return None
        return None

    def _save_property_id(self, property_id: str):
        """Save property ID"""
        config = {'property_id': property_id}
        with open(self.config_path, 'w') as f:
            json.dump(config, f)

    def get_authorization_url(self, client_secrets_file: str) -> str:
        """
        Get OAuth authorization URL

        Args:
            client_secrets_file: Path to client_secrets.json

        Returns:
            Authorization URL
        """
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file,
            scopes=self.SCOPES,
            redirect_uri='http://localhost:5001/oauth2callback'
        )

        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )

        return auth_url

    def exchange_code_for_token(self, code: str, client_secrets_file: str) -> bool:
        """
        Exchange authorization code for access token

        Args:
            code: Authorization code from OAuth callback
            client_secrets_file: Path to client_secrets.json

        Returns:
            True if successful
        """
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file,
                scopes=self.SCOPES,
                redirect_uri='http://localhost:5001/oauth2callback'
            )

            flow.fetch_token(code=code)

            # Save credentials
            self._save_credentials(flow.credentials)
            self.credentials = flow.credentials

            return True
        except Exception as e:
            print(f"Error exchanging code: {e}")
            return False

    def _save_credentials(self, credentials: Credentials):
        """Save credentials to file"""
        with open(self.token_path, 'w') as token:
            token.write(credentials.to_json())

    def _load_credentials(self) -> Optional[Credentials]:
        """Load credentials from file"""
        if not self.token_path.exists():
            return None

        try:
            credentials = Credentials.from_authorized_user_file(
                str(self.token_path),
                self.SCOPES
            )

            # Refresh if expired
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                self._save_credentials(credentials)

            return credentials
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return None

    def is_authenticated(self) -> bool:
        """Check if client has valid credentials"""
        credentials = self._load_credentials()
        return credentials is not None and credentials.valid

    def set_property_id(self, property_id: str):
        """
        Set GA4 property ID

        Args:
            property_id: GA4 property ID (just the number, not "properties/123456789")
        """
        # Ensure property ID is in correct format
        if not property_id.startswith('properties/'):
            property_id = f'properties/{property_id}'

        self.property_id = property_id
        self._save_property_id(property_id)

    def _load_service_account_credentials(self) -> Optional[Credentials]:
        """Load service account credentials from file"""
        if not self.service_account_path.exists():
            return None

        try:
            credentials = service_account.Credentials.from_service_account_file(
                str(self.service_account_path),
                scopes=self.SCOPES
            )
            self.auth_method = 'service_account'
            return credentials
        except Exception as e:
            print(f"Error loading service account credentials: {e}")
            return None

    def connect(self) -> bool:
        """
        Connect to GA4 API
        Tries service account first, then OAuth

        Returns:
            True if connected successfully
        """
        # Try service account first
        self.credentials = self._load_service_account_credentials()

        # Fall back to OAuth if service account not available
        if not self.credentials:
            self.credentials = self._load_credentials()
            if self.credentials:
                self.auth_method = 'oauth'

        if not self.credentials:
            return False

        try:
            self.client = BetaAnalyticsDataClient(credentials=self.credentials)
            return True
        except Exception as e:
            print(f"Error connecting to GA4 API: {e}")
            return False

    def fetch_user_behavior(
        self,
        start_date: str = None,
        end_date: str = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Fetch user behavior metrics

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            days: Number of days to look back (if dates not provided)

        Returns:
            Dictionary with GA4 metrics
        """
        if not self.connect():
            raise Exception("Not authenticated. Please authorize first.")

        if not self.property_id:
            raise Exception("Property ID not set. Call set_property_id() first.")

        # Default dates
        if not end_date:
            end_date = 'yesterday'
        if not start_date:
            start_date = f'{days}daysAgo'

        request = RunReportRequest(
            property=self.property_id,
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name='totalUsers'),
                Metric(name='sessions'),
                Metric(name='screenPageViews'),
                Metric(name='engagementRate'),
                Metric(name='bounceRate'),
                Metric(name='averageSessionDuration'),
                Metric(name='newUsers')
            ],
            dimensions=[Dimension(name='date')]
        )

        try:
            response = self.client.run_report(request)

            # Parse response
            daily_data = []
            for row in response.rows:
                date = row.dimension_values[0].value
                metrics = row.metric_values

                daily_data.append({
                    'date': date,
                    'users': int(metrics[0].value),
                    'sessions': int(metrics[1].value),
                    'page_views': int(metrics[2].value),
                    'engagement_rate': float(metrics[3].value) * 100,  # Convert to percentage
                    'bounce_rate': float(metrics[4].value) * 100,  # Convert to percentage
                    'avg_session_duration': int(float(metrics[5].value)),  # Convert to seconds
                    'new_users': int(metrics[6].value)
                })

            return {
                'source': 'Google Analytics 4 API',
                'property_id': self.property_id,
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'data': daily_data,
                'total_rows': len(daily_data)
            }

        except Exception as e:
            print(f"Error fetching GA4 data: {e}")
            return {
                'error': str(e),
                'property_id': self.property_id
            }

    def get_summary_metrics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get summary metrics for the period

        Args:
            days: Number of days to look back

        Returns:
            Summary metrics
        """
        data = self.fetch_user_behavior(days=days)

        if 'error' in data:
            return {
                'total_users': 0,
                'total_sessions': 0,
                'total_page_views': 0,
                'avg_engagement_rate': 0,
                'avg_bounce_rate': 0,
                'avg_session_duration': 0
            }

        daily_data = data.get('data', [])

        if not daily_data:
            return {
                'total_users': 0,
                'total_sessions': 0,
                'total_page_views': 0,
                'avg_engagement_rate': 0,
                'avg_bounce_rate': 0,
                'avg_session_duration': 0
            }

        total_users = sum(d['users'] for d in daily_data)
        total_sessions = sum(d['sessions'] for d in daily_data)
        total_page_views = sum(d['page_views'] for d in daily_data)

        avg_engagement = sum(d['engagement_rate'] for d in daily_data) / len(daily_data)
        avg_bounce = sum(d['bounce_rate'] for d in daily_data) / len(daily_data)
        avg_duration = sum(d['avg_session_duration'] for d in daily_data) / len(daily_data)

        return {
            'total_users': total_users,
            'total_sessions': total_sessions,
            'total_page_views': total_page_views,
            'avg_engagement_rate': round(avg_engagement, 1),
            'avg_bounce_rate': round(avg_bounce, 1),
            'avg_session_duration': int(avg_duration),
            'pages_per_session': round(total_page_views / total_sessions, 1) if total_sessions > 0 else 0,
            'new_users': sum(d['new_users'] for d in daily_data)
        }

    def disconnect(self):
        """Remove stored credentials"""
        if self.token_path.exists():
            self.token_path.unlink()
        if self.config_path.exists():
            self.config_path.unlink()
        self.credentials = None
        self.client = None


# Global instance
ga4_api_client = GA4APIClient()
