"""CRM Automation Example - Automated HubSpot reporting workflows.

This example demonstrates common CRM reporting and analysis patterns using the 
HubSpot tool (read-only). Perfect for generating insights and notifications.

Workflows:
1. Daily Lead Digest - Find and report on new leads
2. Deal Pipeline Report - Analyze deals by stage
3. Contact Data Audit - Identify contacts with missing information
4. Company Data Review - Analyze company data quality

Usage:
    python crm_automation.py --workflow daily-leads
    python crm_automation.py --workflow deal-report
    python crm_automation.py --workflow contact-audit
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


def contact_data_audit(agent: Agent) -> None:
    """Audit contact records for missing or incomplete data."""
    print("🔍 Auditing contact records...\n")

    result = agent("""
    Contact data audit workflow:
    
    1. Search HubSpot for contacts and analyze data quality:
       - Contacts without company association
       - Contacts without job title
       - Contacts without lifecycle stage
       - Limit to 50 contacts for analysis
    
    2. For each contact, identify gaps:
       - Missing required fields
       - Incomplete contact information
       - No recent activity or engagement
       - Email domain analysis for company matching
    
    3. Generate actionable insights:
       - List contacts needing attention
       - Contacts with potential company matches (by email domain)
       - Suggested lifecycle stages based on available data
       - Priority items for manual data entry
    
    4. Send audit report to Teams:
       - Number of contacts analyzed
       - Data quality statistics
       - Top 10 contacts needing updates
       - Recommended actions for CRM team
    
    Provide complete audit summary.
    """)

    print("\n✅ Contact data audit completed!")


def company_data_review(agent: Agent) -> None:
    """Review and analyze company data quality."""
    print("🏢 Reviewing company data...\n")

    result = agent("""
    Company data review workflow:
    
    1. Search HubSpot for companies:
       - Get companies with key properties
       - Limit to 100 for comprehensive analysis
    
    2. Analyze data quality issues:
       - Companies with missing domain
       - Companies with incomplete information
       - Missing industry classification
       - Incomplete location data (country/city)
       - Duplicate company names (potential duplicates)
    
    3. Generate insights and recommendations:
       - Companies needing immediate attention
       - Suggested domain names based on company names
       - Industry classification suggestions
       - Location data corrections needed
       - Potential duplicate companies to merge
    
    4. Send analysis report to Teams:
       - Data quality statistics
       - Top 20 companies needing updates
       - Priority recommendations
       - Overall data health score
    
    Provide complete analysis summary.
    """)

    print("\n✅ Company data review completed!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated CRM workflows with HubSpot integration"
    )
    parser.add_argument(
        "--workflow",
        choices=["daily-leads", "deal-report", "contact-audit", "company-review"],
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
        elif args.workflow == "contact-audit":
            contact_data_audit(agent)
        elif args.workflow == "company-review":
            company_data_review(agent)

        return 0

    except Exception as e:
        print(f"❌ Error executing workflow: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

