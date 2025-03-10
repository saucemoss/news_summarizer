from requests_html import HTMLSession
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
import html

import ArticleTextExtrator
import LLMSummariser

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def extract_links(description):
    # Ensure the input is a string
    if not isinstance(description, str):
        description = str(description)

    # Unescape HTML entities
    decoded_description = html.unescape(description)

    # Parse with BeautifulSoup
    soup = BeautifulSoup(decoded_description, "html.parser")

    # Extract all href links
    links = [a["href"] for a in soup.find_all("a", href=True)]

    return links

def get_topic_list():
    url = 'https://news.google.com/rss'
    s = HTMLSession()
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    topic_list = []
    for item in soup.find_all('item'):
        title = item.find('title').text
        links = extract_links(item.find('description'))
        topic = {'title' : title,
                 'links' : links}
        topic_list.append(topic)

    return topic_list


topics = get_topic_list()
print(topics[1].get('title'))
for link in topics[1].get('links'):
    print(link)
    article_text = ArticleTextExtrator.get_text(link)
    LLMSummariser.get_article_summary_gemini(article_text)
