#!/usr/bin/python
# coding: utf-8

import sqlite3

def print_categories():
    db = sqlite3.connect('data/mydb')
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT categoryId, parentId, name FROM categories''')
    for row in cursor:
        # row[0] returns the first column in the query (categoryId), row[1] returns parentID column.
        print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
    db.close()

def insert_category(category):
    db = sqlite3.connect('data/mydb')
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''INSERT INTO categories(categoryId, parentID, name)
                  VALUES(:categoryId,:parentID, :name)''',
                   # {'categoryId': subCategoryId, 'parentID': mainCategory['categoryId'], 'name': textForCSV})
                   category)
    db.close()