#!/usr/bin/python
# coding: utf-8

import requests
from lxml import etree
from requests import Response

def parse_articles(fullUrl):
    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(fullUrl)  # type: Response
    tree = etree.HTML(item.content, myparser)
    columns = tree.xpath('//table[@class="articles"]/tr[@class="columns"]/th/text()')  # type: object

    # print descriptions
    theOutput = open('articles.out', 'a')
    theOutput.write('\n' + fullUrl + '\n')
    for description in columns:
        #    sDesc = description.decode('UTF-8')
        #    theOutput.write(sDesc)
        theOutput.write(description.strip()+';')

    theOutput.write('\n')
    numColumns = len(columns)
    # root.xpath(
    #     "//*[re:test(local-name(), '^TEXT.*')]",
    #     namespaces={'re': "http://exslt.org/regular-expressions"})

    articleNrs = tree.xpath('//table[@class="articles"]/tr[starts-with(@class,"stdrow")]/td/span/text()')

    # articleNr = tree.xpath('//table[@class="articles"]/tr[re:test(local-name(),".*stdrow1.*"])]/td/span/text()',
    #                        namespaces={'re': "http://exslt.org/regular-expressions"})

    # first all the rows
    rows = tree.xpath('//table[@class="articles"]/tr[starts-with(@class,"stdrow")]/td/text()')

    articlePos = 0
    presentColumn = 0
    if len(rows) == 1:
        theOutput.write("\nFound a single item\n")
    for row in rows:
        if presentColumn == 0:
            theOutput.write(articleNrs[articlePos] + ';')
            articlePos = articlePos + 1
        theOutput.write(row.strip() + ';')
        presentColumn = presentColumn + 1
        if presentColumn == numColumns - 1:
            theOutput.write('\n')
            presentColumn = 0


