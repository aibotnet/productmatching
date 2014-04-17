'''

    parsing search result page and gives  link for
    product review page.

'''


import re
import lxml.html
import Xpath

class SearchResPage():

    def __init__(self, xpathobj):
        self.title  = None
        self.s_link = None
        self.domain = None
        self.xObj   = xpathobj



    '''

        Remove Special charecter between charecters.

    '''
    def removeSpecialCharecterFromWord(self, word):
        return re.sub(r'[^.\w/]', '', word)




    def getKeyWordList(self):
        searchString = ''
        for el in self.title.split(' '):
            el = self.removeSpecialCharecterFromWord(el)
            if el.strip() == '':
                continue
            if searchString == '':
                searchString = el
            else:
                searchString += '+'+el
        return searchString




    def makelINK(self):
        return self.s_link%(self.getKeyWordList())




    def getLinksFromProductPage(self):
        link_set = set()
        try:

            link  = self.makelINK()
            doc = lxml.html.parse(link)

        except Exception:
            print '\nFailed to search on :\t\t: ', self.domain
            print '\t and link is\t: ', link,'\n\n'
            return link_set


        print 'Parsing search result page of  \t: ', self.domain
        try:
            for i in range(1, 4):
                srpXpath = self.xObj.getSrpXpath(self.domain)
                xpath = srpXpath%(i)
                #print '\t'+xpath
                for link in doc.xpath(xpath):
                    link_set.add(link)

        except Exception:
            print '\tError in parsing search result page\n\n'

        return link_set


    def getProductPageURLs(self, prodTitle, searchLink):
        self.title  = prodTitle
        self.s_link = searchLink
        self.domain = searchLink.split('/')[2]
        return  self.getLinksFromProductPage()
