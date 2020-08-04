# Copyright 2017 ARRIS Enterprises, LLC.

# this is the new makefile
TOPDIR = ..
include $(TOPDIR)/rules.mk

# this is the old makefile (edited to work with the new one)
PIP = pip		# or sudo python3 -m pip or ...
PYTHON = python		# or python2 or python3 or ...
PROTOC = protoc

PROTO = $(wildcard *.proto)

PROTOPY = $(PROTO:%.proto=%_pb2.py)

init:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

schema: $(PROTOPY)

test:
	$(PYTHON) test.py

%_pb2.py: %.proto
	$(PROTOC) --proto_path=. --python_out=. $<

CLEAN += $(PROTOPY)

