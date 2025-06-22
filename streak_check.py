import requests
import os
import random
from datetime import datetime
from zoneinfo import ZoneInfo

# Load environment variables
username = os.environ['LEETCODE_USERNAME']
chat_id = os.environ['CHAT_ID']
token = os.environ['TELEGRAM_TOKEN']

# Telegram API URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{token}/sendMessage"

# Motivational messages
success_messages = [
    "✅ Beast mode active. You’ve submitted today. Keep the streak alive! 🔥",
    "🧠 Brains > excuses. You're winning this grind.",
    "📈 Daily effort = future flex. Keep going!",
    "🚀 Streak is intact, captain. Onwards to greatness!",
    "🔥 Submission detected. Consistency is sexy.",
    "👊 You're in the 1% who showed up. Respect!"
]

# Warning message
warning_message = "⚠️ Utkarsh! You haven’t submitted on LeetCode today. Clock’s ticking! ⏰🔥"

# Function to check if today's submission is made
def has_submitted_today(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        return False

    data = response.json()
    last_submission_time = data.get('lastSubmission', None)
    if not last_submission_time:
        return False

    # Parse and compare dates
    utc_now = datetime.now(ZoneInfo("UTC")).date()
    submitted_date = datetime.strptime(last_submission_time, "%Y-%m-%dT%H:%M:%S.%fZ").date()

    return submitted_date == utc_now

# Function to send message via Telegram
def send_telegram_message(message):
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(TELEGRAM_API_URL, data=payload)
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")

# Main logic
if has_submitted_today(username):
    send_telegram_message(random.choice(success_messages))
else:
    send_telegram_message(warning_message)
