check:
	flake8 src
	mypy src
	PYTHONPATH=./src:$PYTHONPATH python -m pytest --cov=flake_master --cov-report=xml -p no:warnings --disable-socket
