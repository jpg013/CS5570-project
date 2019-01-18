# Makfile for project

run:
	python main.py

test:
	python -m unittest discover -s ./tests -p '*_test.py'