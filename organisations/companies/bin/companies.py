#!/usr/bin/env python3

import sys
from datetime import datetime
import csv
from thingstance import Thing
from thingstance.representations.tsv import Writer

part = sys.argv[1]


def writer(register, fields=[]):
    path = 'data/%s/%s.tsv' % (register, part)
    stream = open(path, 'w')
    return Writer(stream, fieldnames=fields)


def iso_date(s):
    if not s:
        return None
    day, month, year = s.rsplit('/', 3)
    return datetime(int(year), int(month), int(day)).isoformat()


Company = Thing()
Company.yaml = open('cache/Company.yaml').read()

Address = Thing()
Address.yaml = open('cache/Address.yaml').read()

companies = writer('Company', Company.fields)
addresses = writer('Address', Address.fields)

reader = csv.DictReader(sys.stdin)
reader.fieldnames = [field.strip() for field in reader.fieldnames]

for row in reader:

    company = Thing()

    # CompanyName
    company.name = row['CompanyName']

    # CompanyNumber
    company.companyNumber = row['CompanyNumber']

    # RegAddress.CareOf
    # RegAddress.POBox
    # RegAddress.AddressLine1
    # RegAddress.AddressLine2
    # RegAddress.PostTown
    # RegAddress.County
    # RegAddress.Country
    # RegAddress.PostCode

    address = Thing()

    address.postOfficeBoxNumber = row['RegAddress.POBox']
    address.streetAddress = (row['RegAddress.CareOf'] +
                             row['RegAddress.AddressLine1'])
    address.addressRegion = row['RegAddress.AddressLine2']
    address.addressLocality = row['RegAddress.PostTown']
    address.postalCode = row['RegAddress.PostCode']
    address.addressCountry = row['RegAddress.Country']

    company.address = address.hash
    addresses.write(address)

    # CompanyCategory
    company.companyCategory = row['CompanyCategory']

    # CompanyStatus

    # CountryOfOrigin
    company.addressCountry = row['CountryOfOrigin']

    # DissolutionDate
    company.dissolutionDate = iso_date(row['DissolutionDate'])

    # IncorporationDate
    company.foundingDate = iso_date(row['IncorporationDate'])

    #
    #  accounts, returns, mortgages and partnerships feel like separate things
    #

    # Accounts.AccountRefDay
    # Accounts.AccountRefMonth
    # Accounts.NextDueDate
    # Accounts.LastMadeUpDate
    # Accounts.AccountCategory

    # Returns.NextDueDate
    # Returns.LastMadeUpDate

    # Mortgages.NumMortCharges
    # Mortgages.NumMortOutstanding
    # Mortgages.NumMortPartSatisfied
    # Mortgages.NumMortSatisfied

    # SICCode.SicText_1
    # SICCode.SicText_2
    # SICCode.SicText_3
    # SICCode.SicText_4

    # LimitedPartnerships.NumGenPartners
    # LimitedPartnerships.NumLimPartners

    # URI
    company.sameAs = row['URI']

    #
    #  could possibly be used to create previous versions of a company
    #

    # PreviousName_1.CONDATE
    # PreviousName_1.CompanyName

    # PreviousName_2.CONDATE
    # PreviousName_2.CompanyName

    # PreviousName_3.CONDATE
    # PreviousName_3.CompanyName

    # PreviousName_4.CONDATE
    # PreviousName_4.CompanyName

    # PreviousName_5.CONDATE
    # PreviousName_5.CompanyName

    # PreviousName_6.CONDATE
    # PreviousName_6.CompanyName

    # PreviousName_7.CONDATE
    # PreviousName_7.CompanyName

    # PreviousName_8.CONDATE
    # PreviousName_8.CompanyName

    # PreviousName_9.CONDATE
    # PreviousName_9.CompanyName

    # PreviousName_10.CONDATE
    # PreviousName_10.CompanyName

    companies.write(company)

companies.close()
addresses.close()
