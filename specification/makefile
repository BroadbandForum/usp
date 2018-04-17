# Copyright 2017 ARRIS Enterprises, LLC.

PIP = pip		# or sudo python3 -m pip or ...
PYTHON = python		# or python2 or python3 or ...
PROTOC = protoc

PROTO = $(wildcard *.proto)

PROTOPY = $(PROTO:%.proto=%_pb2.py)

all: $(PROTOPY)

init:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

schema: $(PROTOPY)

test:
	$(PYTHON) test.py

%_pb2.py: %.proto
	$(PROTOC) --proto_path=. --python_out=. $<

clean:
	$(RM) $(PROTOPY)
