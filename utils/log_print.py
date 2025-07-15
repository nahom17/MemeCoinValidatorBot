import os
from datetime import datetime

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
LOG_FILE = os.path.join(LOG_DIR, 'terminal_output.log')

os.makedirs(LOG_DIR, exist_ok=True)

def log_print(*args, **kwargs):
    # Convert all args to string and join with space
    message = ' '.join(str(arg) for arg in args)
    # Add timestamp
    timestamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    # Print to terminal
    print(timestamped, **kwargs)
    # Append to log file
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(timestamped + '\n')
    except Exception as e:
        print(f"[log_print error] {e}")