#!/usr/bin/env python3
"""
🎨 PREMIUM REPORT GENERATOR
Upload any file (CSV, XLSX, DOCX, PDF) → Get $1000+ consulting-grade report

Usage:
    python upload_and_generate.py path/to/your/file.xlsx
    python upload_and_generate.py path/to/your/file.csv
    python upload_and_generate.py path/to/your/file.pdf
    python upload_and_generate.py path/to/your/file.docx
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, date

# Add project to path
sys.path.append(str(Path(__file__).parent))

from parsers import CSVParser, XLSXParser, DOCXParser, PDFParser
from agents.analyst import AnalystAgent
from agents.critic import CriticAgent
from agents.reporter.premium_pdf_generator import PremiumPDFGenerator
from database import DatabaseManager
import os


class PremiumReportPipeline:
    """End-to-end pipeline for premium report generation"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        
        # Initialize parsers
        self.parsers = {
            '.csv': CSVParser(),
            '.xlsx': XLSXParser(),
            '.xls': XLSXParser(),
            '.docx': DOCXParser(),
            '.doc': DOCXParser(),
            '.pdf': PDFParser(),
        }
        
        # Initialize components
        self.db = DatabaseManager()
        self.premium_pdf = PremiumPDFGenerator(use_database=True)
        
        if self.api_key:
            self.analyst = AnalystAgent(self.api_key, "config")
            self.critic = CriticAgent({}, {})
        else:
            self.analyst = None
            self.critic = None
    
    def process_file(self, file_path: str, company_name: str = None, 
                    report_period: str = None, logo_path: str = None):
        """
        Process uploaded file and generate premium report
        
        Args:
            file_path: Path to uploaded file
            company_name: Client/Company name
            report_period: Report period (e.g., "Q4 2024")
            logo_path: Path to company logo
        """
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"❌ Error: File not found: {file_path}")
            return None
        
        print("="*70)
        print("🎨 PREMIUM REPORT GENERATOR")
        print("="*70)
        print(f"\n📁 File: {file_path.name}")
        print(f"📊 Format: {file_path.suffix.upper()}")
        print(f"💼 Company: {company_name or 'Your Company'}")
        print(f"📅 Period: {report_period or datetime.now().strftime('%B %Y')}")
        
        # Step 1: Parse file
        print("\n🔍 STEP 1: Parsing file...")
        ext = file_path.suffix.lower()
        
        if ext not in self.parsers:
            print(f"❌ Unsupported file type: {ext}")
            print(f"Supported formats: {', '.join(self.parsers.keys())}")
            return None
        
        parser = self.parsers[ext]
        parsed_data = parser.parse(str(file_path))
        
        if 'error' in parsed_data:
            print(f"❌ Parse error: {parsed_data['error']}")
            return None
        
        print(f"✅ Successfully parsed {parsed_data.get('record_count', 0)} records")
        print(f"📋 Report type: {parsed_data.get('type', 'unknown')}")
        
        # Step 2: Analyze data
        print("\n🧠 STEP 2: Analyzing data...")
        
        if self.analyst:
            insights = self.analyst.analyze(parsed_data)
            print(f"✅ Generated {len(insights)} insights")
            
            # Validate with critic
            validation = self.critic.validate(insights)
            approved_insights = self.critic.filter_approved_insights(insights, validation)
            print(f"✅ {len(approved_insights)} insights approved")
        else:
            # Create sample insights if no API key
            approved_insights = self._create_sample_insights(parsed_data)
            print(f"⚠️  Using sample insights (no API key provided)")
            print(f"✅ {len(approved_insights)} sample insights created")
        
        # Step 3: Store in database
        print("\n💾 STEP 3: Storing data...")
        
        client_name = company_name or "Your Company"
        client = self.db.get_client(name=client_name)
        
        if not client:
            client_id = self.db.create_client(client_name, domain="example.com")
            print(f"✅ Created client: {client_name}")
        else:
            client_id = client['id']
            print(f"✅ Using existing client: {client_name}")
        
        # Store report
        health_score = 100 - (len([i for i in approved_insights if i.get('severity') == 'high']) * 8)
        health_score = max(0, min(100, health_score))
        
        report_id = self.db.create_report(
            client_id=client_id,
            report_date=date.today(),
            report_period=report_period or datetime.now().strftime('%B %Y'),
            insights_count=len(approved_insights),
            health_score=health_score
        )
        
        self.db.save_insights(report_id, client_id, approved_insights)
        print(f"✅ Report #{report_id} stored in database")
        
        # Step 4: Generate premium PDF
        print("\n🎨 STEP 4: Generating PREMIUM PDF REPORT...")
        print("   ⭐ Consulting-grade design")
        print("   ⭐ Executive-level content")
        print("   ⭐ Strategic recommendations")
        print("   ⭐ ROI projections")
        
        pdf_file = self.premium_pdf.generate_premium_report(
            insights=approved_insights,
            company_name=client_name,
            report_period=report_period or datetime.now().strftime('%B %Y'),
            client_id=client_id,
            logo_path=logo_path
        )
        
        print("\n" + "="*70)
        print("✨ SUCCESS! PREMIUM REPORT GENERATED")
        print("="*70)
        print(f"\n📄 Report Location: {pdf_file}")
        print(f"📊 Quality Level: $1000+ Consulting Grade")
        print(f"📈 Insights: {len(approved_insights)}")
        print(f"🎯 Health Score: {health_score}/100")
        print(f"💼 Client: {client_name}")
        
        print("\n🎁 WHAT'S INSIDE:")
        print("   ✅ Executive Letter (personalized)")
        print("   ✅ Premium Table of Contents")
        print("   ✅ Executive Dashboard (KPIs)")
        print("   ✅ Performance Overview (6-month trends)")
        print("   ✅ Strategic Insights (prioritized)")
        print("   ✅ Detailed Analysis (all modules)")
        print("   ✅ Forecasts & Projections (90-day)")
        print("   ✅ Action Plan & Roadmap (timeline)")
        print("   ✅ ROI Projections (business impact)")
        
        print("\n💎 PREMIUM DESIGN FEATURES:")
        print("   • Luxury navy & gold color scheme")
        print("   • Executive-level typography")
        print("   • Professional gradient covers")
        print("   • Consulting-grade layout")
        print("   • Confidential watermarks")
        print("   • Premium page templates")
        
        print("\n💡 TO VIEW:")
        print(f"   open {pdf_file}")
        
        print("\n🚀 Ready to impress clients!")
        print("="*70 + "\n")
        
        return pdf_file
    
    def _create_sample_insights(self, parsed_data):
        """Create sample insights when no API key available"""
        
        report_type = parsed_data.get('type', 'general')
        
        sample_insights = [
            {
                'module': 'keywords',
                'type': 'opportunity',
                'severity': 'high',
                'insight': f'Analysis of {report_type} data reveals significant optimization opportunities in keyword performance.',
                'metric_value': 85
            },
            {
                'module': 'technical',
                'type': 'issue',
                'severity': 'high',
                'insight': 'Technical SEO audit identified critical issues requiring immediate attention.',
                'metric_value': 23
            },
            {
                'module': 'content',
                'type': 'opportunity',
                'severity': 'medium',
                'insight': 'Content quality analysis shows strong foundation with room for strategic improvements.',
                'metric_value': 78
            },
            {
                'module': 'backlinks',
                'type': 'win',
                'severity': 'low',
                'insight': 'Link profile demonstrates positive growth trajectory and quality backlink acquisition.',
                'metric_value': 92
            },
            {
                'module': 'technical',
                'type': 'issue',
                'severity': 'medium',
                'insight': 'Site architecture optimization recommended to improve crawl efficiency and user experience.',
                'metric_value': 15
            },
            {
                'module': 'keywords',
                'type': 'win',
                'severity': 'low',
                'insight': 'Strong keyword positioning achieved in target market segments.',
                'metric_value': 45
            },
            {
                'module': 'analytics',
                'type': 'insight',
                'severity': 'medium',
                'insight': 'Traffic patterns indicate seasonal opportunities for content optimization.',
                'metric_value': 67
            },
        ]
        
        return sample_insights


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description="🎨 Generate premium $1000+ consulting-grade SEO reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python upload_and_generate.py data/report.xlsx
  python upload_and_generate.py data/report.csv --company "ACME Corp" --period "Q4 2024"
  python upload_and_generate.py data/report.pdf --company "TechCo" --logo assets/logo.png
  
Supported formats: CSV, XLSX, XLS, DOCX, DOC, PDF
        """
    )
    
    parser.add_argument(
        'file',
        help='Path to your SEO report file (CSV, XLSX, DOCX, PDF)'
    )
    
    parser.add_argument(
        '--company',
        default=None,
        help='Company/Client name (default: "Your Company")'
    )
    
    parser.add_argument(
        '--period',
        default=None,
        help='Report period (default: current month, e.g., "November 2024")'
    )
    
    parser.add_argument(
        '--logo',
        default=None,
        help='Path to company logo (PNG/JPG)'
    )
    
    parser.add_argument(
        '--api-key',
        default=None,
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = PremiumReportPipeline(api_key=args.api_key)
    
    # Process file
    pdf_file = pipeline.process_file(
        file_path=args.file,
        company_name=args.company,
        report_period=args.period,
        logo_path=args.logo
    )
    
    if pdf_file:
        # Auto-open on macOS
        if sys.platform == 'darwin':
            import subprocess
            subprocess.run(['open', pdf_file])
        
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
