import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path


class ReporterAgent:
    """Formats insights into client-ready reports"""
    
    def __init__(self, config: Dict, prompts: Dict, output_dir: str = "outputs"):
        self.config = config
        self.prompts = prompts
        self.output_dir = Path(output_dir)
        
    def create_executive_summary(self, insights: List[Dict]) -> str:
        """
        Create executive summary (≤300 words)
        
        Args:
            insights: List of validated insights
            
        Returns:
            Markdown formatted summary
        """
        # Group by severity
        high_severity = [i for i in insights if i['severity'] == 'high']
        medium_severity = [i for i in insights if i['severity'] == 'medium']
        low_severity = [i for i in insights if i['severity'] == 'low']
        
        # Build summary
        summary = f"# Executive Summary\n\n"
        summary += f"**Report Generated**: {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        # Overall assessment
        if len(high_severity) > 3:
            summary += "This month's analysis reveals **significant issues requiring immediate attention**. "
        elif len(high_severity) > 0:
            summary += "This month's analysis shows **some critical issues** alongside opportunities for improvement. "
        else:
            summary += "This month's analysis shows **overall positive performance** with room for optimization. "
        
        summary += f"We identified **{len(insights)} total findings** across SEO modules.\n\n"
        
        # Key highlights
        summary += "## Key Highlights\n\n"
        
        # Top 3-5 findings
        top_findings = high_severity[:3] + medium_severity[:2]
        for finding in top_findings[:5]:
            module = finding['module'].title()
            summary += f"• **{module}**: {finding['finding']}\n"
        
        # Critical issues
        if high_severity:
            summary += "\n## Critical Issues\n\n"
            for issue in high_severity[:3]:
                summary += f"• {issue['finding']}\n"
        
        # Opportunities
        opportunities = [i for i in insights if i.get('category') == 'opportunity' or 'opportunity' in i.get('finding', '').lower()]
        if opportunities:
            summary += "\n## Opportunities\n\n"
            for opp in opportunities[:2]:
                summary += f"• {opp['finding']}\n"
        
        summary += f"\n**Next Steps**: Review the detailed action plan below for prioritized recommendations.\n"
        
        return summary
    
    def create_action_plan(self, insights: List[Dict]) -> str:
        """
        Create prioritized action plan (5-10 items)
        
        Args:
            insights: List of validated insights
            
        Returns:
            Markdown formatted action plan
        """
        # Sort by severity
        high = sorted([i for i in insights if i['severity'] == 'high'], 
                     key=lambda x: x.get('metrics', {}).get('count', 0), reverse=True)
        medium = sorted([i for i in insights if i['severity'] == 'medium'],
                       key=lambda x: x.get('metrics', {}).get('count', 0), reverse=True)
        low = sorted([i for i in insights if i['severity'] == 'low'],
                    key=lambda x: x.get('metrics', {}).get('count', 0), reverse=True)
        
        action_plan = f"# Action Plan\n\n"
        action_plan += f"**Generated**: {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        # High Priority
        if high:
            action_plan += "## 🔴 High Priority (Do First)\n\n"
            action_plan += "_These issues have the biggest impact on SEO performance._\n\n"
            
            for idx, item in enumerate(high[:5], 1):
                action_plan += f"### {idx}. {item['finding']}\n\n"
                action_plan += f"**Module**: {item['module'].title()}\n\n"
                action_plan += f"**Impact**: {self._describe_impact(item)}\n\n"
                action_plan += f"**Action**: {item['recommendation']}\n\n"
                
                if item.get('affected_items'):
                    action_plan += f"**Affected Items**: {len(item['affected_items'])} items\n\n"
                
                action_plan += "---\n\n"
        
        # Medium Priority
        if medium:
            action_plan += "## 🟡 Medium Priority (Important)\n\n"
            action_plan += "_These improvements will enhance performance but are less urgent._\n\n"
            
            for idx, item in enumerate(medium[:3], 1):
                action_plan += f"### {idx}. {item['finding']}\n\n"
                action_plan += f"**Action**: {item['recommendation']}\n\n"
                action_plan += "---\n\n"
        
        # Low Priority
        if low:
            action_plan += "## 🟢 Low Priority (Nice to Have)\n\n"
            action_plan += "_These optimizations can be addressed after higher priorities._\n\n"
            
            for idx, item in enumerate(low[:2], 1):
                action_plan += f"- {item['finding']}: {item['recommendation']}\n"
        
        return action_plan
    
    def create_module_report(self, module: str, insights: List[Dict]) -> str:
        """
        Create detailed module report
        
        Args:
            module: Module name (keywords, technical, etc.)
            insights: Insights for this module only
            
        Returns:
            Markdown formatted module report
        """
        if not insights:
            return ""
        
        report = f"# {module.title()} Report\n\n"
        report += f"**Generated**: {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        # Performance overview
        report += "## Performance Overview\n\n"
        report += self._generate_overview(insights)
        report += "\n\n"
        
        # Key metrics
        report += "## Key Metrics\n\n"
        report += self._generate_metrics_table(insights)
        report += "\n\n"
        
        # Detailed insights
        report += "## Insights\n\n"
        for idx, insight in enumerate(insights, 1):
            report += f"### {idx}. {insight['finding']}\n\n"
            report += f"**Severity**: {insight['severity'].upper()}\n\n"
            
            if insight.get('metrics'):
                report += "**Metrics**:\n"
                for key, value in insight['metrics'].items():
                    report += f"- {key.replace('_', ' ').title()}: {value}\n"
                report += "\n"
            
            report += f"**Recommendation**: {insight['recommendation']}\n\n"
            report += "---\n\n"
        
        return report
    
    def export_json(self, insights: List[Dict], filename: str):
        """Export insights as JSON for dashboard integration"""
        output_path = self.output_dir / "dashboards" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_insights": len(insights),
            "by_severity": {
                "high": len([i for i in insights if i['severity'] == 'high']),
                "medium": len([i for i in insights if i['severity'] == 'medium']),
                "low": len([i for i in insights if i['severity'] == 'low'])
            },
            "by_module": self._group_by_module(insights),
            "insights": insights
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(output_path)
    
    def save_report(self, content: str, filename: str, report_type: str):
        """Save report to appropriate directory"""
        if report_type == 'summary':
            output_path = self.output_dir / "summaries" / filename
        elif report_type == 'action_plan':
            output_path = self.output_dir / "action-plans" / filename
        elif report_type == 'module':
            output_path = self.output_dir / "summaries" / filename
        else:
            output_path = self.output_dir / filename
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return str(output_path)
    
    def _describe_impact(self, insight: Dict) -> str:
        """Generate impact description"""
        metrics = insight.get('metrics', {})
        
        if 'estimated_traffic_loss' in metrics:
            return f"Estimated {metrics['estimated_traffic_loss']} clicks lost"
        elif 'potential_clicks' in metrics:
            return f"Potential to gain {metrics['potential_clicks']} additional clicks"
        elif 'count' in metrics:
            return f"Affects {metrics['count']} items"
        else:
            return "See metrics for details"
    
    def _generate_overview(self, insights: List[Dict]) -> str:
        """Generate performance overview text"""
        high_count = len([i for i in insights if i['severity'] == 'high'])
        
        if high_count > 0:
            return f"This module shows {high_count} critical issues requiring immediate attention. " \
                   f"Total of {len(insights)} findings identified with actionable recommendations."
        else:
            return f"This module shows healthy performance with {len(insights)} optimization opportunities identified."
    
    def _generate_metrics_table(self, insights: List[Dict]) -> str:
        """Generate metrics summary table"""
        table = "| Metric | Value |\n"
        table += "|--------|-------|\n"
        table += f"| Total Findings | {len(insights)} |\n"
        table += f"| High Severity | {len([i for i in insights if i['severity'] == 'high'])} |\n"
        table += f"| Medium Severity | {len([i for i in insights if i['severity'] == 'medium'])} |\n"
        table += f"| Low Severity | {len([i for i in insights if i['severity'] == 'low'])} |\n"
        
        return table
    
    def _group_by_module(self, insights: List[Dict]) -> Dict[str, int]:
        """Group insights by module"""
        modules = {}
        for insight in insights:
            module = insight.get('module', 'unknown')
            modules[module] = modules.get(module, 0) + 1
        return modules
