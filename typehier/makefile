XML = $(wildcard *.xml)

HTML = $(XML:%.xml=%.html)
TEXT = $(XML:%.xml=%.txt)

DMDIR = $(HOME)/links/cwmp-ils

REPORT = report.pl
REPORTFLAGS += --include=$(DMDIR)
REPORTFLAGS += --showunion 
REPORTFLAGS += --quiet 

all: html text

html: $(HTML)

text: $(TEXT)

clean:
	$(RM) $(HTML) $(TEXT)

%.html: %.xml
	$(REPORT) $(REPORTFLAGS) --report=html $< --outfile=$@

%.txt: %.xml
	$(REPORT) $(REPORTFLAGS) --report=text $< --outfile=$@

.DELETE_ON_ERROR:
