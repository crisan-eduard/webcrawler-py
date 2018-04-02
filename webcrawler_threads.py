#
#	WEB CRAWLER
#
#	GRAB LINKS FROM WEBSITE
#
#	STORES IN A LIST: check for dup,insert element, crawl and delete first element
#
'''
    WEBCRAWLER ALGORITHM
    phase 1: initialization
        -create queue_file, history_file
        -get start url
        -scrape parse url
        -put scraped content into queue_file
        -put start url in history
    phase 2: crawling on threads
        -def crawl(queue_file, history_file):
            while size_of(queue_file)>0:
                line = read_delete_line(queue_file)
                if file_contains_line(history_file,line)==False:
                    append_line_to_file(line,history_file)
                    links_set = get_links(line)
                    for link in links_set:
                        append_line_to_file(link,queue_file)
        call on multiple threads
'''
import os
import housekeeping
import time
import threading
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.parse import urlparse

# def handle_url(url,initialurl):
# 	''' get scheme and other stuff from initialurl and modify url '''
# 	parsed_url = urlparse(initialurl)
# 	scheme = parsed_url.scheme
# 	path = parsed_url.path

# 	if(url[0] == '/' && url[1] != '/'):
# 		return scheme + ":/" + url

def to_String(list):
    i = 0
    for element in list:
        print("[" + str(i) + "]" + element + "\n")
        # print("["+i+"]")
        i = i + 1
    # print (element)
    print("--------------------------------------")


def grab_urls(my_url):
    '''return set of links from my_url page'''
    # my_url = 'https://mediagalaxy.ro/electrocasnice-mari/masini-de-spalat-rufe/masini-de-spalat-frontale'
    # my_url = 'http://localhost/links.html'
    # open connectiomn, grab the page, close connection

    links = []  # stack of urls to scrape
    visited = []  # historic record

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    # get the HTML content
    page_soup = soup(page_html, "html.parser")

    # grab href tags
    containers = page_soup.findAll(href=True)

    for container in containers:
        if "http:" in container["href"] or "https:" in container["href"]:
            if container["href"] not in visited:
                links.append(container["href"])
                visited.append(container["href"])
    return links
    # print(container["href"]+"\n")


# grab href tags\

# print (links)
# print("--------------------")

def initialize(queue_file, history_file):
    start_url = "http://www.cprarad.ro/"
    housekeeping.create_text_file("queue_file")
    housekeeping.create_text_file("history_file")
    links_set = grab_urls(start_url)
    for link in links_set:
        housekeeping.append_line_to_file(link, queue_file)
    housekeeping.append_line_to_file(start_url, history_file)


def crawl(queue_file, history_file):
    while os.path.getsize(queue_file)>0:
        line = housekeeping.read_delete_line(queue_file)
        if housekeeping.file_contains_line(history_file, line) == False:
            try:
                housekeeping.append_line_to_file(line, history_file)
                links_set = grab_urls(line)
                for link in links_set:
                    housekeeping.append_line_to_file(link,queue_file)
            except:
                print("*unable to crawl")

initialize("queue_file.txt", "history_file.txt")
#crawl("queue_file.txt", "history_file.txt")

nr_of_threads = 10

for t in range(nr_of_threads):
    t= threading.Thread(target=crawl,args=("queue_file.txt", "history_file.txt", ))
    t.daemon = True
    t.start()
    t.join()


