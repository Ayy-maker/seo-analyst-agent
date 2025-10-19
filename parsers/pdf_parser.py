"""
PDF Parser for SEO Reports
Extracts text and tables from PDF documents
"""

from pathlib import Path
from typing import Dict, List
import re


class PDFParser:
    """Parse PDF files containing SEO data"""
    
    def parse(self, file_path: str) -> Dict:
        """Parse PDF file and extract SEO data"""
        try:
            # Try to import PyPDF2
            try:
                import PyPDF2
            except ImportError:
                print("⚠️  PyPDF2 not installed. Already in requirements.txt")
                return {
                    'source_file': Path(file_path).name,
                    'error': 'PyPDF2 not installed. Run: pip install PyPDF2',
                    'status': 'error'
                }
            
            # Extract text from PDF
            text_content = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(text)
            
            full_text = '\n\n'.join(text_content)
            
            # Identify report type
            report_type = self._identify_report_type(full_text)
            
            # Extract structured data
            structured_data = self._extract_metrics_from_text(full_text)
            
            return {
                'source_file': Path(file_path).name,
                'type': report_type,
                'format': 'pdf',
                'raw_text': full_text[:5000],  # First 5000 chars
                'structured_data': structured_data,
                'record_count': len(structured_data),
                'pages': len(pdf_reader.pages),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'source_file': Path(file_path).name,
                'error': f"Failed to parse PDF: {str(e)}",
                'status': 'error'
            }
    
    def _identify_report_type(self, text: str) -> str:
        """Identify what type of SEO report this is"""
        text_lower = text.lower()
        
        if 'search console' in text_lower or 'google search' in text_lower:
            return 'search-console'
        elif 'analytics' in text_lower or 'ga4' in text_lower:
            return 'analytics'
        elif 'ahrefs' in text_lower or 'backlink' in text_lower:
            return 'backlinks'
        elif 'semrush' in text_lower or 'keyword' in text_lower:
            return 'keywords'
        elif 'screaming frog' in text_lower or 'crawl' in text_lower:
            return 'technical'
        else:
            return 'general'
    
    def _extract_metrics_from_text(self, text: str) -> List[Dict]:
        """Extract metrics from text"""
        metrics = []
        
        # Common SEO metrics patterns
        patterns = [
            (r'(?:organic\s+)?traffic[:\s]+([0-9,]+)', 'traffic'),
            (r'(?:total\s+)?clicks[:\s]+([0-9,]+)', 'clicks'),
            (r'impressions[:\s]+([0-9,]+)', 'impressions'),
            (r'(?:average\s+)?ctr[:\s]+([0-9.]+)%?', 'ctr'),
            (r'(?:average\s+)?position[:\s]+([0-9.]+)', 'position'),
            (r'keywords[:\s]+([0-9,]+)', 'keywords'),
            (r'backlinks[:\s]+([0-9,]+)', 'backlinks'),
            (r'domain\s+authority[:\s]+([0-9]+)', 'domain_authority'),
            (r'page\s+speed[:\s]+([0-9.]+)', 'page_speed'),
        ]
        
        for pattern, metric_name in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                value = matches[0].replace(',', '')
                try:
                    metrics.append({
                        'metric': metric_name,
                        'value': float(value)
                    })
                except ValueError:
                    pass
        
        return metrics if metrics else [{'content': text[:1000]}]
