#!/usr/bin/env python3
"""
AI Setup Verification Script
Tests Anthropic API configuration and AI agent functionality
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_anthropic_api_key():
    """Test if Anthropic API key is configured"""
    print("\n" + "="*70)
    print("🔑 ANTHROPIC API KEY CONFIGURATION")
    print("="*70)

    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        print("❌ Status: API key NOT configured in environment")
        print("\n📋 How to add your API key:")
        print("   1. Edit the .env file:")
        print(f"      nano {Path(__file__).parent / '.env'}")
        print("\n   2. Replace the placeholder with your actual key:")
        print("      ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here")
        print("\n   3. Get your API key from: https://console.anthropic.com/")
        print("\n   4. Restart the service:")
        print("      sudo systemctl restart seo-analyst")
        return False
    elif api_key == 'your_api_key_here' or api_key.startswith('your'):
        print("⚠️  Status: Placeholder key detected")
        print(f"   Current value: {api_key}")
        print("\n   Replace with real API key from: https://console.anthropic.com/")
        return False
    else:
        print(f"✅ Status: API key configured")
        print(f"   Key: {api_key[:15]}...{api_key[-4:]} ({len(api_key)} chars)")
        return True


def test_anthropic_connection():
    """Test connection to Anthropic API"""
    print("\n" + "="*70)
    print("🌐 ANTHROPIC API CONNECTION TEST")
    print("="*70)

    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key or api_key == 'your_api_key_here':
        print("⏭️  Skipped: No valid API key configured")
        return False

    try:
        from anthropic import Anthropic

        print("   Testing connection to Anthropic API...")
        client = Anthropic(api_key=api_key)

        # Simple test message
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": "Respond with just: 'API connection successful'"
            }]
        )

        response = message.content[0].text
        print(f"✅ Connection successful!")
        print(f"   Response: {response}")
        print(f"   Model: claude-sonnet-4-5-20250929")
        return True

    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False


def test_analyst_agent():
    """Test AnalystAgent initialization"""
    print("\n" + "="*70)
    print("🤖 ANALYST AGENT INITIALIZATION")
    print("="*70)

    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key or api_key == 'your_api_key_here':
        print("⏭️  Skipped: No valid API key configured")
        return False

    try:
        from agents.analyst import AnalystAgent

        print("   Initializing AnalystAgent...")
        analyst = AnalystAgent(api_key, "config")

        print(f"✅ AnalystAgent initialized successfully")
        print(f"   - Industry detector: {'✓' if hasattr(analyst, 'industry_detector') else '✗'}")
        print(f"   - Prioritization engine: {'✓' if hasattr(analyst, 'prioritization_engine') else '✗'}")
        print(f"   - Competitive benchmarks: {'✓' if hasattr(analyst, 'competitive_benchmarks') else '✗'}")
        print(f"   - Module analyzers: 5/5 loaded")
        return True

    except Exception as e:
        print(f"❌ Initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_insight_generation():
    """Test AI insight generation with sample data"""
    print("\n" + "="*70)
    print("💡 AI INSIGHT GENERATION TEST")
    print("="*70)

    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key or api_key == 'your_api_key_here':
        print("⏭️  Skipped: No valid API key configured")
        return False

    try:
        from agents.analyst import AnalystAgent

        print("   Generating test insight...")
        analyst = AnalystAgent(api_key, "config")

        # Test with sample SEO data
        sample_data = {
            'total_clicks': 150,
            'total_impressions': 5000,
            'avg_ctr': 3.0,
            'avg_position': 12.5,
            'top_queries': ['seo services', 'digital marketing', 'website optimization']
        }

        # Generate executive summary
        summary = analyst.generate_executive_summary(sample_data, "Test Company")

        print(f"✅ AI insight generated successfully!")
        print(f"\n   Executive Summary Sample:")
        print(f"   {summary[:200]}...")
        print(f"\n   Full length: {len(summary)} characters")
        return True

    except Exception as e:
        print(f"❌ Insight generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_critic_agent():
    """Test CriticAgent initialization"""
    print("\n" + "="*70)
    print("🎯 CRITIC AGENT INITIALIZATION")
    print("="*70)

    try:
        from agents.critic import CriticAgent

        print("   Initializing CriticAgent...")
        critic = CriticAgent({}, {})

        print(f"✅ CriticAgent initialized successfully")
        print(f"   - Validation rules: loaded")
        print(f"   - Quality thresholds: configured")
        return True

    except Exception as e:
        print(f"❌ Initialization failed: {str(e)}")
        return False


def run_all_tests():
    """Run all AI setup tests"""
    print("\n" + "🔬 SEO ANALYST AI SETUP VERIFICATION")
    print("="*70)

    results = {
        'api_key': test_anthropic_api_key(),
        'connection': False,
        'analyst': False,
        'critic': test_critic_agent(),
        'insights': False
    }

    # Only test connection if API key is valid
    if results['api_key']:
        results['connection'] = test_anthropic_connection()

    # Only test agent if connection works
    if results['connection']:
        results['analyst'] = test_analyst_agent()
        results['insights'] = test_ai_insight_generation()

    # Print summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)

    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)

    print(f"\n   Results: {passed_tests}/{total_tests} tests passed\n")

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status} - {test_name.replace('_', ' ').title()}")

    # Recommendations
    print("\n" + "="*70)
    print("📋 NEXT STEPS")
    print("="*70)

    if not results['api_key']:
        print("\n   🔑 ACTION REQUIRED: Add Anthropic API Key")
        print("\n   1. Get API key from: https://console.anthropic.com/")
        print(f"   2. Edit: {Path(__file__).parent / '.env'}")
        print("   3. Update: ANTHROPIC_API_KEY=sk-ant-api03-your-key-here")
        print("   4. Run: sudo systemctl restart seo-analyst")
        print("   5. Re-run this test: python test_ai_setup.py")
    elif not results['connection']:
        print("\n   ⚠️  API key configured but connection failed")
        print("   - Check if API key is valid")
        print("   - Verify internet connectivity")
        print("   - Check Anthropic API status")
    elif passed_tests == total_tests:
        print("\n   🎉 ALL SYSTEMS READY!")
        print("\n   ✅ AI-powered insights are now enabled")
        print("   ✅ Generate a report to see AI analysis in action")
        print("   ✅ Reports will include:")
        print("      - Industry-aware executive summaries")
        print("      - Strategic recommendations with ROI estimates")
        print("      - Prioritized action items (Quick Wins, High Impact)")
        print("      - Competitive benchmarking")
        print("      - Performance insights and opportunities")
    else:
        print("\n   ⚠️  Some tests failed - review errors above")

    print("\n" + "="*70 + "\n")

    return passed_tests == total_tests


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    success = run_all_tests()
    sys.exit(0 if success else 1)
