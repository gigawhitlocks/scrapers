from bs4 import BeautifulSoup
import urllib2
import uuid
from pprint import pprint
from subprocess import call
def get_links(url):
    print "Preparing..."
    f = urllib2.urlopen(url)
    htmldoc = f.read()
    soup = BeautifulSoup(htmldoc)
    links = soup.find_all('a')
    categories = []
    for link in links:
        if "software" in link['href']:
            categories.append(link['href'])

    download_pages = []
    for category in categories:
        f = urllib2.urlopen("{}/{}".format(url, category))
        htmldoc = f.read()
        soup = BeautifulSoup(htmldoc)
        links = soup.find_all('a')
        for link in links:
            try:
                if u'program-entry-download-link' in link['class']:
                     download_pages.append(link['href'])
            except KeyError:
                pass


    for page in download_pages:
        f = urllib2.urlopen("{}/{}".format(url, page))
        htmldoc = f.read()
        soup = BeautifulSoup(htmldoc)
        links = soup.find_all('a')
        for link in links:
            try:
                if u'program-header-download-link' in link['class'] and link['href']:
                    g = urllib2.urlopen("{}{}".format(url, link['href']))
                    name = link['href'].split("/")[1][8:]
                    name += unicode(uuid.uuid4())
                    htmldoc = g.read()
                    soup = BeautifulSoup(htmldoc)
                    divs = soup.find_all('meta')
                    for meta in divs:
                        try:
                            if "url=" in meta['content']:
                                path =  meta['content'].split()[1].split("=")[1]
                                call("wget -nc -O {} {}{}".format(name, url, path), shell=True)
                        except KeyError:
                            pass
            except KeyError:
                pass




link_pages = get_links("http://filehippo.com")
