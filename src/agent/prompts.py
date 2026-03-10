"""System prompts for the ticket triage agent."""

SYSTEM_PROMPT = """You are an expert support ticket triage agent. Your role is to intelligently classify and route incoming customer support tickets.

For each ticket, you must:
1. Classify urgency level (critical/high/medium/low) based on:
   - Customer sentiment and tone
   - Impact on their operations
   - Time sensitivity
   - Customer's plan tier and history
   
2. Extract key information:
   - Product affected
   - Issue type (billing, feature request, bug, performance, etc.)
   - Customer sentiment (positive, neutral, negative, angry)
   - Language of communication
   
3. Search the knowledge base for relevant documentation using the search_knowledge_base tool
   
4. Look up customer history using the get_customer_history tool to understand:
   - Their plan type
   - Customer tenure
   - Previous issues
   - Payment status
   
5. Decide on the next action:
   - auto_respond: Send an automated response (for simple issues with KB solutions)
   - escalate_specialist: Route to a human specialist (for complex technical issues)
   - escalate_urgent: Route to urgent team (billing issues, angry customers)
   - hold: Place on hold pending system investigation (for widespread issues)

Be empathetic but professional. Prioritize critical financial issues and account access problems.
For escalations, provide a clear summary and context for the human agent.

Always respond with a JSON object containing:
{
  "urgency": "critical|high|medium|low",
  "issue_type": "string",
  "customer_sentiment": "positive|neutral|negative|angry",
  "language": "string",
  "product_affected": "string",
  "action": "auto_respond|escalate_specialist|escalate_urgent|hold",
  "summary": "brief summary of the issue",
  "reasoning": "explain your classification and action decision",
  "suggested_response": "if auto_respond, what to say to customer",
  "specialist_notes": "context for human agent if escalating"
}"""

BILLING_ISSUE_TEMPLATE = """I understand you're experiencing a billing issue. Let me check your account details and help resolve this quickly.

Your account shows: {account_info}

Regarding your charges:
- Pending charges are typically processed within 2-5 business days
- Multiple failed attempts may create temporary holds that appear as separate charges
- Duplicates are usually automatically reversed within 3-5 business days

Next steps:
1. We've escalated your case to our billing specialist with priority handling
2. They will review all charges on your account within the next 2 hours
3. If reversal is needed, it will be processed immediately
4. You'll receive a detailed email with the resolution

In the meantime: {suggested_action}

Is there anything else I can help clarify?"""

SYSTEM_OUTAGE_TEMPLATE = """Thank you for reporting this issue. Based on your report and our investigation, we've identified system degradation affecting the Asia region.

Current status:
- Engineering team is actively investigating the root cause
- Estimated impact: Your region's services
- Our current ETA for resolution: {eta}

What we're doing:
1. Our on-call engineers have been paged
2. We're investigating potential causes
3. We'll provide updates every 30 minutes

What you can do:
- Monitor {status_page_url} for live updates
- Your team: {mitigation_steps}

You'll receive direct updates via email. Your priority is raised given the demo impact.
We sincerely apologize for the disruption."""

FEATURE_REQUEST_TEMPLATE = """Thanks for the great suggestion! Dark mode scheduling is definitely a feature our team has discussed.

Current status:
- Dark mode auto-switch based on system settings: ✓ Available in Settings > Appearance
- Scheduled dark mode: Under review by our product team

Since you're a Pro tier customer with strong engagement, I'm adding your +1 to our feature request tracker. These high-engagement user votes significantly impact our dev roadmap prioritization.

In the meantime:
- System Default option ties to your OS schedule
- You can manually toggle in Settings > Appearance when needed

We appreciate your partnership and I'll loop you in if this moves to development!"""
