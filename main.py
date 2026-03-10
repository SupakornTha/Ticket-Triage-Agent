"""Main entry point for the Support Ticket Triage Agent."""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent.triage_agent import TicketTriageAgent
from data.sample_tickets import SAMPLE_TICKETS


def print_result(result: dict, ticket_id: str) -> None:
    """Pretty print triage result."""
    print(f"\n{'='*80}")
    print(f"TICKET: {ticket_id}")
    print(f"{'='*80}")
    
    # Display main classification
    print(f"\n📊 CLASSIFICATION:")
    print(f"  Urgency:     {result.get('urgency', 'N/A').upper()}")
    print(f"  Issue Type:  {result.get('issue_type', 'N/A')}")
    print(f"  Sentiment:   {result.get('customer_sentiment', 'N/A')}")
    
    # Display decision
    print(f"\n🎯 DECISION:")
    action = result.get('action', 'N/A').upper()
    action_descriptions = {
        'AUTO_RESPOND': '✓ Send automatic response',
        'ESCALATE_SPECIALIST': '→ Route to specialist',
        'ESCALATE_URGENT': '⚠ Escalate to urgent team',
        'HOLD': '⏸ Place on hold'
    }
    print(f"  Action: {action_descriptions.get(action, action)}")
    
    # Display summary
    if result.get('summary'):
        print(f"\n📝 SUMMARY:")
        print(f"  {result['summary']}")
    
    # Display reasoning
    if result.get('reasoning'):
        print(f"\n💡 REASONING:")
        for line in result['reasoning'].split('\n'):
            if line.strip():
                print(f"  {line}")
    
    # Display automatic response if applicable
    if result.get('suggested_response'):
        print(f"\n💬 SUGGESTED AUTO-RESPONSE:")
        for line in result['suggested_response'].split('\n'):
            if line.strip():
                print(f"  {line}")
    
    # Display specialist notes if escalating
    if result.get('specialist_notes'):
        print(f"\n👤 SPECIALIST NOTES:")
        for line in result['specialist_notes'].split('\n'):
            if line.strip():
                print(f"  {line}")
    
    print(f"\n{'='*80}\n")


def main():
    """Run the triage agent on sample tickets."""
    print("Support Ticket Triage Agent")
    print("============================\n")
    
    # Initialize agent
    try:
        agent = TicketTriageAgent()
        print("✓ Agent initialized successfully\n")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Process each sample ticket
    for i, ticket in enumerate(SAMPLE_TICKETS, 1):
        print(f"\n⏳ Processing ticket {i}/{len(SAMPLE_TICKETS)}...")
        
        try:
            result = agent.triage_ticket(ticket)
            print_result(result, ticket.get("ticket_id"))
            
            # Save result to file
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            ticket_id = ticket.get("ticket_id")
            output_file = output_dir / f"{ticket_id}_triage_result.json"
            
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"✓ Result saved to {output_file}")
            
        except Exception as e:
            print(f"❌ Error processing ticket: {e}")
            print(f"   Please ensure your OpenAI API key is valid and you have credits.")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
