VERSION := $(shell cat VERSION)

.PHONY: test sdist develop release clean upload

test:
	python -m riemann_fping.tests.test_fping

develop:
	pip install -r requirements_dev.txt

dist/riemann-fping-$(VERSION).tar.gz:
	python setup.py sdist

sdist: dist/riemann-fping-$(VERSION).tar.gz

upload: 
	python setup.py sdist upload

release:
	git tag $(VERSION)

clean:
	rm -rf --preserve-root --one-file-system -- dist
