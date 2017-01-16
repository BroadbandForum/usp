# Copyright 2017 ARRIS Enterprises, LLC.

PROTO = $(wildcard *.proto)

PROTOPY = $(PROTO:%.proto=%_pb2.py)

all: $(PROTOPY)

init:
	pip install --upgrade pip
	pip install -r requirements.txt

schema:
	protoc --proto_path=. --python_out=. usp.proto

test:
	python test.py

%_pb2.py: %.proto
	protoc --python_out=. $<

clean:
	$(RM) $(PROTOPY)
