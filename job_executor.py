import json
from InstagramAPI import InstagramAPI


#443099971

class JobExecutor:
    def __init__(self):
        self.api = InstagramAPI("username", "password")
        self.comment_text = "#HBDSwiggy"
        self.api.login()

    def comment(self, post_id):
        print("Commenting...")
        self.api.comment(post_id, self.comment_text)
        return self.api.LastJson
        
    def process_jobs(self, post_ids):
        for post_id in post_ids:
            self.comment(post_id)
        return True
