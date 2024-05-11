from bs4 import BeautifulSoup
import requests
import re
import pandas as pd



# search terms
search_terms = ["internet scam", "cyber crime", "phishing", "fraudster", "data breach"]

# convert to search words
search_words = ["+".join(term.split()) for term in search_terms]

# get relevant stories
def get_apnews_data(search_words: list[str]):

    # get url
    url = "https://apnews.com/search?q="

    # iterate over search words
    for word in search_words:

        # convert to search words
        search_word = "+".join(word.split())

        # form url with query
        url_query = url + search_word + "&p=1"

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

        # find div with class "PagePromo"
        page_promos = soup.find_all("div", {"class": "PagePromo-title"})

        # filter out trending stories
        page_promos = [entry for entry in page_promos if not bool(entry.find("a", {"class", "Link AnClick-TrendingLink"}))]

        # filter if it does not have search word in headline or content
        page_promos = [entry for entry in page_promos if bool(re.search(re.escape(word), entry.text.lower()))]

        # get headlines after removing new line character
        page_promos_headlines = [entry.text for entry in page_promos]
        page_promos_link = [entry.find("a", attrs={"href": re.compile("^http")}).get("href") for entry in page_promos]
        print([entry.get("href") in page_promos_link for entry in soup.find_all("a", {"class": "Link"})])

get_apnews_data(["fraudster"])








def get_soup(url):
    # create object page
    url_page = requests.get(url)

    # use lxml parser to convert page
    url_soup = BeautifulSoup(url_page.text, "lxml")

    return url_soup



def cp24_banner():
    # get cp24 soup
    cp24_soup = get_soup("https://toronto.citynews.ca/toronto-gta-gas-prices/")

    # find div with class="float-box" and get its text
    cp_24_text = cp24_soup.find("div", {"class": "float-box"}).text

    # extract banner
    banner_start_index = cp_24_text.find("En-Pro")