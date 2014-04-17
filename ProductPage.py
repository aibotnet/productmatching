

class ProductPage:

    def __init__(self,title, spec, mpn, rlist):
        self.title = title
        self.specification = spec
        self.mpn = mpn
        self.revList = rlist

    def getTitle(self):
        return self.title

    def getSpecification(self):
        return self.specification

    def getMpn(self):
        return self.mpn

    def getRevList(self):
        return self.revList

    def displayData(self):
        print '-----------------------------'
        print self.title
        print self.specification
        print self.mpn
        print self.revList