"""Main ticket triage agent using OpenAI GPT."""

import json
import os
from typing import Any, Dict, Optional
from openai import OpenAI
from src.agent.prompts import SYSTEM_PROMPT
from src.tools.knowledge_base import search_knowledge_base
from src.tools.customer_history import get_customer_history, get_account_status


class TicketTriageAgent:
    """Agent that triages support tickets using GPT and tools."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the triage agent.
        
        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Using GPT-4o mini for better reasoning and cost efficiency
        
    def _build_tool_instructions(self) -> str:
        """Build instructions for available tools."""
        return """

You have access to the following tools to help with triage:

1. search_knowledge_base(query: str) -> List[Dict]
   - Search our knowledge base for relevant documentation
   - Returns matching articles with content
   - Use when you need to check if there's an existing solution
   
2. get_customer_history(customer_id: str) -> Dict
   - Look up customer account and history information
   - Returns plan, tenure, payment status, urgency flags
   - Use to understand customer profile and context

IMPORTANT: When you need to use a tool, format it exactly like this:
<tool_call>
{"name": "search_knowledge_base", "arguments": {"query": "payment failed"}}
</tool_call>

or

<tool_call>
{"name": "get_customer_history", "arguments": {"customer_id": "cust_001"}}
</tool_call>

Always use tools when:
- You need to search for solutions to reported issues
- You need customer context (plan, history, flags)
- The issue type makes a tool lookup relevant

After getting tool results, incorporate them into your analysis.
"""

    def _parse_tool_calls(self, text: str) -> list[Dict[str, Any]]:
        """Parse tool calls from agent response."""
        tool_calls = []
        import re
        
        # Find all <tool_call> blocks
        pattern = r'<tool_call>\s*({.*?})\s*</tool_call>'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                tool_call = json.loads(match)
                tool_calls.append(tool_call)
            except json.JSONDecodeError:
                pass
        
        return tool_calls
    
    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool and return the result."""
        if tool_name == "search_knowledge_base":
            query = arguments.get("query", "")
            return search_knowledge_base(query)
        
        elif tool_name == "get_customer_history":
            customer_id = arguments.get("customer_id", "")
            return get_customer_history(customer_id)
        
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def triage_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Triage a support ticket using GPT and tools.
        
        Args:
            ticket: Dictionary containing:
                - customer_id: The customer ID
                - messages: List of messages from the ticket
                - timestamp: When the ticket was created
                
        Returns:
            Triage result with classification and routing decision
        """
        customer_id = ticket.get("customer_id")
        messages = ticket.get("messages", [])
        
        # Format the ticket for the agent
        ticket_content = "\n".join([f"[{msg.get('time', 'Unknown')}] {msg.get('text', '')}" 
                                   for msg in messages])
        
        user_message = f"""Please triage this customer support ticket:

Customer ID: {customer_id}

Ticket Messages:
{ticket_content}

Analyze the ticket:
1. Use get_customer_history to look up the customer's details
2. Use search_knowledge_base to find relevant solutions
3. Classify the urgency and issue type
4. Decide on the appropriate action
5. Provide specific reasoning and next steps

Return your analysis as a JSON object."""
        
        tool_instructions = self._build_tool_instructions()
        
        # First API call with tools
        messages_list = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT + tool_instructions
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        # Make first request
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=2000,
            messages=messages_list
        )
        
        assistant_message = response.choices[0].message.content
        
        # Parse and execute tool calls
        tool_calls = self._parse_tool_calls(assistant_message)
        tool_results = []
        
        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            arguments = tool_call.get("arguments", {})
            result = self._execute_tool(tool_name, arguments)
            tool_results.append({
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            })
        
        # If tools were used, make a follow-up request with tool results
        if tool_results:
            messages_list.append({"role": "assistant", "content": assistant_message})
            
            tool_results_text = "\n".join([
                f"Tool: {tr['tool']}\nArguments: {json.dumps(tr['arguments'])}\nResult:\n{json.dumps(tr['result'], indent=2)}"
                for tr in tool_results
            ])
            
            messages_list.append({
                "role": "user",
                "content": f"""Tool results:

{tool_results_text}

Now provide your final triage decision as a JSON object with these fields:
{{
  "urgency": "critical|high|medium|low",
  "issue_type": "string",
  "customer_sentiment": "positive|neutral|negative|angry",
  "action": "auto_respond|escalate_specialist|escalate_urgent|hold",
  "summary": "brief summary",
  "reasoning": "explanation",
  "suggested_response": "if auto_respond",
  "specialist_notes": "context for human agent"
}}"""
            })
            
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=2000,
                messages=messages_list
            )
            
            final_message = response.choices[0].message.content
        else:
            final_message = assistant_message
        
        # Extract JSON from the response
        try:
            # Find JSON in the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', final_message)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {
                    "error": "Could not parse agent response",
                    "raw_response": final_message
                }
        except json.JSONDecodeError:
            result = {
                "error": "Invalid JSON in agent response",
                "raw_response": final_message
            }
        
        # Add metadata
        result["customer_id"] = customer_id
        result["tool_results"] = tool_results
        
        return result
