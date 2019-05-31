VIRT_ENV     := venv
PROJECT_NAME := python-zeppelin

# Variables for Sphinx documentation
# You can set these variables from the command line.
SPHINXOPTS    = 
SPHINXBUILD   = $(VIRT_ENV)/bin/sphinx-build
SPHINXPROJ    = PythonZeppelin
SOURCEDIR     = docs
BUILDDIR      = build


.PHONY: help
help: $(VIRT_ENV)
	@echo "$(VIRT_ENV) - Create a python virtualenv"
	@echo "clean - Remove build and python file artifacts"
	@echo "test - Run tests if any"
	@echo "docs - Create Sphinx HTML docs"


$(VIRT_ENV): $(VIRT_ENV)/bin/activate
$(VIRT_ENV)/bin/activate:
	rm -rf $(VIRT_ENV) && \
	virtualenv -p python3 $(VIRT_ENV) && \
	$(VIRT_ENV)/bin/pip install -U pip && \
	$(VIRT_ENV)/bin/pip install -r $(SOURCEDIR)/requirements.txt && \
	$(VIRT_ENV)/bin/python setup.py develop && \
	touch $(VIRT_ENV)/bin/activate


.PHONY: clean
clean: clean-build clean-pyc
	rm -fr temp/


.PHONY: clean-build
clean-build:
	rm -fr build/; \
	rm -fr dist/; \
	rm -fr *.egg-info


.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +; \
	find . -name '*.pyo' -exec rm -f {} +; \
	find . -name '*~' -exec rm -f {} +


.PHONY: docs
docs: $(VIRT_ENV)
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


.PHONY: test
test: $(VIRT_ENV)
	$(VIRT_ENV)/bin/python setup.py test


.PHONY: shell
shell: export PS1 := \[\033[2m\]($(VIRT_ENV))\[\033[0m\]\h:\w\$$ 
shell: $(VIRT_ENV)
	vex --path $(VIRT_ENV)
