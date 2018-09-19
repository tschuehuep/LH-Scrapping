#!/usr/bin/python
# coding: utf-8

from scrapcategories import parse_categories
from scrapdescription import parse_description
from scraparticles import parse_articles
import requests
import csv
from lxml import etree
from requests import Response
import sqlite3



# Finds the subcategories which are found on the relative Url, relative to https://domain
def parse_subcategories(mainCategory, domain):
    # Creates or opens a file called mydb with a SQLite3 DB
    db = sqlite3.connect('data/mydb')
    # Get a cursor object
    cursor = db.cursor()
    myparser = etree.HTMLParser(encoding="utf-8")
    item = requests.get(
        'https://' + domain + mainCategory['link'])  # type: Response
    tree = etree.HTML(item.content, myparser)
    subCategories = tree.xpath('//a[@class="anav"]') # /li/p/a')  # type: object

    theOutput = open('subCategories.out', 'a')
    allSubCategories = []
    allCategoriesForCSV = []
    subCategoryId = int(mainCategory['categoryId']) * 10
    for subCategory in subCategories:
        link = subCategory.attrib['href']
        textForCSV = subCategory.text.strip()
        text = mainCategory['text'] + "/" + textForCSV
        allSubCategories.append({'link':link, 'text':text, 'categoryId':str(subCategoryId)})
        theOutput.write("<" + text  +"> with the href: " + link + "\n")
        we have too many subcategories, so we have to have a 2 digit subcategory id, at least at some point
        allCategoriesForCSV.append(
            {'categoryId': str(subCategoryId), 'parentID': mainCategory['categoryId'], 'name': textForCSV, 'active': str(1)})
        cursor.execute('''INSERT INTO categories(categoryId, parentId, name)
                      VALUES(:categoryId,:parentId, :name)''',
                       {'categoryId': subCategoryId, 'parentId': mainCategory['categoryId'], 'name': textForCSV})
        db.commit()
        subCategoryId = subCategoryId + 1


    if allSubCategories:
        with open(file='categories.csv', mode='a', encoding='UTF-8') as csvfile:
            fieldnames = ['categoryId', 'parentID', 'name', 'position', 'metatitle', 'metakeywords', 'metadescription',
                          'cmsheadline', 'cmstext', 'template', 'active', 'blog', 'external', 'hidefilter',
                          'attribute_attribute1', 'attribute_attribute2', 'attribute_attribute3', 'attribute_attribute4',
                          'attribute_attribute5', 'attribute_attribute6', 'CustomerGroup']
            filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            filewriter.writerows(allCategoriesForCSV)
        theOutput.write("found subcategories, recursing")
        for subCategory in allSubCategories:
            parse_subcategories(subCategory,domain)
    else:
        theOutput.write("<got to the end>\n")
        # we dont need to make a category for the leaf
        # theOutput.write("<" + mainCategory['text']  +"> with the href: " + mainCategory['link'] + "\n")
        # completeDescription = parse_description("https://" + domain + mainCategory['link'],mainCategory['categoryId'])
        # with open(file='categories.csv', mode='a', encoding='UTF-8') as csvfile:
        #     fieldnames = ['categoryId', 'parentID', 'name', 'position', 'metatitle', 'metakeywords', 'metadescription',
        #                   'cmsheadline', 'cmstext', 'template', 'active', 'blog', 'external', 'hidefilter',
        #                   'attribute_attribute1', 'attribute_attribute2', 'attribute_attribute3', 'attribute_attribute4',
        #                   'attribute_attribute5', 'attribute_attribute6', 'CustomerGroup']
        #     filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     singleCategory = {'categoryId': mainCategory['categoryId'], 'parentID':"not known", 'name': mainCategory['text'],
        #                       'active': str(1),'cmstext':completeDescription}
        #     filewriter.writerow(singleCategory)

        # don't parse articles while testing categories
        # parse_articles("https://" + domain + mainCategory['link'])
    theOutput.close()
    db.commit()
    cursor.execute('''SELECT categoryId, parentId, name FROM categories''')
    for row in cursor:
        # row[0] returns the first column in the query (categoryId), row[1] returns parentId column.
        print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
    db.close()
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
#for mainCategory in allMainCategories :
#    allSubCategories = parse_subcategories(mainCategory,myurl)
parse_subcategories(allMainCategories[4],myurl)
csvfile.close()