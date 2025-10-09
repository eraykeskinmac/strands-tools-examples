"""Team Notifications Example - Microsoft Teams integration patterns.

This example demonstrates different types of Teams notifications using
adaptive cards and templates.

Notification Types:
1. Simple notifications (info, success, warning, error)
2. Approval requests with action buttons
3. Status updates with progress indicators
4. Custom rich cards with data visualization

Usage:
    python team_notifications.py --type simple --message "Test notification"
    python team_notifications.py --type approval --title "Budget Approval"
    python team_notifications.py --type status --project "Website" --status "In Progress"
"""

import argparse
import sys

from strands import Agent
from strands_tools_community import teams


def send_simple_notification(agent: Agent, title: str, message: str, color: str = "default") -> None:
    """Send a simple notification to Teams.

    Args:
        agent: Strands Agent instance
        title: Notification title
        message: Notification message
        color: Color scheme (default, good, attention, warning)
    """
    print(f"📢 Sending notification: {title}\n")

    result = agent(f"""
    Send a Teams notification:
    - Title: {title}
    - Message: {message}
    - Color: {color}
    
    Use the notification template.
    """)

    print("\n✅ Notification sent!")


def send_approval_request(agent: Agent, title: str, details: str) -> None:
    """Send an approval request to Teams.

    Args:
        agent: Strands Agent instance
        title: Approval request title
        details: Detailed description
    """
    print(f"✋ Sending approval request: {title}\n")

    # Generate approval URLs (in real scenario, these would be actual endpoints)
    approve_url = "https://example.com/approve/123"
    reject_url = "https://example.com/reject/123"

    result = agent(f"""
    Send an approval request to Teams:
    - Title: {title}
    - Details: {details}
    - Approve URL: {approve_url}
    - Reject URL: {reject_url}
    
    Use the approval template with action buttons.
    """)

    print("\n✅ Approval request sent!")


def send_status_update(agent: Agent, project: str, status: str, details: str) -> None:
    """Send a project status update to Teams.

    Args:
        agent: Strands Agent instance
        project: Project name
        status: Current status
        details: Status details
    """
    print(f"📊 Sending status update for: {project}\n")

    # Determine color based on status
    status_colors = {
        "completed": "good",
        "in progress": "accent",
        "on hold": "warning",
        "blocked": "attention",
    }
    color = status_colors.get(status.lower(), "default")

    result = agent(f"""
    Send a status update to Teams:
    - Project: {project}
    - Status: {status}
    - Details: {details}
    - Color: {color}
    
    Use the status template.
    """)

    print("\n✅ Status update sent!")


def send_custom_card(agent: Agent) -> None:
    """Send a custom adaptive card with rich content."""
    print("🎨 Sending custom adaptive card...\n")

    result = agent("""
    Send a custom adaptive card to Teams with:
    
    1. Header section:
       - Title: "Weekly Performance Report"
       - Subtitle: Current week
       - Icon/emoji for visual appeal
    
    2. Key metrics section (use FactSet):
       - New Leads: 42 (+12% vs last week)
       - Deals Closed: 8 ($156K revenue)
       - Response Time: 2.3 hours average
       - Customer Satisfaction: 94%
    
    3. Top performers section:
       - List top 3 sales reps with deal counts
       - Use formatted text with highlights
    
    4. Action items section:
       - Follow up on 15 pending proposals
       - Schedule 5 discovery calls
       - Update 23 stale opportunities
    
    5. Footer:
       - Link to full report
       - Generated timestamp
    
    Make it visually appealing with proper spacing and formatting.
    """)

    print("\n✅ Custom card sent!")


def send_daily_digest(agent: Agent) -> None:
    """Send a daily digest with multiple sections."""
    print("📰 Sending daily digest...\n")

    result = agent("""
    Create and send a comprehensive daily digest to Teams:
    
    Title: "Daily Sales Digest - [Today's Date]"
    
    Sections:
    
    1. 📊 Today's Highlights
       - Total revenue generated
       - Number of deals closed
       - New qualified leads
       - Meetings scheduled
    
    2. 🎯 Pipeline Status
       - Open deals count and total value
       - Deals in negotiation
       - Deals closing this week
    
    3. ⚡ Action Required
       - Overdue tasks (count)
       - Calls to return (count)
       - Proposals to send (count)
    
    4. 🏆 Achievements
       - Deal of the day
       - Most active sales rep
       - Fastest response time
    
    5. 📅 Tomorrow's Schedule
       - Scheduled calls: [count]
       - Meetings: [count]
       - Deadlines: [count]
    
    Use good color scheme and include action button to "View Full Dashboard"
    """)

    print("\n✅ Daily digest sent!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Send notifications to Microsoft Teams"
    )
    parser.add_argument(
        "--type",
        choices=["simple", "approval", "status", "custom", "digest"],
        required=True,
        help="Type of notification to send"
    )
    parser.add_argument("--title", help="Notification title")
    parser.add_argument("--message", help="Notification message")
    parser.add_argument("--details", help="Detailed description (for approval)")
    parser.add_argument("--project", help="Project name (for status)")
    parser.add_argument("--status", help="Status (for status updates)")
    parser.add_argument(
        "--color",
        choices=["default", "good", "attention", "warning", "accent"],
        default="default",
        help="Color scheme"
    )

    args = parser.parse_args()

    # Create agent with teams tool
    agent = Agent(tools=[teams])

    # Execute based on notification type
    try:
        if args.type == "simple":
            if not args.title or not args.message:
                print("❌ Error: --title and --message required for simple notifications")
                return 1
            send_simple_notification(agent, args.title, args.message, args.color)

        elif args.type == "approval":
            if not args.title or not args.details:
                print("❌ Error: --title and --details required for approval requests")
                return 1
            send_approval_request(agent, args.title, args.details)

        elif args.type == "status":
            if not args.project or not args.status:
                print("❌ Error: --project and --status required for status updates")
                return 1
            details = args.details or f"{args.project} is currently {args.status}"
            send_status_update(agent, args.project, args.status, details)

        elif args.type == "custom":
            send_custom_card(agent)

        elif args.type == "digest":
            send_daily_digest(agent)

        return 0

    except Exception as e:
        print(f"❌ Error sending notification: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

