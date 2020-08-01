from bs4 import BeautifulSoup
import urllib2
from time import sleep

#gets links from a category page and returns in a list
def get_links_from_category(url):
    #our output list
    urls = []
    
    response = urllib2.urlopen(url)
    html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    #the containers for all of the category entries
    for cur in soup.find_all('div', {"class": "category-page__member-left"}):
        for link in cur.find_all('a', href=True):
            urls.append("https://fallenlondon.fandom.com" + link['href'])

    return urls

#gets the title and body text from an entry page
def get_data_from_page(url):
    #output data
    title = ""
    description = ""
    
    response = urllib2.urlopen(url)
    html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    #the containers for all of the category entries
    title = soup.find('meta', {"property": "og:title"})['content']
    description = soup.find('meta', {"property": "og:description"})['content']

    return title, description
    

#category for iron republic entries
iron_republic = "https://fallenlondon.fandom.com/wiki/Category:Iron_Republic_Streets"

urls = get_links_from_category(iron_republic)

final_output = ""

for url in urls:
    title, description = get_data_from_page(url)
    final_output += "Title: " + title + "\n " + "Description: " + description + "\n"
    sleep(3)

print(final_output)
