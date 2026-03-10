"""Knowledge base search tool for the triage agent.

This module provides article search and retrieval for the triage agent.
Articles are structured with id, title, keywords, and content.

Structure of each article:
    {
        "id": "unique_identifier",
        "title": "Article Title",
        "keywords": ["keyword1", "keyword2"],
        "content": "Article content..."
    }

To add new articles, append to KB_ARTICLES list with the above structure.
"""

from typing import Dict, List, Any, TypedDict, Optional


# ============================================================================
# Type Definitions
# ============================================================================

class KBArticle(TypedDict):
    """Type definition for knowledge base articles."""
    id: str
    title: str
    keywords: List[str]
    content: str


class SearchResult(TypedDict):
    """Type definition for search results."""
    id: str
    title: str
    content: str
    relevance_score: float


# ============================================================================
# Search Configuration
# ============================================================================

# Scoring weights for different match types
KEYWORD_MATCH_WEIGHT = 2.0      # Highest priority: exact keyword match
TITLE_MATCH_WEIGHT = 1.0        # Medium priority: title contains query
CONTENT_MATCH_WEIGHT = 0.5      # Lowest priority: content contains query

# Default number of search results to return
DEFAULT_MAX_RESULTS = 3


# ============================================================================
# Knowledge Base Articles
# ============================================================================

KB_ARTICLES: List[KBArticle] = [
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


def search_knowledge_base(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> List[SearchResult]:
    """
    Search the knowledge base for articles matching the query.
    
    Uses relevance scoring to rank results by match type:
    - Keyword matches (weight: 2.0) - highest priority
    - Title matches (weight: 1.0) - medium priority  
    - Content matches (weight: 0.5) - lowest priority
    
    Args:
        query: Search query string. Case-insensitive.
        max_results: Maximum number of results to return (default: 3)
        
    Returns:
        List of matching articles sorted by relevance_score (highest first).
        Each result includes id, title, content, and relevance_score.
        Returns empty list if no matches found.
        
    Example:
        >>> results = search_knowledge_base("payment failed")
        >>> for article in results:
        ...     print(f"{article['title']} (score: {article['relevance_score']})")
    """
    if not query or not query.strip():
        return []
    
    query_lower = query.lower().strip()
    results: List[SearchResult] = []
    
    for article in KB_ARTICLES:
        score = _calculate_relevance_score(query_lower, article)
        
        if score > 0:
            search_result: SearchResult = {
                "id": article["id"],
                "title": article["title"],
                "content": article["content"],
                "relevance_score": score
            }
            results.append(search_result)
    
    # Sort by relevance (highest score first) and return top N results
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:max_results]


def _calculate_relevance_score(query_lower: str, article: KBArticle) -> float:
    """
    Calculate relevance score for an article based on query match.
    
    Scoring breakdown:
    - Each keyword match: +2.0
    - Title match: +1.0
    - Content match: +0.5
    
    Args:
        query_lower: Lowercase query string
        article: Knowledge base article to score
        
    Returns:
        Total relevance score (0 if no matches)
    """
    score = 0.0
    
    # Keyword matches (highest priority)
    for keyword in article["keywords"]:
        if keyword in query_lower:
            score += KEYWORD_MATCH_WEIGHT
    
    # Title match (medium priority)
    if query_lower in article["title"].lower():
        score += TITLE_MATCH_WEIGHT
    
    # Content match (lowest priority)
    if query_lower in article["content"].lower():
        score += CONTENT_MATCH_WEIGHT
    
    return score


def get_article(article_id: str) -> Optional[KBArticle]:
    """
    Retrieve a specific article by its ID.
    
    Args:
        article_id: Unique identifier of the article
        
    Returns:
        Article dictionary if found, None otherwise
        
    Example:
        >>> article = get_article("billing_failed_payment")
        >>> if article:
        ...     print(article["title"])
    """
    if not article_id:
        return None
    
    for article in KB_ARTICLES:
        if article["id"] == article_id:
            return article
    
    return None


def list_all_articles() -> List[Dict[str, Any]]:
    """
    Get a list of all available articles (metadata only).
    
    Useful for displaying available articles or checking article inventory.
    
    Returns:
        List of dictionaries with: id, title, keywords_count
        
    Example:
        >>> articles = list_all_articles()
        >>> print(f"Total articles: {len(articles)}")
        >>> for article in articles:
        ...     print(f"  - {article['title']} ({article['keywords_count']} keywords)")
    """
    return [
        {
            "id": article["id"],
            "title": article["title"],
            "keywords_count": len(article["keywords"])
        }
        for article in KB_ARTICLES
    ]

