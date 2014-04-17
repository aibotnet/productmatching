from Product import *
from SearchResPage import *
from Xpath import *
from IdentifyReview import *
import re


'''

    Create a list of product information
    where each entry contain
    whole detail about product.
'''


def getProductList(filename):
    productList = []; doc = []
    inf = open(filename)

    for line in inf:
        for stream in line.split('|'):
            token = stream.split('\n')[0]

            if '</page>' in token:

                currentDoc  = ''.join(doc)
                revTitle    = re.search('<title>(.*?)</title>',  currentDoc, re.DOTALL)
                revSpec     = re.search('<spec>(.*?)</spec>',  currentDoc, re.DOTALL)
                imp         = re.search('<imp>(.*?)</imp>',  currentDoc, re.DOTALL)
                cat         = re.search('<cat>(.*?)</cat>', currentDoc, re.DOTALL)
                ptitleid    = re.search('<ptitleid>(.*?)</ptitleid>', currentDoc, re.DOTALL)
                pid         = re.search('<pid>(.*?)</pid>', currentDoc, re.DOTALL)


                try: # for title
                    title = revTitle.group(1)
                    for el in title.split('\n'):
                        if el is '':
                            continue
                        else:
                            title = el
                            break
                except Exception:
                    print 'Unstructured Product Info File : no <title>  tag found'


                try: #for specification
                    spec = revSpec.group(1)
                except Exception:
                    print 'Unstructured Product Info File : no <spec> tag found'


                try: #for imp tag
                    imp = imp.group(1)

                    implist = []
                    for el in imp.split('\n'):
                        if el == '':
                            continue
                        else:
                            for word in el.split(' '):
                                if word.strip() == '':
                                    continue
                                implist.append(word)
                            break

                except Exception:
                    print 'Unstructured Product Info File : no <imp> tag found '



                try: #for cat tag
                    cat = cat.group(1)

                    for el in cat.split('\n'):
                        if el == '':
                            continue
                        else:
                            cat = el
                            break

                except Exception:
                    print 'Unstructured Product Info File : no <cat> tag found '

                try: #for ptitleid tag
                    ptitleid = ptitleid.group(1)

                    for el in ptitleid.split('\n'):
                        if el == '':
                            continue
                        else:
                            ptitleid = el
                            break

                except Exception:
                    print 'Unstructured Product Info File : no <ptitleid> tag found '

                try: #for pid tag
                    pid = pid.group(1)

                    for el in pid.split('\n'):
                        if el == '':
                            continue
                        else:
                            pid = el
                            break

                except Exception:
                    print 'Unstructured Product Info File : no <pid> tag found '

                productList.append(Product(title, spec,  implist, cat, ptitleid, pid))

                doc = []
            doc.append(stream)
    return productList


def getDomainMap(filename):
    file = open(filename)
    string = ''
    domainMap = {}

    for line in file:
        string+=line


    all = re.search('<all>(.*?)</all>', string, re.DOTALL)
    try:
        list =[]
        for line in all.group(1).split('\n'):
            if line.strip() == '':
                continue
            else:
                list.append(line.strip())

        domainMap['all'] = list
    except Exception:
        print 'Error in file :', filename, ' : no <all> tag is found'


    ele = re.search('<electronics>(.*?)</electronics>', string, re.DOTALL)
    try:
        list =[]
        for line in ele.group(1).split('\n'):
            if line.strip() == '':
                continue
            else:
                list.append(line.strip())
        domainMap['electronics'] = list
    except Exception:
        print 'Error in file :', filename, ' : no <electronic> tag is found'

    app = re.search('<appliances>(.*?)</appliances>', string, re.DOTALL)
    try:
        list =[]
        for line in app.group(1).split('\n'):
            if line.strip() == '':
                continue
            else:
                list.append(line.strip())
        domainMap['appliances'] = list
    except Exception:
        print 'Error in file :', filename, ' : no <appliances> tag is found'



    comp = re.search('<computers>(.*?)</computers>', string, re.DOTALL)
    try:
        list =[]
        for line in comp.group(1).split('\n'):
            if line.strip() == '':
                continue
            else:
                list.append(line.strip())

        domainMap['computers'] = list
    except Exception:
        print 'Error in file :', filename, ' : no <computers> tag is found'


    other = re.search('<others>(.*?)</others>', string, re.DOTALL)
    try:
        list =[]
        for line in other.group(1).split('\n'):
            if line.strip() == '':
                continue
            else:
                list.append(line.strip())

        domainMap['others'] = list
    except Exception:
        print 'Error in file :', filename, ' : no <others> tag is found'


    return domainMap


def getDomainSearchLinkMap(filename):
    file = open(filename)
    dsmap = {}
    for line in file:
        try:
            tokens  = line.split('|')
            domain = tokens[0].strip()
            s_link = tokens[1].strip()
            dsmap[domain] = s_link.split('\n')[0]
        except Exception:
            print 'File Format Error : ', filename
    return dsmap


'''

	Main module

'''



def main():

    productList = getProductList('textfile/productInfo.txt')
    d_map = getDomainMap('textfile/domainList.txt')
    d_slink_map = getDomainSearchLinkMap('textfile/searchLink.txt')


    '''
        Object of xpath class
    '''

    xp = Xpath()
    xp.loadXpaths('textfile/xpath.txt', 'textfile/allDomain.txt' )


    sp = SearchResPage(xp)
    ir = IdentifyReview(xp)

    for el in productList:
        cat = el.getCatogary()


        '''
            Get all domain from which we have to find reviews.
        '''
        dset = set()
        if cat in d_map.keys():
            try:
                for domain in d_map[cat]:
                    dset.add(domain)
            except Exception:
                print 'no domain in catogary : ', cat
        else:
            for domain in d_map['others']:  # if no domain for product category website we take domain
                dset.add(domain)            # from other category

        for domain in d_map['all']:         # this category websites always included
            dset.add(domain)



        '''
             Search  Link for Domains
        '''
        s_link = []
        for dom in dset:
            s_link.append(d_slink_map[dom])


        ppUrlSet = set()
        for slink in s_link:
            plink_list = sp.getProductPageURLs(el.getTitle(), slink)
            for plink in plink_list:

                #if title and specification mached in this
                #link then add this link to file reviewurl.txt

                if ir.mach(el, plink):
                    ppUrlSet.add(plink)

        print '************ Mached Link ************'
        for link in ppUrlSet:
            print  link
        print '************ end ********************'

        #save mached link to file


if __name__ == '__main__':
	main()
