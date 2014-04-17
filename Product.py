class Product:

    def __init__(self, title, spec, impWordList, catogary, ptitleid, pid):
        self.title = title
        self.specification = spec
        '''
            List Contain Important Word.
            Target website must always contain these words
        '''
        self.imp_word_list = impWordList
        self.catogary = catogary
        self.ptitleid = ptitleid
        self.pid = pid



    def getTitle(self):
        return self.title


    def getSpecification(self):
        return self.specification


    def getImpWordList(self):
        return self.imp_word_list

    def getCatogary(self):
        return self.catogary

    def getPtitleId(self):
        return self.ptitleid

    def getPid(self):
        return self.pid

    def displayData(self):
        print '-----------------------------'
        print self.title
        print self.imp_word_list
        print self.catogary
        print self.ptitleid
        print self.pid
        print '---------------------------\n', self.specification

