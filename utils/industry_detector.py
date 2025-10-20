"""
Industry Detection System
Automatically detects business industry from company name and SEO data patterns
"""
import re
from typing import Dict, List, Optional


class IndustryDetector:
    """
    Automatically detect industry from company name and data patterns
    """

    # Industry identification keywords
    INDUSTRY_KEYWORDS = {
        'automotive': {
            'keywords': ['tyre', 'tire', 'auto', 'car', 'vehicle', 'mechanic', 'automotive',
                        'motor', 'garage', 'service', 'repair', 'wheel', 'brake'],
            'patterns': ['tyres', 'tires', 'auto repair', 'car service', 'mechanic']
        },
        'legal': {
            'keywords': ['lawyer', 'attorney', 'legal', 'law', 'solicitor', 'barrister',
                        'counsel', 'advocate', 'litigation', 'court'],
            'patterns': ['law firm', 'legal services', 'attorney at law']
        },
        'healthcare': {
            'keywords': ['dental', 'dentist', 'doctor', 'clinic', 'medical', 'health',
                        'hospital', 'physician', 'surgery', 'practice', 'care'],
            'patterns': ['dental clinic', 'medical center', 'health care']
        },
        'real_estate': {
            'keywords': ['property', 'real estate', 'realty', 'homes', 'house', 'apartment',
                        'realtor', 'broker', 'estate agent', 'letting'],
            'patterns': ['real estate', 'property management', 'estate agent']
        },
        'restaurant': {
            'keywords': ['restaurant', 'cafe', 'dining', 'food', 'bistro', 'bar', 'grill',
                        'eatery', 'kitchen', 'cuisine', 'diner'],
            'patterns': ['restaurant', 'cafe', 'food']
        },
        'ecommerce': {
            'keywords': ['shop', 'store', 'boutique', 'market', 'retail', 'outlet',
                        'warehouse', 'emporium', 'goods'],
            'patterns': ['online store', 'shop', 'boutique']
        },
        'saas': {
            'keywords': ['software', 'app', 'platform', 'cloud', 'tech', 'digital',
                        'solution', 'system', 'analytics', 'crm', 'erp'],
            'patterns': ['software', 'platform', 'app']
        },
        'education': {
            'keywords': ['school', 'university', 'college', 'academy', 'learning',
                        'education', 'training', 'course', 'tutor', 'institute'],
            'patterns': ['school', 'academy', 'education']
        },
        'fitness': {
            'keywords': ['gym', 'fitness', 'yoga', 'pilates', 'training', 'workout',
                        'exercise', 'health club', 'studio'],
            'patterns': ['fitness', 'gym', 'yoga']
        },
        'beauty': {
            'keywords': ['salon', 'beauty', 'hair', 'spa', 'nail', 'cosmetic',
                        'barber', 'stylist', 'aesthetics'],
            'patterns': ['beauty salon', 'hair salon', 'spa']
        }
    }

    # Industry-specific context and characteristics
    INDUSTRY_CONTEXT = {
        'automotive': {
            'description': 'Automotive services and tyre fitting',
            'local_important': True,
            'mobile_dominant': True,
            'seasonal': True,
            'emergency_focused': True,
            'avg_ctr': 0.045,
            'typical_position': 15.2
        },
        'legal': {
            'description': 'Legal services and law firms',
            'local_important': True,
            'mobile_dominant': False,
            'seasonal': False,
            'emergency_focused': False,
            'avg_ctr': 0.038,
            'typical_position': 12.8
        },
        'healthcare': {
            'description': 'Healthcare and medical services',
            'local_important': True,
            'mobile_dominant': True,
            'seasonal': False,
            'emergency_focused': True,
            'avg_ctr': 0.042,
            'typical_position': 14.5
        },
        'real_estate': {
            'description': 'Real estate and property services',
            'local_important': True,
            'mobile_dominant': False,
            'seasonal': True,
            'emergency_focused': False,
            'avg_ctr': 0.035,
            'typical_position': 18.3
        },
        'restaurant': {
            'description': 'Restaurant and food services',
            'local_important': True,
            'mobile_dominant': True,
            'seasonal': False,
            'emergency_focused': False,
            'avg_ctr': 0.050,
            'typical_position': 10.2
        },
        'ecommerce': {
            'description': 'E-commerce and online retail',
            'local_important': False,
            'mobile_dominant': True,
            'seasonal': True,
            'emergency_focused': False,
            'avg_ctr': 0.032,
            'typical_position': 20.5
        },
        'saas': {
            'description': 'Software as a Service',
            'local_important': False,
            'mobile_dominant': False,
            'seasonal': False,
            'emergency_focused': False,
            'avg_ctr': 0.028,
            'typical_position': 16.8
        },
        'education': {
            'description': 'Education and training services',
            'local_important': True,
            'mobile_dominant': False,
            'seasonal': True,
            'emergency_focused': False,
            'avg_ctr': 0.040,
            'typical_position': 13.5
        },
        'fitness': {
            'description': 'Fitness and wellness',
            'local_important': True,
            'mobile_dominant': True,
            'seasonal': True,
            'emergency_focused': False,
            'avg_ctr': 0.045,
            'typical_position': 11.8
        },
        'beauty': {
            'description': 'Beauty and personal care',
            'local_important': True,
            'mobile_dominant': True,
            'seasonal': False,
            'emergency_focused': False,
            'avg_ctr': 0.048,
            'typical_position': 9.5
        }
    }

    def detect_industry(self, company_name: str, data: Optional[Dict] = None) -> str:
        """
        Detect industry from company name and optional SEO data patterns

        Args:
            company_name: Name of the company
            data: Optional SEO data (keywords, etc.)

        Returns:
            Industry identifier (e.g., 'automotive', 'legal', 'general')
        """
        company_lower = company_name.lower()

        # Score each industry
        industry_scores = {}

        for industry, config in self.INDUSTRY_KEYWORDS.items():
            score = 0

            # Check company name for keywords
            for keyword in config['keywords']:
                if keyword in company_lower:
                    score += 3

            # Check for patterns
            for pattern in config['patterns']:
                if pattern in company_lower:
                    score += 5

            industry_scores[industry] = score

        # If we have data, analyze keywords for additional signals
        if data and 'keywords' in data:
            for industry, config in self.INDUSTRY_KEYWORDS.items():
                keywords_data = data.get('keywords', [])
                for kw_data in keywords_data[:10]:  # Check top 10 keywords
                    keyword = kw_data.get('query', '').lower()
                    for industry_keyword in config['keywords']:
                        if industry_keyword in keyword:
                            industry_scores[industry] = industry_scores.get(industry, 0) + 1

        # Get the industry with highest score
        if industry_scores:
            best_industry = max(industry_scores.items(), key=lambda x: x[1])
            if best_industry[1] > 0:
                return best_industry[0]

        # Default to general if no clear match
        return 'general'

    def get_industry_context(self, industry: str) -> Dict:
        """
        Return industry-specific context and benchmarks

        Args:
            industry: Industry identifier

        Returns:
            Dictionary with industry characteristics and benchmarks
        """
        return self.INDUSTRY_CONTEXT.get(industry, {
            'description': 'General business',
            'local_important': False,
            'mobile_dominant': True,
            'seasonal': False,
            'emergency_focused': False,
            'avg_ctr': 0.035,
            'typical_position': 18.0
        })

    def get_location_from_name(self, company_name: str) -> Optional[str]:
        """
        Extract location from company name if present

        Args:
            company_name: Company name

        Returns:
            Location string or None
        """
        # Common location patterns
        patterns = [
            r'\b(sydney|melbourne|brisbane|perth|adelaide|canberra)\b',
            r'\b(nsw|vic|qld|wa|sa|act|nt|tas)\b',
            r'\b(north|south|east|west|central)\b',
        ]

        company_lower = company_name.lower()
        for pattern in patterns:
            match = re.search(pattern, company_lower)
            if match:
                return match.group(1).title()

        return None


# Global instance for easy import
industry_detector = IndustryDetector()
