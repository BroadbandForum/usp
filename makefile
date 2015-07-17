YANG = Device.yang STBService.yang StorageService.yang

TREE = $(YANG:%.yang=%.tree)

DMDIR = $(HOME)/links/cwmp-ils
YANGDIR = $(HOME)/Documents/bbf/Standards/WT-355/bbf/modules/standard

REPORT = report.pl
REPORTFLAGS += --quiet
REPORTFLAGS += --include=$(DMDIR)
REPORTFLAGS += --plugin=dm2yang --report=dm2yang

RFCSTRIP = rfcstrip

YANGRULE = $(REPORT) $(REPORTFLAGS) $< | $(RFCSTRIP)

PYANG = pyang
PYANGFLAGS = --path=$(YANGDIR)

TREERULE = $(PYANG) --path=$(YANGDIR) --format=tree $< >$@

VPATH = $(DMDIR)

all: tree

tree: $(TREE)

clean:
	$(RM) $(YANG) $(TREE)

Device.yang: tr-181-2-10.xml dm2yang.pm
	$(YANGRULE)

STBService.yang: tr-135-1-4.xml dm2yang.pm
	$(YANGRULE)

StorageService.yang: tr-140-1-2.xml dm2yang.pm
	$(YANGRULE)

%.tree: %.yang
	-$(TREERULE)

.DELETE_ON_ERROR:
