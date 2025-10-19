import pandas as pd
from pathlib import Path
from typing import Dict, Any
from .base_parser import BaseParser


class XLSXParser(BaseParser):
    """Parser for XLSX files (Excel exports from SEO tools)"""
    
    def parse(self, file_path: str, sheet_name: str = 0) -> Dict[str, Any]:
        """
        Parse XLSX file into standard format
        
        Args:
            file_path: Path to XLSX file
            sheet_name: Sheet name or index to parse (default: first sheet)
            
        Returns:
            Standardized report dictionary
        """
        try:
            # Read Excel with pandas
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Normalize column names
            df = self.normalize_columns(df)
            
            # Detect report type
            report_type = self.detect_type(df)
            
            # Convert to list of dictionaries
            data = df.to_dict('records')
            
            # Clean data
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
                if pd.isna(value):
                    cleaned_row[key] = None
                else:
                    cleaned_row[key] = value
            cleaned.append(cleaned_row)
        return cleaned
    
    def _detect_source(self, df: pd.DataFrame) -> str:
        """Detect data source from column patterns"""
        columns = [col.lower() for col in df.columns]
        
        # Ahrefs patterns
        if 'domain_rating' in columns or 'url_rating' in columns:
            return "Ahrefs"
        
        # SEMrush patterns
        if 'keyword_difficulty' in columns or 'search_volume' in columns:
            return "SEMrush"
        
        # Moz patterns
        if 'domain_authority' in columns or 'page_authority' in columns:
            return "Moz"
        
        # Screaming Frog patterns
        if 'indexability' in columns and 'status_code' in columns:
            return "Screaming Frog"
        
        return "Unknown"
    
    def _extract_date_range(self, df: pd.DataFrame) -> Dict[str, str]:
        """Extract date range from data if available"""
        date_range = {"start": None, "end": None}
        
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
