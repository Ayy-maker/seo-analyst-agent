#!/usr/bin/env python3
"""
Generate test reports for all clients to verify improvements
Simple version that tests with minimal/empty data to verify "no data" messages
"""

import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))

from database import DatabaseManager
from agents.reporter.enhanced_html_generator import EnhancedHTMLGenerator
from dotenv import load_dotenv

load_dotenv()

html_generator = EnhancedHTMLGenerator()

def generate_client_report(client):
    """Generate report for a single client with minimal data"""
    print(f"\n{'='*60}")
    print(f"Generating report for: {client['name']}")
    print(f"{'='*60}")

    client_id = client['id']
    client_name = client['name']

    # Create minimal dataset to test "no data" messages and baseline analysis
    print("📊 Creating minimal test dataset...")
    normalized_data = {
        'company': client_name,
        'kpis': {
            'total_clicks': {'value': 5, 'change': 0},
            'total_impressions': {'value': 1500, 'change': 0},
            'ctr': {'value': 0.33, 'change': 0},
            'avg_position': {'value': 55.5, 'change': 0},
            'total_users': {'value': 100, 'change': 0},
            'total_sessions': {'value': 120, 'change': 0}
        },
        'queries': [],  # Empty to test "no data" message
        'landing_pages': [],  # Empty to test "no data" message
        'devices': [],  # Empty to test "no data" message
        'user_activity': {
            'daily_users': [],
            'sessions_by_channel': []
        }
    }

    # Generate AI recommendations (Phase 3)
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        print("🤖 Generating AI recommendations...")
        try:
            from agents.analyst import AnalystAgent
            from utils.prioritization_engine import prioritization_engine

            analyst = AnalystAgent(api_key=api_key)
            recommendations = analyst.generate_strategic_recommendations(normalized_data, client_name)
            prioritized_recs = prioritization_engine.prioritize_recommendations(recommendations)
            priority_summary = prioritization_engine.get_priority_summary(prioritized_recs)

            if 'phase3' not in normalized_data:
                normalized_data['phase3'] = {}
            normalized_data['phase3']['prioritized_recommendations'] = prioritized_recs
            normalized_data['phase3']['priority_summary'] = priority_summary
            print("✅ AI recommendations generated")
        except Exception as e:
            print(f"⚠️  AI recommendations failed: {e}")
    else:
        print("⚠️  No API key - skipping AI recommendations")

    # Generate HTML report
    print("📄 Generating HTML report...")
    html_output = html_generator.generate_full_report(
        seo_data=normalized_data,
        company_name=client_name,
        client_id=client_id
    )

    # Save report
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    safe_name = client_name.lower().replace(' ', '-')
    report_filename = f"seo-report-{safe_name}-{timestamp}.html"
    report_path = f"outputs/html-reports/{report_filename}"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"✅ Report saved: {report_path}")

    # Verify improvements in the report
    print("\n🔍 Verifying improvements...")
    improvements = {
        'has_no_data_message_queries': 'No query data available yet' in html_output,
        'has_no_data_message_pages': 'No landing page data available yet' in html_output,
        'has_no_data_message_devices': 'No device data available yet' in html_output,
        'has_baseline_analysis': 'Baseline Performance Analysis' in html_output or 'Performance Insights' in html_output,
        'has_building_foundation': 'Building SEO Foundation' in html_output or 'Key Strengths' in html_output,
        'no_generic_claims': 'brand authority' not in html_output.lower() and 'market leader' not in html_output.lower(),
        'has_recommendations': 'phase3' in normalized_data and normalized_data.get('phase3', {}).get('prioritized_recommendations')
    }

    for check, result in improvements.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}: {result}")

    # Get metrics summary
    kpis = normalized_data.get('kpis', {})
    print("\n📊 Metrics Summary:")
    print(f"   Total Clicks: {kpis.get('total_clicks', {}).get('value', 0)}")
    print(f"   Total Impressions: {kpis.get('total_impressions', {}).get('value', 0)}")
    print(f"   Avg Position: {kpis.get('avg_position', {}).get('value', 0):.1f}")
    print(f"   CTR: {kpis.get('ctr', {}).get('value', 0):.2f}%")
    print(f"   Total Users: {kpis.get('total_users', {}).get('value', 0)}")

    return report_path, improvements

def main():
    """Generate reports for all clients"""
    print("\n" + "="*60)
    print("🚀 COMPREHENSIVE CLIENT REPORT TEST")
    print("="*60)

    db = DatabaseManager()
    clients = db.get_all_clients()

    print(f"\nFound {len(clients)} clients to test")

    results = {}

    for client in clients:
        try:
            report_path, improvements = generate_client_report(client)
            results[client['name']] = {
                'success': True,
                'report': report_path,
                'improvements': improvements
            }
        except Exception as e:
            print(f"\n❌ ERROR generating report for {client['name']}: {e}")
            results[client['name']] = {
                'success': False,
                'error': str(e)
            }

    # Final summary
    print("\n" + "="*60)
    print("📋 FINAL SUMMARY")
    print("="*60)

    successful = sum(1 for r in results.values() if r.get('success', False))
    total = len(results)

    print(f"\n✅ Reports Generated: {successful}/{total}")

    for client_name, result in results.items():
        if result.get('success'):
            print(f"\n{client_name}:")
            print(f"   📄 Report: {result['report']}")
            improvements = result['improvements']
            all_passed = all(improvements.values())
            status = "✅ ALL CHECKS PASSED" if all_passed else "⚠️  SOME CHECKS FAILED"
            print(f"   {status}")
        else:
            print(f"\n{client_name}: ❌ FAILED - {result.get('error', 'Unknown error')}")

    print("\n" + "="*60)
    print("✅ TEST COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
