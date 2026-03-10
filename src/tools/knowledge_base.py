"""Knowledge base search tool for the triage agent."""

from typing import Dict, List, Any

# Mock knowledge base with FAQ and documentation
KNOWLEDGE_BASE = {
    "billing_failed_payment": {
        "title": "Why did my payment fail?",
        "content": """Common reasons for payment failures:
1. Incorrect card details or expired card
2. Insufficient funds
3. Bank blocking the transaction (security)
4. Merchant restrictions on unusual activity
5. Duplicate charges due to multiple retry attempts

Solutions:
- Try with a different payment method
- Contact your bank to verify the merchant is allowed
- Wait 24 hours and retry (if temporary hold)
- Check for pending charges before retrying""",
        "keywords": ["payment", "failed", "charge", "billing", "card", "upgrade"]
    },
    "billing_duplicate_charges": {
        "title": "How do duplicate charges occur and get reversed?",
        "content": """Understanding duplicate charges:
- Failed transactions can trigger retry mechanisms
- Each retry attempt may appear as a separate pending charge
- Pending charges are temporary and may disappear after 3-5 business days
- Only COMPLETED charges count toward your account

Reversal process:
- Most duplicates auto-reverse within one billing cycle
- Automatic refunds are typically processed within 5-7 business days
- If not auto-resolved, submit a support ticket with specific charge dates
- Enterprise customers: escalated to billing team within 2 hours""",
        "keywords": ["duplicate", "charge", "refund", "pending", "reversed", "billing"]
    },
    "access_error500": {
        "title": "What does Error 500 mean?",
        "content": """Error 500 indicates: Internal Server Error
This means something went wrong on our systems, not your side.

Troubleshooting:
1. Try a different browser (Chrome, Firefox, Safari)
2. Clear browser cache and cookies
3. Try from a different device or network
4. Check https://status.company.com for ongoing incidents

If still failing:
- Provide browser console errors (F12 > Console)
- Specify your region and browser details
- This will be escalated to engineering immediately""",
        "keywords": ["error", "500", "can't access", "system", "down", "loading"]
    },
    "access_regional_outage": {
        "title": "Is there an outage in my region?",
        "content": """How to check for regional outages:
1. Visit https://status.company.com for real-time status
2. System checks by region (Americas, Europe, Asia)
3. Look for 'Operational', 'Degraded', or 'Outage' status

For Enterprise customers:
- You have dedicated status alerts
- Direct escalation path to incident management
- Maximum 1-hour response time on critical issues

Regional outage markers:
- Multiple users in same region reporting same error
- Status page shows degradation or outage
- Timeline correlates with issue start time
- Affects specific services (API, Web, etc.)""",
        "keywords": ["outage", "region", "down", "error", "status", "asia", "thailand"]
    },
    "appearance_dark_mode": {
        "title": "How to enable dark mode?",
        "content": """Enabling dark mode in our application:

Pro Plan and above:
1. Go to Settings > Appearance
2. Select 'System Default' or 'Light'
3. 'System Default' respects your OS dark mode setting

Note: Dark mode toggle depends on your plan:
- Free & Startup: Light mode only
- Pro & above: System Default option available

For Mac users:
- Enable dark mode in macOS: System Preferences > General > Dark
- Our app will respect this when set to 'System Default'

Known issues:
- Some older app versions don't update immediately on OS theme change
- Solution: Restart the app or toggle the option""",
        "keywords": ["dark mode", "theme", "appearance", "light", "system", "settings"]
    },
    "feature_dark_mode_schedule": {
        "title": "Can dark mode be scheduled?",
        "content": """Scheduled dark mode feature:

Current availability:
- Using 'System Default' provides schedule if OS has it configured
- macOS and Windows both support scheduled theme switching
- App respects your OS schedule when System Default is selected

Future roadmap:
- In-app dark mode scheduling is under consideration
- Vote on feature requests to help prioritize development
- Estimated timeline: TBD (depends on priority ranking)

Workaround:
- Configure your OS to switch themes on a schedule
- App will automatically follow when set to System Default""",
        "keywords": ["schedule", "dark mode", "time", "auto", "feature"]
    }
}

def search_knowledge_base(query: str) -> List[Dict[str, Any]]:
    """
    Search the knowledge base for relevant articles.
    
    Args:
        query: Search query string
        
    Returns:
        List of matching knowledge base articles with relevance scores
    """
    query_lower = query.lower()
    results = []
    
    for key, article in KNOWLEDGE_BASE.items():
        relevance_score = 0
        
        # Check keywords
        for keyword in article["keywords"]:
            if keyword in query_lower:
                relevance_score += 2
        
        # Check title
        if query_lower in article["title"].lower():
            relevance_score += 1
        
        # Check content
        if query_lower in article["content"].lower():
            relevance_score += 0.5
        
        if relevance_score > 0:
            results.append({
                "id": key,
                "title": article["title"],
                "content": article["content"],
                "relevance_score": relevance_score
            })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return results[:3]  # Return top 3 results
