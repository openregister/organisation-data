#!/usr/bin/env python3

"""Explode Opencharities CSV into entries charities"""

# data available from http://opencharities.org/charities.csv.zip
# see also https://countculture.wordpress.com/2010/09/06/introducing-open-charities-opening-up-the-charities-register/

import csv
import sys

reader = csv.DictReader(sys.stdin)

field_translation=[
    ['name','title'],
    ['charity','charity_number'],
    #'address':'address', # don't think we can easily link to address register
    ['company','company_number'],
    #'charity_classification_uids':'charity_tags', #???
    #['created_at': ''], #???
    ['start-date','date_registered'],
    ['end-date','date_removed']
]


def get_field(row, source):
    # hack for massaging particular fields
    if source == 'company_number':
        # pad with zeros to 8 chars to match company register
        company = row[source]
        if company == None or company == '':
            return company
        return company.zfill(8)
    return row[source]


def print_tsv_line(items):
    print("\t".join(items))


print_tsv_line([dest for dest,source in field_translation])

for num,row in enumerate(reader):
    print_tsv_line([get_field(row,source) for dest,source in field_translation])
