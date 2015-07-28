#
#  generate openregister entries from Court Finder open data
#
#  https://courttribunalfinder.service.gov.uk/api.html
#
COURTFINDER_URL=https://courttribunalfinder.service.gov.uk/courts.json

COURTS_DATA=\
	data/Court/courts.tsv

#
#  Register information from the register.register
#
REGISTER_URL=https://raw.githubusercontent.com/openregister/register.register/master/data/Register
REGISTERS=\
	cache/Court.yaml\
	cache/Address.yaml

COUNTRY_URL=https://raw.githubusercontent.com/openregister/country.register/master/data/Country/countries.yaml
COUNTRIES=\
	cache/countries.yaml

.PHONY: all flake8 prune out

all:	flake8 $(COURTS_DATA)

#
#  Court entries
#  - also generates Address
#
data/Court/courts.tsv:	cache/courts.json bin/courts.py $(REGISTERS) $(COUNTRIES)
	@mkdir -p data/Court data/Address
	cat cache/courts.json | bin/courts.py > $@

#
#  download data
#
cache/courts.json:;	mkdir -p cache && curl -s "$(COURTFINDER_URL)" > $@

#
#  registers
#
cache/Court.yaml:;	mkdir -p cache && curl -L -s "$(REGISTER_URL)/Court.yaml" > $@
cache/Address.yaml:;	mkdir -p cache && curl -L -s "$(REGISTER_URL)/Address.yaml" > $@

#
#  country codes
#
cache/countries.yaml:;	mkdir -p cache && curl -L -s "$(COUNTRY_URL)" > $@

#
#  clean
#
prune::
	rm -rf cache data

clean::
	rm -rf $(REGISTERS) $(COUNTRIES) data

#
#  python
#
init::
	pip3 install -r requirements.txt

upgrade:
	pip3 install --upgrade -r requirements.txt

flake8::
	flake8 bin

