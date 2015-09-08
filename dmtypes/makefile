XML = $(wildcard *.xml)
UML = $(wildcard *.uml)

HTML = $(XML:%.xml=%.html)
PNG = $(UML:%.uml=%.png)

DMDIR = $(HOME)/links/cwmp-ils

REPORT = report.pl
REPORTFLAGS += --include=$(DMDIR)

PLANTUMLCLIENT = plantumlclient

all: html png

html: $(HTML)

png: $(PNG)

clean:
	$(RM) $(HTML) $(PNG)

%.html: %.xml
	$(REPORT) $(REPORTFLAGS) --report=html $< --outfile=$@

%.png: %.uml
	$(PLANTUMLCLIENT) $<

.DELETE_ON_ERROR:
