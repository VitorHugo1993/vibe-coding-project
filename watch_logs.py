#!/usr/bin/env python3
"""
Simple log viewer for API requests
Watches the api_requests.log file and displays new entries in real-time
"""

import os
import time
import sys

LOG_FILE = "api_requests.log"
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'gray': '\033[90m',
}

def colorize(text, color):
    """Add color to text"""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"

def format_log_line(line):
    """Format and colorize log lines"""
    if '➡️' in line:
        # Request line
        parts = line.split(' - ')
        if len(parts) >= 3:
            timestamp = colorize(parts[0], 'gray')
            arrow = colorize('➡️', 'green')
            message = parts[2].replace('➡️', arrow)
            
            # Colorize method
            if 'GET' in message:
                message = message.replace('GET', colorize('GET', 'cyan'))
            elif 'POST' in message:
                message = message.replace('POST', colorize('POST', 'green'))
            elif 'PUT' in message:
                message = message.replace('PUT', colorize('PUT', 'yellow'))
            elif 'DELETE' in message:
                message = message.replace('DELETE', colorize('DELETE', 'red'))
            
            # Colorize role
            if 'Role:' in message:
                role_parts = message.split('Role:')
                role = role_parts[1].strip()
                message = role_parts[0] + 'Role: ' + colorize(role, 'magenta')
            
            return f"{timestamp} - {message}"
    
    elif '⬅️' in line:
        # Response line
        parts = line.split(' - ')
        if len(parts) >= 3:
            timestamp = colorize(parts[0], 'gray')
            arrow = colorize('⬅️', 'blue')
            message = parts[2].replace('⬅️', arrow)
            
            # Colorize status
            if 'Status: 200' in message or 'Status: 201' in message:
                message = message.replace('Status:', colorize('Status:', 'green'))
            elif 'Status: 4' in message:
                message = message.replace('Status:', colorize('Status:', 'yellow'))
            elif 'Status: 5' in message:
                message = message.replace('Status:', colorize('Status:', 'red'))
            
            # Colorize duration
            if 'Duration:' in message:
                dur_parts = message.split('Duration:')
                message = dur_parts[0] + colorize('Duration:', 'cyan') + dur_parts[1]
            
            return f"{timestamp} - {message}"
    
    return line

def print_header():
    """Print header"""
    print("\n" + "="*80)
    print(colorize("🔍 Nezasa Connect API - Request Monitor", 'bold'))
    print(colorize(f"📁 Watching: {LOG_FILE}", 'gray'))
    print("="*80 + "\n")
    print(colorize("Press Ctrl+C to exit\n", 'gray'))

def tail_file(filename):
    """Tail a file and yield new lines as they appear"""
    with open(filename, 'r') as f:
        # Go to the end of the file
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if line:
                yield line.strip()
            else:
                time.sleep(0.1)

def watch_existing_logs():
    """Display existing logs"""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                lines = f.readlines()
                if lines:
                    print(colorize("📋 Existing logs:", 'yellow'))
                    print("-" * 80)
                    for line in lines[-20:]:  # Show last 20 lines
                        print(format_log_line(line.strip()))
                    print("-" * 80 + "\n")
                    print(colorize("🔄 Watching for new requests...\n", 'green'))
                else:
                    print(colorize("📭 No logs yet. Waiting for API requests...\n", 'yellow'))
        except Exception as e:
            print(colorize(f"⚠️  Error reading log file: {e}", 'red'))
    else:
        print(colorize(f"⚠️  Log file not found: {LOG_FILE}", 'red'))
        print(colorize("💡 Make sure the API server is running\n", 'yellow'))

def main():
    """Main function"""
    try:
        print_header()
        watch_existing_logs()
        
        # Watch for new logs
        if os.path.exists(LOG_FILE):
            for line in tail_file(LOG_FILE):
                print(format_log_line(line))
                sys.stdout.flush()
    except KeyboardInterrupt:
        print(colorize("\n\n✋ Stopped watching logs. Goodbye!", 'yellow'))
        sys.exit(0)
    except Exception as e:
        print(colorize(f"\n❌ Error: {e}", 'red'))
        sys.exit(1)

if __name__ == "__main__":
    main()

