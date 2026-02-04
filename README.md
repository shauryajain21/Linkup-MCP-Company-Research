# Linkup Company Research MCP

An MCP server that provides comprehensive company research tools powered by [Linkup](https://linkup.so). Connect it to Claude, Cursor, or any MCP-compatible client to get instant company intelligence.

## Features

- **17 research tools** covering all aspects of company intelligence
- **Dual output formats**: Natural language answers with sources, or structured JSON for automation
- **Full parameter control**: Date filters, domain filters, image support, and result limits
- **Optimized prompts**: Following Linkup's best practices for accurate, comprehensive research

## Tools

| Tool | Description | Search Depth |
|------|-------------|--------------|
| `company_overview` | Company identity, location, size, industry, business model | Deep |
| `company_products` | Products, services, pricing, and use cases | Standard |
| `company_business_model` | Revenue streams, unit economics, go-to-market strategy | Standard |
| `company_target_market` | Ideal customer profile, segments, geographic markets | Standard |
| `company_financials` | Revenue, profitability, key metrics (ARR, MRR, GMV, NRR) | Deep |
| `company_funding` | Funding rounds, valuation, investors | Deep |
| `company_leadership` | CEO, C-suite, founders, board members, key hires | Standard |
| `company_culture` | Glassdoor ratings, work policy, benefits, employer brand | Standard |
| `company_clients` | Customers, case studies, testimonials | Deep |
| `company_partnerships` | Strategic partners, integrations, ecosystem | Deep |
| `company_technology` | Tech stack, patents, R&D, open source contributions | Deep |
| `competitive_landscape` | Competitors, market position, differentiators | Deep |
| `company_market` | Industry context, TAM/SAM/SOM, trends, regulations | Deep |
| `company_news` | Latest news, product launches, announcements | Standard |
| `company_strategy` | Growth plans, expansion, M&A history, IPO signals | Deep |
| `company_risks` | Risk assessment across competitive, regulatory, legal dimensions | Deep |
| `company_esg` | ESG initiatives, sustainability, reputation, controversies | Standard |

## Output Formats

All tools support two output formats via the `output_format` parameter:

### Natural Language (`output_format="answer"`)
Returns a comprehensive answer with up to 5 cited sources. Best for human consumption.

### Structured JSON (`output_format="structured"`)
Returns data in a defined JSON schema. Best for automation, CRM integration, and data pipelines.

## Parameters

### Common Parameters (all tools)
| Parameter | Type | Description |
|-----------|------|-------------|
| `company_name` | str | **Required.** The company to research |
| `output_format` | str | `"answer"` (default) or `"structured"` |
| `max_results` | int | Maximum sources to consider (1-50, default: 10-15) |

### Date Filters (news, financials, funding)
| Parameter | Type | Description |
|-----------|------|-------------|
| `from_date` | str | Start date in YYYY-MM-DD format |
| `to_date` | str | End date in YYYY-MM-DD format |

### Domain Filters (news)
| Parameter | Type | Description |
|-----------|------|-------------|
| `include_domains` | str | Comma-separated domains to include (e.g., "techcrunch.com,reuters.com") |
| `exclude_domains` | str | Comma-separated domains to exclude |

### Other Parameters
| Parameter | Type | Tools | Description |
|-----------|------|-------|-------------|
| `include_images` | bool | overview, competitive_landscape, leadership | Include relevant images |
| `topic` | str | news | Filter by topic (e.g., "funding", "product launch") |
| `product_name` | str | products | Filter for a specific product |

## Installation

### Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "linkup-company-research": {
      "command": "uvx",
      "args": ["linkup-company-research-mcp"],
      "env": {
        "LINKUP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add linkup-company-research -- uvx linkup-company-research-mcp
```

Then set your API key:
```bash
export LINKUP_API_KEY="your-api-key-here"
```

### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "linkup-company-research": {
      "command": "uvx",
      "args": ["linkup-company-research-mcp"],
      "env": {
        "LINKUP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Get Your API Key

1. Go to [linkup.so](https://linkup.so)
2. Sign up or log in
3. Navigate to API settings
4. Generate your API key

## Example Usage

Once connected, you can ask your AI assistant things like:

### Basic Research
- "Give me an overview of Stripe"
- "What's the latest news about OpenAI?"
- "Who are Figma's main competitors?"

### With Parameters
- "Get Anthropic's funding news from the last 6 months" (date filter)
- "Find Notion's customers and case studies"
- "What tech stack does Vercel use?"

### Structured Output for Automation
- "Get Stripe's company overview in structured format" (returns JSON)
- "Research HubSpot's leadership team as JSON" (for CRM integration)

## Tool Details

### company_overview
Researches the company's website, LinkedIn, and press coverage to provide detailed information about what they do, their industry, size, and business model.

### company_products
Researches product pages, pricing, and documentation to provide detailed information about offerings, pricing models, and use cases.

### company_business_model
Researches how the company makes money, their revenue streams, unit economics, and go-to-market strategy.

### company_target_market
Researches the company's ideal customer profile, customer segments, geographic markets, and vertical focus.

### company_financials
Researches revenue, profitability, key business metrics (ARR, MRR, GMV, NRR), and financial health indicators.

### company_funding
Researches funding history, funding rounds, valuation, and investors through Crunchbase, PitchBook, press releases, and financial news.

### company_leadership
Identifies CEO, C-suite executives, founders, board members, key hires, and notable departures.

### company_culture
Researches Glassdoor ratings, employer awards, culture attributes, work policy (remote/hybrid/in-office), and benefits.

### company_clients
Researches customer pages, case studies, press releases, and review sites to identify verified customers and their use cases.

### company_partnerships
Researches partner pages, integration marketplaces, press releases, and partner programs to map the company's ecosystem.

### company_technology
Analyzes engineering blogs, job postings, tech detection tools, patents, and open source contributions to understand technical capabilities.

### competitive_landscape
Identifies competitors, market positioning, differentiators, and competitive advantages through research of industry reports, review sites, and company materials.

### company_market
Researches industry classification, market size (TAM/SAM/SOM), industry growth rate, market trends, and regulatory environment.

### company_news
Searches news sources, press releases, and publications for recent coverage including product launches, funding, partnerships, and M&A activity.

### company_strategy
Researches growth strategy, expansion plans (geographic, product, vertical), M&A history, acquisition rumors, and IPO signals.

### company_risks
Researches competitive risks, regulatory risks, legal exposure, key person dependency, customer concentration, technology risks, and market risks.

### company_esg
Researches ESG initiatives, sustainability commitments, environmental programs, social initiatives, governance, controversies, and brand perception.

## Development

```bash
# Clone and install locally
git clone https://github.com/LinkupPlatform/linkup-company-research-mcp
cd linkup-company-research-mcp
pip install -e .

# Run the server directly
LINKUP_API_KEY="your-key" linkup-company-research
```

### Project Structure

```
src/linkup_company_research/
├── __init__.py
├── server.py      # Main MCP server with 17 tools
├── schemas.py     # JSON schemas for structuredOutput
├── prompts.py     # Optimized prompt templates
└── types.py       # Type definitions
```

## License

MIT
