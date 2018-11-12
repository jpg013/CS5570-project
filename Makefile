# Makfile for project

run:
	python3 main.py

test:
	python3 -m unittest discover -s ./tests -p '*_test.py'	

