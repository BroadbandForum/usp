XML = $(wildcard *.xml)
TXT = $(wildcard *.txt)

HTML = $(XML:%.xml=%.html)
PNG = $(TXT:%.txt=%.png)

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

%.png: %.txt
	$(PLANTUMLCLIENT) $<

.DELETE_ON_ERROR:
