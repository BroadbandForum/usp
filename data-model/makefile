UML = $(wildcard *.uml)
PNG = $(UML:%.uml=%.png)

PLANTUMLCLIENT = plantumlclient

all: png

png: $(PNG)

clean:
	$(RM) $(PNG)

%.png: %.uml
	$(PLANTUMLCLIENT) $<

.DELETE_ON_ERROR:
