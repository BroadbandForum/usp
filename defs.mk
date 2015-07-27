# XXX need to define some variable name conventions, e.g. BBF prefix, that
#     reduces chances of conflicts; still use simple names for things that
#     users see?

# this assumes a certain default directory structure
# XXX need to document the assumptions; can override via environment variables
#     or on the command line
ROOTDIR = $(TOPDIR)/../..

# https://github.com/YangModels/yang.git
# XXX no longer using this
YANGDIR = $(ROOTDIR)/yang

# https://github.com/BroadbandForum/pyang.git --branch bbf
PYANGDIR = $(ROOTDIR)/pyang

# e.g. installed via homebrew plantuml recipe
PLANTUMLDIR = /usr/local/bin

# e.g. installed via homebrew imagemagick recipe
CONVERT = convert

PYANG = PYTHONPATH=$(PYANGDIR) $(PYANGDIR)/bin/pyang

# XXX this isn't used by default; see rules.mk
PLANTUML = $(PLANTUMLDIR)/plantuml

# pyang flags
PYANGFLAGS += --path=body
PYANGFLAGS += --path=$(TOPDIR)/modules/standard
PYANGFLAGS += --path=$(TOPDIR)/modules/types
PYANGFLAGS += --path=$(PYANGDIR)/modules
PYANGFLAGS += --bbf

PYANGDEPENDFLAGS += --format=depend
PYANGDEPENDFLAGS += --depend-include-path
PYANGDEPENDFLAGS += --depend-from-submodules

PYANGTREEFLAGS += --format=tree
PYANGTREE2FLAGS += --tree-depth=2
PYANGTREE3FLAGS += --tree-depth=3
PYANGTREE4FLAGS += --tree-depth=4

PYANGUMLFLAGS += --format=uml
PYANGUMLFLAGS += --uml-description
#PYANGUMLFLAGS += --uml-inline-augments
#PYANGUMLFLAGS += --uml-inline-groupings

###############################################################################
# variables

ifeq "$(origin YANG)" "undefined"
  YANG = $(wildcard *.yang)
endif

PNG  = $(YANG:%.yang=%.png)
TREE = $(YANG:%.yang=%.tree)
UML  = $(YANG:%.yang=%.uml)

# if non-blank, this MUST include the terminating slash
TARGETDIR = docs/
