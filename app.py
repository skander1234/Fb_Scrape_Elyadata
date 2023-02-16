from fastapi import FastAPI
from typing import Optional
import requests
from pymongo import MongoClient
from facebook_scraper import get_posts

app = FastAPI()

@app.get("/")
def read_root():
    try:
        client = MongoClient("mongodb://mongoadmin:secret@mongodb")
        db = client.posts
        db.testdbb.insert_one({ "Welcome message": "Welcome to root directory" })
    except:
        return {"Error": "Unable to connect to MongoDB server"}
    return {"Hello message": "Welcome to root directory Elyadata"}

@app.get("/page/{page_id}")
def read_itemm(page_id: str, q: Optional[int] = 1):
    try:
        r = requests.get("https://www.facebook.com/"+page_id)
        client = MongoClient("mongodb://mongoadmin:secret@mongodb")
        db = client.posts
        if str(r) == '<Response [200]>':
            titles = []
            posts = get_posts(page_id, pages=q)
            for post in posts:
                see = db.testdbb.count_documents({'post_id': post['post_id']})
                print(see)
                titles.append(post['text'][:50])
                if see == 1:
                    continue
                else:
                    t = post
                    t['pageid'] = page_id
                    print(t)
                    db.testdbb.insert_one(post)
            return {"You are looking for this page's content": page_id, "Here are the last titles": titles}
        else:
            return {"page_id": "Sorry, but '"+page_id+"' is not a valid facebook page, please make sure that the facebook page is still available and that it is public as the server wasn't able to get a valid response from the facebook page"}
    except:
        return {"Error": "An unexpected error occurred while processing your request."}
