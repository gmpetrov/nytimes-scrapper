import re
import requests
from functools import reduce
from bs4 import BeautifulSoup

REGEX = re.compile(r'.*millennial.*', re.IGNORECASE)
BASE_YEAR_URL = "https://spiderbites.nytimes.com/{year}/"

def scrap_article(url):
    res = requests.get(url)
    html = res.text.encode('utf-8')
    return BeautifulSoup(html, "html.parser")

def keep_article(content):
    return REGEX.match(content) is not None

def scrap_year_links(year):
    url = BASE_YEAR_URL.format(year=str(year))

    res = requests.get(url)
    html = res.text.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    div_months = soup.findAll('div', attrs={"class": u"articlesMonth"})

    a_tags = map((lambda x: x.findAll('a')), div_months)
    
    links = []

    for each in a_tags:
        hrefs = map((lambda x: x['href']), each)
        links.extend(hrefs)
    
    return links
    
def scrap_year_article_links(uri):
    url = "https://spiderbites.nytimes.com{uri}".format(uri=uri)

    res = requests.get(url)
    html = res.text.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    headlines = soup.find('ul', attrs={"id": u"headlines"})

    a_tags = soup.findAll('a')
    
    return map((lambda x: x['href']), a_tags)


def scrap_nytimes(year):

    years_links = scrap_year_links(year)

    all_year_articles_urls = []

    for each in years_links:
        all_year_articles_urls.extend(scrap_year_article_links(each))
        
    
    articles_matching_regex = []

    for article_url in all_year_articles_urls:
        content = scrap_article(article_url)
        if keep_article(str(content)):
            articles_matching_regex.append(url)
            print article_url
        else:
            print "does not match regex"

    return articles_matching_regex

years = ["2018"]

for each in years:
    scrap_nytimes(each)




