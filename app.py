from flask import Flask, request, render_template, redirect, url_for, session, Response
import re
import sqlite3
from datetime import datetime
from groq import Groq  
import io   
import csv  

app = Flask(__name__)

# --- SECURITY CONFIGURATION ---
# The secret key is required by Flask to encrypt the user's browser session
app.secret_key = "super_secret_enterprise_key_change_in_production"

# Hardcoded admin credentials for the prototype
ADMIN_USER = "admin"
ADMIN_PASS = "secure123"

# --- DATABASE SETUP (The Vault) ---
def init_db():
    conn = sqlite3.connect('security_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS intercepts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  raw_input TEXT,
                  sanitized_output TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- THE REAL AI CONNECTION ---
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

def ask_real_ai(safe_prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful corporate AI assistant. Answer queries professionally."},
                {"role": "user", "content": safe_prompt}
            ],
            model="llama-3.1-8b-instant", 
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"AI Connection Error: {str(e)}"

# --- 1. THE SECURE DLP ENGINE ---
def sanitize_data(text):
    # 1. Hide Emails
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    safe_text = re.sub(email_pattern, '[REDACTED_EMAIL]', text)
    
    # 2. Hide Credit Cards
    cc_pattern = r'\b\d{16}\b|\b\d{4}-\d{4}-\d{4}-\d{4}\b'
    safe_text = re.sub(cc_pattern, '[REDACTED_CREDIT_CARD]', safe_text)
    
    # 3. Hide Passwords
    password_pattern = r'(?i)(password\s*(?:is|:|=)\s*)(\S+)'
    safe_text = re.sub(password_pattern, r'\1[REDACTED_PASSWORD]', safe_text)

    # 4. Hide Custom SAP IDs
    sap_pattern = r'(?i)(sap id\s*(?:is|:|=)?\s*)(\d+)'
    safe_text = re.sub(sap_pattern, r'\1[REDACTED_UPES_ID]', safe_text)
    
    # 5. Hide AWS Access Keys
    aws_pattern = r'(?i)(AKIA[0-9A-Z]{16})'
    safe_text = re.sub(aws_pattern, '[REDACTED_AWS_KEY]', safe_text)
    
    return safe_text

# --- 2. THE FRONT DOOR ---
@app.route('/')
def home():
    return render_template('index.html')

# --- 3. THE INTERCEPT ZONE (FULLY CONNECTED TO AI) ---
@app.route('/intercept', methods=['POST'])
def catch_message():
    raw_text = ""
    is_file = False
    
    # Grab the question the user typed in the chat box
    user_question = request.form.get('employee_prompt', '')
    if user_question.strip() == '':
        user_question = "Please summarize this document."
    
    # Check if a file was uploaded
    if 'secure_file' in request.files and request.files['secure_file'].filename != '':
        file = request.files['secure_file']
        raw_file_text = file.read().decode('utf-8')
        raw_text = raw_file_text
        is_file = True
    else:
        raw_text = user_question

    # Scrub the data clean (Regex Engine)
    clean_text = sanitize_data(raw_text)
    
    # Talk to the REAL AI
    if is_file:
        # If it's a file, we combine the user's question with the clean file text
        combined_prompt = f"{user_question}\n\n--- FILE DATA ---\n{clean_text}"
        ai_reply = ask_real_ai(combined_prompt)
    else:
        # If it's just a normal chat message, just send the clean text
        ai_reply = ask_real_ai(clean_text)
    
    # Log it to the Vault
    conn = sqlite3.connect('security_logs.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_danger = f"[FILE UPLOAD] {raw_text[:100]}..." if is_file else raw_text
    log_safe = f"[SANITIZED FILE] {clean_text[:100]}..." if is_file else clean_text
    
    c.execute("INSERT INTO intercepts (timestamp, raw_input, sanitized_output) VALUES (?, ?, ?)", 
              (timestamp, log_danger, log_safe))
    conn.commit()
    conn.close()
    
    return render_template('index.html', ai_response=ai_reply)

# --- 4. THE LOGIN GATEWAY ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            session['logged_in'] = True  
            return redirect(url_for('admin_dashboard')) 
        else:
            return render_template('login.html', error="INVALID CREDENTIALS DETECTED")
            
    return render_template('login.html')

# --- 5. THE LOGOUT ROUTE ---
@app.route('/logout')
def logout():
    session.pop('logged_in', None) 
    return redirect(url_for('home'))

# --- 6. THE SECRET ADMIN DASHBOARD (NOW LOCKED) ---
@app.route('/admin')
def admin_dashboard():
    # If they don't have the VIP wristband, kick them to the login page
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('security_logs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM intercepts ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    
    return render_template('admin.html', audit_logs=logs)

# --- 7. THE LOG EXPORTER (CSV REPORTING) ---
@app.route('/export')
def export_logs():
    # Only let them download if they are logged in!
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('security_logs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM intercepts ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Event ID', 'Timestamp', 'Original Payload', 'Sanitized Output'])
    
    for log in logs:
        writer.writerow([f"EVT-{log[0]}", log[1], log[2], log[3]])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=dlp_audit_logs.csv"}
    )

if __name__ == '__main__':
    app.run(port=5000)