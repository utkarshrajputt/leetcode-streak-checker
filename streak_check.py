import requests
import os
import random
from datetime import datetime
from zoneinfo import ZoneInfo

username = os.environ['LEETCODE_USERNAME']
chat_id = os.environ['CHAT_ID']
token = os.environ['TELEGRAM_TOKEN']

TELEGRAM_API_URL = f"https://api.telegram.org/bot{token}/sendMessage"

success_messages = [
    "✅ Beast mode active. You’ve submitted today. Keep the streak alive! 🔥",
    "🧠 Brains > excuses. You're winning this grind.",
    "📈 Daily effort = future flex. Keep going!",
    "🚀 Streak is intact, captain. Onwards to greatness!",
    "🔥 Submission detected. Consistency is sexy.",
    "👊 You're in the 1% who showed up. Respect!"
]

warning_message = "⚠️ Utkarsh! You haven’t submitted on LeetCode today. Clock’s ticking! ⏰🔥"

def has_submitted_today(username):
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/{username}/",
        "User-Agent": "Mozilla/5.0"
    }

    query = """
    query recentSubmissionList($username: String!) {
      recentSubmissionList(username: $username, limit: 5) {
        timestamp
        statusDisplay
        title
      }
    }
    """

    payload = {
        "query": query,
        "variables": {"username": username}
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print("❌ Failed to fetch data from LeetCode GraphQL.")
        return False

    submissions = response.json()["data"]["recentSubmissionList"]
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()

    for sub in submissions:
        try:
            sub_time = datetime.fromtimestamp(int(sub["timestamp"]), ZoneInfo("Asia/Kolkata")).date()
            if sub_time == today:
                return True
        except Exception as e:
            print(f"⚠️ Failed to parse submission timestamp: {e}")

    return False


def send_telegram_message(message):
    try:
        requests.post(TELEGRAM_API_URL, data={"chat_id": chat_id, "text": message})
    except Exception as e:
        print(f"❌ Telegram send error: {e}")

# Main logic
if has_submitted_today(username):
    send_telegram_message(random.choice(success_messages))
else:
    send_telegram_message(warning_message)
# Log the current date and time for debugging
print(f"Checked streak for {username} on {datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')}")
# This will help in tracking when the script was last run