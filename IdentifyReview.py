from ProductPage import *
import lxml.html
import re
from porterStemmer import *

class IdentifyReview:

    def __init__(self, xobj):
        self.ppObj=None
        self.stopWordSet  = self.getStopWordsSet('textfile/stopWords.txt')
        self.xpObj = xobj
        self.domain=None

    def getStopWordsSet(self, filename):
        fd = open(filename, 'r')
        stopWordList = []
        for words in fd:
            stopWordList.append(words.split('\n')[0])
        return  set(stopWordList)


    def createProductpageObject(self, pplink):
        try:
            doc         = lxml.html.parse(pplink)
            title       = doc.xpath(self.xpObj.getTitleXpath(self.domain))
            spec        = doc.xpath(self.xpObj.getSpecificationXpath(self.domain))
            self.ppObj  = ProductPage(title, spec, None, None)

            return True
        except Exception:
            print '\tError in parsing product page xpath missing \n\t',pplink,'\n\n\n'
            return False

    def removeSpecialCharecterFromWord(self, word):
        return re.sub(r'[^.\w/-]', '', word)


    def removeStopWords(self, mlist):
        for ele in mlist:
            if ele in self.stopWordSet:
                index =mlist.index(ele)
                del(mlist[index])

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def removeSpacesBetweenToken(self ,mlist):
        for token in mlist:
            for char in token:
                if char == ' ':
                    del(char)


    def getTokenList(self, lines):
        p = PorterStemmer()
        finList = []


        for line in lines.split('\n'):
            for sen in line.split('-'):
                mlist=line.split(' ')
                n= len(mlist)
                for i in range(n):
                    mlist[i] = self.removeSpecialCharecterFromWord(mlist[i])
                    mlist[i] = mlist[i].strip()
                    mlist[i] = mlist[i].lower()

                #removing blank token
                for word in mlist:
                    if word.strip() == '' or word.strip() == '-':
                        i = mlist.index(word)
                        del(mlist[i])

                #removing stopwords
                self.removeStopWords(mlist)
                finList += mlist


        '''
            Stemming of word
        '''
        n = len(finList)
        for i in range(n):
            finList[i] = p.stem(finList[i],0,len(finList[i])-1)
        for word in finList:
            if word.strip() == '':
                i = finList.index(word)
                del(finList[i])
        return finList


    '''
        Return probability
    '''
    def getPercentageMach(self, Nset, pset):
        n=len(Nset);count=0
        if n==0:
            return 100
        for element in Nset:
            if element in pset:
                count+=1
            else:
                print '\t\t', element

        percentage = (float(count)/float(n)) * 100
        return percentage



    '''
        Compare product title and discription
        and mached review will saved in file.
    '''
    def mach(self, productObj, prodPageLink):
        #print '\tLink is : ', prodPageLink
        productTitle  = productObj.getTitle()
        specification = productObj.getSpecification()
        impword       = productObj.getImpWordList()
        self.domain   = prodPageLink.split('/')[2]
        if not self.createProductpageObject(prodPageLink):
            return False
        '''
            create a file named product title.
            for each product this file is created for storing review
        '''
        filename =''
        for el in productTitle.split('\n'):
            if el:
                filename += el
        filename =re.sub(r'[^\w.]', '', filename+'.txt')
        out = open(filename, 'w+')


        N_tlist = self.getTokenList(productTitle)
        N_slist = self.getTokenList(specification)
        N_impList = []
        for item in impword:
            for token in self.getTokenList(item):
                N_impList.append(token)
        N_tset  = set(N_tlist)
        N_sset  = set(N_slist)
        N_imp   = set(N_impList)


        #start matching
        try:
            p_set = set()
            tlist   = self.getTokenList(self.ppObj.getTitle()[0])
            for el in tlist:
                p_set.add(el)

            for el in self.ppObj.getSpecification():
                for token in  self.getTokenList(el):
                    p_set.add(token)


            N_t_per = self.getPercentageMach(N_tset, p_set)

            print '\tTitle Mached : ', N_t_per, '%'
            N_s_per = self.getPercentageMach(N_sset, p_set)
            print '\tSpecification Mached : ', N_s_per, '%'
            for item in N_imp:
                if item in p_set:
                    print '\timportant item < %s > mached'%(item)
                else:
                    print '\timportant item < %s > not mached'%(item)

        except Exception:
            print '\tMaching exception\n\n'

        out.close()

        return True