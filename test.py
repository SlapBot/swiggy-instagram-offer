import time
import json
import requests
from bs4 import BeautifulSoup
from job_executor import JobExecutor


headers = {
    'Connection': 'close', 
    'Accept': '*/*', 
    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 
    'Cookie2': '$Version=1', 
    'Accept-Language': 'en-US', 
    'User-Agent': 'Instagram 10.26.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'
}

je = JobExecutor()

def get_posts():    
    r = requests.get("https://www.instagram.com/swiggyindia/", headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    raw_data = soup.find_all("script")[4].text
    data = json.loads(raw_data[21:len(raw_data)-1])

    posts = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
    return posts


first_posts = get_posts()
latest_post_id = first_posts[0]['node']['id']

info_data = {
    'id': latest_post_id
}

def process_jobs(new_posts):
    je.process_jobs(new_posts)

print("Latest Post Id: %s" % latest_post_id)
# Now starts polling.

while(True):
    print("Polling...")
    new_posts = []
    posts = get_posts()
    print("Checking for new post...")
    for i in range(0, len(posts)):
        post_id = posts[i]['node']['id']
        if post_id == latest_post_id:
            print("No new post found...")
            break
        else:
            print("New post found! with id: %s" % post_id)
            new_posts.append(post_id)
    if len(new_posts) > 0:
        print("Processing jobs...")
        process_jobs(new_posts)
        latest_post_id = new_posts[0]
        new_posts = []
        print("All jobs processed.")
    print("Waiting to poll again...")
    # time.sleep(1)
