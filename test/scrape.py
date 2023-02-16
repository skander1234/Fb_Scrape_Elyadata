import time
import requests
from facebook_scraper import get_posts


time.sleep(1)

posts=get_posts("SortedFood", pages=3)    
i=0
for post in posts:      
    i+=1
assert(i==4)
print("Scrapping done") 

