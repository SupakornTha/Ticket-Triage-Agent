# Support Ticket Triage Agent

An intelligent AI-powered agent that automatically triages incoming customer support tickets using GPT-4, classifying urgency, extracting key information, and deciding on appropriate routing actions.

## Features

- **Urgency Classification**: Automatically rates tickets as critical, high, medium, or low
- **Issue Extraction**: Identifies product affected, issue type, customer sentiment, and language
- **Knowledge Base Search**: Finds relevant FAQ and documentation for potential solutions
- **Customer Context**: Looks up customer history to inform routing decisions
- **Smart Routing**: Recommends appropriate actions (auto-respond, escalate, hold)
- **Multilingual Support**: Handles tickets in multiple languages

## Quick Start

### Option 1: Demo Mode (No API Key Required)

See example triage outputs without making any API calls:

```bash
# 1. Clone the repository
git clone https://github.com/SupakornTha/Ticket-Triage-Agent.git
cd Ticket-Triage-Agent

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run demo (shows example outputs)
python demo.py
```

Example output: Triage results for 3 sample tickets saved to `output/TKT_*.json`.

### Option 2: Real Agent with OpenAI API

Process tickets using GPT-4o-mini for live analysis:

**Prerequisites:**
- Python 3.8+
- OpenAI API key (get one from https://platform.openai.com/api-keys)

**Setup:**

1. **Clone the repository**:

```bash
git clone https://github.com/SupakornTha/Ticket-Triage-Agent.git
cd Ticket-Triage-Agent
```

2. **Create a virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set your OpenAI API key**:

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

5. **Run the agent**:

```bash
python main.py
```

The agent will:

1. Load three sample support tickets
2. Use GPT-4o-mini to analyze each ticket
3. Search the knowledge base for relevant solutions
4. Look up customer history
5. Make triage decisions
6. Save results to `output/` directory

### Example Output

```
TICKET: TKT_001
================================================================================

📊 CLASSIFICATION:
  Urgency:     CRITICAL
  Issue Type:  Billing - Duplicate Charges
  Sentiment:   Angry

🎯 DECISION:
  Action: ⚠ Escalate to urgent team

📝 SUMMARY:
  Critical billing issue with triple charge and escalating customer anger. Time-sensitive due to presentation deadline.

👤 SPECIALIST NOTES:
  - Customer has 3 pending $29.99 charges from failed upgrade attempts
  - Free tier customer (tenure: 4 months)
  - Threatening bank dispute if not resolved by end of day
  - Needs Pro export features for presentation in ~2 hours
```

## Project Structure

```
Ticket-Triage-Agent/
├── main.py                          # Entry point
├── demo.py                          # Demo mode (no API cost)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── ARCHITECTURE.md                  # Design decisions & evaluation
├── src/
│   ├── agent/
│   │   ├── triage_agent.py         # Main agent implementation
│   │   └── prompts.py              # System prompts & templates
│   └── tools/
│       ├── knowledge_base.py       # FAQ search tool
│       └── customer_history.py     # Customer lookup tool
├── data/
│   └── sample_tickets.py           # Sample tickets for testing
└── output/                         # Triage results (created on run)
```

## API Reference

### TicketTriageAgent

```python
from src.agent.triage_agent import TicketTriageAgent

# Initialize
agent = TicketTriageAgent(api_key="sk-...")

# Triage a ticket
result = agent.triage_ticket({
    "customer_id": "cust_001",
    "messages": [
        {"time": "3 hours ago", "text": "My payment failed..."},
        {"time": "now", "text": "This is urgent!"}
    ]
})

# Result contains:
# - urgency: critical|high|medium|low
# - issue_type: string
# - customer_sentiment: positive|neutral|negative|angry
# - action: auto_respond|escalate_specialist|escalate_urgent|hold
# - summary: brief overview
# - reasoning: classification explanation
# - suggested_response: if auto_respond
# - specialist_notes: if escalating
```

### Tools

**1. Search Knowledge Base**

```python
from src.tools.knowledge_base import search_knowledge_base

results = search_knowledge_base("payment failed")
# Returns: List of matching articles with content
```

**2. Get Customer History**

```python
from src.tools.customer_history import get_customer_history

customer = get_customer_history("cust_001")
# Returns: plan, tenure, payment status, urgency flags
```

## Sample Tickets

The project includes 3 diverse test cases:

1. **TKT_001**: Billing issue with escalating frustration
   - Free tier customer with triple charges
   - Time-critical (presentation deadline)
   - Expected action: ESCALATE_URGENT

2. **TKT_002**: System outage in Asia region
   - Enterprise customer with demo impact
   - Multi-user impact (Error 500)
   - Language: Thai
   - Expected action: HOLD (system investigation)

3. **TKT_003**: Feature request with troubleshooting
   - Engaged Pro user
   - Dark mode configuration issue
   - Feature request for scheduled dark mode
   - Expected action: AUTO_RESPOND (with feature notes)

## Configuration

### System Prompts

Edit `src/agent/prompts.py` to customize:

- Triage instructions and criteria
- Response templates for different issue types
- Escalation criteria

### Knowledge Base

Edit `src/tools/knowledge_base.py` to:

- Add new FAQ articles
- Modify search keywords
- Update solution content

### Customer Data

Edit `src/tools/customer_history.py` to:

- Add customer accounts
- Modify urgency flags
- Change SLA tiers

## Extending the Agent

### Adding New Tools

1. Create tool implementation in `src/tools/`
2. Document the tool in agent prompts
3. Implement execution in `triage_agent.py`'s `_execute_tool` method

### Adding New Ticket Types

1. Add sample ticket to `data/sample_tickets.py`
2. Update knowledge base if new issue type requires solutions
3. Adjust system prompts if new classification logic needed

## Costs

- Uses GPT-4 API (~$0.01-0.03 per ticket depending on content length)
- For high volume: Consider GPT-3.5-Turbo for 1/10 the cost
- Knowledge base is mocked (no database queries)
- Customer history is mocked (no real system queries)

## Troubleshooting

### "OpenAI API key not provided"

```bash
export OPENAI_API_KEY='your-api-key-here'
python main.py
```

### "Could not parse agent response"

- May occur if GPT response format doesn't match expectations
- Agent will return raw response for debugging
- Check system prompts for JSON instruction clarity

### Rate limiting

- OpenAI API may rate limit high volumes
- Implement backoff logic in production (see ARCHITECTURE.md)

## Evaluation in Production

See [ARCHITECTURE.md](./ARCHITECTURE.md) for:

- Production metrics to track
- Confusion matrix for classification accuracy
- Human review sampling strategy
- Escalation rate baseline

## License

Internal use only.

## Support

For questions about the implementation, see ARCHITECTURE.md for design decisions and rationale.
