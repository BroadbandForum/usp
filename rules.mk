# defs.mk must already have been included

ifeq "$(origin TARGETS)" "undefined"
  TARGETS := $(TREE)
endif

# XXX there must be a cleaner way of handling TARGETDIR
PDF  := $(PDF:%=$(TARGETDIR)%)
PNG  := $(PNG:%=$(TARGETDIR)%)
PNGLAST := $(PNGLAST:%=$(TARGETDIR)%)
TREE := $(TREE:%=$(TARGETDIR)%)
UML  := $(UML:%=$(TARGETDIR)%)
TARGETS := $(TARGETS:%=$(TARGETDIR)%)

# XXX should add all the phony targets

all: $(SUBDIRS:%=all.%) $(TARGETS)

$(SUBDIRS:%=all.%): all.%: %
	$(MAKE) -C $* all

png: $(SUBDIRS:%=png.%) $(PNG)

$(SUBDIRS:%=png.%): png.%: %
	$(MAKE) -C $* png

pdf: $(SUBDIRS:%=pdf.%) $(PDF)

$(SUBDIRS:%=pdf.%): pdf.%: %
	$(MAKE) -C $* pdf

tree: $(SUBDIRS:%=tree.%) $(TREE)

$(SUBDIRS:%=tree.%): tree.%: %
	$(MAKE) -C $* tree

uml: $(SUBDIRS:%=uml.%) $(UML)

$(SUBDIRS:%=uml.%): uml.%: %
	$(MAKE) -C $* uml

# XXX restore this if plantuml server and client aren't available
#$(TARGETDIR)%.png: %.uml
#	$(PLANTUML) -p <$< >$@

$(TARGETDIR)%.png: $(TARGETDIR)%.uml
	plantumlclient $<

# XXX this assumes that PDF is just one file
$(PDF): $(PNG)
	$(CONVERT) $(filter-out $(PNGLAST), $^) $(PNGLAST) $@

$(TARGETDIR)%.tree: %.yang
	$(PYANG) $(PYANGFLAGS) $(PYANGTREEFLAGS) $< >$@

$(TARGETDIR)%.2.tree: %.yang
	$(PYANG) $(PYANGFLAGS) $(PYANGTREEFLAGS) $(PYANGTREE2FLAGS) $< >$@

$(TARGETDIR)%.3.tree: %.yang
	$(PYANG) $(PYANGFLAGS) $(PYANGTREEFLAGS) $(PYANGTREE3FLAGS) $< >$@

$(TARGETDIR)%.4.tree: %.yang
	$(PYANG) $(PYANGFLAGS) $(PYANGTREEFLAGS) $(PYANGTREE4FLAGS) $< >$@

$(TARGETDIR)%.uml: %.yang
	$(PYANG) $(PYANGFLAGS) $(PYANGUMLFLAGS) $< >$@

clean: $(SUBDIRS:%=clean.%)
	$(RM) $(TARGETS) $(CLEAN)

$(SUBDIRS:%=clean.%): clean.%: %
	$(MAKE) -C $* clean

distclean: $(SUBDIRS:%=distclean.%)
	$(RM) $(TARGETS) $(UML) $(PNG) $(PDF) $(DEPS) $(CLEAN) $(DISTCLEAN)

$(SUBDIRS:%=distclean.%): distclean.%: %
	$(MAKE) -C $* distclean

# dependencies
TARGTYPES = png tree uml
DEPS = $(YANG:%.yang=$(TARGETDIR)%.dep)

-include $(DEPS)

$(DEPS): $(TARGETDIR)%.dep: %.yang
	$(PYANG) $(PYANGFLAGS) $(PYANGDEPENDFLAGS) \
	  --depend-target="$(TARGTYPES:%=$(TARGETDIR)$*.%)" $^ >$@

.DELETE_ON_ERROR:
