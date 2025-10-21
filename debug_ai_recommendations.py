#!/usr/bin/env python3
"""Debug AI recommendations structure"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

from integrations.gsc_api_client import GSCAPIClient
from integrations.ga4_api_client import GA4APIClient
from utils.data_normalizer import data_normalizer
from agents.analyst import AnalystAgent
from utils.prioritization_engine import prioritization_engine

api_key = os.getenv('ANTHROPIC_API_KEY')
company_name = "The Profit Platform"

# Fetch data
print("Fetching data...")
gsc_client = GSCAPIClient()
gsc_client.connect()
queries = gsc_client.fetch_queries_with_metrics("sc-domain:theprofitplatform.com.au", days=30)

gsc_parsed = {
    'source': 'Google Search Console',
    'site_url': 'sc-domain:theprofitplatform.com.au',
    'record_count': len(queries),
    'data': queries
}
normalized_data = data_normalizer.normalize_gsc_data(gsc_parsed, company_name)

ga4_client = GA4APIClient(property_id="500340846")
ga4_client.connect()
behavior_data = ga4_client.fetch_user_behavior(days=30)

ga4_parsed = {
    'source': 'Google Analytics 4',
    'property_id': "500340846",
    'record_count': behavior_data.get('total_rows', 0),
    'data': behavior_data.get('data', [])
}
ga4_metrics = data_normalizer.normalize_ga4_data(ga4_parsed)

merged_data = data_normalizer.merge_gsc_and_ga4_data(normalized_data, ga4_metrics)

print("\nGenerating AI recommendations...")
analyst = AnalystAgent(api_key, "config")
recommendations = analyst.generate_strategic_recommendations(merged_data, company_name)

print(f"\nReceived {len(recommendations)} recommendations from AI")
print("\nRecommendation structure:")
print(json.dumps(recommendations, indent=2))

print("\n\nPrioritizing...")
prioritized = prioritization_engine.prioritize_recommendations(recommendations)

print(f"\nPrioritized structure:")
print(json.dumps(prioritized, indent=2))

# Save to file
with open('debug_recommendations.json', 'w') as f:
    json.dump({
        'raw_recommendations': recommendations,
        'prioritized_recommendations': prioritized
    }, f, indent=2)

print("\n✅ Saved to debug_recommendations.json")
