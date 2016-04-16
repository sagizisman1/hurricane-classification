#!/opt/local/bin/python

# This is am html img scraper. 
# This script uses 2 arguments (URL path and Local Dir Name)
# Example of script incantation: 
##  python extractImg.py https://en.wikipedia.org/wiki/2015_Atlantic_hurricane_season hurr2015
# Maggie Sallee - 4/20/2016

from sys import argv
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import urllib
import logging


def createSoup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)

def getUrlImages(url, localDir):
    soup = createSoup(url)

    # Find images
    images = [img for img in soup.findAll('img')]
    print (str(len(images)) + " images found.")

    # Get the source
    imageCount = 0
    imageLinks = [each.get('src') for each in images]
    for each in imageLinks:
        #Add and counter:
        imageCount = imageCount+1
        localFile = each.split('/')[-1]
        localPath = localDir + '/' + localFile
        
        try:
           urllib.urlretrieve('https:' + each, localPath)
        except Exception, e:
                logging.warn("error downloading %s: %s" % (localFile, e))
        print "Image #: ", imageCount, ": Filepath: ",each," copied to: ", localPath, "\n\n"
    return imageLinks

# Main Scrip: Get url, and directory with argv: 
script, inputUrl, imgDir = argv

# Get images from a given URL to a given local directory:
getUrlImages(inputUrl, imgDir)

print "End of getting images from", inputUrl, "\n"

### End of Program #####################
