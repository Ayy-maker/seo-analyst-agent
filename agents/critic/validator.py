from typing import Dict, List, Any
from datetime import datetime


class CriticAgent:
    """Validates insights from Analyst Agent for accuracy and actionability"""
    
    def __init__(self, config: Dict, prompts: Dict):
        self.config = config
        self.prompts = prompts
        self.priorities = config.get('PRIORITIES', {})
        
    def validate(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate all insights
        
        Args:
            insights: List of insights from Analyst
            
        Returns:
            Validation report with approved/rejected/flagged insights
        """
        approved = []
        rejected = []
        flagged = []
        issues = []
        
        for insight in insights:
            validation_result = self._validate_insight(insight)
            
            if validation_result['status'] == 'approved':
                approved.append(insight['id'])
            elif validation_result['status'] == 'rejected':
                rejected.append(insight['id'])
                issues.append(validation_result['issue'])
            elif validation_result['status'] == 'flagged':
                flagged.append(insight['id'])
                issues.append(validation_result['issue'])
        
        return {
            "validation_passed": len(rejected) == 0,
            "timestamp": datetime.now().isoformat(),
            "approved_insights": approved,
            "rejected_insights": rejected,
            "flagged_for_review": flagged,
            "issues_found": issues,
            "summary": {
                "total": len(insights),
                "approved": len(approved),
                "rejected": len(rejected),
                "flagged": len(flagged)
            }
        }
    
    def _validate_insight(self, insight: Dict[str, Any]) -> Dict[str, str]:
        """Validate a single insight"""
        
        # Check 1: Has required fields
        required_fields = ['id', 'module', 'category', 'severity', 'finding', 'recommendation']
        missing_fields = [f for f in required_fields if f not in insight]
        
        if missing_fields:
            return {
                "status": "rejected",
                "issue": {
                    "insight_id": insight.get('id', 'unknown'),
                    "severity": "critical",
                    "problem": f"Missing required fields: {', '.join(missing_fields)}",
                    "suggested_fix": "Ensure all required fields are present"
                }
            }
        
        # Check 2: Has data support
        if not self._has_data_support(insight):
            return {
                "status": "rejected",
                "issue": {
                    "insight_id": insight['id'],
                    "severity": "critical",
                    "problem": "No data support - missing metrics or affected_items",
                    "suggested_fix": "Add metrics and affected_items to support finding"
                }
            }
        
        # Check 3: Severity is appropriate
        if not self._check_severity(insight):
            return {
                "status": "flagged",
                "issue": {
                    "insight_id": insight['id'],
                    "severity": "warning",
                    "problem": f"Severity '{insight['severity']}' may not match category '{insight['category']}'",
                    "suggested_fix": "Review severity classification"
                }
            }
        
        # Check 4: Recommendation is actionable
        if not self._is_actionable(insight):
            return {
                "status": "flagged",
                "issue": {
                    "insight_id": insight['id'],
                    "severity": "warning",
                    "problem": "Recommendation may be too vague",
                    "suggested_fix": "Make recommendation more specific and actionable"
                }
            }
        
        # Check 5: No obvious contradictions
        # (would need context of other insights for full check)
        
        return {"status": "approved"}
    
    def _has_data_support(self, insight: Dict) -> bool:
        """Check if insight has supporting data"""
        has_metrics = 'metrics' in insight and insight['metrics']
        has_affected_items = 'affected_items' in insight and insight['affected_items']
        
        return has_metrics or has_affected_items
    
    def _check_severity(self, insight: Dict) -> bool:
        """Check if severity matches configured priorities"""
        category = insight.get('category', '')
        severity = insight.get('severity', 'medium')
        
        # Check against configured priorities
        high_priority_categories = self.priorities.get('high', [])
        medium_priority_categories = self.priorities.get('medium', [])
        low_priority_categories = self.priorities.get('low', [])
        
        if category in high_priority_categories:
            return severity == 'high'
        elif category in medium_priority_categories:
            return severity == 'medium'
        elif category in low_priority_categories:
            return severity == 'low'
        
        # If category not in config, accept as-is but flag for review
        return True
    
    def _is_actionable(self, insight: Dict) -> bool:
        """Check if recommendation is actionable"""
        recommendation = insight.get('recommendation', '').lower()
        
        # Vague phrases that indicate non-actionable advice
        vague_phrases = [
            'improve seo',
            'optimize better',
            'fix issues',
            'enhance performance',
            'make better'
        ]
        
        # Check if recommendation is too short (< 20 chars likely too vague)
        if len(recommendation) < 20:
            return False
        
        # Check for vague phrases
        if any(phrase in recommendation for phrase in vague_phrases):
            return False
        
        # Action words that indicate specific recommendations
        action_words = [
            'review', 'update', 'add', 'remove', 'implement',
            'optimize', 'fix', 'create', 'consolidate', 'redirect',
            'compress', 'minify', 'cache', 'reduce', 'improve'
        ]
        
        return any(word in recommendation for word in action_words)
    
    def filter_approved_insights(self, 
                                 insights: List[Dict],
                                 validation_report: Dict) -> List[Dict]:
        """Return only approved insights"""
        approved_ids = validation_report.get('approved_insights', [])
        return [i for i in insights if i['id'] in approved_ids]
