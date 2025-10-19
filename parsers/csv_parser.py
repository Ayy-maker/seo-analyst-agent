import pandas as pd
from pathlib import Path
from typing import Dict, Any
from .base_parser import BaseParser


class CSVParser(BaseParser):
    """Parser for CSV files (Google Search Console, exports, etc.)"""
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse CSV file into standard format
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Standardized report dictionary
        """
        try:
            # Read CSV with pandas
            df = pd.read_csv(file_path)
            
            # Normalize column names
            df = self.normalize_columns(df)
            
            # Detect report type
            report_type = self.detect_type(df)
            
            # Convert to list of dictionaries
            data = df.to_dict('records')
            
            # Clean data (remove NaN values)
            data = self._clean_data(data)
            
            # Extract metadata
            source = self._detect_source(df)
            date_range = self._extract_date_range(df)
            
            # Create standard output
            result = self.create_standard_output(
                report_type=report_type,
                data=data,
                source=source,
                date_range=date_range
            )
            
            # Validate
            if not self.validate_data(result):
                raise ValueError(f"Data validation failed for {file_path}")
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "file": file_path,
                "type": "unknown"
            }
    
    def _clean_data(self, data: list) -> list:
        """Remove NaN and None values from data"""
        cleaned = []
        for row in data:
            cleaned_row = {}
            for key, value in row.items():
                # Skip NaN values
                if pd.isna(value):
                    cleaned_row[key] = None
                else:
                    cleaned_row[key] = value
            cleaned.append(cleaned_row)
        return cleaned
    
    def _detect_source(self, df: pd.DataFrame) -> str:
        """Detect data source from column patterns"""
        columns = [col.lower() for col in df.columns]
        
        # Google Search Console patterns
        gsc_patterns = ['query', 'impressions', 'clicks', 'ctr', 'position']
        if all(pattern in columns for pattern in gsc_patterns):
            return "Google Search Console"
        
        # Ahrefs patterns
        ahrefs_patterns = ['domain_rating', 'url_rating']
        if any(pattern in columns for pattern in ahrefs_patterns):
            return "Ahrefs"
        
        # SEMrush patterns
        semrush_patterns = ['keyword', 'position', 'search_volume']
        if all(pattern in columns for pattern in semrush_patterns):
            return "SEMrush"
        
        # Screaming Frog patterns
        sf_patterns = ['address', 'status_code', 'indexability']
        if all(pattern in columns for pattern in sf_patterns):
            return "Screaming Frog"
        
        return "Unknown"
    
    def _extract_date_range(self, df: pd.DataFrame) -> Dict[str, str]:
        """Extract date range from data if available"""
        date_range = {"start": None, "end": None}
        
        # Look for date columns
        date_columns = ['date', 'Date', 'DATE', 'day', 'Day']
        date_col = None
        
        for col in date_columns:
            if col in df.columns:
                date_col = col
                break
        
        if date_col:
            try:
                dates = pd.to_datetime(df[date_col])
                date_range["start"] = dates.min().strftime('%Y-%m-%d')
                date_range["end"] = dates.max().strftime('%Y-%m-%d')
            except:
                pass
        
        return date_range
