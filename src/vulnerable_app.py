#!/usr/bin/env python3
"""
Vulnerable Flask Application - For Educational Purposes Only
This application contains intentional security vulnerabilities.
"""

from flask import Flask, request, render_template_string
import os
import subprocess
import sqlite3
import yaml
import re

app = Flask(__name__)

# Vulnerability 1: Hardcoded credentials (Secret Detection will find this)
DATABASE_PASSWORD = "super_secret_password_123"
API_KEY = "sk-1234567890abcdef"

# Vulnerability 2: SQL Injection
def get_user(username):
    """Vulnerable to SQL injection attacks."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # BAD: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# Vulnerability 3: Command Injection
@app.route('/ping')
def ping():
    """Ping a host with basic input validation."""
    host = request.args.get('host', 'localhost')
    # Allow only simple hostname / IP-like characters to reduce injection risk
    if not re.fullmatch(r"[A-Za-z0-9\.\-:]+", host):
        return "Invalid host", 400
    # Use argument list and avoid shell=True to prevent command injection
    result = subprocess.check_output(["ping", "-c", "1", host])
    return result

# Vulnerability 4: Server-Side Template Injection (SSTI)
@app.route('/greet')
def greet():
    """Vulnerable to SSTI attacks."""
    name = request.args.get('name', 'Guest')
    # BAD: User input in template string
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)

# Vulnerability 5: Insecure Deserialization
@app.route('/load_config')
def load_config():
    """Vulnerable to YAML deserialization attacks."""
    config_data = request.args.get('config', '{}')
    # BAD: yaml.load without safe_load
    config = yaml.load(config_data, Loader=yaml.FullLoader)
    return str(config)

# Vulnerability 6: Path Traversal
@app.route('/read_file')
def read_file():
    """Vulnerable to path traversal attacks."""
    filename = request.args.get('file', 'default.txt')
    # BAD: No path validation
    with open(f"/app/files/{filename}", 'r') as f:
        return f.read()

if __name__ == '__main__':
    # Vulnerability 7: Debug mode in production
    app.run(host='0.0.0.0', port=5000, debug=True)
