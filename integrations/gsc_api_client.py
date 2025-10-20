"""
Google Search Console API Client
Automatically fetches search performance data using Google Search Console API
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json
import os

# Google API imports (installed in requirements.txt)
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    GOOGLE_APIS_AVAILABLE = False


class GSCAPIClient:
    """Google Search Console API client for automated data fetching"""

    # OAuth 2.0 scopes required for Search Console API
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

    def __init__(self, credentials_dir: str = None):
        """
        Initialize GSC API client

        Args:
            credentials_dir: Directory to store OAuth credentials
        """
        if not GOOGLE_APIS_AVAILABLE:
            raise ImportError(
                "Google API libraries not installed. "
                "Run: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client"
            )

        self.credentials_dir = Path(credentials_dir or 'config/credentials')
        self.credentials_dir.mkdir(parents=True, exist_ok=True)

        self.token_path = self.credentials_dir / 'gsc_token.json'
        self.credentials = None
        self.service = None

    def get_authorization_url(self, client_secrets_file: str) -> str:
        """
        Get OAuth authorization URL for user to authorize app

        Args:
            client_secrets_file: Path to client_secrets.json from Google Cloud Console

        Returns:
            Authorization URL for user to visit
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
            True if successful, False otherwise
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

    def connect(self) -> bool:
        """
        Connect to Google Search Console API

        Returns:
            True if connected successfully, False otherwise
        """
        self.credentials = self._load_credentials()

        if not self.credentials:
            return False

        try:
            self.service = build('searchconsole', 'v1', credentials=self.credentials)
            return True
        except Exception as e:
            print(f"Error connecting to GSC API: {e}")
            return False

    def list_sites(self) -> List[str]:
        """
        List all sites user has access to in Search Console

        Returns:
            List of site URLs
        """
        if not self.connect():
            raise Exception("Not authenticated. Please authorize first.")

        try:
            sites_list = self.service.sites().list().execute()
            return [site['siteUrl'] for site in sites_list.get('siteEntry', [])]
        except HttpError as e:
            print(f"Error listing sites: {e}")
            return []

    def fetch_search_analytics(
        self,
        site_url: str,
        start_date: str = None,
        end_date: str = None,
        dimensions: List[str] = None,
        row_limit: int = 25000
    ) -> Dict[str, Any]:
        """
        Fetch search analytics data from Google Search Console

        Args:
            site_url: Site URL (must match GSC property)
            start_date: Start date (YYYY-MM-DD), defaults to 30 days ago
            end_date: End date (YYYY-MM-DD), defaults to yesterday
            dimensions: List of dimensions ['query', 'page', 'country', 'device']
            row_limit: Maximum rows to return (max 25000)

        Returns:
            Dictionary with search analytics data
        """
        if not self.connect():
            raise Exception("Not authenticated. Please authorize first.")

        # Default dates
        if not end_date:
            end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Default dimensions
        if not dimensions:
            dimensions = ['query']

        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': row_limit,
            'startRow': 0
        }

        try:
            response = self.service.searchanalytics().query(
                siteUrl=site_url,
                body=request_body
            ).execute()

            return {
                'source': 'Google Search Console API',
                'site_url': site_url,
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'rows': response.get('rows', []),
                'total_rows': len(response.get('rows', []))
            }

        except HttpError as e:
            print(f"Error fetching search analytics: {e}")
            return {
                'error': str(e),
                'site_url': site_url
            }

    def fetch_queries_with_metrics(
        self,
        site_url: str,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Fetch all queries with clicks, impressions, CTR, and position

        Args:
            site_url: Site URL
            days: Number of days to look back

        Returns:
            List of queries with metrics
        """
        end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        response = self.fetch_search_analytics(
            site_url=site_url,
            start_date=start_date,
            end_date=end_date,
            dimensions=['query']
        )

        if 'error' in response:
            return []

        # Transform to normalized format
        queries = []
        for row in response.get('rows', []):
            queries.append({
                'query': row['keys'][0],
                'clicks': int(row.get('clicks', 0)),
                'impressions': int(row.get('impressions', 0)),
                'ctr': float(row.get('ctr', 0)),
                'position': float(row.get('position', 0))
            })

        return queries

    def get_site_summary(self, site_url: str, days: int = 30) -> Dict[str, Any]:
        """
        Get summary metrics for a site

        Args:
            site_url: Site URL
            days: Number of days to look back

        Returns:
            Summary metrics
        """
        queries = self.fetch_queries_with_metrics(site_url, days)

        if not queries:
            return {
                'total_clicks': 0,
                'total_impressions': 0,
                'average_ctr': 0,
                'average_position': 0,
                'total_queries': 0
            }

        total_clicks = sum(q['clicks'] for q in queries)
        total_impressions = sum(q['impressions'] for q in queries)

        return {
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'average_ctr': (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
            'average_position': sum(q['position'] for q in queries) / len(queries) if queries else 0,
            'total_queries': len(queries),
            'top_queries': sorted(queries, key=lambda x: x['clicks'], reverse=True)[:10]
        }

    def disconnect(self):
        """Remove stored credentials"""
        if self.token_path.exists():
            self.token_path.unlink()
        self.credentials = None
        self.service = None


# Global instance
gsc_api_client = GSCAPIClient()
