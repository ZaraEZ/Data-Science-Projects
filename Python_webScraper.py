'''
Author: Zara Zarzour
Date: 10/28/2021
"I have not given or received any unauthorized assistance on this assignment"
Homework #6, Program #2
'''

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin

class Collector(HTMLParser):
    '''
    Collector class is inherited from HTMLParser. A few inherited methods will be improved within this class to collect the URLs from the website, append to a list, find words, and count them
    '''

    def __init__(self, url):
        '''
        Initializes the web parser, URL, and a dictionary for the words
        '''
        HTMLParser.__init__(self)
        self.url = url
        self.links = set()
        self.words = {}

    def handle_starttag(self, tag, attrs):
        '''
        handle_starttag collects hyperlink URLs in their absolute format; overriden from HTMLParser
        '''
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    #construct the absolute URL
                    absolute = urljoin(self.url, attr[1])
                    #collect HTTP URLs
                    if absolute[:4] == 'http':  
                        self.links.add(absolute)

    def getLinks(self):
        '''
        getLinks() returns hyperlinks URLs in their absolute format
        '''
        return self.links

    def handle_data(self, data):
        '''
        handle_data will split and count the words, while excluding certain keywords that may interfere with the results; overriden from HTMLParser
        '''
        #key words to exclude from the word count (this was based on evidence from the output)
        excluded = ['p', 'web','div', 'in', 'span', 'a', 'h1', 'h2', 'h2', 'h3', 'h4', 'parentheight', 'wpid', 'bgcolor', 'by', 'at', 'var', 'or', 'the', 'is', 'if', 'to', 'for', 'on', 'of', 'be', 'a', 'this', 'and', 'are', 'il']
        
        #it's easier to compare words when they're all in lower case
        sourceCode = data.lower()

        #splitting the words in the source code/ URL
        newWords = sourceCode.split()
        for word in newWords:
            #as long as every character in the string is a letter and none of the words in the excluded list match the word
            if word.isalpha() and word not in excluded:
                #start counting
                if word in self.words:
                    self.words[word] += 1
                else:
                    self.words[word] = 1

    def returnListofWords(self):
        '''
        returnListofWords returns a list of words that was created in handle_data 
        '''
        return self.words


def implementation(url):
    '''
    implementation will open the URLs, get the words list from each and counts, sort it into a dictionary, then display the results
    '''
    
    print('\n\nVisiting', url)

    #obtain links in the webpage
    content = urlopen(url).read().decode()
    collector = Collector(url)
    collector.feed(content)
    urls = collector.getLinks()

    #get the dictionary of all words and counts; word and number of occurences (as a dictionary) are assigned to X
    words = collector.returnListofWords()

    #sort the the dictionary of words and convert it to a list 
    sortedWords = sorted(words.items(), key=lambda item: item[1], reverse=True)
    
    #assign the first 25 words to wordlist and format it
    wordlist = sortedWords[:25]
    print('\n{:21} {:25}'.format('WORD', 'COUNT'))
    
    #print the wordlist of formatted and most common 25 words 
    for count in wordlist:
        print('{:15} {:10}'.format(count[0], count[1]))
    
    #return urls for comparison to ensure the program does not run through the same URL multiple times
    return urls 


#initialize visited to an empty set; holds all the URLs that were already visited 
visitedLinks = set()


def crawl(url):
    '''
    crawl() is a recursive web crawler that calls implementation and compares links to those visited and other exceptions 
    '''
    
    #add the currently used url to the visitedLinks set
    visitedLinks.add(url)

    #implentation() returns a list of hyperlink URLs within the webpage's URL
    links = implementation(url)

    #recursively continue crawl from every link in links
    for link in links:
        #this limits us to only depaul campuses links
        if 'https://www.depaul.edu/about/campuses/' in link:
            #this ensures that duplicate or shortcut pages do not reappear later and get reimplemented in this program (BASED ON TRIAL AND ERROR)
            if 'shortcut' not in link and '-1' not in link and '-2' not in link and '-3' not in link and '-4' not in link and '#g_6a7afe2c_9a20_4841_99b5_d44e97c1dbe7' not in link:
                if link not in visitedLinks:
                    try:
                        crawl(link)
                    except:
                        pass


#WARNING: IF YOU CHANGE THIS LINK, THE PROGRAM WILL KEEP RUNNIN AND RUNNIN. 
crawl('https://www.depaul.edu/about/campuses/Pages/default.aspx')