PROTO = $(wildcard *.proto)

PROTOPY = $(PROTO:%.proto=%_pb2.py)

all: $(PROTOPY)

%_pb2.py: %.proto
	protoc --python_out=. $<

clean:
	$(RM) $(PROTOPY)
