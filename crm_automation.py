"""CRM Automation Example - Automated HubSpot workflows.

This example demonstrates common CRM automation patterns using the HubSpot tool,
including lead qualification, deal management, and reporting.

Workflows:
1. Daily Lead Digest - Find and qualify new leads
2. Deal Pipeline Report - Analyze deals by stage
3. Contact Enrichment - Update contact properties
4. Company Cleanup - Standardize company data

Usage:
    python crm_automation.py --workflow daily-leads
    python crm_automation.py --workflow deal-report
    python crm_automation.py --workflow enrich-contacts
"""

import argparse
import sys
from datetime import datetime, timedelta

from strands import Agent
from strands_tools_community import hubspot, teams


def daily_leads_digest(agent: Agent) -> None:
    """Generate and send daily digest of new qualified leads."""
    print("📊 Generating daily leads digest...\n")

    # Calculate date range
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    result = agent(f"""
    Generate a daily leads digest:
    
    1. Search HubSpot for contacts created since {yesterday}
       - Lifecycle stage: Marketing Qualified Lead or Sales Qualified Lead
       - Include: firstname, lastname, email, company, phone, jobtitle
       - Get up to 50 contacts
    
    2. For each lead, extract:
       - Name and job title
       - Company name
       - Contact information
       - Lead source
       - Lead score if available
    
    3. Group leads by:
       - Lifecycle stage
       - Lead source
       - Industry if available
    
    4. Send a formatted digest to Teams with:
       - Total number of new leads
       - Breakdown by category
       - Top 10 highest priority leads
       - Action items for sales team
    
    Provide a summary of the digest.
    """)

    print("\n✅ Daily leads digest completed!")


def deal_pipeline_report(agent: Agent) -> None:
    """Generate deal pipeline analysis report."""
    print("💼 Generating deal pipeline report...\n")

    result = agent("""
    Create a deal pipeline analysis report:
    
    1. Search HubSpot for all open deals:
       - Exclude: closedwon, closedlost stages
       - Include: dealname, amount, dealstage, pipeline, closedate, hubspot_owner_id
       - Get all deals (limit: 200)
    
    2. Analyze the pipeline:
       - Total deal value by stage
       - Number of deals per stage
       - Average deal size per stage
       - Deals closing this month
       - Deals at risk (close date in past)
    
    3. Calculate metrics:
       - Total pipeline value
       - Weighted pipeline (by stage probability)
       - Average deal cycle time
       - Conversion rates between stages
    
    4. Send comprehensive report to Teams:
       - Pipeline overview with visual indicators
       - Stage-by-stage breakdown
       - Deals requiring attention
       - Forecast for current month
    
    Provide executive summary.
    """)

    print("\n✅ Deal pipeline report completed!")


def enrich_contacts(agent: Agent) -> None:
    """Enrich contact records with missing information."""
    print("🔍 Enriching contact records...\n")

    result = agent("""
    Contact enrichment workflow:
    
    1. Search HubSpot for contacts missing key information:
       - Contacts without company association
       - Contacts without job title
       - Contacts without lifecycle stage
       - Limit to 20 contacts for batch processing
    
    2. For each contact:
       - Check if email domain matches existing company
       - Suggest company association if match found
       - Infer job title from available data if possible
       - Recommend lifecycle stage based on engagement
    
    3. Prepare update recommendations:
       - List contacts that can be automatically updated
       - Flag contacts requiring manual review
       - Suggest new companies to create
    
    4. Send enrichment report to Teams:
       - Number of contacts processed
       - Automatic updates made
       - Manual reviews needed
       - Data quality score
    
    Provide enrichment summary.
    """)

    print("\n✅ Contact enrichment completed!")


def company_cleanup(agent: Agent) -> None:
    """Standardize and cleanup company records."""
    print("🏢 Cleaning up company records...\n")

    result = agent("""
    Company data cleanup workflow:
    
    1. Search HubSpot for companies:
       - Get all companies with basic properties
       - Limit to 50 for initial cleanup batch
    
    2. Identify cleanup opportunities:
       - Companies with missing domain
       - Companies with inconsistent naming
       - Companies missing industry classification
       - Companies without proper country/city data
    
    3. Suggest standardizations:
       - Standardize company names (capitalize properly)
       - Infer domains from company names
       - Classify industries based on available data
       - Normalize location data
    
    4. Generate cleanup report for Teams:
       - Data quality issues found
       - Suggested corrections
       - Priority items for manual review
       - Overall data quality score
    
    Provide cleanup summary.
    """)

    print("\n✅ Company cleanup analysis completed!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated CRM workflows with HubSpot integration"
    )
    parser.add_argument(
        "--workflow",
        choices=["daily-leads", "deal-report", "enrich-contacts", "company-cleanup"],
        required=True,
        help="Workflow to execute"
    )
    parser.add_argument(
        "--no-teams",
        action="store_true",
        help="Skip Teams notifications"
    )

    args = parser.parse_args()

    # Create agent
    tools = [hubspot]
    if not args.no_teams:
        tools.append(teams)

    agent = Agent(tools=tools)

    # Execute selected workflow
    try:
        if args.workflow == "daily-leads":
            daily_leads_digest(agent)
        elif args.workflow == "deal-report":
            deal_pipeline_report(agent)
        elif args.workflow == "enrich-contacts":
            enrich_contacts(agent)
        elif args.workflow == "company-cleanup":
            company_cleanup(agent)

        return 0

    except Exception as e:
        print(f"❌ Error executing workflow: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

