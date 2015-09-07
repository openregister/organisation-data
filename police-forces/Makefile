FORCES_DATA=data/forces.jsonl

.PHONY: all clean flake8 init upgrade

all:	flake8 $(FORCES_DATA)

clean::
	rm -rf data

$(FORCES_DATA): bin/forces.py
	@mkdir -p data
	bin/forces.py

#
#  python
#
init::
	pip3 install -r requirements.txt

upgrade:
	pip3 install --upgrade -r requirements.txt

flake8::
	flake8 bin

