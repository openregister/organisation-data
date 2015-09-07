#!/usr/bin/env python3

import json
import requests
import time

# creates data from data.police.uk about police forces
# unfortunately this API seems to only cover England and Wales

FORCES_URL = 'https://data.police.uk/api/forces'
FORCE_URL_PATTERN = 'https://data.police.uk/api/forces/%s'
NEIGHBOURHOODS_URL_PATTERN = 'https://data.police.uk/api/%s/neighbourhoods'
NEIGHBOURHOOD_URL_PATTERN = 'https://data.police.uk/api/%s/%s'

FORCES_FILENAME = 'data/forces.jsonl'
NEIGHBOURHOODS_FILENAME = 'data/neighbourhoods.jsonl'
# LOCATIONS_FILENAME = 'data/locations.jsonl'

forces_resp = requests.get(FORCES_URL)

forces_file = open(FORCES_FILENAME, 'w')
neighbourhoods_file = open(NEIGHBOURHOODS_FILENAME, 'w')
# locations_file = open(LOCATIONS_FILENAME, 'w')

for raw_force in forces_resp.json():
    force_id = raw_force['id']

    # TODO: fetch more (website, description etc) from the forces API
    force = {
        'police-force': force_id,
        'name': raw_force['name']
    }
    force['police-force'] = force_id

    print("Processing force '%s'...\n" % force_id)

    forces_file.write(json.dumps(force))
    forces_file.write('\n')

    neighbourhoods_url = NEIGHBOURHOODS_URL_PATTERN % force_id
    neighbourhoods_resp = requests.get(neighbourhoods_url)

    for raw_neighbourhood in neighbourhoods_resp.json():
        neighbourhood_id = raw_neighbourhood['id']

        neighbourhood_url = NEIGHBOURHOOD_URL_PATTERN % \
            (force_id, neighbourhood_id)
        neighbourhood_json = requests.get(neighbourhood_url).json()

        neighbourhood = {
            'police-force-neighbourhood': force_id + '-' + neighbourhood_id,
            'police-force': force_id,
            'name': raw_neighbourhood['name'],
            'latitude':  neighbourhood_json['centre']['latitude'],
            'longitude': neighbourhood_json['centre']['longitude']
        }

        neighbourhoods_file.write(json.dumps(neighbourhood))
        neighbourhoods_file.write('\n')

        # for raw_location in neighbourhood_json['locations']:

        time.sleep(1)  # be nice, don't hammer the API

    forces_file.flush()
    neighbourhoods_file.flush()
    time.sleep(0.3)  # be nice, don't hammer the API
