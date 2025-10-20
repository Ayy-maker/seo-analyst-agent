"""
Realistic Demo Data Generator
Generates industry-specific, realistic SEO data for demonstrations
"""
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class DemoDataGenerator:
    """
    Generate realistic demo data based on industry
    """

    # Industry-specific keyword templates
    INDUSTRY_KEYWORDS = {
        'automotive': {
            'informational': [
                'how to check tyre pressure',
                'when to replace tyres',
                'tyre rotation guide',
                'winter vs summer tyres',
                'how long do tyres last',
                'tyre maintenance tips'
            ],
            'commercial': [
                'buy tyres online {location}',
                'cheap tyres {location}',
                'tyre brands comparison',
                'best tyres for {car_model}',
                'tyre prices {location}',
                'discount tyres near me'
            ],
            'local': [
                'tyres near me',
                'mobile tyre fitting {suburb}',
                '24 hour tyre service {location}',
                'tyre shop {location}',
                'emergency tyre repair {location}',
                'tyre fitting service {suburb}'
            ]
        },
        'legal': {
            'informational': [
                'what is a settlement agreement',
                'how long does probate take',
                'legal rights in divorce',
                'personal injury claim process',
                'employment law basics',
                'small claims court guide'
            ],
            'commercial': [
                'hire lawyer {location}',
                'best family lawyer near me',
                'personal injury attorney {location}',
                'divorce lawyer {location}',
                'employment lawyer fees {location}',
                'conveyancing solicitor {location}'
            ],
            'local': [
                'lawyer near me',
                'legal services {location}',
                'solicitor {suburb}',
                'law firm {location}',
                'legal advice {location}',
                'attorney {suburb}'
            ]
        },
        'healthcare': {
            'informational': [
                'dental implant procedure',
                'teeth whitening cost',
                'root canal treatment',
                'dental insurance coverage',
                'how often dental checkup',
                'wisdom teeth removal'
            ],
            'commercial': [
                'dentist near me',
                'dental clinic {location}',
                'emergency dentist {suburb}',
                'cosmetic dentist {location}',
                'affordable dental care {location}',
                'family dentist {suburb}'
            ],
            'local': [
                'dentist {suburb}',
                'dental practice {location}',
                'dental surgery {suburb}',
                'teeth cleaning {location}',
                'dental appointment {suburb}',
                'dentist open saturday {location}'
            ]
        },
        'real_estate': {
            'informational': [
                'how to buy a house',
                'property market trends',
                'first home buyer guide',
                'property investment tips',
                'rental yield calculation',
                'property inspection checklist'
            ],
            'commercial': [
                'houses for sale {location}',
                'real estate agent {suburb}',
                'property for sale {location}',
                'apartments {suburb}',
                'buy property {location}',
                'homes for sale {suburb}'
            ],
            'local': [
                'real estate {suburb}',
                'property {location}',
                'estate agent {suburb}',
                'realtor {location}',
                'property manager {suburb}',
                'real estate listings {location}'
            ]
        },
        'restaurant': {
            'informational': [
                'best restaurants {location}',
                'italian food near me',
                'restaurant reservations',
                'fine dining {location}',
                'lunch specials near me',
                'cafe menu'
            ],
            'commercial': [
                'book restaurant {location}',
                'order food online {suburb}',
                'restaurant delivery {location}',
                'takeaway {suburb}',
                'dinner reservations {location}',
                'restaurant near me'
            ],
            'local': [
                'restaurants {suburb}',
                'dining {location}',
                'cafe {suburb}',
                'food {location}',
                'restaurant {suburb} open now',
                'breakfast {location}'
            ]
        }
    }

    # Car models for automotive industry
    CAR_MODELS = ['Toyota Camry', 'Mazda 3', 'Hyundai i30', 'Ford Ranger',
                  'Mitsubishi Outlander', 'Honda Civic', 'Subaru Forester']

    # Australian locations
    LOCATIONS = {
        'sydney': ['Bondi', 'Parramatta', 'Chatswood', 'Manly', 'Penrith'],
        'melbourne': ['St Kilda', 'Brunswick', 'Richmond', 'Fitzroy', 'Preston'],
        'brisbane': ['South Bank', 'Fortitude Valley', 'Newstead', 'West End', 'Chermside'],
        'perth': ['Fremantle', 'Subiaco', 'Joondalup', 'Claremont', 'Mandurah'],
        'adelaide': ['Glenelg', 'North Adelaide', 'Norwood', 'Brighton', 'Marion']
    }

    def __init__(self):
        random.seed(42)  # For consistent demo data

    def generate_keywords(self, industry: str, location: str = 'Sydney', count: int = 20) -> List[Dict]:
        """
        Generate realistic keywords with metrics based on industry benchmarks

        Args:
            industry: Industry identifier
            location: Business location
            count: Number of keywords to generate

        Returns:
            List of keyword dictionaries with realistic metrics
        """
        keywords = []
        templates = self.INDUSTRY_KEYWORDS.get(industry, self.INDUSTRY_KEYWORDS['automotive'])

        # Get suburbs for location
        city_lower = location.lower()
        suburbs = self.LOCATIONS.get(city_lower, self.LOCATIONS['sydney'])

        # Generate keywords from each intent type
        for intent, keyword_list in templates.items():
            for i, template in enumerate(keyword_list):
                if len(keywords) >= count:
                    break

                # Populate template
                keyword = self._populate_template(template, location, suburbs)

                # Generate realistic metrics based on intent and position
                metrics = self._generate_realistic_metrics(intent, i)

                keywords.append({
                    'query': keyword,
                    'clicks': metrics['clicks'],
                    'impressions': metrics['impressions'],
                    'ctr': metrics['ctr'],
                    'position': metrics['position'],
                    'intent': intent
                })

        # Sort by clicks descending
        keywords.sort(key=lambda x: x['clicks'], reverse=True)

        return keywords[:count]

    def _populate_template(self, template: str, location: str, suburbs: List[str]) -> str:
        """
        Replace placeholders in keyword template

        Args:
            template: Keyword template with {placeholders}
            location: City name
            suburbs: List of suburbs

        Returns:
            Populated keyword string
        """
        keyword = template

        # Replace location
        if '{location}' in keyword:
            keyword = keyword.replace('{location}', location.lower())

        # Replace suburb
        if '{suburb}' in keyword:
            suburb = random.choice(suburbs)
            keyword = keyword.replace('{suburb}', suburb.lower())

        # Replace car model (for automotive)
        if '{car_model}' in keyword:
            car_model = random.choice(self.CAR_MODELS)
            keyword = keyword.replace('{car_model}', car_model.lower())

        return keyword

    def _generate_realistic_metrics(self, intent: str, index: int) -> Dict:
        """
        Generate realistic CTR/position based on intent type and benchmarks

        Commercial intent typically has:
        - Higher CTR (5-8%)
        - Better positions (3-10)

        Informational intent typically has:
        - Lower CTR (2-4%)
        - Variable positions (5-20)

        Local intent has:
        - High CTR (6-10%)
        - Good positions (2-8)

        Args:
            intent: Keyword intent type
            index: Position in list (affects metrics)

        Returns:
            Dictionary with realistic metrics
        """
        # Base metrics by intent
        intent_config = {
            'commercial': {
                'ctr_range': (0.05, 0.08),
                'position_range': (3, 10),
                'impression_base': 1000
            },
            'informational': {
                'ctr_range': (0.02, 0.04),
                'position_range': (5, 20),
                'impression_base': 1500
            },
            'local': {
                'ctr_range': (0.06, 0.10),
                'position_range': (2, 8),
                'impression_base': 800
            }
        }

        config = intent_config.get(intent, intent_config['commercial'])

        # Position varies by index (top keywords have better positions)
        position_min, position_max = config['position_range']
        position = position_min + (index * 0.8)  # Gradually worse positions
        position = min(position, position_max)
        position = round(position + random.uniform(-0.5, 0.5), 1)

        # CTR is influenced by position (better position = higher CTR)
        ctr_min, ctr_max = config['ctr_range']
        # Top positions get higher CTR
        position_factor = 1 - ((position - position_min) / (position_max - position_min)) * 0.5
        ctr = (ctr_min + (ctr_max - ctr_min) * position_factor) * random.uniform(0.9, 1.1)
        ctr = round(ctr, 3)

        # Impressions vary by keyword popularity
        impressions = int(config['impression_base'] * random.uniform(0.7, 1.5))

        # Clicks = impressions × CTR
        clicks = int(impressions * ctr)

        return {
            'clicks': max(clicks, 1),
            'impressions': impressions,
            'ctr': round(ctr * 100, 1),  # Convert to percentage
            'position': max(1.0, position)
        }

    def generate_landing_pages(self, industry: str, location: str = 'Sydney') -> List[Dict]:
        """
        Generate realistic landing pages based on industry best practices

        Args:
            industry: Industry identifier
            location: Business location

        Returns:
            List of landing page dictionaries with metrics
        """
        # Common pages across industries
        pages = [
            {'url': '/', 'name': 'Homepage'},
            {'url': '/services/', 'name': 'Services'},
            {'url': '/about/', 'name': 'About'},
            {'url': '/contact/', 'name': 'Contact'},
        ]

        # Industry-specific pages
        industry_pages = {
            'automotive': [
                {'url': '/mobile-fitting/', 'name': 'Mobile Fitting'},
                {'url': '/tyre-brands/', 'name': 'Tyre Brands'},
                {'url': '/emergency-service/', 'name': 'Emergency Service'},
            ],
            'legal': [
                {'url': '/practice-areas/', 'name': 'Practice Areas'},
                {'url': '/our-team/', 'name': 'Our Team'},
                {'url': '/case-results/', 'name': 'Case Results'},
            ],
            'healthcare': [
                {'url': '/treatments/', 'name': 'Treatments'},
                {'url': '/appointments/', 'name': 'Book Appointment'},
                {'url': '/dental-care/', 'name': 'Dental Care'},
            ]
        }

        # Add industry-specific pages
        if industry in industry_pages:
            pages.extend(industry_pages[industry])

        # Add metrics to each page
        total_clicks = 258  # Example total from Hot Tyres report
        for i, page in enumerate(pages):
            # Homepage gets most traffic
            if i == 0:
                clicks = int(total_clicks * 0.52)  # 52%
            elif i == 1:
                clicks = int(total_clicks * 0.18)  # 18%
            elif i == 2:
                clicks = int(total_clicks * 0.11)  # 11%
            else:
                remaining = total_clicks - sum(p.get('clicks', 0) for p in pages if 'clicks' in p)
                clicks = max(int(remaining / (len(pages) - i)), 1)

            page['clicks'] = clicks
            page['impressions'] = int(clicks / random.uniform(0.025, 0.035))
            page['ctr'] = round((clicks / page['impressions']) * 100, 1)
            page['position'] = round(random.uniform(8, 22), 1)
            page['growth'] = random.choice([250, 300, 350, 385, 420, 450])  # Growth percentage

        return pages

    def generate_complete_dataset(self,
                                 industry: str,
                                 location: str = 'Sydney',
                                 historical_months: int = 7) -> Dict:
        """
        Generate complete SEO dataset for demo purposes

        Args:
            industry: Industry identifier
            location: Business location
            historical_months: Number of months of historical data

        Returns:
            Complete dataset dictionary
        """
        # Generate current month data
        keywords = self.generate_keywords(industry, location, count=20)
        landing_pages = self.generate_landing_pages(industry, location)

        # Calculate totals
        total_clicks = sum(k['clicks'] for k in keywords)
        total_impressions = sum(k['impressions'] for k in keywords)
        avg_ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
        avg_position = sum(k['position'] for k in keywords) / len(keywords) if keywords else 0

        # Generate historical trend data
        historical_data = self._generate_historical_trends(total_clicks, historical_months)

        # Device distribution (realistic for industry)
        device_distribution = self._generate_device_distribution(industry)

        return {
            'keywords': keywords,
            'landing_pages': landing_pages,
            'totals': {
                'clicks': total_clicks,
                'impressions': total_impressions,
                'ctr': round(avg_ctr, 2),
                'avg_position': round(avg_position, 1)
            },
            'historical': historical_data,
            'devices': device_distribution,
            'location': location,
            'industry': industry
        }

    def _generate_historical_trends(self, current_clicks: int, months: int = 7) -> List[Dict]:
        """
        Generate historical trend data showing growth

        Args:
            current_clicks: Current month clicks
            months: Number of historical months

        Returns:
            List of monthly data points
        """
        historical = []
        base_clicks = int(current_clicks * 0.26)  # Start at 26% of current (for 286% growth)

        for i in range(months):
            # Gradually increase clicks
            month_clicks = int(base_clicks + (current_clicks - base_clicks) * (i / (months - 1)))

            # Add some randomness
            month_clicks = int(month_clicks * random.uniform(0.95, 1.05))

            historical.append({
                'month_offset': i - (months - 1),  # -6, -5, -4, ..., 0
                'clicks': month_clicks,
                'impressions': int(month_clicks / random.uniform(0.028, 0.032)),
                'health_score': int(72 + (15 * (i / (months - 1))))  # 72% to 87%
            })

        return historical

    def _generate_device_distribution(self, industry: str) -> Dict:
        """
        Generate realistic device distribution based on industry

        Args:
            industry: Industry identifier

        Returns:
            Device distribution dictionary
        """
        # Industry-specific device preferences
        mobile_heavy_industries = ['automotive', 'restaurant', 'healthcare', 'beauty', 'fitness']

        if industry in mobile_heavy_industries:
            # Mobile-heavy: 65-72% mobile, remaining split between desktop/tablet
            mobile = round(random.uniform(65, 72), 1)
            remaining = 100 - mobile
            desktop = round(remaining * random.uniform(0.75, 0.85), 1)  # 75-85% of remaining
            tablet = round(100 - mobile - desktop, 1)
        else:
            # Desktop-heavy: 45-55% mobile, 38-48% desktop, rest tablet
            mobile = round(random.uniform(45, 55), 1)
            desktop = round(random.uniform(38, 48), 1)
            tablet = round(100 - mobile - desktop, 1)

        # Ensure tablet is never negative (defensive fix)
        if tablet < 0:
            tablet = 0
            # Recalculate to ensure percentages sum to 100
            total = mobile + desktop
            mobile = round((mobile / total) * 100, 1)
            desktop = round(100 - mobile, 1)

        return {
            'mobile': mobile,
            'desktop': desktop,
            'tablet': tablet
        }


# Global instance for easy import
demo_data_generator = DemoDataGenerator()
