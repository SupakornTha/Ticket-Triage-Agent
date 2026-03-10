"""Validation script to verify project structure and imports."""

import sys
from pathlib import Path

def validate_project():
    """Validate project structure and imports."""
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}\n")
    
    # Check required files
    required_files = [
        "main.py",
        "README.md",
        "ARCHITECTURE.md",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "src/agent/triage_agent.py",
        "src/agent/prompts.py",
        "src/tools/knowledge_base.py",
        "src/tools/customer_history.py",
        "data/sample_tickets.py"
    ]
    
    print("✓ Checking required files...")
    missing_files = []
    for file in required_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n✗ Missing files: {missing_files}")
        return False
    
    print("\n✓ Checking imports...")
    # Try importing modules
    try:
        sys.path.insert(0, str(project_root))
        from src.tools.knowledge_base import search_knowledge_base
        print("  ✓ knowledge_base module imports correctly")
        
        from src.tools.customer_history import get_customer_history
        print("  ✓ customer_history module imports correctly")
        
        from src.agent.prompts import SYSTEM_PROMPT
        print("  ✓ prompts module imports correctly")
        
        from data.sample_tickets import SAMPLE_TICKETS
        print(f"  ✓ sample_tickets module imports correctly ({len(SAMPLE_TICKETS)} tickets)")
        
        # Don't import triage_agent yet since it requires OpenAI
        print("  ℹ triage_agent requires OpenAI API key (skipped for now)")
        
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False
    
    print("\n✓ Testing tools...")
    # Test knowledge base search
    results = search_knowledge_base("payment failed")
    print(f"  ✓ knowledge_base search returns {len(results)} results")
    
    # Test customer history lookup
    customer = get_customer_history("cust_001")
    print(f"  ✓ customer_history lookup works (plan: {customer.get('plan')})")
    
    # Test sample tickets
    print(f"  ✓ {len(SAMPLE_TICKETS)} sample tickets available")
    
    print("\n" + "="*50)
    print("✓ All validation checks passed!")
    print("="*50)
    print("\nNext steps:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='sk-...'")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the agent: python main.py")
    
    return True

if __name__ == "__main__":
    success = validate_project()
    sys.exit(0 if success else 1)
