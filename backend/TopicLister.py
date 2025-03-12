from requests_html import HTMLSession
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
import html
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def extract_links(description):
    # Ensure the input is a string
    if not isinstance(description, str):
        description = str(description)

    decoded_description = html.unescape(description)
    soup = BeautifulSoup(decoded_description, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]

    return links

def get_topic_list():
    url = 'https://news.google.com/rss'
    s = HTMLSession()
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    topic_list = []
    key_counter = 0
    for item in soup.find_all('item'):
        title = item.find('title').text
        links = extract_links(item.find('description'))
        key_counter+=1
        topic = {'key' : key_counter,
                 'title' : title,
                 'links' : links}
        topic_list.append(topic)

    return topic_list