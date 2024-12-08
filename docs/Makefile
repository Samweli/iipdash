# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
REFS = ..
REFS_EXCLUDES = ../apps/*/migrations ../apps/*/tests ../manage.py

.PHONY: help livehtml apidocs Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build, watch and serve docs with live reload
livehtml:
	sphinx-autobuild -b html --host 0.0.0.0 --port 9000 --watch $(REFS) -c . $(SOURCEDIR) $(BUILDDIR)/html

# Outputs rst files from django application code
apidocs:
	sphinx-apidoc -o $(SOURCEDIR)/ref $(REFS) -M -f $(REFS_EXCLUDES)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
