data/public-body: bin/importOrganisations.py
	bin/importOrganisations.py

#
#  code
#
init::
	pip3 install -r requirements.txt

flake8:
	flake8 bin

clean::
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
