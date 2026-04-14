from datetime import datetime
import time
import os
import requests
import json

DEBUG=True

def log(message):
    if DEBUG:
        print(message)


response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")

top_stories_list = response.json()

top_stories_count = len(top_stories_list)

# I am only going to retain 500 stories if we fetched more than 500
if top_stories_count > 500:
    log(f"Obtained {top_stories_count} stories. Retaining only the top 500 ...")
    top_stories_json = top_stories_list[:500]
elif top_stories_count == 0:
    log(f"Obtained zero stories from the api end point !!!")
else:
    log(f"Successfully obtained {top_stories_count} stories from the api endpoint.")


# This dictionary has id -> story mapping and has all the details of the stories.
stories = {}
headers = {"User-Agent": "TrendPulse/1.0"}

successful_count = 0
failed_count  = 0

log(f"Fetching the story details for each obtained id: \n")
for id in top_stories_list:
    try:
        response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json", headers=headers)
    except Exception as e:
        # log(f"Error: Unable to fetch details for story with id: {id}")
        failed_count += 1
    else:
        successful_count += 1
        # log(f"Successfully got the response for story with id: {id}")
        story_dict = response.json()
        stories[id] = story_dict
    

    # Carriage Return (\r) sets the cursor at the beginning of the line
    # I am then Erasing the current line by printing 100 spaces.
    print("\r" + " " * 100, end="")
    print(f"\rStatus: Successful Requests: {successful_count}, Failed Requests: {failed_count}, Total Requests: {successful_count+failed_count}", end="")

print("")
log(f"Successfully fetched {successful_count} stories.")
log(f"Failed to fetch {failed_count} stories.")



categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# This represens the count of all stories that are categorized
total_count = 0 

# This is a dict with category -> story_list mapping. Each story in story_list is a dictionary.
stories_by_category = {} 

# This is a dict with id -> story mapping.
unclassified_stories = {}
for category, keywords in categories.items():
    log(f"Searching for stories belonging to {category} category")

    count = 0
    stories_by_category[category] = []
    for id,story in stories.items():
        title = story.get("title").lower()

        story_dict = {  
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score"),
            "num_comments": story.get("descendants"),
            "author": story.get("by"),
            "collected_at": datetime.now()
        }

        matched = False
        for keyword in keywords:
            if keyword.lower() in title:
                matched = True
                break
        
        # I am only adding it to the category list if it has less than 25 stories.
        # This is mentioned in the instructions: Collect up to 25 stories per category (125 total).
        if matched and len(stories_by_category[category]) < 25:
            count += 1
            stories_by_category[category].append(story_dict)
        else:
            unclassified_stories[story.get("id")] = story

    total_count+= count
    log(f"{count} stories matched the category {category}\n")
    # log("Sleeping for 5 seconds") 
    time.sleep(2)

log(f"Classified {total_count} stories into categories")


os.makedirs("data", exist_ok=True)

# This list comprehension logic combines the stories across all categories into a single list.
all_stories= [
    story 
    for stories_list in stories_by_category.values()
        for story in stories_list
]


date_str = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_str}.json"

with open(filename, "w") as f:
    json.dump(all_stories, f, indent=4, default=str)

print(f"Collected {len(all_stories)} stories. Saved to {filename}")

