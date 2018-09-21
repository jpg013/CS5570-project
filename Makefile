# Makfile for project

run:
	python3 main.py

test:
	python -m unittest discover -s ./ -p '*_test.py'	

