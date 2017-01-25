XML = $(filter-out %-full.xml,$(wildcard *.xml))

HTML = $(XML:%.xml=%.html) $(XML:%.xml=%-diffs.html)

FULL = $(XML:%.xml=%-full.xml)

SCHEMADIR = ../schema

# XXX this is user-specific
DMDIR = $(HOME)/links/cwmp-ils

# XXX this assumes it's in the path; should use an
#     assumed relative location for the report tool
#     and the published data models
REPORT = report.pl
REPORTFLAGS += --include=$(SCHEMADIR)
REPORTFLAGS += --include=$(DMDIR)

all: html full

html: $(HTML)

full: $(FULL)

clean:
	$(RM) $(HTML)

%.html: %.xml
	$(REPORT) $(REPORTFLAGS) --report=html $< --outfile=$@

%-diffs.html: %.xml
	$(REPORT) $(REPORTFLAGS) --report=html --lastonly $< --outfile=$@

%-full.xml: %.xml
	$(REPORT) $(REPORTFLAGS) --report=xml $< --outfile=$@

.DELETE_ON_ERROR:
