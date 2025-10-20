import json
from pathlib import Path
from typing import Dict, List, Any
from anthropic import Anthropic
from .keywords import KeywordsAnalyzer
from .technical import TechnicalAnalyzer
from .onpage import OnPageAnalyzer
from .backlinks import BacklinksAnalyzer
from .traffic import TrafficAnalyzer


class AnalystAgent:
    """Main Analyst Agent that coordinates analysis across all modules"""
    
    def __init__(self, api_key: str, config_path: str = "config"):
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
        self.config = self._load_config(config_path)
        self.prompts = self._load_prompts(config_path)
        
        # Initialize module analyzers
        self.keywords_analyzer = KeywordsAnalyzer(self.config, self.prompts)
        self.technical_analyzer = TechnicalAnalyzer(self.config, self.prompts)
        self.onpage_analyzer = OnPageAnalyzer(self.config, self.prompts)
        self.backlinks_analyzer = BacklinksAnalyzer(self.config, self.prompts)
        self.traffic_analyzer = TrafficAnalyzer(self.config, self.prompts)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from env.json"""
        try:
            with open(f"{config_path}/env.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _load_prompts(self, config_path: str) -> Dict[str, str]:
        """Load all prompt files"""
        prompts = {}
        prompts_dir = Path(config_path) / "prompts"
        
        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob("*.md"):
                with open(prompt_file, 'r') as f:
                    prompts[prompt_file.stem] = f.read()
        
        return prompts
    
    def analyze(self, parsed_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze a parsed report and generate insights
        
        Args:
            parsed_report: Standardized report from parser
            
        Returns:
            List of insights with recommendations
        """
        report_type = parsed_report.get('type', 'unknown')
        data = parsed_report.get('data', [])
        
        if report_type == 'keywords':
            return self.keywords_analyzer.analyze(data, parsed_report)
        elif report_type == 'technical':
            return self.technical_analyzer.analyze(data, parsed_report)
        elif report_type == 'onpage':
            return self.onpage_analyzer.analyze(data, parsed_report)
        elif report_type == 'backlinks':
            return self.backlinks_analyzer.analyze(data, parsed_report)
        elif report_type == 'traffic':
            return self.traffic_analyzer.analyze(data, parsed_report)
        else:
            return []
    
    def generate_insight_with_llm(self, 
                                  module: str,
                                  finding: str,
                                  data_summary: str) -> str:
        """
        Use LLM to generate detailed insight and recommendation
        
        Args:
            module: Module name (keywords, technical, etc.)
            finding: Brief finding description
            data_summary: Relevant data points
            
        Returns:
            Generated recommendation text
        """
        system_prompt = self.prompts.get('master', '') + "\n\n" + self.prompts.get('analyst', '')
        
        user_prompt = f"""
Based on this SEO data finding, provide a clear, actionable recommendation.

Module: {module}
Finding: {finding}
Data: {data_summary}

Provide:
1. Brief explanation of the issue/opportunity
2. Specific recommendation (what to do)
3. Expected impact

Keep it concise and actionable.
"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            return message.content[0].text
        except Exception as e:
            return f"Recommendation: {finding}"
