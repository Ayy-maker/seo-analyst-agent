"""
Google Search Console API Integration
Auto-fetch keyword data directly from GSC
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Optional


class GSCFetcher:
    """Fetch data from Google Search Console API"""
    
    # GSC API scopes
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
    
    def __init__(self, credentials_file: str = 'config/gsc_credentials.json'):
        """
        Initialize GSC API client
        
        Args:
            credentials_file: Path to OAuth2 credentials JSON
        """
        self.credentials_file = credentials_file
        self.token_file = 'config/gsc_token.pickle'
        self.service = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Search Console API
        
        Returns:
            True if authentication successful
        """
        creds = None
        
        # Load saved token if exists
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ Credentials file not found: {self.credentials_file}")
                    print("\nTo get credentials:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create a project and enable Search Console API")
                    print("3. Create OAuth2 credentials")
                    print("4. Download JSON and save as config/gsc_credentials.json")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('searchconsole', 'v1', credentials=creds)
        print("✅ Authenticated with Google Search Console")
        return True
    
    def list_properties(self) -> List[str]:
        """
        List all GSC properties you have access to
        
        Returns:
            List of property URLs
        """
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            site_list = self.service.sites().list().execute()
            properties = [site['siteUrl'] for site in site_list.get('siteEntry', [])]
            return properties
        except Exception as e:
            print(f"❌ Failed to list properties: {e}")
            return []
    
    def fetch_keywords(self,
                      property_url: str,
                      days: int = 28,
                      row_limit: int = 1000) -> Optional[pd.DataFrame]:
        """
        Fetch keyword performance data from GSC
        
        Args:
            property_url: Website property URL (e.g., 'https://example.com/')
            days: Number of days to fetch (default 28)
            row_limit: Maximum rows to return
            
        Returns:
            DataFrame with keywords data or None if failed
        """
        if not self.service:
            if not self.authenticate():
                return None
        
        # Calculate date range
        end_date = datetime.now() - timedelta(days=3)  # GSC has 3-day lag
        start_date = end_date - timedelta(days=days)
        
        # Prepare request
        request = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'dimensions': ['query'],
            'rowLimit': row_limit,
            'dataState': 'final'
        }
        
        try:
            print(f"📊 Fetching keywords from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
            
            response = self.service.searchanalytics().query(
                siteUrl=property_url, body=request).execute()
            
            if 'rows' not in response:
                print("⚠️ No data found")
                return None
            
            # Convert to DataFrame
            rows = response['rows']
            data = []
            for row in rows:
                data.append({
                    'query': row['keys'][0],
                    'clicks': row['clicks'],
                    'impressions': row['impressions'],
                    'ctr': row['ctr'] * 100,  # Convert to percentage
                    'position': row['position']
                })
            
            df = pd.DataFrame(data)
            print(f"✅ Fetched {len(df)} keywords")
            
            return df
            
        except Exception as e:
            print(f"❌ Failed to fetch keywords: {e}")
            return None
    
    def fetch_pages(self,
                   property_url: str,
                   days: int = 28,
                   row_limit: int = 1000) -> Optional[pd.DataFrame]:
        """
        Fetch page performance data from GSC
        
        Args:
            property_url: Website property URL
            days: Number of days to fetch
            row_limit: Maximum rows
            
        Returns:
            DataFrame with pages data
        """
        if not self.service:
            if not self.authenticate():
                return None
        
        end_date = datetime.now() - timedelta(days=3)
        start_date = end_date - timedelta(days=days)
        
        request = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'dimensions': ['page'],
            'rowLimit': row_limit,
            'dataState': 'final'
        }
        
        try:
            print(f"📄 Fetching pages data...")
            response = self.service.searchanalytics().query(
                siteUrl=property_url, body=request).execute()
            
            if 'rows' not in response:
                return None
            
            rows = response['rows']
            data = []
            for row in rows:
                data.append({
                    'page': row['keys'][0],
                    'clicks': row['clicks'],
                    'impressions': row['impressions'],
                    'ctr': row['ctr'] * 100,
                    'position': row['position']
                })
            
            df = pd.DataFrame(data)
            print(f"✅ Fetched {len(df)} pages")
            return df
            
        except Exception as e:
            print(f"❌ Failed to fetch pages: {e}")
            return None
    
    def export_to_csv(self, df: pd.DataFrame, filename: str, output_dir: str = 'data'):
        """Export fetched data to CSV"""
        output_path = Path(output_dir) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ Exported to {output_path}")
        return str(output_path)


# CLI usage
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch data from Google Search Console')
    parser.add_argument('--property', required=True, help='Property URL (e.g., https://example.com/)')
    parser.add_argument('--days', type=int, default=28, help='Number of days to fetch')
    parser.add_argument('--output', default='data/gsc-keywords.csv', help='Output CSV file')
    parser.add_argument('--list', action='store_true', help='List available properties')
    
    args = parser.parse_args()
    
    fetcher = GSCFetcher()
    
    if args.list:
        properties = fetcher.list_properties()
        print("\n📋 Available properties:")
        for prop in properties:
            print(f"  - {prop}")
    else:
        df = fetcher.fetch_keywords(args.property, days=args.days)
        if df is not None:
            fetcher.export_to_csv(df, args.output)
