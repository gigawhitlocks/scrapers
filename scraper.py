from bs4 import BeautifulSoup
import urllib2
from subprocess import call
def get_images(url):
    print url
    f = urllib2.urlopen(url)
    htmldoc = f.read()
    soup = BeautifulSoup(htmldoc)
    links = soup.find_all('a')
    for link in links:
        if link.img:
            call("wget -N http:{}".format(link['href']), shell=True)
        try:
            if link['class'] == [u'replylink']:
                new_url = "http://boards.4chan.org/hr/{}".format(link['href'])
                get_images(new_url)
        except KeyError:
            pass
for i in range(0,10):
    get_images('http://boards.4chan.org/hr/{}'.format(i))
