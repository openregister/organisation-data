#!/usr/bin/env python3

import sys
import json
from entry import Entry
from entry.representations.tsv import Writer

writer = Writer(sys.stdout, fieldnames=[
    'id',
    'name',
    'latitude',
    'longitude',
    'streetAddress',
    'addressLocality',
    'addressRegion',
    'postalCode',
    'AddressCountry',
    'facility',
    'type'])

# 'longitude',
# 'image_file',
# 'postalAddress_streetAddress',
# 'postalAddress_postTown',
# 'postalAddress_county',
# 'postalAddress_postalCode',
# 'postalAddress_country',
# 'visitingAddress_streetAddress',
# 'visitingAddress_',
# 'visitingAddress_county',
# 'visitingAddress_postalCode',
# 'visitingAddress_country',
# 'facility',
# 'alert',
# 'lawType',
# 'courtType'])

for row in json.load(sys.stdin):

    entry = Entry()

    entry.id = str(row['slug'])

    if entry.id != "barnstaple-magistrates-court-north-and-east-devon":

        entry.name = str(row['name'])
        entry.facility = ""
        # entry.lawType = ""
        entry.type = ""
        # entry.image_file = ""
        # entry.alert = ""

        if 'lat' in row:
            entry.latitude = str(row['lat'])
            entry.longitude = str(row['lon'])

        # https://courtfinder-servicegovuk-production.s3.amazonaws.com/images/
        # if 'image_file' in row:
        #    entry.image_file = str(row['image_file'])

        # get address data for this row
        jData = row.get("addresses")

        # loop address data
        for rowX in jData:
            # create links to address

            tmpAddress = ""

            if rowX.get("type") == "Visting":
                # entry.visitingAddress_streetAddress = rowX.get("address")

                # tmpAddress = entry.visitingAddress_streetAddress
                # tmpAddress = tmpAddress.replace('\n', ' ').replace('\r', '')
                # entry.visitingAddress_streetAddress = tmpAddress

                # entry.visitingAddress_postTown = rowX.get("town")
                # entry.visitingAddress_county = rowX.get("county")
                # entry.visitingAddress_postalCode = rowX.get("postcode")
                # entry.visitingAddress_country = ""

                entry.streetAddress = rowX.get("address")

                tmpAddress = entry.streetAddress
                tmpAddress = tmpAddress.replace('\n', ' ').replace('\r', '')
                entry.streetAddress = tmpAddress

                entry.addressLocality = rowX.get("town")
                entry.addressRegion = rowX.get("county")
                entry.postalCode = rowX.get("postcode")
                entry.addressCountry = ""

            elif rowX.get("type") == "Postal":

                # entry.postalAddress_streetAddress = rowX.get("address")
                # tmpAddress = entry.postalAddress_streetAddress
                # tmpAddress = tmpAddress.replace('\n', ' ').replace('\r', '')
                # entry.postalAddress_streetAddress = tmpAddress

                # entry.postalAddress_postTown = rowX.get("town")
                # entry.postalAddress_county = rowX.get("county")
                # entry.postalAddress_postalCode = rowX.get("postcode")
                # entry.postalAddress_country = ""
                entry.addressCountry = ""

            # end if

        # end for

        # get facility data for this row
        jData = row.get("facilities")

        # loop facility data for this row
        for rowX in jData:
            # create list type
            if entry.facility != "":
                entry.facility = entry.facility + ","
            # end if

            entry.facility = entry.facility + rowX.get("name")

        entry.facility = entry.facility.replace('\n', '').replace('\r', '')
        entry.facility = entry.facility.replace('<p>', '').replace('</p>', '')

        # end for

        # # get law type data for this row
        # jData = row.get("areas_of_law")

        # # loop law type data for this row
        # for rowX in jData:

        #    # create list type
        #    if entry.lawType != "":
        #        entry.lawType = entry.lawType + ","
        #    # end if

        #   entry.lawType = entry.lawType + rowX.get("name")

        # entry.lawType = entry.lawType.replace('\n', '').replace('\r', '')

        # # end for

        # # get court type data for this row
        jData = row.get("court_types")

        # loop court type data for this row
        for rowX in jData:
            # create list type
            if entry.type != "":
                entry.type = entry.type + ","
            # end if

            entry.type = entry.type + rowX

        # end for

        # entry.alert = row.get("alert")

        try:
            writer.write(entry)
        except:
            pass

    # end for

writer.close()
