class Abbrevation:
    def __init__(self):
        self.dataSet = []
        self.labels  = []


    def loadDataSet(self , infile):
        fd = open(infile, 'r')

        for  line in fd:
            print line
    def classifyAbbreviation(self , abbr):
        pass