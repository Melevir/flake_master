check:
	flake8 flake_master
	mypy flake_master
	python -m pytest --cov=flake_master --cov-report=xml -p no:warnings --disable-network
	safety check -r requirements_dev.txt
	mdl README.md
