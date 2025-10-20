import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from .keywords import KeywordsAnalyzer
from .technical import TechnicalAnalyzer
from .onpage import OnPageAnalyzer
from .backlinks import BacklinksAnalyzer
from .traffic import TrafficAnalyzer

# Import Phase 2 enhancements
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'utils'))
from industry_detector import industry_detector
from .prompts import IndustryAwarePrompts


class AnalystAgent:
    """
    Main Analyst Agent with Phase 2 AI Enhancements
    - Industry-aware analysis using Claude Sonnet 4.5
    - Advanced pattern recognition
    - Strategic recommendations with ROI estimates
    """

    def __init__(self, api_key: str, config_path: str = "config"):
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
        self.config = self._load_config(config_path)
        self.prompts = self._load_prompts(config_path)

        # Phase 2: Add industry-aware prompts
        self.industry_prompts = IndustryAwarePrompts()
        self.industry_detector = industry_detector

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

    # ========== Phase 2: AI Enhancement Methods ==========

    def generate_executive_summary(self, data: Dict[str, Any], company_name: str) -> str:
        """
        Generate industry-aware executive summary using Claude Sonnet 4.5

        Args:
            data: SEO performance data
            company_name: Name of the company for industry detection

        Returns:
            Professional executive summary (3-4 sentences)
        """
        # Detect industry
        industry = self.industry_detector.detect_industry(company_name, data)

        # Generate industry-aware prompt
        prompt = self.industry_prompts.get_executive_summary_prompt(industry, data)

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,  # Higher for quality summary
                temperature=0.3,  # Lower for more factual output
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text
        except Exception as e:
            print(f"Error generating executive summary: {e}")
            return "Executive summary generation failed. Please check API configuration."

    def generate_strategic_recommendations(self,
                                          data: Dict[str, Any],
                                          company_name: str) -> List[Dict[str, Any]]:
        """
        Generate strategic recommendations with ROI estimates

        Args:
            data: SEO performance data
            company_name: Name of the company

        Returns:
            List of recommendation dictionaries with priorities and impact estimates
        """
        # Detect industry
        industry = self.industry_detector.detect_industry(company_name, data)

        # Generate recommendations prompt
        prompt = self.industry_prompts.get_strategic_recommendations_prompt(industry, data)

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4000,  # Higher for detailed recommendations
                temperature=0.4,  # Balanced creativity/accuracy
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse JSON recommendations from response
            response_text = message.content[0].text

            # Extract JSON objects from response
            recommendations = self._extract_json_recommendations(response_text)

            return recommendations

        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return []

    def generate_performance_insights(self,
                                     data: Dict[str, Any],
                                     company_name: str) -> Dict[str, List[Dict]]:
        """
        Generate deep performance insights with pattern recognition

        Args:
            data: SEO performance data
            company_name: Name of the company

        Returns:
            Dictionary with 'strengths' and 'opportunities' lists
        """
        # Detect industry
        industry = self.industry_detector.detect_industry(company_name, data)

        # Generate performance insights prompt
        prompt = self.industry_prompts.get_performance_insights_prompt(industry, data)

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=3000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            # Parse strengths and opportunities
            insights = self._parse_performance_insights(response_text)

            return insights

        except Exception as e:
            print(f"Error generating performance insights: {e}")
            return {'strengths': [], 'opportunities': []}

    def generate_competitive_analysis(self,
                                     data: Dict[str, Any],
                                     company_name: str,
                                     competitors: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate competitive intelligence analysis

        Args:
            data: SEO performance data
            company_name: Name of the company
            competitors: Optional list of competitor names

        Returns:
            Competitive analysis dictionary
        """
        # Detect industry
        industry = self.industry_detector.detect_industry(company_name, data)

        # Generate competitive analysis prompt
        prompt = self.industry_prompts.get_competitive_analysis_prompt(
            industry, data, competitors
        )

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            return {
                'analysis': message.content[0].text,
                'industry': industry,
                'competitors': competitors or []
            }

        except Exception as e:
            print(f"Error generating competitive analysis: {e}")
            return {'analysis': '', 'industry': industry, 'competitors': []}

    def _extract_json_recommendations(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Extract JSON recommendation objects from Claude's response

        Args:
            response_text: Response text from Claude

        Returns:
            List of recommendation dictionaries
        """
        recommendations = []

        # Find all JSON blocks in the response
        import re
        json_pattern = r'```json\s*(.*?)\s*```'
        matches = re.findall(json_pattern, response_text, re.DOTALL)

        for match in matches:
            try:
                rec = json.loads(match)
                recommendations.append(rec)
            except json.JSONDecodeError:
                continue

        return recommendations

    def _parse_performance_insights(self, response_text: str) -> Dict[str, List[Dict]]:
        """
        Parse strengths and opportunities from response

        Args:
            response_text: Response text from Claude

        Returns:
            Dictionary with 'strengths' and 'opportunities' lists
        """
        insights = {
            'strengths': [],
            'opportunities': []
        }

        # Split by section headers
        strengths_section = ""
        opportunities_section = ""

        if "Key Strengths" in response_text or "💪" in response_text:
            parts = response_text.split("Growth Opportunities")
            if len(parts) == 2:
                strengths_section = parts[0]
                opportunities_section = parts[1]

        # Parse each section (simplified - could be more sophisticated)
        # For now, just store the text sections
        insights['strengths_text'] = strengths_section.strip()
        insights['opportunities_text'] = opportunities_section.strip()

        return insights
