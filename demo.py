"""Demo script showing example triage outputs without requiring OpenAI API."""

import json
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from data.sample_tickets import SAMPLE_TICKETS


# Mock triage results for demonstration
DEMO_RESULTS = [
    {
        "customer_id": "cust_001",
        "urgency": "critical",
        "issue_type": "Billing - Duplicate Charges",
        "customer_sentiment": "angry",
        "action": "escalate_urgent",
        "summary": "Critical billing issue with triple charge and escalating customer anger. Time-sensitive due to presentation deadline (2 hours).",
        "reasoning": "Customer is extremely upset (multiple escalations in 1 hour). Three identical $29.99 charges are pending despite only one successful upgrade attempt. Free tier customer threatening bank dispute. Immediate specialized attention required.",
        "suggested_response": None,
        "specialist_notes": "URGENT ACTION REQUIRED:\n- Customer has 3 pending $29.99 charges (total $89.97)\n- Free tier customer since 4 months ago\n- Presentation deadline: 2 hours from now\n- Previously threatened bank dispute if not resolved by end of day\n- Recommend: 1) Immediate charge reversal for duplicates, 2) Upgrade account to Pro immediately, 3) Personal follow-up call within 15 minutes"
    },
    {
        "customer_id": "cust_002",
        "urgency": "critical",
        "issue_type": "System Access - Regional Outage",
        "customer_sentiment": "negative",
        "action": "hold",
        "summary": "Critical system outage affecting Asia region. Error 500 across multiple browsers/users. Enterprise customer with demo impact.",
        "reasoning": "Multiple signals indicate regional issue: Same error (500) across Chrome, Safari, Firefox; Multiple users affected (teammates can't access either); Status page shows operational but users report otherwise. Enterprise customer with 45 seats affected. Demo with major client this afternoon at risk.",
        "specialist_notes": "CRITICAL INFRASTRUCTURE ISSUE:\n- Scope: Asia region outage, Error 500\n- Impact: Enterprise customer (45 seats), 8 months customer\n- Revenue risk: Major client demo this afternoon - deal may be lost if not resolved\n- Triage action: Escalate to infrastructure/SRE team immediately\n- Customer language: Thai (provide Thai-language updates)\n- ETA: Customer needs resolution within 4 hours for demo\n- Action: Place on hold pending status update; notify SRE team; provide status updates every 30 minutes"
    },
    {
        "customer_id": "cust_003",
        "urgency": "low",
        "issue_type": "Feature Request + Troubleshooting",
        "customer_sentiment": "positive",
        "action": "auto_respond",
        "summary": "Pro tier customer asking about dark mode scheduling feature. Positive engagement, no blocking issues.",
        "reasoning": "Customer is engaged Pro tier user (daily logins, 5 months tenure). Positive tone throughout. Resolved troubleshooting issue (found 'System Default' option). Now asking about feature request (scheduled dark mode). Low urgency, engaged user who appreciates communication.",
        "suggested_response": "Thanks for the great suggestion! Dark mode scheduling is definitely a feature our team has discussed.\n\nCurrent status:\n- Dark mode auto-switch based on system settings: ✓ Available in Settings > Appearance\n- Scheduled dark mode: Under review by our product team\n\nSince you're a Pro tier customer with strong engagement, I'm adding your +1 to our feature request tracker. These high-engagement user votes significantly impact our dev roadmap prioritization.\n\nIn the meantime:\n- System Default option ties to your OS schedule\n- You can manually toggle in Settings > Appearance when needed\n\nWe appreciate your partnership and I'll loop you in if this moves to development!",
        "specialist_notes": None
    }
]


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
        print(f"\n💬 AUTO-RESPONSE:")
        print(f"  {result['suggested_response']}")
    
    # Display specialist notes if escalating
    if result.get('specialist_notes'):
        print(f"\n👤 SPECIALIST NOTES:")
        for line in result['specialist_notes'].split('\n'):
            if line.strip():
                print(f"  {line}")
    
    print(f"\n{'='*80}\n")


def main():
    """Run the demo with mock triage results."""
    print("Support Ticket Triage Agent - DEMO MODE")
    print("=" * 50)
    print("(Using example results - no API calls made)\n")
    
    # Show sample tickets and their demo results
    for i, (ticket, result) in enumerate(zip(SAMPLE_TICKETS, DEMO_RESULTS), 1):
        print(f"⏳ Processing ticket {i}/{len(SAMPLE_TICKETS)}...")
        print_result(result, ticket.get("ticket_id"))
        
        # Save result to file
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        ticket_id = ticket.get("ticket_id")
        output_file = output_dir / f"{ticket_id}_triage_result.json"
        
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✓ Result saved to {output_file}")
    
    print("\n" + "="*80)
    print("✓ Demo completed successfully!")
    print("="*80)
    print("\nTo use with real OpenAI API:")
    print("1. Get your API key from https://platform.openai.com/api-keys")
    print("2. Copy .env.example to .env")
    print("3. Add your API key: OPENAI_API_KEY=sk-...")
    print("4. Run: python main.py")


if __name__ == "__main__":
    main()
