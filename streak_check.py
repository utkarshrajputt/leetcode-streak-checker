import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

username = os.environ['LEETCODE_USERNAME']
chat_id = os.environ['CHAT_ID']
token = os.environ['TELEGRAM_TOKEN']

def has_submitted_today(username):
    url = f"https://leetcode-stats-api.herokuapp.com/{username}"
    r = requests.get(url)
    if r.status_code != 200:
        return False

    data = r.json()
    last_submission_time = data.get('lastSubmission', None)
    if not last_submission_time:
        return False

    utc_now = datetime.now(ZoneInfo("UTC")).date()
    submitted_date = datetime.strptime(last_submission_time, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    return submitted_date == utc_now

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

if not has_submitted_today(username):
    send_telegram_message("⚠️ Utkarsh! You haven’t submitted on LeetCode today. Clock’s ticking! ⏰🔥")
else:
    print("✅ You’ve already submitted today. No alert needed.")
