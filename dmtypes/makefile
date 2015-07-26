XML = csda-example.xml flat-example.xml

HTML = $(XML:%.xml=%.html)

DMDIR = $(HOME)/links/cwmp-ils

REPORT = report.pl
REPORTFLAGS += --include=$(DMDIR)

all: html

html: $(HTML)

clean:
	$(RM) $(HTML)

%.html: %.xml
	$(REPORT) $(REPORTFLAGS) --report=html $< --outfile=$@

.DELETE_ON_ERROR:
