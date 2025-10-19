#!/usr/bin/env python3
"""
Simple validation script to check project structure
No external dependencies required
"""

import os
import json
from pathlib import Path


def check_file_exists(path, description):
    """Check if a file exists"""
    if Path(path).exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} NOT FOUND")
        return False


def check_directory_exists(path, description):
    """Check if a directory exists"""
    if Path(path).is_dir():
        print(f"✓ {description}: {path}/")
        return True
    else:
        print(f"✗ {description}: {path}/ NOT FOUND")
        return False


def validate_json_file(path):
    """Validate JSON file syntax"""
    try:
        with open(path, 'r') as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON syntax error: {e}")
        return False
    except Exception as e:
        print(f"  ⚠️  Error reading file: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("SEO Analyst Agent - Project Validation")
    print("="*60 + "\n")
    
    checks_passed = 0
    checks_total = 0
    
    # Check core files
    print("Core Files:")
    checks_total += 4
    checks_passed += check_file_exists("main.py", "Main orchestrator")
    checks_passed += check_file_exists("requirements.txt", "Dependencies")
    checks_passed += check_file_exists(".env.example", "Environment template")
    checks_passed += check_file_exists(".gitignore", "Git ignore rules")
    
    # Check parsers
    print("\nParsers:")
    checks_total += 4
    checks_passed += check_file_exists("parsers/__init__.py", "Parsers module")
    checks_passed += check_file_exists("parsers/base_parser.py", "Base parser")
    checks_passed += check_file_exists("parsers/csv_parser.py", "CSV parser")
    checks_passed += check_file_exists("parsers/xlsx_parser.py", "XLSX parser")
    
    # Check agents
    print("\nAgents:")
    checks_total += 7
    checks_passed += check_file_exists("agents/analyst/__init__.py", "Analyst module")
    checks_passed += check_file_exists("agents/analyst/analyzer.py", "Analyst agent")
    checks_passed += check_file_exists("agents/analyst/keywords.py", "Keywords analyzer")
    checks_passed += check_file_exists("agents/analyst/technical.py", "Technical analyzer")
    checks_passed += check_file_exists("agents/critic/__init__.py", "Critic module")
    checks_passed += check_file_exists("agents/critic/validator.py", "Critic agent")
    checks_passed += check_file_exists("agents/reporter/formatter.py", "Reporter agent")
    
    # Check configuration
    print("\nConfiguration:")
    checks_total += 6
    config_exists = check_file_exists("config/env.json", "Environment config")
    checks_passed += config_exists
    if config_exists:
        if validate_json_file("config/env.json"):
            print("  ✓ Valid JSON syntax")
        
    schema_exists = check_file_exists("config/data-schemas.json", "Data schemas")
    checks_passed += schema_exists
    if schema_exists:
        if validate_json_file("config/data-schemas.json"):
            print("  ✓ Valid JSON syntax")
    
    checks_passed += check_file_exists("config/prompts/master.md", "Master prompt")
    checks_passed += check_file_exists("config/prompts/analyst.md", "Analyst prompt")
    checks_passed += check_file_exists("config/prompts/critic.md", "Critic prompt")
    checks_passed += check_file_exists("config/prompts/reporter.md", "Reporter prompt")
    
    # Check directories
    print("\nDirectories:")
    checks_total += 5
    checks_passed += check_directory_exists("data", "Data directory")
    checks_passed += check_directory_exists("data/samples", "Sample data")
    checks_passed += check_directory_exists("outputs", "Outputs directory")
    checks_passed += check_directory_exists("outputs/summaries", "Summaries output")
    checks_passed += check_directory_exists("outputs/action-plans", "Action plans output")
    
    # Check sample data
    print("\nSample Data:")
    checks_total += 2
    checks_passed += check_file_exists("data/samples/search-console-keywords.csv", "Keywords sample")
    checks_passed += check_file_exists("data/samples/technical-audit.csv", "Technical sample")
    
    # Check documentation
    print("\nDocumentation:")
    checks_total += 7
    checks_passed += check_file_exists("README.md", "README")
    checks_passed += check_file_exists("PRD.md", "Product requirements")
    checks_passed += check_file_exists("QUICKSTART.md", "Quick start guide")
    checks_passed += check_file_exists("WORKFLOW.md", "Workflow documentation")
    checks_passed += check_file_exists("IMPLEMENTATION.md", "Implementation guide")
    checks_passed += check_file_exists("PROJECT_SUMMARY.md", "Project summary")
    checks_passed += check_file_exists("STATUS.md", "Status document")
    
    # Check examples
    print("\nExample Outputs:")
    checks_total += 5
    checks_passed += check_file_exists("examples/executive-summary-example.md", "Summary example")
    checks_passed += check_file_exists("examples/action-plan-example.md", "Action plan example")
    checks_passed += check_file_exists("examples/keywords-report-example.md", "Keywords report example")
    checks_passed += check_file_exists("examples/technical-report-example.md", "Technical report example")
    checks_passed += check_file_exists("examples/dashboard-data-example.json", "Dashboard JSON example")
    
    # Summary
    print("\n" + "="*60)
    print(f"Validation Complete: {checks_passed}/{checks_total} checks passed")
    
    if checks_passed == checks_total:
        print("✅ All checks passed! Project structure is complete.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure API key: cp .env.example .env && edit .env")
        print("3. Run analysis: python main.py analyze --reports data/samples/*.csv")
        return 0
    else:
        print(f"⚠️  {checks_total - checks_passed} checks failed.")
        print("Some files or directories are missing.")
        return 1


if __name__ == '__main__':
    exit(main())
