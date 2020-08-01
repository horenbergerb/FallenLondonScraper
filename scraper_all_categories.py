from bs4 import BeautifulSoup
import urllib2
from time import sleep

#gets all the possible categories' links
#starts in the "places" link
#for each name, generates what should be the category link
def get_all_category_links():
    places_url = "https://fallenlondon.fandom.com/wiki/Category:Places"

    #our output list
    urls = []
    
    response = urllib2.urlopen(places_url)
    html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    #the containers for all of the category entries
    cur = soup.find('div', {"class": "category-page__members"})
    for link in cur.find_all('a', href=True):
        urls.append("https://fallenlondon.fandom.com/wiki/Category:" + link['title'].replace(" ", "_"))

    #remove duplicates
    urls = list(dict.fromkeys(urls))

        
    return urls


#gets links from a category page and returns in a list
def get_links_from_category(url):
    print("Starting Location: {}".format(url))
    #our output list
    urls = []

    try:
        response = urllib2.urlopen(url)
    except:
        print("Failure to open link!")
        return -1
    html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    #the containers for all of the category entries
    for cur in soup.find_all('div', {"class": "category-page__member-left"}):
        for link in cur.find_all('a', href=True):
            urls.append("https://fallenlondon.fandom.com" + link['href'])

    #remove duplicates
    urls = list(dict.fromkeys(urls))
            
    return urls

#gets the title and body text from an entry page
def get_data_from_page(url):
    print("   Event: {}".format(url))
    #output data
    title = ""
    description = ""

    try:
        response = urllib2.urlopen(url)
    except:
        print("   Failure to open link!")
        return -1, -1
    html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    #the containers for all of the category entries
    title = soup.find('meta', {"property": "og:title"})['content']
    description = soup.find('meta', {"property": "og:description"})['content']

    return title, description
    

#getting all the category links
cat_urls = get_all_category_links()

final_output = ""

#iterate through places
for place_url in cat_urls:
    #iterate_through_entries for place
    urls = get_links_from_category(place_url)
    #catch bad links
    if urls == -1:
        continue

    for url in urls:
        title, description = get_data_from_page(url)
        #catch bad links
        if title == -1 and description == -1:
            continue
        final_output += "Title: " + title + "\n" + "Description: " + description + "\n"
        #not sure if i ought to sleep to avoid detection
        #sleep(3)

print(final_output)

text_file = open("all_places.txt", 'w')
n = text_file.write(final_output.encode('utf8'))
text_file.close()
