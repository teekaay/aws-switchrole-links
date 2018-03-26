PROJECT = aws_switchrole_links

test:
	nosetests

lint: 
	flake8 $(PROJECT) --exit-zero

clean:
	find . -name '*.pyc' -exec rm {} +
	find . -name '*.pyo' -exec rm {} +
	find . -name '__pycache__' -type d -exec rm -r {} +
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info