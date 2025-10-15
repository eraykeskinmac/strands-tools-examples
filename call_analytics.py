"""Call Analytics Example - End-to-end call processing workflow.

This example demonstrates how to combine Deepgram, HubSpot, and Teams tools
to create a complete call analytics and CRM lookup workflow.

Workflow:
1. Transcribe call recording using Deepgram
2. Search for contact in HubSpot by phone number
3. Get contact details and history
4. Send summary notification to Teams with transcript and customer info

Usage:
    python call_analytics.py recording.mp3 +1234567890
"""

import argparse
import sys
from datetime import datetime

from strands import Agent
from strands_deepgram import deepgram
from strands_hubspot import hubspot
from strands_teams import teams


def process_call(audio_file: str, phone_number: str) -> None:
    """Process a call recording through the complete analytics workflow.

    Args:
        audio_file: Path to audio recording file
        phone_number: Phone number to search in HubSpot
    """
    # Create agent with all tools
    agent = Agent(tools=[deepgram, hubspot, teams])

    print(f"\n📞 Processing call recording: {audio_file}")
    print(f"🔍 Searching for contact: {phone_number}\n")

    # Complete workflow using agent
    result = agent(f"""
    Process this customer call:
    
    1. Transcribe the audio file: {audio_file}
       - Use speaker diarization
       - Detect sentiment
       - Identify topics
    
    2. Search HubSpot for contact with phone number: {phone_number}
       - Try different phone formats (with/without country code)
       - Get contact details including name, email, and company
       - Get associated deals and recent interactions if available
    
    3. Send a comprehensive summary to Teams:
       - Contact information (name, company, email)
       - Call transcript with speaker labels
       - Call duration and timestamp
       - Key topics discussed
       - Sentiment analysis
       - Suggested next steps or action items
       - Link to contact in HubSpot
    
    Provide a complete summary of all steps.
    """)

    print("\n✅ Call processing completed!")
    print(f"Result summary available in agent response above.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Process call recordings with Deepgram, HubSpot, and Teams integration"
    )
    parser.add_argument("audio_file", help="Path to audio recording file")
    parser.add_argument("phone_number", help="Phone number to search in HubSpot")
    parser.add_argument(
        "--no-teams",
        action="store_true",
        help="Skip Teams notification"
    )

    args = parser.parse_args()

    # Check if audio file exists
    import os
    if not os.path.exists(args.audio_file):
        print(f"❌ Error: Audio file not found: {args.audio_file}")
        return 1

    # Process the call
    try:
        process_call(args.audio_file, args.phone_number)
        return 0
    except Exception as e:
        print(f"❌ Error processing call: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

