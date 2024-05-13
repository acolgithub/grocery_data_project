import requests
import json
import re
import pandas as pd

import sqlite3
from sqlite_database import create_sqlite_database, add_data


class Subreddit():

    def __init__(self, subreddit: str) -> None:

        self.subreddit = subreddit
        self.json_url = "https://www.reddit.com/r/" + subreddit + ".json?limit=100"
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}


    def get_subreddit_info(self, keywords):

        # return list of info
        info_list = []

        # store request
        url_request = ""

        # try to send request for data to url
        try:
            url_request = requests.get(url=self.json_url, headers=self.header)

            # raise an HTTP error
            url_request.raise_for_status()

        # if there is an exception
        except requests.exceptions.HTTPError as e:

            # indicate subreddit lead to an HTTP error
            print(f"The subreddit, {self.subreddit}, lead to HTTP error.")

            # catastrophic error
            raise SystemExit(e)
        

        # convert to json
        json_format = url_request.json()

        # get reddit posts
        reddit_posts = json_format["data"]["children"]

        # iterate over reddit post
        for post in reddit_posts:

            # check that reddit post is of t3 kind and contains a url
            if post["kind"] == "t3" and "url_overridden_by_dest" in post["data"].keys():

                # create regex to check if url corresponds to image or form
                unwanted_url_regex = "\/(?:gallery|form)\/|(?:jpeg|png|gif)$"

                # check if post contains a url that is not an image or form
                if not re.search(re.compile(unwanted_url_regex), post["data"]["url_overridden_by_dest"]):

                    # append if title of post contains desired keywords
                    if any(re.search(r"\b" + re.escape(keyword) + r"\b", post["data"]["title"].lower()) for keyword in keywords):

                        info_list.append([
                            self.subreddit,
                            post["data"]["title"],
                            post["data"]["url_overridden_by_dest"],
                            "https://www.reddit.com" + post["data"]["permalink"]
                        ])

        return info_list


# define function to search for keywords from given subreddits
def get_reddit_data(subreddits: list[Subreddit], keywords: list[str]) -> pd.DataFrame:

    # set up list of reddit info
    reddit_info_list = []

    # set up column names
    columns = ["subreddit", "description", "link", "permalink"]

    for subreddit in subreddits:

        reddit_info_list.extend(subreddit.get_subreddit_info(keywords))

    return pd.DataFrame(data=reddit_info_list, columns=columns)


# names of subreddits of interest
names = ["privacy", "cybersecurity", "hackers"]

# create list of Subreddit objects
subreddits = [Subreddit(name) for name in names]

# list of keywords of interest
keywords = ["phish", "scam", "hack", "fraud", "breach", "attack", "fraudster", "internet scam", "cyber crime"]

stories_of_interest = get_reddit_data(subreddits, keywords)
print(stories_of_interest.link.to_list())




# # create database file
# create_sqlite_database("datascraping_reddit_database.db")

# # try to connect to database
# try:

#     # start connection
#     conn = sqlite3.connect("datascraping_reddit_database.db")


# except sqlite3.Error as e:

#         # if connection fails print error
#         print(e)


# # stories_of_interest.to_sql("data", con=conn)
# statement = '''SELECT * FROM data'''

# # get cursor
# cur = conn.cursor()

# # write table
# # stories_of_interest.to_sql(name="datascraping_reddit_database", con=conn)

# # execute statement
# cur.execute(statement)

# # print all data
# output = cur.fetchall()
# for row in output:
#     print(row)

# # commit statement
# conn.commit()


# # close connection   
# conn.close()




















