"""Customer history lookup tool for the triage agent."""

from typing import Dict, Any, Optional

# Mock customer database
CUSTOMER_DATABASE = {
    "cust_001": {  # Ticket 1 customer
        "customer_id": "cust_001",
        "plan": "free",
        "tenure_months": 4,
        "region": "US",
        "language": "en",
        "account_status": "active",
        "previous_tickets": 0,
        "last_ticket": None,
        "payment_method": "card",
        "pending_charges": 3,
        "charges": [
            {"amount": 29.99, "date": "2026-03-10", "status": "pending", "card_last4": "4242"},
            {"amount": 29.99, "date": "2026-03-10", "status": "pending", "card_last4": "4242"},
            {"amount": 29.99, "date": "2026-03-10", "status": "pending", "card_last4": "4242"},
        ],
        "urgency_flags": ["billing_issue", "new_customer", "escalating_tone", "time_critical"],
        "notes": "First-time paying customer, multiple failed upgrade attempts"
    },
    "cust_002": {  # Ticket 2 customer
        "customer_id": "cust_002",
        "plan": "enterprise",
        "seats": 45,
        "tenure_months": 8,
        "region": "Asia",
        "language": "th",
        "account_status": "active",
        "company_size": "large",
        "previous_tickets": 0,
        "payment_status": "current",
        "sla_tier": "24/7_with_1h_response",
        "urgency_flags": ["system_outage", "enterprise_customer", "revenue_impact", "critical"],
        "demo_scheduled": "2026-03-10T14:00:00",
        "notes": "First critical issue, high-value customer with demo impact"
    },
    "cust_003": {  # Ticket 3 customer
        "customer_id": "cust_003",
        "plan": "pro",
        "tenure_months": 5,
        "region": "US",
        "language": "en",
        "account_status": "active",
        "engagement": "high",  # Daily logins
        "previous_tickets": 0,
        "last_login": "2026-03-10T09:00:00",
        "payment_status": "current",
        "urgency_flags": ["feature_request", "engaged_user"],
        "notes": "Active user, asking about features, positive tone"
    }
}


def get_customer_history(customer_id: str) -> Optional[Dict[str, Any]]:
    """
    Look up customer history and account information.
    
    Args:
        customer_id: The unique customer identifier
        
    Returns:
        Customer history and account details, or None if not found
    """
    if customer_id not in CUSTOMER_DATABASE:
        return {
            "error": f"Customer {customer_id} not found",
            "customer_id": customer_id,
            "default_handling": "treat as new customer with caution"
        }
    
    customer = CUSTOMER_DATABASE[customer_id]
    return {
        "customer_id": customer.get("customer_id"),
        "plan": customer.get("plan"),
        "tenure_months": customer.get("tenure_months"),
        "region": customer.get("region"),
        "language": customer.get("language"),
        "account_status": customer.get("account_status"),
        "payment_status": customer.get("payment_status"),
        "sla_tier": customer.get("sla_tier"),
        "previous_tickets": customer.get("previous_tickets"),
        "engagement_level": customer.get("engagement", "standard"),
        "company_size": customer.get("company_size"),
        "seats": customer.get("seats"),
        "pending_charges": customer.get("pending_charges"),
        "charges": customer.get("charges", []),
        "urgency_flags": customer.get("urgency_flags", []),
        "notes": customer.get("notes")
    }


def get_account_status(customer_id: str) -> Dict[str, Any]:
    """Get quick account status snapshot."""
    customer = CUSTOMER_DATABASE.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}
    
    return {
        "customer_id": customer_id,
        "plan": customer.get("plan"),
        "account_status": customer.get("account_status"),
        "payment_status": customer.get("payment_status"),
        "pending_charges": customer.get("pending_charges", 0),
        "tenure_months": customer.get("tenure_months")
    }
