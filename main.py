#!/usr/bin/env python3
"""
SEO Analyst Agent - Main Orchestrator

Usage:
    python main.py analyze --reports data/*.csv
    python main.py analyze --reports data/search-console.csv --api-key YOUR_KEY
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

from parsers import CSVParser, XLSXParser
from agents.analyst import AnalystAgent
from agents.critic import CriticAgent
from agents.reporter import ReporterAgent, EnhancedHTMLGenerator
from database import DatabaseManager


class SEOAnalyst:
    """Main orchestrator for SEO analysis workflow"""
    
    def __init__(self, api_key: str = None, config_path: str = "config"):
        # Load environment variables
        load_dotenv()
        
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            print("⚠️  Warning: No API key provided. LLM features will be limited.")
        
        # Load configuration
        self.config = self._load_config(config_path)
        self.prompts = self._load_prompts(config_path)
        
        # Initialize components
        self.csv_parser = CSVParser()
        self.xlsx_parser = XLSXParser()
        self.analyst = AnalystAgent(self.api_key, config_path) if self.api_key else None
        self.critic = CriticAgent(self.config, self.prompts)
        self.reporter = ReporterAgent(self.config, self.prompts)
        
        # HTML generator for reports
        self.html_generator = EnhancedHTMLGenerator()
        self.db = DatabaseManager()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        try:
            with open(f"{config_path}/env.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _load_prompts(self, config_path: str) -> Dict[str, str]:
        """Load prompt files"""
        prompts = {}
        prompts_dir = Path(config_path) / "prompts"
        
        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob("*.md"):
                with open(prompt_file, 'r') as f:
                    prompts[prompt_file.stem] = f.read()
        
        return prompts
    
    def analyze(self, report_paths: List[str]) -> Dict:
        """
        Main analysis workflow
        
        Steps:
        1. Parse reports
        2. Analyze with Analyst Agent
        3. Validate with Critic Agent
        4. Generate reports with Reporter Agent
        5. Save outputs
        """
        print(f"\n🔍 SEO Analyst Agent - Starting Analysis\n")
        print(f"Reports to analyze: {len(report_paths)}")
        print("=" * 60)
        
        # Step 1: Parse reports
        print("\n📄 Step 1: Parsing reports...")
        parsed_reports = []
        
        for path in report_paths:
            print(f"  - Parsing: {Path(path).name}")
            parsed = self._parse_report(path)
            
            if 'error' in parsed:
                print(f"    ❌ Error: {parsed['error']}")
                continue
            
            print(f"    ✓ Type: {parsed['type']}, Records: {parsed['record_count']}")
            parsed_reports.append(parsed)
        
        if not parsed_reports:
            print("\n❌ No valid reports parsed. Exiting.")
            return {}
        
        # Step 2: Analyze
        print("\n🧠 Step 2: Analyzing reports...")
        all_insights = []
        
        if not self.analyst:
            print("  ⚠️  Skipping AI analysis (no API key)")
        else:
            for report in parsed_reports:
                print(f"  - Analyzing: {report['type']}")
                insights = self.analyst.analyze(report)
                print(f"    ✓ Found {len(insights)} insights")
                all_insights.extend(insights)
        
        if not all_insights:
            print("\n⚠️  No insights generated.")
            return {}
        
        # Step 3: Validate
        print("\n✅ Step 3: Validating insights...")
        validation = self.critic.validate(all_insights)
        print(f"  - Total insights: {validation['summary']['total']}")
        print(f"  - Approved: {validation['summary']['approved']}")
        print(f"  - Rejected: {validation['summary']['rejected']}")
        print(f"  - Flagged: {validation['summary']['flagged']}")
        
        approved_insights = self.critic.filter_approved_insights(all_insights, validation)
        
        # Step 4: Generate reports
        print("\n📝 Step 4: Generating reports...")
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        
        # Executive summary
        summary = self.reporter.create_executive_summary(approved_insights)
        summary_file = self.reporter.save_report(
            summary, 
            f"executive-summary-{timestamp}.md",
            "summary"
        )
        print(f"  ✓ Executive Summary: {summary_file}")
        
        # Action plan
        action_plan = self.reporter.create_action_plan(approved_insights)
        action_file = self.reporter.save_report(
            action_plan,
            f"action-plan-{timestamp}.md",
            "action_plan"
        )
        print(f"  ✓ Action Plan: {action_file}")
        
        # Module reports
        modules = set(i['module'] for i in approved_insights)
        for module in modules:
            module_insights = [i for i in approved_insights if i['module'] == module]
            module_report = self.reporter.create_module_report(module, module_insights)
            module_file = self.reporter.save_report(
                module_report,
                f"{module}-report-{timestamp}.md",
                "module"
            )
            print(f"  ✓ {module.title()} Report: {module_file}")
        
        # JSON export
        json_file = self.reporter.export_json(
            approved_insights,
            f"dashboard-data-{timestamp}.json"
        )
        print(f"  ✓ Dashboard Data: {json_file}")
        
        # 🎨 Generate Professional PDF Report
        print("\n📄 Generating Professional PDF Report...")
        
        # Get or create client
        client_name = "SEO Client"  # TODO: Make this configurable
        client = self.db.get_client(name=client_name)
        if not client:
            client_id = self.db.create_client(client_name, domain="example.com")
            print(f"  ✓ Created new client: {client_name}")
        else:
            client_id = client['id']
            print(f"  ✓ Using existing client: {client_name}")
        
        # Store report in database
        report_id = self.db.create_report(
            client_id=client_id,
            report_date=datetime.now().date(),
            report_period="Monthly Analysis",
            insights_count=len(approved_insights),
            health_score=100 - (len([i for i in approved_insights if i.get('severity') == 'high']) * 8)
        )
        
        # Store insights in database
        self.db.save_insights(report_id, client_id, approved_insights)
        
        # Generate HTML report
        html_file = self.html_generator.generate_full_report(
            company_name=client_name,
            report_period="Monthly Analysis",
            seo_data=None  # Will use default sample data
        )
        
        # Update report with HTML file path
        self.db.update_report(report_id, file_path=html_file)
        print(f"  ✓ Enhanced HTML Report: {html_file}")
        
        print("\n" + "=" * 60)
        print("✨ Analysis complete!")
        print(f"\nGenerated {len(approved_insights)} actionable insights")
        print(f"Reports saved to: outputs/")
        print(f"📊 Professional HTML Report: {html_file}\n")
        
        return {
            "insights": approved_insights,
            "validation": validation,
            "files": {
                "summary": summary_file,
                "action_plan": action_file,
                "dashboard": json_file,
                "html_report": html_file
            }
        }
    
    def _parse_report(self, file_path: str) -> Dict:
        """Parse a report file based on extension"""
        path = Path(file_path)
        
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        ext = path.suffix.lower()
        
        if ext == '.csv':
            return self.csv_parser.parse(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self.xlsx_parser.parse(file_path)
        else:
            return {"error": f"Unsupported file type: {ext}"}


def main():
    parser = argparse.ArgumentParser(
        description="SEO Analyst Agent - Automated SEO Report Analysis"
    )
    
    parser.add_argument(
        'command',
        choices=['analyze'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--reports',
        nargs='+',
        required=True,
        help='Path(s) to report files (CSV, XLSX)'
    )
    
    parser.add_argument(
        '--api-key',
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )
    
    parser.add_argument(
        '--config',
        default='config',
        help='Path to config directory (default: config)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyst = SEOAnalyst(api_key=args.api_key, config_path=args.config)
        result = analyst.analyze(args.reports)
        
        if result:
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
