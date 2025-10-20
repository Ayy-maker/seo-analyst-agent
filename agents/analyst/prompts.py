"""
Industry-Aware Prompts for Claude Sonnet 4.5
Leverages advanced AI capabilities for deep SEO analysis
"""

import json
from typing import Dict, List


class IndustryAwarePrompts:
    """
    Generate sophisticated prompts that leverage Claude Sonnet 4.5's
    advanced reasoning, pattern recognition, and industry knowledge
    """

    INDUSTRY_CONTEXTS = {
        'automotive': """
        You are analyzing SEO data for an automotive business (tyres/auto services).

        Key Industry Factors:
        - Seasonal trends: Winter tyres surge Nov-Feb, summer tyres Mar-May
        - High mobile usage: 65-75% mobile searches (urgent need, location-based)
        - Local intent critical: "near me" searches dominate
        - Price-sensitive market: Heavy comparison shopping
        - Emergency nature: 24/7 availability matters
        - Trust signals: Reviews and certifications crucial

        Competitive Landscape:
        - National chains (e.g., Jax Tyres, Bob Jane)
        - Local independent shops
        - Mobile fitting services (growing segment)
        - Online retailers with fitting network

        User Journey:
        1. Emergency search (flat tyre) → mobile → immediate booking
        2. Planned replacement → desktop research → price comparison → booking
        3. Seasonal switch → advance planning → brand preference

        Typical Conversion Metrics:
        - Average order value: $400-$800 per tyre set
        - Mobile conversions: 15-25% higher urgency
        - "Near me" searches: 3x conversion rate vs generic
        """,

        'legal': """
        You are analyzing SEO data for a legal services firm.

        Key Industry Factors:
        - High-value conversions: Each client worth $5k-$50k+
        - Long research phase: Users research 2-4 weeks before contact
        - Desktop dominant: 60-70% desktop (serious research)
        - Local + specialization: "family lawyer sydney" + "divorce"
        - Trust paramount: Reviews, credentials, case results
        - Urgent vs planned: Accident (urgent) vs estate planning (planned)

        Competitive Landscape:
        - Large firms dominating branded searches
        - Boutique specialists for niche practice areas
        - Legal directories (FindLaw, LawPath)
        - High competition for commercial keywords

        User Journey:
        1. Identify need → informational search → research lawyers
        2. Compare 3-5 firms → read reviews → check credentials
        3. Contact top 2-3 → consultations → engagement decision

        Typical Conversion Metrics:
        - Contact rate: 2-5% of organic visitors
        - Average client value: $15,000-$50,000
        - Research phase: 7-21 days average
        """,

        'healthcare': """
        You are analyzing SEO data for healthcare/dental services.

        Key Industry Factors:
        - Insurance-driven decisions: Coverage affects provider choice
        - Emergency vs routine: Split between urgent care and scheduled
        - High mobile usage: 60-70% mobile searches
        - Local + services: "dentist perth" + "teeth whitening"
        - Trust critical: Reviews, qualifications, patient testimonials
        - Appointment booking: Online scheduling reduces friction

        Competitive Landscape:
        - Hospital systems with large marketing budgets
        - Private practices (general + specialist)
        - Corporate chains (dental, optometry)
        - Healthdirect and directory listings

        User Journey:
        1. Identify need → search local providers → check reviews
        2. Verify insurance/payment → check availability
        3. Book appointment online or call

        Typical Conversion Metrics:
        - Appointment booking rate: 5-10% of visitors
        - Patient lifetime value: $2,000-$5,000
        - Mobile call-to-action: 40% higher conversion
        """,

        'real_estate': """
        You are analyzing SEO data for real estate services.

        Key Industry Factors:
        - High-value transactions: Commission per sale $5k-$50k
        - Long decision cycles: 3-12 months property search
        - Desktop research heavy: 55-65% desktop
        - Location hyper-focused: Suburb-level targeting essential
        - Market sensitivity: Pricing, inventory, rates affect traffic
        - Visual content critical: Photos, virtual tours drive engagement

        Competitive Landscape:
        - National portals (realestate.com.au, domain.com.au)
        - Boutique local agencies
        - Franchise networks (Ray White, LJ Hooker)
        - New online-only agencies

        User Journey:
        1. Research suburbs → property listings → compare agents
        2. Attend open homes → shortlist agents → market appraisal
        3. Select agent → list property → sale process

        Typical Conversion Metrics:
        - Appraisal request: 1-3% of visitors
        - Average commission: $15,000-$25,000
        - Lead nurture: 3-6 months average
        """,

        'restaurant': """
        You are analyzing SEO data for restaurant/food services.

        Key Industry Factors:
        - High mobile usage: 70-80% mobile searches
        - Location critical: "near me" and suburb searches dominate
        - Time-sensitive: Evening/weekend traffic spikes
        - Visual-driven: Photos, menus, ambiance images crucial
        - Review-dependent: Google ratings heavily influence choice
        - Booking friction: Online reservations increase conversions

        Competitive Landscape:
        - Delivery platforms (UberEats, DoorDash, Menulog)
        - Booking platforms (OpenTable, TheFork)
        - Direct competitors in same cuisine/area
        - Google Maps prominence crucial

        User Journey:
        1. Occasion identified → cuisine/location search → browse options
        2. Check reviews + photos + menu → make booking
        3. Visit + experience → leave review

        Typical Conversion Metrics:
        - Booking rate: 8-15% of visitors
        - Average order value: $80-$150 per table
        - Call-to-action: Click-to-call or online booking
        """,

        'general': """
        You are analyzing SEO performance data for this business.

        Consider:
        - Industry-specific factors that may affect performance
        - Competitive dynamics in their market
        - Typical customer journey and decision-making process
        - Seasonal or cyclical patterns
        - Mobile vs desktop behavior patterns
        """
    }

    def get_executive_summary_prompt(self, industry: str, data: Dict) -> str:
        """
        Generate industry-aware executive summary prompt for Sonnet 4.5
        """
        industry_context = self.INDUSTRY_CONTEXTS.get(industry, self.INDUSTRY_CONTEXTS['general'])

        return f"""
{industry_context}

Analyze this SEO performance data and generate a compelling, business-focused executive summary.

DATA SUMMARY:
{json.dumps(data, indent=2)}

REQUIREMENTS:

1. **Industry-Specific Context**: Reference industry trends, benchmarks, and competitive factors
2. **Root Cause Analysis**: Explain WHY metrics changed (not just that they did)
   - What specific actions or external factors drove changes?
   - Which patterns indicate strategic success vs lucky timing?

3. **Business Impact Translation**: Convert SEO metrics into business outcomes
   - Estimate revenue/lead value based on industry benchmarks
   - Quantify opportunity costs of gaps or weaknesses

4. **Strategic Positioning**: Compare performance to typical {industry} competitors
   - Where are we outperforming industry norms?
   - What competitive advantages or disadvantages exist?

5. **Forward-Looking Insights**: Identify emerging opportunities and risks
   - What trends suggest future growth or decline?
   - Which early signals require attention?

TONE: Professional, insightful, business-focused (not marketing hype)
LENGTH: 3-4 sentences maximum
INCLUDE: Specific numbers, percentages, business impact estimates

CRITICAL DON'Ts:
- Generic phrases like "achieved remarkable growth" or "strong performance"
- Stating obvious facts without explanation ("clicks increased 286%")
- Ignoring industry-specific context
- Writing more than 4 sentences
- Using superlatives without data backing

Example GOOD summary for automotive:
"Organic traffic grew 286% (67→258 clicks/month) driven primarily by mobile 'near me' searches and emergency service keywords, indicating successful local SEO and Google Business Profile optimization. With automotive sector average conversion rates of 12-15%, this represents approximately 31-39 additional bookings worth $12,000-$31,000 in monthly revenue. Position improvements for commercial-intent keywords ('buy tyres sydney', 'mobile fitting') suggest strong competitive positioning against national chains, while underperformance in informational content ('tyre maintenance tips') reveals a content gap opportunity worth an estimated 500+ monthly impressions."

Generate a similar industry-specific executive summary now:
"""

    def get_strategic_recommendations_prompt(self, industry: str, data: Dict) -> str:
        """
        Generate advanced recommendations prompt for Sonnet 4.5
        """
        industry_context = self.INDUSTRY_CONTEXTS.get(industry, self.INDUSTRY_CONTEXTS['general'])

        return f"""
{industry_context}

As an expert SEO strategist specializing in {industry}, analyze this data and provide
strategic recommendations that leverage advanced pattern recognition and industry insights.

ANALYSIS DATA:
{json.dumps(data, indent=2)}

ADVANCED ANALYSIS REQUIRED:

1. **Pattern Recognition & Correlation Analysis**
   - Hidden correlations (e.g., mobile traffic spike correlates with local keywords)
   - Device behavior patterns (mobile vs desktop intent differences)
   - Geographic concentration patterns
   - Keyword intent clustering and gaps
   - CTR anomalies (keywords underperforming vs position)
   - Seasonality signals in the data

2. **Competitive Intelligence**
   - Where are we winning vs typical {industry} competitors?
   - What gaps exist in our keyword coverage compared to market leaders?
   - Which competitor strategies should we adopt or avoid?
   - How does our device/location mix compare to industry norms?

3. **Predictive Insights & Forecasting**
   - Based on current trajectory, forecast next quarter performance
   - Identify early warning signs of decline or risk
   - Anticipate seasonal opportunities (based on industry patterns)
   - Predict impact of proposed recommendations

4. **Revenue Optimization & Prioritization**
   - Which improvements have highest revenue impact given {industry} conversion rates?
   - Estimated dollar value of each recommendation
   - ROI calculation (effort vs estimated return)
   - Quick wins vs strategic long-term plays

OUTPUT FORMAT:

For each recommendation, provide structured JSON:

```json
{{
  "recommendation": "Clear, specific, actionable recommendation",
  "priority": "QUICK WIN | HIGH IMPACT | STRATEGIC",
  "timeline": "2 weeks | 1 month | 3 months",
  "effort": "Low (5-10h) | Medium (20-40h) | High (40h+)",
  "impact_estimate": "Est. +XXX clicks/month, +XX conversions, $XX,XXX revenue",
  "confidence": "High (80%+) | Medium (50-80%) | Low (<50%)",
  "reasoning": "Data-driven explanation of why this matters",
  "data_evidence": ["Specific metrics supporting this recommendation"],
  "implementation_steps": [
    "Step 1: Specific action with details",
    "Step 2: Specific action with details",
    "Step 3: Specific action with details"
  ],
  "kpis": ["Metric to track success", "Secondary metric"],
  "dependencies": ["What needs to be in place first"],
  "risks": ["Potential downside or challenge to mitigate"]
}}
```

Provide 8 recommendations prioritized by impact/effort ratio.

CRITICAL: Be SPECIFIC, not generic:
❌ BAD: "Optimize for mobile users"
✅ GOOD: "Create dedicated /mobile-tyre-fitting-[suburb] landing pages for 'emergency tyre service' keywords (position 8-15, 2,400 monthly impressions) to capture high-intent mobile traffic converting at 25%+ vs site average of 12%"

❌ BAD: "Improve content quality"
✅ GOOD: "Add 'Free tyre health check' lead magnet to /tyre-maintenance-tips page (currently position 6.2, 890 monthly impressions) to convert informational searchers into leads, estimated +45 bookings/month based on 15% opt-in, 35% conversion rate"
"""

    def get_performance_insights_prompt(self, industry: str, data: Dict) -> str:
        """
        Prompt for deep forensic analysis of performance data
        """
        industry_context = self.INDUSTRY_CONTEXTS.get(industry, self.INDUSTRY_CONTEXTS['general'])

        return f"""
{industry_context}

You are conducting a forensic analysis of SEO performance data for a {industry} business.
Use Claude Sonnet 4.5's advanced reasoning to identify patterns a human analyst might miss.

DATA FOR ANALYSIS:
{json.dumps(data, indent=2)}

DEEP ANALYSIS REQUIRED:

1. **Causal Analysis (Not Just Correlation)**
   - What specific changes drove the metrics movement?
   - Which factors are correlated vs actually causal?
   - What external factors (seasonality, competition, algorithm updates) affected performance?
   - Evidence-based explanation of cause and effect

2. **Hidden Pattern Detection** (Leverage Sonnet 4.5's Advanced Reasoning)
   - Device behavior patterns: How does mobile vs desktop intent differ?
   - Temporal patterns: Time-of-day, day-of-week, seasonal variations
   - Geographic patterns: Traffic concentration by location
   - Keyword intent clustering: How do different keyword types perform?
   - CTR anomalies: Keywords dramatically over/under-performing position
   - Impression share gaps: Where are we missing visibility?

3. **Opportunity Detection & Prioritization**
   - Quick wins: Keywords at position 11-20 (page 2 → page 1 potential)
   - Content gaps: High-volume keywords we're completely missing
   - Cannibalization detection: Multiple pages competing for same keyword
   - Low-hanging fruit: High impression, low CTR keywords (title/description fixes)
   - Page 1 vulnerabilities: Keywords at position 8-10 (at risk of dropping to page 2)

4. **Risk Assessment & Vulnerability Analysis**
   - Traffic concentration risk: Over-reliance on few keywords?
   - Competitive threats: Where are we losing ground to competitors?
   - Technical risks: Pages with unexplained ranking drops
   - Seasonal risks: Over-dependence on seasonal keywords?
   - Position volatility: Keywords with unstable rankings

OUTPUT TWO SECTIONS:

**💪 Key Strengths** (5 items)
For each strength, provide:
- What we're doing well (specific metric evidence)
- Why this matters for {industry} specifically
- How to amplify it further (specific action)
- Estimated impact of amplification

Example:
"Mobile tyre fitting keywords (position 3.2 avg, 67.8% mobile traffic) significantly outperform industry benchmark (position 6-8). This matters because mobile 'near me' searches convert 3x higher in automotive. Amplification: Create suburb-specific landing pages for top 10 suburbs (estimated +120 clicks/month, +30 bookings, $12k revenue)."

**📈 Growth Opportunities** (5 items)
For each opportunity, provide:
- What the data reveals (specific pattern/gap)
- Why it's significant for {industry}
- Estimated impact if addressed (clicks, conversions, revenue)
- Suggested next steps (specific actions)
- Priority level (Quick Win / High Impact / Strategic)

Example:
"Page 2 keywords (position 11-20) represent 8 opportunities with combined 4,200 monthly impressions. Moving just 5 to page 1 (position 5-8) could add +180 clicks/month (+22 conversions, $8,800 revenue) based on {industry} CTR curves. Action: Technical SEO audit + internal linking optimization for these specific pages. Priority: QUICK WIN (high impact, low effort)."

CRITICAL: Use data evidence throughout. "Mobile traffic is strong (67.8%)" is better than "good mobile performance".
Calculate revenue estimates using industry-standard conversion rates and average order values.
"""

    def get_competitive_analysis_prompt(self, industry: str, data: Dict, competitors: List[str] = None) -> str:
        """
        Generate competitive intelligence analysis prompt
        """
        industry_context = self.INDUSTRY_CONTEXTS.get(industry, self.INDUSTRY_CONTEXTS['general'])
        competitors_str = ', '.join(competitors) if competitors else 'typical industry competitors'

        return f"""
{industry_context}

Analyze competitive positioning for this {industry} business against {competitors_str}.

PERFORMANCE DATA:
{json.dumps(data, indent=2)}

COMPETITIVE INTELLIGENCE ANALYSIS:

1. **Keyword Gap Analysis**
   - Which high-value keywords are competitors ranking for that we're missing?
   - What keyword categories do they dominate vs where we're strong?
   - Content gaps based on competitive keyword coverage

2. **Strategic Positioning**
   - Where do we have competitive advantages (data evidence)?
   - Where are we disadvantaged vs competitors?
   - Which battles should we fight vs avoid?

3. **Traffic Opportunity Sizing**
   - Estimate potential traffic gain from closing keyword gaps
   - Calculate revenue opportunity based on competitor visibility
   - Prioritize opportunities by impact/effort

4. **Actionable Competitive Strategy**
   - Which competitor strategies should we adopt?
   - Where can we differentiate and win?
   - Specific tactics to close competitive gaps

OUTPUT:
Provide competitive insights with specific recommendations, revenue estimates, and priority rankings.
"""


# Global instance for easy import
industry_prompts = IndustryAwarePrompts()
