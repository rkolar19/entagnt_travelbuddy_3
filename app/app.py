import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- CONFIGURATION ---
# We use environment variables so your team doesn't leak IDs in Git.
# Defaults are set to your current project 'mydummy-1'
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "mydummy-1")
AGENT_ID = os.getenv("GCP_AGENT_ID", "4a387c16-bb1a-499b-ae2c-ccf83627c39b")
LOCATION = os.getenv("GCP_LOCATION", "global")

# --- HTML TEMPLATE ---
# This is the "Face" of your agent. 
# It includes the df-messenger v1 library and the chat bubble.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel Buddy | Enterprise Agent</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .welcome-card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; max-width: 400px; }
        h1 { color: #1a73e8; }
        p { color: #5f6368; line-height: 1.5; }
    </style>
</head>
<body>
    <div class="welcome-card">
        <h1>Travel Buddy 3.0</h1>
        <p>Your AI-powered travel consultant is ready. Click the bubble on the bottom right to begin your journey.</p>
    </div>

    <script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>
    <df-messenger
      project-id="{{ project_id }}"
      agent-id="{{ agent_id }}"
      location="{{ location }}"
      language-code="en">
      <df-messenger-chat-bubble 
        chat-title="Travel Buddy 3"
        chat-icon="https://www.gstatic.com/images/icons/material/system/2x/flight_takeoff_black_24dp.png">
      </df-messenger-chat-bubble>
    </df-messenger>
</body>
</html>
"""

@app.route('/')
def home():
    """Renders the main agent interface."""
    return render_template_string(
        HTML_TEMPLATE, 
        project_id=PROJECT_ID, 
        agent_id=AGENT_ID,
        location=LOCATION
    )

@app.route('/healthz')
def health_check():
    """Required for Cloud Run/GKE to ensure the container is running."""
    return "OK", 200

if __name__ == "__main__":
    # Local port 8080 is standard for Google Cloud Run compatibility
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
