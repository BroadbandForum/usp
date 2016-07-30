XML = $(wildcard *.xml)

HTML = $(XML:%.xml=%.html) $(XML:%.xml=%-diffs.html)

# XXX this is user-specific
DMDIR = $(HOME)/links/cwmp-ils

# XXX this assumes it's in the path; should use an
#     assumed relative location for the report tool
#     and the published data models
REPORT = report.pl
REPORTFLAGS += --include=$(DMDIR)

all: html 

html: $(HTML)

clean:
	$(RM) $(HTML)

%.html: %.xml
	$(REPORT) $(REPORTFLAGS) --report=html $< --outfile=$@

%-diffs.html: %.xml
	$(REPORT) $(REPORTFLAGS) --report=html --lastonly $< --outfile=$@

.DELETE_ON_ERROR:
