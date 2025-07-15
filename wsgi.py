#!/usr/bin/env python3
"""
WSGI entry point for hosting deployment
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the Flask app
from dashboard.app import app

# Configure for production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['DEBUG'] = False

if __name__ == "__main__":
    app.run()