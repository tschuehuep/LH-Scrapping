#!/usr/bin/python
# coding: utf-8

from scrapcategories import parse_categories
from scrapdescription import parse_description
from scraparticles import parse_articles
import requests
from lxml import etree
from requests import Response

# Finds the subcategories which are found on the relative Url, relative to https://domain
def parse_subcategories(mainCategory, domain):
    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(
        'https://' + domain + mainCategory['link'])  # type: Response
    tree = etree.HTML(item.content, myparser)
    subCategories = tree.xpath('//a[@class="anav"]') # /li/p/a')  # type: object

    theOutput = open('subCategories.out', 'a')
    allSubCategories = []
    for subCategory in subCategories:
        link = subCategory.attrib['href']
        text = mainCategory['text'] + "/" + subCategory.text.strip()
        allSubCategories.append({'link':link, 'text':text})
#        theOutput.write("<" + text  +"> with the href: " + link + "\n")
    if allSubCategories:
        theOutput.write("found subcategories, recursing")
        for subCategory in allSubCategories:
            parse_subcategories(subCategory,domain)
    else:
        theOutput.write("<got to the end>\n")
        theOutput.write("<" + mainCategory['text']  +"> with the href: " + mainCategory['link'] + "\n")
        parse_description("https://" + domain + mainCategory['link'])
        parse_articles("https://" + domain + mainCategory['link'])
    theOutput.close()
    return []

theOutput = open('articles.out', 'w')
theOutput.write('Another try\n')
theOutput.close()
theOutput = open('description.out', 'w')
theOutput.write('Another try\n')
theOutput.close()
theOutput = open('subCategories.out', 'w')
theOutput.write('Another try\n')
theOutput.close()
myurl = input("which url?")
allMainCategories = parse_categories(myurl)
# for mainCategory in allMainCategories :
#     allSubCategories = parse_subcategories(mainCategory)
parse_subcategories(allMainCategories[4],myurl)
