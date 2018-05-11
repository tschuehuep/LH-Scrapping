#!/usr/bin/python
# coding: utf-8

import requests
from lxml import etree
from requests import Response

def parse_categories(domain):
    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(
        'https://' + domain)  # type: Response
    tree = etree.HTML(item.content, myparser)
    # html.fromstring(kocher.content)
    categories = tree.xpath('//ul[@class="menuitems"]/li/p/a') # /li/p/a')  # type: object

    # print descriptions
    theOutput = open('categories.out', 'w')
    allCategories = []
    for category in categories:
        #    sDesc = description.decode('UTF-8')
        #    theOutput.write(sDesc)
        link = category.attrib['href']
        text = category.text
        allCategories.append({'link':link, 'text':text})
        theOutput.write("Remote <"+text + "> with the href: " + link + "\n")
    return allCategories