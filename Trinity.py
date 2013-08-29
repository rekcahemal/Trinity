#!/usr/bin/python

#####################################################################################################
#####################################################################################################
## Created on Aug 16, 2013
## 
## @author: Gerasimos Kassaras
## E-mail: g.kassaras@gmail.com
## Nickname: Lamehacker Free Industries
## 
## Conventions used in this coding style:
## Variable Naming Convention: urlSet - Is a set containing a set with url's
## Variable Naming Convention: cleanSet - Is a set that removes certain urls based on some conditions.
## Variable Naming Convention: subUrlSet - Is a sub set of a urlSet.
## Variable Naming Convention: urlList - Is a list containing a set with unfiltered url's
## Variable Naming Convention: cleanList - Is a list that removes certain urls based on some conditions.
## Variable Naming Convention: subUrlList - Is a sub set of a urlSet.
## TODO Naming Convention: The TODO Naming Convention is TODO: 
## Comments: Naming conventions are used are valid for every module within webshark. 
#######################################################################################################
#######################################################################################################

from urlparse import urlparse
from time import gmtime, strftime
from bs4 import BeautifulSoup
import httplib
import itertools
import re

urlList = ["http://www.example.com/"] # Later on this url is going to be fed through command parser.
crawled = [] # Is going to be used to keep state of visited links. 
host = 'http://www.example.com/'
domain = 'www.example.com'

'''
Description: This function is used to fetch the raw html for a single page and also manage the connection.
Status: Finished.
TODO: Move function to separate to connection manager module and fix also url parser.
Usage: Fetching the html page and usded with in the fetch function. 
'''
def response(url): # Takes as an input a string and returns a string 
    # Takes as an input a single url and returns a single page raw html. 
    urlPath = urlparse(url).path # Gets the url path.

    try:
        print 'Calling response function - Fetching URL path: '+urlPath
        conn = httplib.HTTPConnection(domain)
        conn.request("GET",urlPath)
        response = conn.getresponse().read() # Collect http response body.

    except httplib.error as msg:
        print 'Inserted url'+urlPath
        print msg # TODO: Add better exception handling.
        pass

    return response

'''
Description: This function is used to collect all urls from a single page and return a url list.
Status: In progress.
Usage: Is going to be used to collect per raw html input all urls.
'''

def parse(rawHtml) : # Takes as an input a string and returns a list 
    
    loadHtml = rawHtml # Load raw html from raw http response.
    soup = BeautifulSoup(loadHtml)
    urlList = []
    
    for tag in soup.findAll('link', href=True) : # Checks for links within the link tag e.g.<link rel="canonical" href="http://example.com/" />
        urlList.append(tag['href'])

    for tag in soup.findAll('a', href=True) :# Checks for links within the a tag e.g. <a href="http://exmple.com/packages/"</a>
        urlList.append(tag['href'])

    for tag in soup.findAll('meta', content=True) :# Checks for links within the content tag e.g.  <meta property="og:video" content="http://example.com/v/w0?version=3;autohide=1">
        if re.search(r'(^http://)|(^https://)', tag['content'], re.IGNORECASE): # Checks for links that start with http or https.
            urlList.append(tag['content'])

    for tag in soup.findAll('script', src=True) :# Checks for links within the script tag e.g. <script type='text/javascript' src="http://example.com/wp-includes/js/jquery/jquery.js"></script>
        if re.search(r'(^http://)|(^https://)', tag['src'], re.IGNORECASE):
            urlList.append(tag['src'])

    return urlList

'''
Description: This function is used to as a fetcher for the urlList.
Status: In progress
TODO: Would have to revisit. This is going to become the connection manager for future use.
Usage: Is going to be used to collect per page all urls.
'''
def fetch(urlList):# Takes as an input a list and returns a list. 
    
    rawUrlList = [] # This is a none filtered list of urls collected
    
    for url in urlList:
        if not url in crawled: # If the url is already fetched is not going to re-fetch.
            rawUrlList.append(parse(response(url))) # Fetch urls from each page.
            crawled.append(url) # Record non visited links.
            #print 'Calling fetcher() - Crawled :'+str(crawled)
        
    return rawUrlList

'''
Description:This function extracts non html files from from the urls collected.
Status: In progress
Usage: e.g. Extract Windows Files from each URL
'''
def noneHtml(urlList): # Takes as an input a list and returns a list. 

    rm = ['.ZIP','.JPG','.DMG','.MSI','.RAR','BZ2','TGZ','.CHM','.TAR','.EXE','.XZ','.DOC','.PDF','.PNG','.JPG','.TIFF','MAILTO','#','XPI','CRX'] #Add here all the urls you would like to remove from final url list

    cleanList = []
    tmp = urlList

    for fileSuffix in range(len(rm)):
        for element in range(len(tmp)):
            if re.search(rm[fileSuffix],urlList[element],re.IGNORECASE):
                cleanList.append(urlList[element])

    return cleanList

'''
Description: This function transforms the collected urls so as to be use later on by httplib to collect more urls.
Status: Finished.
Comment: Might have to revisit.
Usage: Restrict crawling to the start url.
'''
def restrict(urlList) : # Takes as an input a list and returns a list.
    
    cleanList = []
    
    for url in range(len(urlList)):
        if re.search(r"(^/)|(^../)",urlList[url],re.IGNORECASE):# Search for inner urls.
            cleanList.append(urlList[url])

        if re.search(domain,urlList[url],re.IGNORECASE):# Restrict url collection to same domain.
            cleanList.append(urlList[url])

    return cleanList

'''
Description: This function is going to be used as a mreger for the list returned from the parseHtml function.
Status: Finished.
Usage: Is used to prevent the url parser from crashing by converting a list of lists to a list of urls.
'''
def merge(urlList):# Takes as an input a list and returns a list.
    
    while True:
        if any(isinstance(element, list) for element in urlList): # Checks through all list elements to find lists.
            ''' 
            Check if this is a list of lists of type [...[]...] or of type [...[],[],[]...].
            Examples lists that checks:
                1.[['/about','/search','/help']]
                2.[[['/about']]]
                3.[['/about',['/search'],'/help']]
            '''
            urlList = list(itertools.chain(*urlList))
            ''' 
            Removes external brackets from a list of lists of type [...[]...] or of type [...[],[],[]...].
            Examples lists that alters:
                1. Input:[['/about'],['/search'],['/help']] -> Output: ['/about','/search','/help']
                2. Input:[[[[['/about']]]]] -> Output: ['/about']
                3. Input:[['/about',['/search'],'/hp']] -> Output:['/about','/search','/','h','p'] - Breaks the parser - Should never occur. 
            '''
        else:
            break # Break the loop if this is not a list of lists.
    
    return urlList

'''
Description: This function receives a list with the collected urls and removes double urls.
Status: Finished.
Usage: Is used to avoid re-downloading the same urls and going through loops by the parser.
'''
def deduplicate(urlList):# Takes as an input a list and returns a list.
    
    urlList = list(set(urlList))
    
    return urlList

'''
Description: This function is used to return the crawled links.
Status: Finished
Usage: This is going to be used in the future to get the crawled links.
'''
def getCrawledList():# Takes as an input nothing and returns a list.
    
    return crawled

'''
Description: This function receives a list with the collected urls and subtracts a sublist of urls.
Status: Finished.
Usage: Is used to protect the html parser from crashing and help later on to analyze the non html content.
'''
def removeSet(urlList,urlSublist): # Takes as an input a list and returns a list.
    
    urlSet = set(urlList)
    urlSubset = set(urlSublist)
    clearSet = urlSet - urlSubset
    
    return list(clearSet) # Convert again to list.

'''
Description: This function filters out doubles and and non html comments.
Status: TODO: In progress.
Usage: Is used to protect the html parser from crashing, analyzing the non html content and removing double urls.
'''
def purify(urlList): # Takes as an input a list and returns a list.

    cleanList = urlList
    cleanList = merge(cleanList)
    cleanList = restrict(cleanList) # Restrict urls to main domain.
    cleanList = deduplicate(cleanList)
    cleanList = removeSet(cleanList,noneHtml(cleanList)) # Clean up non html content.

    return cleanList

'''
Description: This function is used to find if the next page contains the same links with the previous page.
Status: Finished
Usage: Is used within the harvest functions as a termination condition.
'''
def isSubset(collectedUrlList,nextPageUrlList):# Takes as an input a list and returns true or false.
    
    collectedUrlSet = set(collectedUrlList)
    nextPageUrlSet = set(nextPageUrlList)
    
    if nextPageUrlSet.issubset(collectedUrlSet):
        return True
    else:
        return False

'''
Description: This function is used to find if the next page contains any links.
Status: Finished
Usage: Is used within the harvest functions as a termination condition.
'''
def emptyList(page):# Takes as an input a list and returns true or false.

    if page == []:
        return True
    else:
        return False

'''
Description: This function is used to export the urls into a file.
Status: Finished
Usage: Is used within the harvest functions as a url exporter.
'''
def exportFeed(filename,urlList):# Takes as an input a list and returns nothing. 

    urlList  = sorted(urlList) # Sort urls so it can be more easy to read.
    fobj = open(filename,'wa')
    
    for link in range(len(urlList)):
        fobj.write('['+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'] '+str(urlList[link])+'\n') # Exports the urls in a file.
    
    fobj.close()

'''
Description: This function is used to fetch a single page urls.
Status: Finished.
Usage: Is used within the harvester to fetch for a single page the urls.
'''
def singlePage(urlList): # Input is a list, output is a list

    urlList = fetch(urlList)
    urlList = purify(urlList)

    return urlList

'''
Description: This function is used maintain the state of the crawler.
Status: In Progress
Usage: Is used within the harvester to remove visited links.
'''
def harvester(urlList):# Accepts the initial domain name as a url list.

    urlCollector = [] # Returns the collected urls and should be equal to the crawled list.
    nextPage = singlePage(urlList)# Gets the start urls (usual a the domain name).

    while True:

        nextPage = singlePage(nextPage)# Fetch the next page.

        if emptyList(nextPage):# If the crawled list contains the urlCollector links then the list shrinks to an empty list.
            break
        
        for eachLink in range(len(nextPage)):
            if not isSubset(urlCollector,nextPage): # Check if the fetched urls is a subset of the collected links.
                urlCollector.append(nextPage[eachLink])

        nextPage = urlCollector
        
    exportFeed('collector.out',getCrawledList())
    
    return urlCollector

if __name__ == '__main__':
    harvester(urlList)