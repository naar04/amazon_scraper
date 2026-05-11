import os
import json
import requests

def post_to_facebook():
    # Get token from GitHub Secrets
    page_id = os.environ["FB_PAGE_ID"]
    access_token = os.environ["FB_ACCESS_TOKEN"]
    
    with open("latest_deals.json", "r") as f:
        deals = json.load(f)

    for deal in deals:
        message = f"🔥 DEAL ALERT! ⭐ {deal['rating']} Stars\n\n{deal['title']}\n\nCheck it out here: {deal['link']}"
        url = f"https://graph.facebook.com/{page_id}/feed"
        payload = {
            'message': message,
            'access_token': access_token
        }
        r = requests.post(url, data=payload)
        print(f"Posted {deal['title']}: {r.status_code}")

if __name__ == "__main__":
    post_to_facebook()
