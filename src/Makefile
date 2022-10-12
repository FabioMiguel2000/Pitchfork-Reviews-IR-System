# Makefile

#all: refine

# Notes: after adding 'data_visualization.py', 
# uncomment the lines below and remove the first line of code 'all: refine'

all: visualize

visualize: refine
 	jupyter notebook scripts/data_visualization.ipynb

refine: merge
	./venv/bin/python3 scripts/data_cleaning.py

merge: setup
	./venv/bin/python3 scripts/merge_data.py

setup:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf reviews.json clean_reviews.json

.PHONY: clean
