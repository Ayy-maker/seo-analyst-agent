"""
Prioritization Engine for SEO Recommendations
Automatically scores and ranks recommendations based on impact/effort analysis
"""

import re
from typing import Dict, List, Any


class PrioritizationEngine:
    """
    Score and prioritize SEO recommendations using multi-factor analysis

    Factors considered:
    - Impact: Traffic/conversion/revenue potential
    - Effort: Time, resources, complexity required
    - Confidence: Reliability of estimates
    - Dependencies: Prerequisites and blockers
    - Timeline: Quick wins vs long-term strategic
    """

    # Effort scoring map
    EFFORT_SCORES = {
        'Low': 2,
        'Medium': 5,
        'High': 8
    }

    # Confidence multipliers
    CONFIDENCE_MULTIPLIERS = {
        'High': 1.0,
        'Medium': 0.8,
        'Low': 0.6
    }

    # Timeline urgency scores
    TIMELINE_SCORES = {
        '2 weeks': 3,
        '1 month': 2,
        '3 months': 1,
        '6 months': 0.5
    }

    def score_recommendation(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive priority score for a recommendation

        Args:
            recommendation: Recommendation dictionary from analyzer

        Returns:
            Enhanced recommendation with scores and priority label
        """
        # Calculate component scores
        impact_score = self._calculate_impact_score(recommendation)
        effort_score = self._calculate_effort_score(recommendation)
        confidence_multiplier = self._get_confidence_multiplier(recommendation)
        timeline_score = self._get_timeline_score(recommendation)

        # Calculate ROI score (impact / effort, adjusted by confidence)
        roi_score = (impact_score / max(effort_score, 1)) * confidence_multiplier

        # Add timeline urgency bonus
        final_score = roi_score + timeline_score

        # Assign priority label
        priority = self._assign_priority_label(final_score, effort_score, timeline_score)

        # Enhance recommendation with scores
        recommendation.update({
            'impact_score': round(impact_score, 2),
            'effort_score': effort_score,
            'roi_score': round(roi_score, 2),
            'final_score': round(final_score, 2),
            'priority': priority,
            'scoring_breakdown': {
                'impact': impact_score,
                'effort': effort_score,
                'confidence_multiplier': confidence_multiplier,
                'timeline_urgency': timeline_score,
                'roi': roi_score
            }
        })

        return recommendation

    def prioritize_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Score and sort all recommendations by priority

        Args:
            recommendations: List of recommendation dictionaries

        Returns:
            Sorted list with priority scores
        """
        # Score each recommendation
        scored = [self.score_recommendation(rec) for rec in recommendations]

        # Sort by final score (descending)
        scored.sort(key=lambda x: x.get('final_score', 0), reverse=True)

        # Add rank numbers
        for i, rec in enumerate(scored, 1):
            rec['rank'] = i

        return scored

    def _calculate_impact_score(self, rec: Dict[str, Any]) -> float:
        """
        Score based on estimated business impact

        Factors:
        - Estimated click increase
        - Conversion potential
        - Revenue impact (mentions of $ values)
        - Competitive advantage

        Returns:
            Impact score (0-10)
        """
        score = 0.0
        impact_str = rec.get('impact_estimate', '').lower()

        # Extract click estimates
        clicks = self._extract_number(impact_str, 'click')
        if clicks > 0:
            # Scale: 50 clicks = 1 point, max 5 points
            score += min(clicks / 50, 5)

        # Extract conversion estimates
        conversions = self._extract_number(impact_str, 'conversion')
        if conversions > 0:
            # Scale: 10 conversions = 1 point, max 3 points
            score += min(conversions / 10, 3)

        # Check for revenue mentions (indicates high value)
        if '$' in impact_str or 'revenue' in impact_str or 'value' in impact_str:
            score += 2  # Bonus for revenue impact

        # Data evidence bonus
        if 'data_evidence' in rec and len(rec.get('data_evidence', [])) > 0:
            score += 1  # Bonus for data-backed recommendations

        return min(score, 10)  # Cap at 10

    def _calculate_effort_score(self, rec: Dict[str, Any]) -> float:
        """
        Score based on implementation effort

        Factors:
        - Time required (hours)
        - Technical complexity
        - Resources needed
        - Dependencies

        Returns:
            Effort score (1-10, higher = more effort)
        """
        effort = rec.get('effort', 'Medium')

        # Extract effort level from strings like "Low (5-10h)" or "Medium"
        if '(' in effort:
            effort_level = effort.split('(')[0].strip()
        else:
            effort_level = effort

        base_score = self.EFFORT_SCORES.get(effort_level, 5)

        # Adjust for dependencies
        dependencies = rec.get('dependencies', [])
        if dependencies and len(dependencies) > 2:
            base_score += 1  # More dependencies = more effort

        # Adjust for implementation steps
        steps = rec.get('implementation_steps', [])
        if steps and len(steps) > 5:
            base_score += 0.5  # Many steps = more effort

        return min(base_score, 10)  # Cap at 10

    def _get_confidence_multiplier(self, rec: Dict[str, Any]) -> float:
        """
        Get confidence multiplier for score adjustment

        Args:
            rec: Recommendation dictionary

        Returns:
            Multiplier (0.6-1.0)
        """
        confidence = rec.get('confidence', 'Medium')

        # Extract confidence level from strings like "High (85%)"
        if '(' in confidence:
            confidence_level = confidence.split('(')[0].strip()
        else:
            confidence_level = confidence

        return self.CONFIDENCE_MULTIPLIERS.get(confidence_level, 0.8)

    def _get_timeline_score(self, rec: Dict[str, Any]) -> float:
        """
        Get urgency bonus based on timeline
        Faster implementations get higher urgency scores

        Args:
            rec: Recommendation dictionary

        Returns:
            Timeline urgency score (0-3)
        """
        timeline = rec.get('timeline', '1 month')
        return self.TIMELINE_SCORES.get(timeline, 1)

    def _assign_priority_label(self, final_score: float, effort_score: float, timeline_score: float) -> str:
        """
        Assign priority label based on scores

        Args:
            final_score: Combined impact/effort/timeline score
            effort_score: Effort required
            timeline_score: Timeline urgency

        Returns:
            Priority label: "QUICK WIN", "HIGH IMPACT", or "STRATEGIC"
        """
        # Quick wins: High score, low effort, short timeline
        if final_score > 8 and effort_score < 4 and timeline_score >= 2:
            return "QUICK WIN"

        # High impact: High score regardless of effort
        elif final_score > 6:
            return "HIGH IMPACT"

        # Strategic: Longer-term, more effort but valuable
        else:
            return "STRATEGIC"

    def _extract_number(self, text: str, keyword: str) -> float:
        """
        Extract numeric value near a keyword in text

        Args:
            text: Text to search
            keyword: Keyword to find (e.g., 'click', 'conversion', '$')

        Returns:
            Extracted number or 0 if not found
        """
        if not text:
            return 0.0

        # Handle dollar amounts specially
        if keyword == '$':
            # Match patterns like "$12,000" or "$12k"
            dollar_pattern = r'\$([0-9,]+)k?'
            match = re.search(dollar_pattern, text)
            if match:
                value = match.group(1).replace(',', '')
                if 'k' in match.group(0).lower():
                    return float(value) * 1000
                return float(value)
            return 0.0

        # For other keywords, find "+X keyword" patterns
        pattern = rf'\+?\s*([0-9,]+)\s*{keyword}'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1).replace(',', '')
            return float(value)

        return 0.0

    def get_priority_summary(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics for prioritized recommendations

        Args:
            recommendations: Scored recommendations list

        Returns:
            Summary dictionary with counts and insights
        """
        total = len(recommendations)
        quick_wins = sum(1 for r in recommendations if r.get('priority') == 'QUICK WIN')
        high_impact = sum(1 for r in recommendations if r.get('priority') == 'HIGH IMPACT')
        strategic = sum(1 for r in recommendations if r.get('priority') == 'STRATEGIC')

        # Calculate average scores
        avg_impact = sum(r.get('impact_score', 0) for r in recommendations) / max(total, 1)
        avg_effort = sum(r.get('effort_score', 0) for r in recommendations) / max(total, 1)
        avg_roi = sum(r.get('roi_score', 0) for r in recommendations) / max(total, 1)

        return {
            'total_recommendations': total,
            'breakdown': {
                'quick_wins': quick_wins,
                'high_impact': high_impact,
                'strategic': strategic
            },
            'percentages': {
                'quick_wins': round((quick_wins / max(total, 1)) * 100, 1),
                'high_impact': round((high_impact / max(total, 1)) * 100, 1),
                'strategic': round((strategic / max(total, 1)) * 100, 1)
            },
            'average_scores': {
                'impact': round(avg_impact, 2),
                'effort': round(avg_effort, 2),
                'roi': round(avg_roi, 2)
            },
            'top_priority': recommendations[0].get('recommendation') if recommendations else None
        }


# Global instance for easy import
prioritization_engine = PrioritizationEngine()
