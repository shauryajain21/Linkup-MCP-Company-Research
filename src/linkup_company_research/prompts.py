"""Optimized prompt templates for Linkup Company Research MCP.

Supports 17 comprehensive company profile tools.

These prompts follow Linkup's best practices:
- Sequential search patterns (search -> scrape)
- Explicit scraping instructions
- Multi-step research flows
- Specific data points to extract
"""


# =============================================================================
# 1. COMPANY OVERVIEW
# =============================================================================

COMPANY_OVERVIEW_PROMPT = """You are an expert business analyst researching {company_name}.

Execute the following research steps:

1. First, find {company_name}'s official website URL
2. Scrape their homepage to understand their core value proposition
3. Find and scrape their "About Us" or "About" page for company background, mission, and history
4. Find their LinkedIn company page and extract company details (employee count, headquarters, industry)
5. Search for founding story, origin, and key milestones

Based on this comprehensive research, provide:

Company Identity:
- Company name (official name)
- Legal entity name(s) if different
- Website URL
- Founded year
- Founder names
- Origin story / founding context (brief narrative)

Locations:
- Headquarters location (city, state/region, country)
- Office locations / geographic footprint

Size & Stage:
- Employee headcount (current, with source)
- Employee count range (e.g., "100-500")
- Employee growth trend (growing/stable/declining)
- Company stage (seed/early/growth/mature/public/turnaround)

Description:
- Company description: What problem do they solve? What do they do?
- Mission statement (if publicly stated)

Social:
- LinkedIn URL
- Twitter/X URL

Do not include products, services, or business model details - those belong in separate tools.
Return only factual data found - do not infer or estimate values."""


# =============================================================================
# 2. PRODUCTS & SERVICES
# =============================================================================

COMPANY_PRODUCTS_PROMPT = """You are an expert product analyst researching {company_name}'s products and services.

{product_filter}

Execute the following research steps:

1. Find and scrape {company_name}'s products page or solutions page
2. Look for individual product pages with detailed descriptions
3. Find their pricing page and extract pricing information
4. Search for product documentation or feature lists
5. Look for product announcements and launch dates

For each product found, provide:

Products:
- Product name
- Description (what it does)
- Product type (software/hardware/service/platform/api/data)
- Target use cases (who uses it and why)
- Key features
- Launch date (if known)

Services:
- Service name
- Description
- Service type

Pricing:
- Pricing model (subscription/usage-based/one-time/freemium/enterprise/hybrid/free)
- Pricing tiers with:
  - Tier name
  - Price
  - Billing frequency
  - Key features included
- Free trial availability
- Pricing page URL

Focus on factual product information. Do not speculate about unreleased products."""


COMPANY_PRODUCTS_FILTER = """Focus specifically on the product: {product_name}"""


# =============================================================================
# 3. BUSINESS MODEL
# =============================================================================

COMPANY_BUSINESS_MODEL_PROMPT = """You are an expert business analyst researching {company_name}'s business model.

Execute the following research steps:

1. Analyze {company_name}'s website to understand their business type
2. Search for investor presentations, pitch decks, or business model descriptions
3. Look for interviews with executives discussing business strategy
4. Find analyst reports or business news about their revenue model
5. Search for any disclosed unit economics or financial metrics

Provide detailed business model information:

Business Type:
- B2B vs B2C vs B2B2C vs D2C vs B2G vs C2C

Business Model:
- Model type (SaaS/marketplace/platform/services/retail/wholesale/licensing/advertising/hardware/hybrid)

Revenue Streams:
- For each revenue stream:
  - Stream name
  - Description of how they make money
  - Percentage of revenue (if known)

Monetization:
- Monetization strategy description

Unit Economics (if available, otherwise typical for this industry):
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- LTV/CAC ratio
- Payback period
- Gross margin

Go-to-Market:
- GTM approach (sales-led/product-led/hybrid/channel/community-led)
- Sales model (self-serve/inside-sales/field-sales/partner/hybrid)

Note sources for any financial metrics. Do not estimate values without stating it's an estimate."""


# =============================================================================
# 4. TARGET MARKET
# =============================================================================

COMPANY_TARGET_MARKET_PROMPT = """You are an expert market analyst researching {company_name}'s target market.

Execute the following research steps:

1. Analyze {company_name}'s website messaging and "Who We Serve" content
2. Look at their case studies to understand customer types
3. Search for investor materials describing their ICP
4. Find job postings mentioning target customer segments
5. Look for analyst or press coverage about their market focus

Provide detailed target market information:

Ideal Customer Profile (ICP):
- Company size focus (SMB/mid-market/enterprise/all)
- Target industries
- Target job titles / personas
- Pain points they solve

Customer Segments:
- For each segment:
  - Segment name
  - Description
  - Estimated size or importance

Geographic Markets:
- For each market:
  - Region
  - Priority (primary/secondary/emerging)

Vertical Focus:
- Industry verticals they specialize in

Use Case Verticals:
- Specific use cases they target

Market Approach:
- Horizontal (broad) vs Vertical (specialized) vs Hybrid

Base this on factual evidence from their marketing and customer materials."""


# =============================================================================
# 5. FINANCIALS (Revenue & Metrics)
# =============================================================================

COMPANY_FINANCIALS_PROMPT = """You are an expert financial analyst researching {company_name}'s financial performance.

{date_filter}

Execute the following research steps:

1. Search for revenue disclosures, earnings reports, or financial filings
2. Look for news articles mentioning revenue figures or growth rates
3. Find investor presentations with financial metrics
4. Search for profitability status and path to profitability discussions
5. Look for key SaaS/business metrics (ARR, MRR, GMV, NRR, churn)

Provide detailed financial information:

Revenue:
- Latest revenue amount
- Currency
- Period (annual, quarterly)
- Date of the data
- Revenue type (ARR/MRR/GMV/total revenue/run rate)

Revenue History:
- Historical revenue figures with dates

Growth:
- Revenue growth rate

Profitability:
- Profitability status (profitable/break-even/unprofitable)
- Path to profitability (if unprofitable)
- Gross margin

Key Metrics:
- ARR (Annual Recurring Revenue)
- MRR (Monthly Recurring Revenue)
- GMV (Gross Merchandise Value)
- ACV (Annual Contract Value)
- NRR (Net Revenue Retention)
- Churn rate

Financial Health:
- Burn rate (if known)
- Runway in months (if known)
- Financial health signals

Note the date and source for each financial data point. Do not estimate values.
Do not include funding or valuation data - that belongs in company_funding."""


# =============================================================================
# 6. FUNDING & VALUATION
# =============================================================================

COMPANY_FUNDING_PROMPT = """You are an expert financial analyst researching {company_name}'s funding and valuation.

{date_filter}

Execute the following research steps:

1. Search Crunchbase, PitchBook, or similar databases for funding history
2. Look for funding announcements and press releases
3. Find investor profiles and identify lead investors for each round
4. Search for valuation mentions in news or analyst reports
5. Find cap table information or notable shareholders

Provide detailed funding information:

Total Funding:
- Total funding raised to date (with source)

Funding Rounds:
For each round:
- Round type (Pre-Seed/Seed/Series A/B/C/D/E+/Growth/Debt/Grant/Other)
- Date of announcement
- Amount raised
- Currency
- Lead investors
- Participating investors
- Valuation at that round (if disclosed)

Latest Valuation:
- Amount
- Date
- Source
- Type (pre-money/post-money)

Valuation History:
- Historical valuations with dates and rounds

Investors:
For each investor:
- Name
- Type (VC/PE/angel/strategic/corporate/government/family office)
- Rounds participated in

Notable Shareholders:
- Known major shareholders

Debt Financing:
- Any debt financing details

Note the source for each data point. Do not estimate values."""


# =============================================================================
# 7. LEADERSHIP & PEOPLE
# =============================================================================

COMPANY_LEADERSHIP_PROMPT = """You are an expert executive researcher investigating {company_name}'s leadership team.

Execute the following research steps:

1. Find and scrape {company_name}'s "Team", "About Us", "Leadership" page
2. Search LinkedIn for executives with C-level and VP titles
3. Look for recent executive announcements and leadership changes
4. Find board member information from press releases or SEC filings
5. Search for key hires and departures in the last 12-24 months

Provide detailed leadership information:

CEO:
- Name
- Tenure start date
- Background
- LinkedIn URL

C-Suite Executives:
For each executive (CTO, CFO, COO, CMO, CPO, CRO, etc.):
- Name
- Title
- Tenure start date
- Background
- Previous companies
- LinkedIn URL

Founders:
For each founder:
- Name
- Current title
- Is still active at company (yes/no)
- Current role in company

Board Members:
For each board member:
- Name
- Affiliation (e.g., "Partner at Sequoia")
- Board role (chair/member/observer)

Key Hires (last 12-24 months):
For each significant hire:
- Name
- Title
- Hire date
- Previous company

Notable Departures:
For each significant departure:
- Name
- Former title
- Departure date
- Reason (if known)

Founder Status:
- Is the company founder-led, professional management, or in transition?

Focus on verified information from official sources."""


# =============================================================================
# 8. EMPLOYER & CULTURE
# =============================================================================

COMPANY_CULTURE_PROMPT = """You are an expert employer brand analyst researching {company_name}'s culture and employer reputation.

Execute the following research steps:

1. Find {company_name}'s Glassdoor page and extract ratings and reviews
2. Look for "Best Places to Work" awards and employer recognition
3. Find their careers page and culture content
4. Search for remote work policy announcements
5. Look for DEI initiatives and benefits information

Provide detailed employer and culture information:

Glassdoor:
- Overall rating (out of 5)
- Number of reviews
- Recommend to friend percentage
- CEO approval percentage
- Common pros (themes from reviews)
- Common cons (themes from reviews)

Employer Reputation:
- Awards (e.g., "Best Places to Work", "Top Startup", etc.)
- Employer brand score (if available)

Culture Attributes:
- Notable culture characteristics (e.g., innovative, fast-paced, collaborative)

Work Policy:
- Type (remote/hybrid/in-office)
- Details
- Office requirements

DEI Initiatives:
- Diversity, equity, and inclusion programs

Benefits Highlights:
- Notable benefits offered

LinkedIn Insights:
- Employee count
- Median tenure

Focus on factual information from verified sources."""


# =============================================================================
# 9. CUSTOMERS & TRACTION
# =============================================================================

COMPANY_CLIENTS_PROMPT = """You are an expert B2B researcher investigating {company_name}'s customers and traction.

Execute the following research steps:

1. Find and scrape {company_name}'s "Customers", "Case Studies", "Success Stories" page
2. Look for customer logos on their homepage
3. Search for "{company_name} customer" and "{company_name} case study"
4. Find press releases announcing customer wins
5. Check review sites like G2, Capterra, TrustRadius for customer information

Provide detailed customer information:

Notable Customers:
For each verified customer:
- Customer name
- Industry
- Company size
- Logo tier (e.g., Fortune 500, Fortune 1000)
- Verification source (case_study/press_release/logo/review/testimonial)
- Use case
- Outcomes/results achieved

Customer Count:
- Total customer count (if disclosed)
- Date of the count
- Source

Customer Count by Segment:
- Enterprise customers
- Mid-market customers
- SMB customers

Case Studies:
For each detailed case study:
- Customer name
- Title
- Summary
- Key metrics/results
- URL

Customer Segments Breakdown:
- Segment name
- Percentage
- Characteristics

Logo Wall:
- List of notable logos displayed

NPS Score:
- Net Promoter Score (if disclosed)

Distinguish between confirmed customers (case studies, press) and logo customers (website display)."""


# =============================================================================
# 10. PARTNERSHIPS & ECOSYSTEM
# =============================================================================

COMPANY_PARTNERSHIPS_PROMPT = """You are an expert business development analyst researching {company_name}'s partnerships and ecosystem.

Execute the following research steps:

1. Find and scrape {company_name}'s "Partners", "Integrations", "Ecosystem" page
2. Search for "{company_name} partnership" and "{company_name} integration"
3. Look for partnership announcements in press releases
4. Check for partner program details
5. Find technical integrations and marketplace listings

Provide comprehensive partnership information:

Strategic Partnerships:
For each major partnership:
- Partner company name
- Partner website
- Partnership type (strategic/technology/channel/platform/integration/reseller/consulting/go-to-market)
- Description
- Date announced

Technology Integrations:
For each integration:
- Integration name
- Category (CRM, Analytics, Communication, etc.)
- Integration type (native/api/third_party/marketplace)
- Description

Channel Partners:
For each channel/reseller partner:
- Name
- Type
- Regions covered

Supplier Dependencies:
For critical suppliers:
- Supplier name
- Dependency type
- Criticality (critical/important/minor)

Partner Program:
- Does a partner program exist?
- Program name
- Partner tiers
- Program URL

Focus on verified partnerships from official announcements."""


# =============================================================================
# 11. TECHNOLOGY & IP
# =============================================================================

COMPANY_TECHNOLOGY_PROMPT = """You are an expert technology analyst researching {company_name}'s technical capabilities.

Execute the following research steps:

1. Search for {company_name}'s engineering blog or technical posts
2. Look at job postings to understand their tech stack
3. Check BuiltWith, StackShare, or similar for technology detection
4. Search for patents filed by {company_name}
5. Find open source contributions on GitHub
6. Look for technical talks, conference presentations

Provide comprehensive technical information:

Proprietary Technology:
- Description of their core technical innovation

Patents:
For each patent:
- Title
- Patent number
- Status (granted/pending/filed)
- Date

Tech Stack:
- Programming languages
- Frameworks (frontend, backend)
- Databases
- Infrastructure
- Cloud providers
- DevOps tools

R&D Focus Areas:
- Key areas of R&D investment

AI/ML Capabilities:
For each capability:
- Capability name
- Description

Data Capabilities:
- Data/analytics capabilities description

Open Source:
For each public repository:
- Repository name
- URL
- Description
- Star count

Certifications:
- Security certifications (SOC 2, ISO 27001, etc.)

Technical Differentiators:
- What makes their technology unique?

Focus on verified technical information."""


# =============================================================================
# 12. COMPETITIVE LANDSCAPE
# =============================================================================

COMPETITIVE_LANDSCAPE_PROMPT = """You are an expert competitive intelligence analyst researching {company_name}.

Execute the following research steps:

1. Identify {company_name}'s primary industry and market category
2. Search for "{company_name} competitors" and "{company_name} alternatives"
3. Look for industry analyst reports mentioning {company_name}
4. Check software review sites (G2, Capterra) for competitive comparisons
5. Search for comparison articles: "{company_name} vs [competitor]"

Provide comprehensive competitive analysis:

Main Competitors:
For each major competitor:
- Company name
- Website
- Description
- Type (direct/indirect competitor)

Competitors by Product:
For each product/service:
- Product name
- Competitors for that product

Competitive Positioning:
- How does {company_name} position themselves in the market?

Key Differentiators:
- What makes {company_name} unique?

Competitive Advantages:
- Technology, pricing, brand, distribution, network effects, etc.

Competitive Weaknesses:
- Areas where competitors are stronger

Market Share:
- Market share estimate (if data available)

Market Position:
- Leader/challenger/follower/niche/emerging

Focus on factual competitive intelligence with sources."""


# =============================================================================
# 13. MARKET & INDUSTRY
# =============================================================================

COMPANY_MARKET_PROMPT = """You are an expert market analyst researching the industry context for {company_name}.

Execute the following research steps:

1. Identify {company_name}'s primary industry classification
2. Search for market size reports (TAM, SAM, SOM) for their market
3. Find industry growth rate forecasts
4. Look for regulatory requirements and compliance needs
5. Research market trends and dynamics

Provide comprehensive market information:

Industry Classification:
- Primary industry
- Sub-industry
- SIC code (if found)
- NAICS code (if found)

Market Size:
- TAM (Total Addressable Market)
- SAM (Serviceable Addressable Market)
- SOM (Serviceable Obtainable Market)
- Currency
- Year of estimate
- Source

Industry Growth Rate:
- Growth rate percentage
- Period
- Source

Market Trends:
For each major trend:
- Trend description
- Impact on the market
- Timeframe

Regulatory Environment:
- Key regulations affecting this market
- Compliance requirements
- Regulatory risk level (low/medium/high)

Industry Dynamics:
- Industry maturity (emerging/growth/mature/declining)
- Market concentration (fragmented/consolidated)
- Barriers to entry

Cite sources for market size and growth data."""


# =============================================================================
# 14. RECENT ACTIVITY (News)
# =============================================================================

COMPANY_NEWS_PROMPT = """You are an expert business news analyst researching {company_name}'s recent activity.

{date_filter}
{topic_filter}

Execute the following research steps:

1. Search for recent news articles mentioning {company_name}
2. Look for official press releases from {company_name}'s newsroom
3. Check major tech/business publications (TechCrunch, Reuters, Bloomberg)
4. Search for product launch announcements
5. Find partnership and M&A news

Provide detailed recent activity information:

Recent News:
For each news item:
- Headline
- Date
- Source/publication
- URL
- Category (product_launch/funding/partnership/m_and_a/executive/expansion/legal/other)
- Summary (2-3 sentences)
- Sentiment (positive/negative/neutral)

Product Launches:
For recent product launches:
- Product name
- Launch date
- Description
- URL

Partnerships Announced:
For recent partnerships:
- Partner name
- Date
- Partnership type
- Description

Funding Activity:
- Recent funding raise
- Date
- Amount
- Investors

M&A Activity:
- Acquisitions made (target, date, value)
- Acquisition rumors

Press Highlights:
- Notable press coverage, awards, recognition

Order results by date, most recent first."""


COMPANY_NEWS_DATE_FILTER = """Search for news from {from_date} to {to_date}."""
COMPANY_NEWS_TOPIC_FILTER = """Focus specifically on news about: {topic}"""


# =============================================================================
# 15. STRATEGIC OUTLOOK
# =============================================================================

COMPANY_STRATEGY_PROMPT = """You are an expert strategy analyst researching {company_name}'s strategic direction.

Execute the following research steps:

1. Search for executive interviews discussing company strategy
2. Look for investor presentations or earnings call transcripts
3. Find announcements about expansion plans
4. Search for M&A history and acquisition news
5. Look for IPO signals or public market discussions

Provide detailed strategic outlook:

Growth Strategy:
- Description of their stated growth strategy
- Key strategic initiatives

Expansion Plans:
- Geographic expansion targets
- Product expansion plans
- Vertical expansion targets

M&A History:
For each acquisition made:
- Target company
- Date
- Deal value (if known)
- Strategic rationale

Acquisition Rumors:
- Companies they might acquire
- Companies that might acquire them

IPO Signals:
- IPO status (not_planned/considering/preparing/filed/public)
- Expected timeline (if any signals)
- IPO indicators (CFO hire, auditor changes, S-1 filing, etc.)

Strategic Priorities:
- Key strategic priorities

Base this on factual statements from company leadership and official announcements."""


# =============================================================================
# 16. RISK FACTORS
# =============================================================================

COMPANY_RISKS_PROMPT = """You are an expert risk analyst assessing {company_name}'s risk factors.

Execute the following research steps:

1. Search for competitive threats and market pressures
2. Look for regulatory challenges or compliance issues
3. Find any litigation or legal exposure
4. Research key person dependencies
5. Look for customer concentration risks
6. Assess technology and market risks

Provide comprehensive risk assessment:

Competitive Risks:
For each competitive risk:
- Risk description
- Severity (low/medium/high)
- Details

Regulatory Risks:
For each regulatory risk:
- Regulation
- Jurisdiction
- Risk level (low/medium/high)
- Description

Legal Exposure:
- Active litigation (case, status, potential impact)
- Past settlements
- Overall legal risk level

Key Person Risk:
- Risk level (low/medium/high)
- Key individuals the company depends on
- Succession plan (if known)

Customer Concentration:
- Top customer revenue percentage (if known)
- Concentration risk level

Technology Risks:
- Technical debt, security vulnerabilities, platform dependencies

Market Risks:
- Market volatility, demand shifts, economic exposure

Supply Chain Risks:
- Key supply chain vulnerabilities

Financial Risks:
- Cash flow, debt, or capital risks

Overall Risk Assessment:
- Overall risk level (low/medium/high)

Focus on factual risk factors, not speculation."""


# =============================================================================
# 17. ESG & REPUTATION
# =============================================================================

COMPANY_ESG_PROMPT = """You are an expert ESG analyst researching {company_name}'s sustainability and reputation.

Execute the following research steps:

1. Find {company_name}'s sustainability or ESG page
2. Look for ESG reports or sustainability commitments
3. Search for environmental initiatives and carbon pledges
4. Find DEI programs and social initiatives
5. Look for any controversies or reputational issues

Provide comprehensive ESG information:

ESG Initiatives:
For each initiative:
- Initiative name
- Category (environmental/social/governance)
- Description
- URL

Sustainability:
- Sustainability commitments (carbon neutral, net zero, etc.)
- Certifications (B Corp, LEED, etc.)
- Sustainability report URL

Environmental:
- Carbon footprint (if disclosed)
- Renewable energy percentage
- Environmental programs

Social:
- DEI programs
- Community initiatives
- Labor practices

Governance:
- Board diversity
- Ethics policies

Controversies:
For any public controversies:
- Issue
- Date
- Description
- Resolution (if any)

Brand Perception:
- Overall sentiment (positive/neutral/negative)
- Notable recognition
- Notable criticism

ESG Rating:
- Rating (if rated by an ESG agency)
- Source
- Date

Focus on factual ESG information from official sources and news."""


# =============================================================================
# 18. COMPREHENSIVE RESEARCH (Single-call for vague queries)
# =============================================================================

RESEARCH_COMPANY_PROMPT = """You are an expert business analyst providing a comprehensive research report on {company_name}.

Execute a thorough multi-step research process:

1. Find {company_name}'s official website and scrape their homepage and About page
2. Search LinkedIn for company details (employee count, headquarters, industry)
3. Search for recent funding rounds and valuation information
4. Find their main products/services and pricing model
5. Identify their main competitors and market position
6. Search for recent news and developments

Provide a comprehensive company profile covering:

## Company Overview
- Official company name
- Website URL
- Founded year and founders
- Headquarters location
- Employee count and growth trend
- Company stage (seed/early/growth/mature/public)
- One-paragraph description of what they do

## Products & Business Model
- Main products/services (brief description of each)
- Business model (SaaS/marketplace/platform/services/etc.)
- Target customers (B2B/B2C, company size, industries)
- Pricing model (subscription/usage-based/freemium/enterprise)

## Funding & Financials
- Total funding raised
- Latest funding round (type, amount, date, lead investors)
- Latest valuation (if known)
- Key investors

## Competitive Position
- Top 3-5 main competitors
- Key differentiators
- Market position (leader/challenger/niche)

## Recent Activity
- 2-3 most notable recent news items (product launches, partnerships, funding, etc.)

Keep the response focused and actionable. Cite sources where possible.
Do not speculate - only report factual information found during research."""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_prompt(tool_name: str, **kwargs) -> str:
    """Get formatted prompt for a tool with variable substitution."""
    prompts = {
        "company_overview": COMPANY_OVERVIEW_PROMPT,
        "company_products": COMPANY_PRODUCTS_PROMPT,
        "company_business_model": COMPANY_BUSINESS_MODEL_PROMPT,
        "company_target_market": COMPANY_TARGET_MARKET_PROMPT,
        "company_financials": COMPANY_FINANCIALS_PROMPT,
        "company_funding": COMPANY_FUNDING_PROMPT,
        "company_leadership": COMPANY_LEADERSHIP_PROMPT,
        "company_culture": COMPANY_CULTURE_PROMPT,
        "company_clients": COMPANY_CLIENTS_PROMPT,
        "company_partnerships": COMPANY_PARTNERSHIPS_PROMPT,
        "company_technology": COMPANY_TECHNOLOGY_PROMPT,
        "competitive_landscape": COMPETITIVE_LANDSCAPE_PROMPT,
        "company_market": COMPANY_MARKET_PROMPT,
        "company_news": COMPANY_NEWS_PROMPT,
        "company_strategy": COMPANY_STRATEGY_PROMPT,
        "company_risks": COMPANY_RISKS_PROMPT,
        "company_esg": COMPANY_ESG_PROMPT,
        "research_company": RESEARCH_COMPANY_PROMPT,
    }

    prompt_template = prompts.get(tool_name)
    if not prompt_template:
        raise ValueError(f"No prompt found for tool: {tool_name}")

    # Handle product filter
    if tool_name == "company_products":
        product_filter = ""
        if kwargs.get("product_name"):
            product_filter = COMPANY_PRODUCTS_FILTER.format(product_name=kwargs["product_name"])
        kwargs["product_filter"] = product_filter

    # Handle date filter for news, financials, funding
    if tool_name in ["company_news", "company_financials", "company_funding"]:
        date_filter = ""
        if kwargs.get("from_date") or kwargs.get("to_date"):
            from_date = kwargs.get("from_date", "the beginning")
            to_date = kwargs.get("to_date", "now")
            date_filter = COMPANY_NEWS_DATE_FILTER.format(from_date=from_date, to_date=to_date)
        kwargs["date_filter"] = date_filter

    # Handle topic filter for news
    if tool_name == "company_news":
        topic_filter = ""
        if kwargs.get("topic"):
            topic_filter = COMPANY_NEWS_TOPIC_FILTER.format(topic=kwargs["topic"])
        kwargs["topic_filter"] = topic_filter

    return prompt_template.format(**kwargs)
