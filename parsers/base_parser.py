import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd


class BaseParser:
    """Base class for all report parsers"""
    
    def __init__(self, schema_path: str = "config/data-schemas.json"):
        self.schema_path = schema_path
        self.schemas = self._load_schemas()
        
    def _load_schemas(self) -> Dict:
        """Load data schemas from config"""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"schemas": {}}
    
    def detect_type(self, df: pd.DataFrame) -> str:
        """
        Detect report type based on column names
        Returns: keywords|technical|onpage|backlinks|traffic
        """
        columns = [col.lower() for col in df.columns]
        
        # Keywords indicators
        keywords_cols = ['query', 'keyword', 'position', 'rank', 'ctr', 'impressions']
        if any(col in columns for col in keywords_cols):
            return 'keywords'
        
        # Technical SEO indicators
        technical_cols = ['status_code', 'indexability', 'crawl_depth', 'lcp', 'cls', 'fid']
        if any(col in columns for col in technical_cols):
            return 'technical'
        
        # On-page indicators
        onpage_cols = ['title', 'meta_description', 'h1', 'word_count', 'schema']
        if any(col in columns for col in onpage_cols):
            return 'onpage'
        
        # Backlinks indicators
        backlink_cols = ['source_url', 'anchor_text', 'domain_rating', 'link_type']
        if any(col in columns for col in backlink_cols):
            return 'backlinks'
        
        # Traffic indicators
        traffic_cols = ['sessions', 'users', 'pageviews', 'bounce_rate', 'conversions']
        if any(col in columns for col in traffic_cols):
            return 'traffic'
        
        return 'unknown'
    
    def normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize column names using mapping rules
        Maps common variations to standard names
        """
        if 'mapping_rules' not in self.schemas:
            return df
        
        aliases = self.schemas['mapping_rules'].get('csv_column_aliases', {})
        rename_map = {}
        
        for standard_name, variants in aliases.items():
            for col in df.columns:
                if col in variants:
                    rename_map[col] = standard_name
                    break
        
        return df.rename(columns=rename_map)
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate parsed data against schema"""
        if data['type'] == 'unknown':
            return False
        
        if 'data' not in data or len(data['data']) == 0:
            return False
        
        return True
    
    def create_standard_output(self, 
                              report_type: str,
                              data: List[Dict],
                              source: str = "Unknown",
                              date_range: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create standardized output format
        """
        return {
            "report_id": f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": report_type,
            "source": source,
            "date_range": date_range or {
                "start": None,
                "end": None
            },
            "parsed_at": datetime.now().isoformat(),
            "data": data,
            "record_count": len(data)
        }
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a report file
        To be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement parse()")
