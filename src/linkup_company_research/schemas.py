"""JSON schemas for structuredOutput mode in Linkup Company Research MCP.

Supports 17 comprehensive company profile tools.
"""

import json
from typing import Any


# =============================================================================
# 1. COMPANY OVERVIEW
# =============================================================================

COMPANY_OVERVIEW_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "legal_name": {"type": "string"},
        "website": {"type": "string"},
        "founded_year": {"type": "integer"},
        "founders": {
            "type": "array",
            "items": {"type": "string"}
        },
        "origin_story": {"type": "string"},
        "headquarters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "state": {"type": "string"},
                "country": {"type": "string"}
            }
        },
        "office_locations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "country": {"type": "string"},
                    "type": {"type": "string"}
                }
            }
        },
        "employee_count": {"type": "integer"},
        "employee_count_range": {"type": "string"},
        "employee_growth_trend": {
            "type": "string",
            "enum": ["growing", "stable", "declining"]
        },
        "company_stage": {
            "type": "string",
            "enum": ["seed", "early", "growth", "mature", "public", "turnaround"]
        },
        "description": {"type": "string"},
        "mission_statement": {"type": "string"},
        "linkedin_url": {"type": "string"},
        "twitter_url": {"type": "string"}
    },
    "required": ["company_name", "description"]
}


# =============================================================================
# 2. PRODUCTS & SERVICES
# =============================================================================

COMPANY_PRODUCTS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "product_type": {
                        "type": "string",
                        "enum": ["software", "hardware", "service", "platform", "api", "data"]
                    },
                    "target_use_cases": {"type": "array", "items": {"type": "string"}},
                    "key_features": {"type": "array", "items": {"type": "string"}},
                    "launch_date": {"type": "string"}
                }
            }
        },
        "services": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "service_type": {"type": "string"}
                }
            }
        },
        "pricing_model": {
            "type": "string",
            "enum": ["subscription", "usage_based", "one_time", "freemium", "enterprise", "hybrid", "free"]
        },
        "pricing_tiers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tier_name": {"type": "string"},
                    "price": {"type": "string"},
                    "billing_frequency": {"type": "string"},
                    "features": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "free_trial": {"type": "boolean"},
        "pricing_url": {"type": "string"}
    },
    "required": ["company_name"]
}


# =============================================================================
# 3. BUSINESS MODEL
# =============================================================================

COMPANY_BUSINESS_MODEL_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "business_type": {
            "type": "string",
            "enum": ["B2B", "B2C", "B2B2C", "D2C", "B2G", "C2C"]
        },
        "business_model": {
            "type": "string",
            "enum": ["SaaS", "marketplace", "platform", "services", "retail", "wholesale",
                     "licensing", "advertising", "hardware", "hybrid"]
        },
        "revenue_streams": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "stream_name": {"type": "string"},
                    "description": {"type": "string"},
                    "percentage_of_revenue": {"type": "string"}
                }
            }
        },
        "monetization_strategy": {"type": "string"},
        "unit_economics": {
            "type": "object",
            "properties": {
                "cac": {"type": "string"},
                "ltv": {"type": "string"},
                "ltv_cac_ratio": {"type": "string"},
                "payback_period": {"type": "string"},
                "gross_margin": {"type": "string"}
            }
        },
        "go_to_market": {
            "type": "string",
            "enum": ["sales_led", "product_led", "hybrid", "channel", "community_led"]
        },
        "sales_model": {
            "type": "string",
            "enum": ["self_serve", "inside_sales", "field_sales", "partner", "hybrid"]
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# 4. TARGET MARKET
# =============================================================================

COMPANY_TARGET_MARKET_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "ideal_customer_profile": {
            "type": "object",
            "properties": {
                "company_size": {
                    "type": "string",
                    "enum": ["SMB", "mid_market", "enterprise", "all"]
                },
                "industries": {"type": "array", "items": {"type": "string"}},
                "job_titles": {"type": "array", "items": {"type": "string"}},
                "pain_points": {"type": "array", "items": {"type": "string"}}
            }
        },
        "customer_segments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "segment_name": {"type": "string"},
                    "description": {"type": "string"},
                    "size_estimate": {"type": "string"}
                }
            }
        },
        "geographic_markets": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "region": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["primary", "secondary", "emerging"]
                    }
                }
            }
        },
        "vertical_focus": {"type": "array", "items": {"type": "string"}},
        "use_case_verticals": {"type": "array", "items": {"type": "string"}},
        "market_approach": {
            "type": "string",
            "enum": ["horizontal", "vertical", "hybrid"]
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# 5. FINANCIALS (Revenue & Metrics)
# =============================================================================

COMPANY_FINANCIALS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "revenue": {
            "type": "object",
            "properties": {
                "amount": {"type": "string"},
                "currency": {"type": "string"},
                "period": {"type": "string"},
                "date": {"type": "string"},
                "revenue_type": {
                    "type": "string",
                    "enum": ["ARR", "MRR", "GMV", "total_revenue", "run_rate"]
                }
            }
        },
        "revenue_history": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "amount": {"type": "string"},
                    "period": {"type": "string"},
                    "date": {"type": "string"}
                }
            }
        },
        "revenue_growth_rate": {"type": "string"},
        "profitability_status": {
            "type": "string",
            "enum": ["profitable", "break_even", "unprofitable"]
        },
        "path_to_profitability": {"type": "string"},
        "gross_margin": {"type": "string"},
        "key_metrics": {
            "type": "object",
            "properties": {
                "arr": {"type": "string"},
                "mrr": {"type": "string"},
                "gmv": {"type": "string"},
                "acv": {"type": "string"},
                "nrr": {"type": "string"},
                "churn_rate": {"type": "string"}
            }
        },
        "burn_rate": {"type": "string"},
        "runway_months": {"type": "integer"},
        "financial_health_signals": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["company_name"]
}


# =============================================================================
# 6. FUNDING & VALUATION
# =============================================================================

COMPANY_FUNDING_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "total_funding": {"type": "string"},
        "funding_rounds": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "round_type": {
                        "type": "string",
                        "enum": ["Pre-Seed", "Seed", "Series A", "Series B", "Series C",
                                 "Series D", "Series E+", "Growth", "Debt", "Grant", "Other"]
                    },
                    "date": {"type": "string"},
                    "amount": {"type": "string"},
                    "currency": {"type": "string"},
                    "lead_investors": {"type": "array", "items": {"type": "string"}},
                    "participating_investors": {"type": "array", "items": {"type": "string"}},
                    "valuation_at_round": {"type": "string"}
                }
            }
        },
        "latest_valuation": {
            "type": "object",
            "properties": {
                "amount": {"type": "string"},
                "date": {"type": "string"},
                "source": {"type": "string"},
                "valuation_type": {
                    "type": "string",
                    "enum": ["pre_money", "post_money"]
                }
            }
        },
        "valuation_history": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "amount": {"type": "string"},
                    "date": {"type": "string"},
                    "round": {"type": "string"}
                }
            }
        },
        "investors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": ["vc", "pe", "angel", "strategic", "corporate", "government", "family_office"]
                    },
                    "rounds_participated": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "notable_shareholders": {"type": "array", "items": {"type": "string"}},
        "debt_financing": {"type": "string"}
    },
    "required": ["company_name"]
}


# =============================================================================
# 7. LEADERSHIP & PEOPLE
# =============================================================================

COMPANY_LEADERSHIP_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "ceo": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "tenure_start": {"type": "string"},
                "background": {"type": "string"},
                "linkedin_url": {"type": "string"}
            }
        },
        "c_suite": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "title": {"type": "string"},
                    "tenure_start": {"type": "string"},
                    "background": {"type": "string"},
                    "previous_companies": {"type": "array", "items": {"type": "string"}},
                    "linkedin_url": {"type": "string"}
                }
            }
        },
        "founders": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "current_title": {"type": "string"},
                    "is_active": {"type": "boolean"},
                    "role_in_company": {"type": "string"}
                }
            }
        },
        "board_members": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "affiliation": {"type": "string"},
                    "board_role": {
                        "type": "string",
                        "enum": ["chair", "member", "observer"]
                    }
                }
            }
        },
        "key_hires_12_24_months": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "title": {"type": "string"},
                    "hire_date": {"type": "string"},
                    "previous_company": {"type": "string"}
                }
            }
        },
        "notable_departures": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "former_title": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "reason": {"type": "string"}
                }
            }
        },
        "founder_status": {
            "type": "string",
            "enum": ["founder_led", "professional_management", "transition"]
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# 8. EMPLOYER & CULTURE
# =============================================================================

COMPANY_CULTURE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "glassdoor": {
            "type": "object",
            "properties": {
                "overall_rating": {"type": "number"},
                "review_count": {"type": "integer"},
                "recommend_to_friend_pct": {"type": "string"},
                "ceo_approval_pct": {"type": "string"},
                "pros": {"type": "array", "items": {"type": "string"}},
                "cons": {"type": "array", "items": {"type": "string"}}
            }
        },
        "employer_reputation": {
            "type": "object",
            "properties": {
                "awards": {"type": "array", "items": {"type": "string"}},
                "employer_brand_score": {"type": "string"}
            }
        },
        "culture_attributes": {"type": "array", "items": {"type": "string"}},
        "work_policy": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["remote", "hybrid", "in_office"]
                },
                "details": {"type": "string"},
                "office_requirements": {"type": "string"}
            }
        },
        "dei_initiatives": {"type": "array", "items": {"type": "string"}},
        "benefits_highlights": {"type": "array", "items": {"type": "string"}},
        "linkedin_insights": {
            "type": "object",
            "properties": {
                "employee_count": {"type": "integer"},
                "median_tenure": {"type": "string"}
            }
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# 9. CUSTOMERS & TRACTION
# =============================================================================

COMPANY_CLIENTS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "notable_customers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "industry": {"type": "string"},
                    "company_size": {"type": "string"},
                    "logo_tier": {"type": "string"},
                    "verification_source": {
                        "type": "string",
                        "enum": ["case_study", "press_release", "logo", "review", "testimonial"]
                    },
                    "use_case": {"type": "string"},
                    "outcomes": {"type": "string"}
                }
            }
        },
        "customer_count": {
            "type": "object",
            "properties": {
                "total": {"type": "string"},
                "date": {"type": "string"},
                "source": {"type": "string"}
            }
        },
        "customer_count_by_segment": {
            "type": "object",
            "properties": {
                "enterprise": {"type": "string"},
                "mid_market": {"type": "string"},
                "smb": {"type": "string"}
            }
        },
        "case_studies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "customer": {"type": "string"},
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "key_metrics": {"type": "array", "items": {"type": "string"}},
                    "url": {"type": "string"}
                }
            }
        },
        "customer_segments_breakdown": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "segment": {"type": "string"},
                    "percentage": {"type": "string"},
                    "characteristics": {"type": "string"}
                }
            }
        },
        "logo_wall": {"type": "array", "items": {"type": "string"}},
        "nps_score": {"type": "string"}
    },
    "required": ["company_name"]
}


# =============================================================================
# 10. PARTNERSHIPS & ECOSYSTEM
# =============================================================================

COMPANY_PARTNERSHIPS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "strategic_partnerships": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "partner_name": {"type": "string"},
                    "partner_website": {"type": "string"},
                    "partnership_type": {
                        "type": "string",
                        "enum": ["strategic", "technology", "channel", "platform",
                                 "integration", "reseller", "consulting", "go_to_market"]
                    },
                    "description": {"type": "string"},
                    "date_announced": {"type": "string"}
                }
            }
        },
        "technology_integrations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "category": {"type": "string"},
                    "integration_type": {
                        "type": "string",
                        "enum": ["native", "api", "third_party", "marketplace"]
                    },
                    "description": {"type": "string"}
                }
            }
        },
        "channel_partners": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "regions": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "supplier_dependencies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "supplier": {"type": "string"},
                    "dependency_type": {"type": "string"},
                    "criticality": {
                        "type": "string",
                        "enum": ["critical", "important", "minor"]
                    }
                }
            }
        },
        "partner_program": {
            "type": "object",
            "properties": {
                "exists": {"type": "boolean"},
                "name": {"type": "string"},
                "tiers": {"type": "array", "items": {"type": "string"}},
                "url": {"type": "string"}
            }
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# 11. TECHNOLOGY & IP
# =============================================================================

COMPANY_TECHNOLOGY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "proprietary_technology": {"type": "string"},
        "patents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "number": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["granted", "pending", "filed"]
                    },
                    "date": {"type": "string"}
                }
            }
        },
        "tech_stack": {
            "type": "object",
            "properties": {
                "languages": {"type": "array", "items": {"type": "string"}},
                "frameworks": {"type": "array", "items": {"type": "string"}},
                "databases": {"type": "array", "items": {"type": "string"}},
                "infrastructure": {"type": "array", "items": {"type": "string"}},
                "cloud_providers": {"type": "array", "items": {"type": "string"}},
                "devops_tools": {"type": "array", "items": {"type": "string"}}
            }
        },
        "rd_focus_areas": {"type": "array", "items": {"type": "string"}},
        "ai_capabilities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "capability": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        },
        "data_capabilities": {"type": "string"},
        "open_source": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "url": {"type": "string"},
                    "description": {"type": "string"},
                    "stars": {"type": "integer"}
                }
            }
        },
        "certifications": {"type": "array", "items": {"type": "string"}},
        "technical_differentiators": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["company_name"]
}


# =============================================================================
# 12. COMPETITIVE LANDSCAPE
# =============================================================================

COMPETITIVE_LANDSCAPE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "main_competitors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "website": {"type": "string"},
                    "description": {"type": "string"},
                    "competitor_type": {
                        "type": "string",
                        "enum": ["direct", "indirect"]
                    }
                }
            }
        },
        "competitors_by_product": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product": {"type": "string"},
                    "competitors": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "competitive_positioning": {"type": "string"},
        "key_differentiators": {"type": "array", "items": {"type": "string"}},
        "competitive_advantages": {"type": "array", "items": {"type": "string"}},
        "competitive_weaknesses": {"type": "array", "items": {"type": "string"}},
        "market_share_estimate": {"type": "string"},
        "market_position": {
            "type": "string",
            "enum": ["leader", "challenger", "follower", "niche", "emerging"]
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# 13. MARKET & INDUSTRY
# =============================================================================

COMPANY_MARKET_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "industry_classification": {
            "type": "object",
            "properties": {
                "primary_industry": {"type": "string"},
                "sub_industry": {"type": "string"},
                "sic_code": {"type": "string"},
                "naics_code": {"type": "string"}
            }
        },
        "market_size": {
            "type": "object",
            "properties": {
                "tam": {"type": "string"},
                "sam": {"type": "string"},
                "som": {"type": "string"},
                "currency": {"type": "string"},
                "year": {"type": "string"},
                "source": {"type": "string"}
            }
        },
        "industry_growth_rate": {
            "type": "object",
            "properties": {
                "rate": {"type": "string"},
                "period": {"type": "string"},
                "source": {"type": "string"}
            }
        },
        "market_trends": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "trend": {"type": "string"},
                    "impact": {"type": "string"},
                    "timeframe": {"type": "string"}
                }
            }
        },
        "regulatory_environment": {
            "type": "object",
            "properties": {
                "key_regulations": {"type": "array", "items": {"type": "string"}},
                "compliance_requirements": {"type": "array", "items": {"type": "string"}},
                "regulatory_risk_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                }
            }
        },
        "industry_dynamics": {
            "type": "object",
            "properties": {
                "maturity": {
                    "type": "string",
                    "enum": ["emerging", "growth", "mature", "declining"]
                },
                "concentration": {
                    "type": "string",
                    "enum": ["fragmented", "consolidated"]
                },
                "barriers_to_entry": {"type": "array", "items": {"type": "string"}}
            }
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# 14. RECENT ACTIVITY (News)
# =============================================================================

COMPANY_NEWS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "recent_news": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "headline": {"type": "string"},
                    "date": {"type": "string"},
                    "source": {"type": "string"},
                    "url": {"type": "string"},
                    "category": {
                        "type": "string",
                        "enum": ["product_launch", "funding", "partnership", "m_and_a",
                                 "executive", "expansion", "legal", "other"]
                    },
                    "summary": {"type": "string"},
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "negative", "neutral"]
                    }
                }
            }
        },
        "product_launches": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"},
                    "launch_date": {"type": "string"},
                    "description": {"type": "string"},
                    "url": {"type": "string"}
                }
            }
        },
        "partnerships_announced": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "partner": {"type": "string"},
                    "date": {"type": "string"},
                    "partnership_type": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        },
        "funding_activity": {
            "type": "object",
            "properties": {
                "recent_raise": {"type": "string"},
                "date": {"type": "string"},
                "amount": {"type": "string"},
                "investors": {"type": "array", "items": {"type": "string"}}
            }
        },
        "ma_activity": {
            "type": "object",
            "properties": {
                "acquisitions_made": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "target": {"type": "string"},
                            "date": {"type": "string"},
                            "value": {"type": "string"}
                        }
                    }
                },
                "acquisition_rumors": {"type": "string"}
            }
        },
        "press_highlights": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["company_name"]
}


# =============================================================================
# 15. STRATEGIC OUTLOOK
# =============================================================================

COMPANY_STRATEGY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "growth_strategy": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "key_initiatives": {"type": "array", "items": {"type": "string"}}
            }
        },
        "expansion_plans": {
            "type": "object",
            "properties": {
                "geographic": {"type": "array", "items": {"type": "string"}},
                "product": {"type": "array", "items": {"type": "string"}},
                "vertical": {"type": "array", "items": {"type": "string"}}
            }
        },
        "ma_history": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "target_company": {"type": "string"},
                    "date": {"type": "string"},
                    "deal_value": {"type": "string"},
                    "rationale": {"type": "string"}
                }
            }
        },
        "acquisition_rumors": {
            "type": "object",
            "properties": {
                "as_acquirer": {"type": "array", "items": {"type": "string"}},
                "as_target": {"type": "array", "items": {"type": "string"}}
            }
        },
        "ipo_signals": {
            "type": "object",
            "properties": {
                "ipo_status": {
                    "type": "string",
                    "enum": ["not_planned", "considering", "preparing", "filed", "public"]
                },
                "expected_timeline": {"type": "string"},
                "indicators": {"type": "array", "items": {"type": "string"}}
            }
        },
        "strategic_priorities": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["company_name"]
}


# =============================================================================
# 16. RISK FACTORS
# =============================================================================

COMPANY_RISKS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "competitive_risks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "risk": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": ["low", "medium", "high"]
                    },
                    "description": {"type": "string"}
                }
            }
        },
        "regulatory_risks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "regulation": {"type": "string"},
                    "jurisdiction": {"type": "string"},
                    "risk_level": {
                        "type": "string",
                        "enum": ["low", "medium", "high"]
                    },
                    "description": {"type": "string"}
                }
            }
        },
        "legal_exposure": {
            "type": "object",
            "properties": {
                "active_litigation": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "case": {"type": "string"},
                            "status": {"type": "string"},
                            "potential_impact": {"type": "string"}
                        }
                    }
                },
                "past_settlements": {"type": "array", "items": {"type": "string"}},
                "legal_risk_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                }
            }
        },
        "key_person_risk": {
            "type": "object",
            "properties": {
                "risk_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                },
                "key_individuals": {"type": "array", "items": {"type": "string"}},
                "succession_plan": {"type": "string"}
            }
        },
        "customer_concentration": {
            "type": "object",
            "properties": {
                "top_customer_revenue_pct": {"type": "string"},
                "concentration_risk_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                }
            }
        },
        "technology_risks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "risk": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        },
        "market_risks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "risk": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        },
        "supply_chain_risks": {"type": "array", "items": {"type": "string"}},
        "financial_risks": {"type": "array", "items": {"type": "string"}},
        "overall_risk_assessment": {
            "type": "string",
            "enum": ["low", "medium", "high"]
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# 17. ESG & REPUTATION
# =============================================================================

COMPANY_ESG_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "esg_initiatives": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "initiative_name": {"type": "string"},
                    "category": {
                        "type": "string",
                        "enum": ["environmental", "social", "governance"]
                    },
                    "description": {"type": "string"},
                    "url": {"type": "string"}
                }
            }
        },
        "sustainability": {
            "type": "object",
            "properties": {
                "commitments": {"type": "array", "items": {"type": "string"}},
                "certifications": {"type": "array", "items": {"type": "string"}},
                "sustainability_report_url": {"type": "string"}
            }
        },
        "environmental": {
            "type": "object",
            "properties": {
                "carbon_footprint": {"type": "string"},
                "renewable_energy_pct": {"type": "string"},
                "environmental_programs": {"type": "array", "items": {"type": "string"}}
            }
        },
        "social": {
            "type": "object",
            "properties": {
                "dei_programs": {"type": "array", "items": {"type": "string"}},
                "community_initiatives": {"type": "array", "items": {"type": "string"}},
                "labor_practices": {"type": "string"}
            }
        },
        "governance": {
            "type": "object",
            "properties": {
                "board_diversity": {"type": "string"},
                "ethics_policies": {"type": "array", "items": {"type": "string"}}
            }
        },
        "controversies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue": {"type": "string"},
                    "date": {"type": "string"},
                    "description": {"type": "string"},
                    "resolution": {"type": "string"}
                }
            }
        },
        "brand_perception": {
            "type": "object",
            "properties": {
                "sentiment": {
                    "type": "string",
                    "enum": ["positive", "neutral", "negative"]
                },
                "notable_recognition": {"type": "array", "items": {"type": "string"}},
                "notable_criticism": {"type": "array", "items": {"type": "string"}}
            }
        },
        "esg_rating": {
            "type": "object",
            "properties": {
                "rating": {"type": "string"},
                "source": {"type": "string"},
                "date": {"type": "string"}
            }
        }
    },
    "required": ["company_name"]
}


# =============================================================================
# SCHEMA REGISTRY
# =============================================================================

SCHEMAS: dict[str, dict[str, Any]] = {
    # Core company info
    "company_overview": COMPANY_OVERVIEW_SCHEMA,
    "company_products": COMPANY_PRODUCTS_SCHEMA,
    "company_business_model": COMPANY_BUSINESS_MODEL_SCHEMA,
    "company_target_market": COMPANY_TARGET_MARKET_SCHEMA,

    # Financial
    "company_financials": COMPANY_FINANCIALS_SCHEMA,
    "company_funding": COMPANY_FUNDING_SCHEMA,

    # People
    "company_leadership": COMPANY_LEADERSHIP_SCHEMA,
    "company_culture": COMPANY_CULTURE_SCHEMA,

    # Traction
    "company_clients": COMPANY_CLIENTS_SCHEMA,
    "company_partnerships": COMPANY_PARTNERSHIPS_SCHEMA,

    # Technology
    "company_technology": COMPANY_TECHNOLOGY_SCHEMA,

    # Market
    "competitive_landscape": COMPETITIVE_LANDSCAPE_SCHEMA,
    "company_market": COMPANY_MARKET_SCHEMA,

    # News & Strategy
    "company_news": COMPANY_NEWS_SCHEMA,
    "company_strategy": COMPANY_STRATEGY_SCHEMA,

    # Risk & ESG
    "company_risks": COMPANY_RISKS_SCHEMA,
    "company_esg": COMPANY_ESG_SCHEMA,
}


def get_schema(tool_name: str) -> dict[str, Any]:
    """Get JSON schema for a tool by name."""
    schema = SCHEMAS.get(tool_name)
    if not schema:
        raise ValueError(f"No schema found for tool: {tool_name}")
    return schema


def get_schema_json(tool_name: str) -> str:
    """Get JSON schema as a JSON string for API requests."""
    return json.dumps(get_schema(tool_name))
