#!/usr/bin/env python3
# File to retrieve organisations list from the json api url and produce a file
# that we find useful.

import urllib.request as ul
import json
import codecs
from entry.representations.tsv import Writer
from entry import Entry

# official branding colour map for ministerial some depts.
colour_map = {}
colour_map['attorney-generals-office'] = '#9f1888'
colour_map['cabinet-office'] = '#005abb'
colour_map['civil-service'] = '#af292e'
colour_map['department-for-business-innovation-skills'] = '#003479'
colour_map['department-for-communities-and-local-government'] = '#00857e'
colour_map['department-for-culture-media-sport'] = '#d40072'
colour_map['department-for-education'] = '#003a69'
colour_map['department-for-environment-food-rural-affairs'] = '#898700'
colour_map['department-for-international-development'] = '#002878'
colour_map['department-for-transport'] = '#006c56'
colour_map['department-for-work-pensions'] = '#00beb7'
colour_map['department-of-energy-climate-change'] = '#009ddb'
colour_map['department-of-health'] = '#00ad93'
colour_map['foreign-commonwealth-office'] = '#003e74'
colour_map['hm-government'] = '#0076c0'
colour_map['hm-revenue-customs'] = '#009390'
colour_map['hm-treasury'] = '#af292e'
colour_map['home-office'] = '#9325b2'
colour_map['ministry-of-defence'] = '#4d2942'
colour_map['ministry-of-justice'] = '#231f20'
colour_map['northern-ireland-office'] = '#002663'
colour_map['office-of-the-advocate-general-for-scotland'] = '#002663'
colour_map['office-of-the-leader-of-the-house-of-lords'] = '#9c132e'
colour_map['scotland-office'] = '#002663'
colour_map['the-office-of-the-leader-of-the-house-of-commons'] = '#317023'
colour_map['uk-export-finance'] = '#005747'
colour_map['uk-trade-investment'] = '#C80651'
colour_map['wales-office'] = '#a33038'

# logo lookup map for ministerial departments only
crest_map = {}
crest_map['prime-ministers-office-10-downing-street'] = 'org-crest'
crest_map['attorney-generals-office'] = 'org-crest'
crest_map['cabinet-office'] = 'org-crest'
crest_map['department-for-business-innovation-skills'] = 'bis_crest'
crest_map['department-for-communities-and-local-government'] = 'org-crest'
crest_map['department-for-culture-media-sport'] = 'org-crest'
crest_map['department-for-education'] = 'org-crest'
crest_map['department-for-environment-food-rural-affairs'] = 'org-crest'
crest_map['department-for-international-development'] = 'org-crest'
crest_map['department-for-transport'] = 'org-crest'
crest_map['department-for-work-pensions'] = 'org-crest'
crest_map['department-of-energy-climate-change'] = 'org-crest'
crest_map['department-of-health'] = 'org-crest'
crest_map['foreign-commonwealth-office'] = 'org-crest'
crest_map['hm-treasury'] = 'org-crest'
crest_map['home-office'] = 'home-office-crest'
crest_map['ministry-of-defence'] = 'mod_crest'
crest_map['ministry-of-justice'] = 'org-crest'
crest_map['northern-ireland-office'] = 'org-crest'
crest_map['office-of-the-advocate-general-for-scotland'] = 'scotland-office-crest'
crest_map['the-office-of-the-leader-of-the-house-of-commons'] = 'portcullis-crest'
crest_map['office-of-the-leader-of-the-house-of-lords'] = 'portcullis-crest'
crest_map['scotland-office'] = 'scotland-office-crest'
crest_map['uk-export-finance'] = 'org-crest'
crest_map['wales-office'] = 'wales_crest'

def array_to_string(arr, pre_process):
  res = ""
  first = True
  for i in arr:
    if first:
      first = False
    else:
      res += ";"
    res += pre_process(i)
  return res

def json_from_url(url):
  input = ul.urlopen(url)
  charset = input.info().get_param('charset', 'utf8')
  text = input.read()
  input.close()

  return json.loads(text.decode(charset))

def init_output():
  output = codecs.open('data/public-body.tsv', encoding='utf-8', mode='w')
  writer = Writer(output, fieldnames = ['public-body', 'name', 'website', 'public-body-type', 'parent-bodies', 'text', 'crest', 'official-colour'])

  return writer

def write_records_to(records, output):
  written_ids = []
  for result in records['results']:
    entry = Entry()
    detailsJson = result['details']

    id = detailsJson['slug']
    setattr(entry, 'public-body', id)
    entry.name = result['title'].replace('\t', ' ')
    entry.website = result['id'].replace('\t', ' ')
    setattr(entry, 'public-body-type', result['format'].replace('\t', ' '))
    setattr(entry, 'parent-bodies', array_to_string(result['parent_organisations'],
      lambda x: x['id']))
    entry.text = ''

    if id in crest_map:
      entry.crest = crest_map[id]
    else:
      entry.crest = ''

    if id in colour_map:
      setattr(entry, 'official-colour', colour_map[id])
    else:
      setattr(entry, 'official-colour', '')

    if id not in written_ids:
      output.write(entry)
      written_ids.append(id)

#print "%s\n" % parser.getAnchorMap()
next_page = "https://www.gov.uk/api/organisations?page=1"
output = init_output()

while(next_page is not None):
  print("Processing page url: %s" % (next_page))
  jsonRes = json_from_url(next_page)
  write_records_to(jsonRes, output)
  if 'next_page_url' in jsonRes:
    next_page = jsonRes['next_page_url']
  else:
    next_page = None

output.close()

