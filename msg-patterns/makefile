UML = $(wildcard *.txt)
PNG = $(UML:%.txt=%.png)

PLANTUMLCLIENT = plantumlclient

all: png

png: $(PNG)

clean:
	$(RM) $(PNG)

%.png: %.txt
	$(PLANTUMLCLIENT) $<

.DELETE_ON_ERROR:
