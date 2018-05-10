#!/usr/bin/python
# coding: utf-8

import requests
from lxml import etree
from requests import Response

myparser = etree.HTMLParser(encoding="utf-8")
item = requests.get(
    #    'https://www.lankhorst-hohorst.de/Katalog/Kochen+und+K%c3%bchlen/Gaskocher/Eno/Bootskocher+Atoll/Produkt.aspx')  # type: Response
    'https://www.lankhorst-hohorst.de/Katalog/Wasser+und+Tanksysteme/Kraftstoffpumpen/Marco/Dieselpumpen/Produkt.aspx')  # type: Response
tree = etree.HTML(item.content, myparser)
# html.fromstring(kocher.content)
descriptions = tree.xpath('//div[@id="descriptioncontent"]/text()')  # type: object

# print descriptions
theOutput = open('description.out', 'w')
for description in descriptions:
    #    sDesc = description.decode('UTF-8')
    #    theOutput.write(sDesc)
    theOutput.write(description)
