PYTHON = python3

.PHONY: reinstall install upload uninstall rebuild build clean gen-demo test

reinstall:
	make uninstall
	make rebuild
	make install
	make clean

install: dist/*.whl
	$(PYTHON) -m pip install dist/*.whl
	$(PYTHON) -m pip show md2html-phuker

upload: dist/*.whl
	test -f dist/*.whl
	test -f dist/*.tar.gz
	$(PYTHON) -m twine check dist/*.whl dist/*.tar.gz
	# username is: __token__
	$(PYTHON) -m twine upload dist/*.whl dist/*.tar.gz

uninstall:
	$(PYTHON) -m pip uninstall -y md2html-phuker

rebuild build dist/*.whl dist/*.tar.gz: ./setup.py ./md2html/md2html.py
	# make sure clean old versions
	make clean

	make test

	make gen-demo

	$(PYTHON) ./setup.py sdist bdist_wheel

	# 'pip install' is buggy when .egg-info exist
	rm -rf *.egg-info build

clean:
	rm -rf *.egg-info build dist

gen-demo: ./md2html/md2html.py ./docs/demo.md
	$(PYTHON) ./md2html/md2html.py -vf ./docs/demo.md -o ./docs/demo-default.html -t 'default - md2html demo'
	$(PYTHON) ./md2html/md2html.py -vf ./docs/demo.md -o ./docs/demo-sidebar-toc.html -t 'sidebar-toc - md2html demo' --style sidebar-toc
	$(PYTHON) ./md2html/md2html.py -vf ./docs/demo.md -o ./docs/demo-dark.html -t 'dark - md2html demo' --style dark
	$(PYTHON) ./md2html/md2html.py -vf ./docs/demo.md -o ./docs/demo-sidebar-toc-dark.html -t 'sidebar-toc - dark - md2html demo' --style sidebar-toc --style dark

test: ./test.py
	$(PYTHON) ./test.py -vv
