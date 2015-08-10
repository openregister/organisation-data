#
#  generate openregister entries from Companies House open data
#
#
#  Companies House "free" data, see:
#  http://download.companieshouse.gov.uk/en_output.html
#
DATE=2015-08-01
URL_PREFIX=http://download.companieshouse.gov.uk/BasicCompanyData-$(DATE)-part
URL_SUFFIX=_5.zip

COMPANIES_DATA=\
	data/Company/part1.tsv\
	data/Company/part2.tsv\
	data/Company/part3.tsv\
	data/Company/part4.tsv\
	data/Company/part5.tsv

#
#  Register information from the register.register
#
REGISTER_URL=https://raw.githubusercontent.com/openregister/registers/master/data/Register
REGISTERS=\
	cache/company.yaml\
	cache/address.yaml

COUNTRY_URL=https://raw.githubusercontent.com/openregister/locations/master/country/data/Country/countries.tsv
COUNTRIES=\
	cache/countries.tsv

.PHONY: all flake8 prune out

all:	flake8 $(COMPANIES_DATA)

#
#  Company entries
#  - also generates Address and CompanyCategory
#
data/Company/part1.tsv:	cache/part1.zip bin/companies.py $(REGISTERS) $(COUNTRIES)
	@mkdir -p data/Company data/Address
	funzip cache/part1.zip | bin/companies.py part1

data/Company/part2.tsv:	cache/part2.zip bin/companies.py $(REGISTERS) $(COUNTRIES)
	@mkdir -p data/Company data/Address
	funzip cache/part2.zip | bin/companies.py part2

data/Company/part3.tsv:	cache/part3.zip bin/companies.py $(REGISTERS) $(COUNTRIES)
	@mkdir -p data/Company data/Address
	funzip cache/part3.zip | bin/companies.py part3

data/Company/part4.tsv:	cache/part4.zip bin/companies.py $(REGISTERS) $(COUNTRIES)
	@mkdir -p data/Company data/Address
	funzip cache/part4.zip | bin/companies.py part4

data/Company/part5.tsv:	cache/part5.zip bin/companies.py $(REGISTERS) $(COUNTRIES)
	@mkdir -p data/Company data/Address
	funzip cache/part5.zip | bin/companies.py part5


#
#  download data
#
cache/part1.zip:;	mkdir -p cache && curl -s "$(URL_PREFIX)1$(URL_SUFFIX)" > $@
cache/part2.zip:;	mkdir -p cache && curl -s "$(URL_PREFIX)2$(URL_SUFFIX)" > $@
cache/part3.zip:;	mkdir -p cache && curl -s "$(URL_PREFIX)3$(URL_SUFFIX)" > $@
cache/part4.zip:;	mkdir -p cache && curl -s "$(URL_PREFIX)4$(URL_SUFFIX)" > $@
cache/part5.zip:;	mkdir -p cache && curl -s "$(URL_PREFIX)5$(URL_SUFFIX)" > $@

#
#  registers
#
cache/company.yaml:;	mkdir -p cache && curl -L -s "$(REGISTER_URL)/company.yaml" > $@
cache/address.yaml:;	mkdir -p cache && curl -L -s "$(REGISTER_URL)/address.yaml" > $@

#
#  country codes
#
cache/countries.tsv:;	mkdir -p cache && curl -L -s "$(COUNTRY_URL)" > $@

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

