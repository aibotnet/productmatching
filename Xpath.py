import re


class Xpath:

    def __init__(self):
        self.srpxpath = {}
        self.nextsrpxpaqth = {}
        self.titlexpathMap = {}
        self.specxpatMap = {}
        self.revxpathMap = {}

    def loadXpaths(self, xpath_filename, domain_filename):

        file = open(xpath_filename)
        doc = ''
        for line in file:
            doc+=line

        domSet = set()

        for line in open(domain_filename):
            domSet.add(line.strip().split('\n')[0])

        for domain in domSet:
            try:

                serchExpr = '<'+domain+'>'+'(.*?)</'+ domain + '>'
                temp = re.search(serchExpr, doc, re.DOTALL).group(1)

                domXpathString = re.search('<spage>(.*?)</spage>', temp, re.DOTALL).group(1)
                srpxpath = re.search('<xp>(.*?)</xp>', domXpathString, re.DOTALL).group(1)

                srp_xpath = ''
                for token in srpxpath.strip().split('\n'):
                    if token == '':
                        continue
                    srp_xpath=token
                self.srpxpath[domain] = srp_xpath

                pp_title = re.search('<title>(.*?)</title>', temp, re.DOTALL).group(1)
                pp_title_xpath = ''
                for token in pp_title.strip().split('\n'):
                    if token == '':
                        continue
                    pp_title_xpath=token
                self.titlexpathMap[domain] = pp_title_xpath

                pp_spec = re.search('<spec>(.*?)</spec>', temp, re.DOTALL).group(1)
                pp_spec_xpath = ''
                for token in pp_spec.strip().split('\n'):
                    if token == '':
                        continue
                    pp_spec_xpath=token
                self.specxpatMap[domain] = pp_spec_xpath

            except Exception:
                print 'Error in xpath file parsing : %s\n'%domain




    def getSrpXpath(self, domain):
        return self.srpxpath[domain]

    def getSrpNextLinkXpath(self, domain):
        return self.nextsrpxpaqth[domain]



    def getTitleXpath(self, domain):
        return self.titlexpathMap[domain]


    def getSpecificationXpath(self, domain):
        return self.specxpatMap[domain]

    def getReviewXpath(self, domain):
        return self.revxpathMap[domain]

