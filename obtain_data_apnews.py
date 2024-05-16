from bs4 import BeautifulSoup
import requests
import re
import pandas as pd




# get relevant stories
def get_apnews_data(regex_search_words: list[str]):

    # get url
    url = "https://apnews.com/"

    # iterate over search words
    for word in regex_search_words:

        # form url with query
        url_query = url + "search?q=" + word + "&p=1"

        # string to hold request
        url_request = ""

        # try to make request
        try:

            url_request = requests.get(url_query)
        
        except requests.exceptions.HTTPError as e:

            # catastrophic error
            raise SystemExit(e)
        
        # get soup object
        soup = BeautifulSoup(url_request.text, "lxml")

        # filter out stories without data-gtm-region tag
        page_promos = [tag for tag in soup.select("div.PagePromo") if tag.has_attr("data-gtm-region")]

        # return list for story headline, description, and link
        story_info = []

        # set up column names
        columns = ["headline", "description", "link"]

        for tag in page_promos:

            # create temporary storage for headline, description, and link from story
            tmp_headline = tag.get("data-gtm-region")
            tmp_description = tag.find_all("span", {"class": "PagePromoContentIcons-text"})[-1].text
            tmp_link = tag.select("div.PagePromo-title")[0].select("a.Link")[0].get("href")
            
            # check if headline or description contains a search word
            if re.search(word, tmp_headline) or re.search(word, tmp_description):

                # append headline, description, and link
                story_info.append([tmp_headline, tmp_description, tmp_link])

        return pd.DataFrame(data=story_info, columns=columns)
    





# search terms
search_terms = ["internet scam", "cyber crime", "phishing", "fraudster", "data breach"]

# convert to search words
search_words = ["+".join(term.split()) for term in search_terms]

# regex search words
regex_search_words = [ re.escape(word) for word in search_words]

print(get_apnews_data(search_terms))
