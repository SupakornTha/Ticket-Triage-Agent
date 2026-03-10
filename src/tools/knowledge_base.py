"""Knowledge base search tool for the triage agent.

Knowledge base articles are defined as a simple list of dictionaries.
Each article has: id, title, content, and keywords for searching.

To add a new article, append to KB_ARTICLES list:
    KB_ARTICLES.append({
        "id": "unique_id",
        "title": "Article Title",
        "content": "...",
        "keywords": ["keyword1", "keyword2"]
    })
"""

from typing import Dict, List, Any


# Knowledge base articles - easy to modify and extend
KB_ARTICLES = [
    {
        "id": "billing_failed_payment",
        "title": "Why did my payment fail?",
        "keywords": ["payment", "failed", "charge", "billing", "card", "upgrade"],
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
- Check for pending charges before retrying"""
    },
    {
        "id": "billing_duplicate_charges",
        "title": "How do duplicate charges occur and get reversed?",
        "keywords": ["duplicate", "charge", "refund", "pending", "reversed"],
        "content": """Understanding duplicate charges:
- Failed transactions can trigger retry mechanisms
- Each retry attempt may appear as a separate pending charge
- Pending charges are temporary and may disappear after 3-5 business days
- Only COMPLETED charges count toward your account

Reversal process:
- Most duplicates auto-reverse within one billing cycle
- Automatic refunds are typically processed within 5-7 business days
- If not auto-resolved, submit a support ticket with specific charge dates
- Enterprise customers: escalated to billing team within 2 hours"""
    },
    {
        "id": "access_error500",
        "title": "What does Error 500 mean?",
        "keywords": ["error", "500", "can't access", "system", "down", "loading"],
        "content": """Error 500 indicates: Internal Server Error
This means something went wrong on our systems, not your side.

Troubleshooting:
1. Try a different browser (Chrome, Firefox, Safari)
2. Clear browser cache and cookies
3. Try from a different device or network
4. Check status.company.com for ongoing incidents

If still failing:
- Provide browser console errors (F12 > Console)
- Specify your region and browser details
- This will be escalated to engineering immediately"""
    },
    {
        "id": "access_regional_outage",
        "title": "Is there an outage in my region?",
        "keywords": ["outage", "region", "down", "error", "status"],
        "content": """How to check for regional outages:
1. Visit status.company.com for real-time status
2. System checks by region (Americas, Europe, Asia)
3. Look for 'Operational', 'Degraded', or 'Outage' status

For Enterprise customers:
- You have dedicated status alerts
- Direct escalation path to incident management
- Maximum 1-hour response time on critical issues

Regional outage markers:
- Multiple users in same region reporting same error
- Status page shows degradation or outage
- Timeline correlates with issue start time"""
    },
    {
        "id": "appearance_dark_mode",
        "title": "How to enable dark mode?",
        "keywords": ["dark mode", "theme", "appearance", "light", "system"],
        "content": """Enabling dark mode in our application:

Pro Plan and above:
1. Go to Settings > Appearance
2. Select 'System Default' or 'Light'
3. 'System Default' respects your OS dark mode setting

Note: Dark mode availability by plan:
- Free & Startup: Light mode only
- Pro & above: System Default option available

For Mac users:
- Enable dark mode in macOS: System Preferences > General > Dark
- App will respect this when set to 'System Default'
- Restart the app if theme doesn't update immediately"""
    },
    {
        "id": "feature_dark_mode_schedule",
        "title": "Can dark mode be scheduled?",
        "keywords": ["schedule", "dark mode", "time", "auto", "feature"],
        "content": """Scheduled dark mode feature:

Current availability:
- Using 'System Default' provides schedule if OS has it configured
- macOS and Windows both support scheduled theme switching
- App respects your OS schedule when System Default is selected

Future roadmap:
- In-app dark mode scheduling is under consideration
- Vote on feature requests to help prioritize development
- Estimated timeline: TBD

Workaround:
- Configure your OS to switch themes on a schedule
- App will automatically follow when set to System Default"""
    }
]


def search_knowledge_base(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Search the knowledge base for relevant articles.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 3)
        
    Returns:
        List of matching articles sorted by relevance
    """
    query_lower = query.lower()
    results = []
    
    for article in KB_ARTICLES:
        score = 0
        
        # Keyword matches (highest priority)
        for keyword in article["keywords"]:
            if keyword in query_lower:
                score += 2
        
        # Title match (medium priority)
        if query_lower in article["title"].lower():
            score += 1
        
        # Content match (lowest priority)
        if query_lower in article["content"].lower():
            score += 0.5
        
        if score > 0:
            results.append({
                "id": article["id"],
                "title": article["title"],
                "content": article["content"],
                "relevance_score": score
            })
    
    # Sort by relevance and return top N
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:max_results]


def get_article(article_id: str) -> Dict[str, Any] | None:
    """
    Get a specific article by ID.
    
    Args:
        article_id: The article ID
        
    Returns:
        Article dict or None if not found
    """
    for article in KB_ARTICLES:
        if article["id"] == article_id:
            return article
    return None


def list_all_articles() -> List[Dict[str, str]]:
    """
    Get a list of all available articles (metadata only).
    
    Returns:
        List of articles with id, title, and keyword count
    """
    return [
        {
            "id": article["id"],
            "title": article["title"],
            "keywords_count": len(article["keywords"])
        }
        for article in KB_ARTICLES
    ]

