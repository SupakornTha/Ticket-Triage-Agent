"""Sample support tickets for testing the triage agent."""

SAMPLE_TICKETS = [
    {
        "customer_id": "cust_001",
        "ticket_id": "TKT_001",
        "created_at": "2026-03-10T14:00:00Z",
        "messages": [
            {
                "time": "3 hours ago",
                "text": "My payment failed when I tried to upgrade to Pro. Can you check what's wrong?"
            },
            {
                "time": "2 hours ago",
                "text": "I tried again with a different card. Now I see TWO pending charges but my account still shows Free plan??"
            },
            {
                "time": "1 hour ago",
                "text": "Okay this is getting ridiculous. Just checked my bank app - I have THREE charges of $29.99 now. None of them refunded. And I STILL don't have Pro access."
            },
            {
                "time": "just now",
                "text": "HELLO?? Is anyone there??? I need this fixed NOW. I have a presentation in 2 hours and I need the Pro export features. If these charges aren't reversed by end of day I'm disputing all of them with my bank."
            }
        ]
    },
    {
        "customer_id": "cust_002",
        "ticket_id": "TKT_002",
        "created_at": "2026-03-10T12:00:00Z",
        "messages": [
            {
                "time": "2 hours ago",
                "text": "ระบบเข้าไม่ได้ครับ ขึ้น error 500"
            },
            {
                "time": "1.5 hours ago",
                "text": "ลองหลายเครื่องแล้ว ทั้ง Chrome, Safari, Firefox ผลเหมือนกันหมด เพื่อนร่วมงานก็เข้าไม่ได้เหมือนกัน"
            },
            {
                "time": "45 mins ago",
                "text": "ตอนนี้ลูกค้าโวยเข้ามาเยอะมาก เรามี demo กับลูกค้ารายใหญ่บ่ายนี้ ถ้าระบบไม่กลับมา deal นี้อาจจะหลุด"
            },
            {
                "time": "just now",
                "text": "เช็ค status.company.com แล้ว บอกว่า all systems operational แต่เราใช้งานไม่ได้จริงๆ ช่วยเช็คให้หน่อยได้ไหมครับ region Asia มีปัญหาหรือเปล่า?"
            }
        ]
    },
    {
        "customer_id": "cust_003",
        "ticket_id": "TKT_003",
        "created_at": "2026-03-08T10:00:00Z",
        "messages": [
            {
                "time": "2 days ago",
                "text": "Hey, just wondering if you support dark mode? No rush 😊"
            },
            {
                "time": "1 day ago",
                "text": "Thanks for the reply! Oh nice, so it's in Settings > Appearance. Found it! But hmm I'm on Pro plan and I only see 'Light' and 'System Default' options. No dark mode toggle?"
            },
            {
                "time": "1 day ago, 3 hours later",
                "text": "Okay so I switched to 'System Default' and my Mac is set to dark mode, but your app still shows light theme. Is this a bug or am I missing something?"
            },
            {
                "time": "today",
                "text": "Also random question while I have you - is there a way to schedule dark mode? Like auto-switch at 6pm? Some apps have that. Would be cool if you guys added it 👀"
            }
        ]
    }
]
