.PHONY: schema

init:
	pip install --upgrade pip
	pip install -r requirements.txt

dirs:
	mkdir -p logs

test:
	nose2 --with-coverage

test-verbose:
	nose2 -v --with-coverage

lint:
	find mtp_proxy -name "*.py" | xargs pylint || :

run:
	python3 -m mtp_proxy.proxy
