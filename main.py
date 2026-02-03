"""Entry point for Railway deployment.

This script adds the src directory to Python's path and runs the remote server.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Now import and run the remote server
from linkup_company_research.remote import main

if __name__ == "__main__":
    main()
