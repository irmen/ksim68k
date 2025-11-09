.PHONY:  all win_dist dist upload

all:
	@echo "Targets:  test, wheel, win_wheel, check_upload, upload"

test:
	rm -rf build *.so
	@echo "************** automatic testing is currently broken **************"
	# python -m build
	# python -m pytest tests

win_wheel: test
	cmd /C del /q dist\*
	py -3.10-32 -m build --wheel
	py -3.11-32 -m build --wheel
	py -3.12-32 -m build --wheel
	py -3.13-32 -m build --wheel
	py -3.14-32 -m build --wheel

wheel: test
	rm -f dist/*
	python -m build --sdist --wheel

upload: check_upload
	twine upload dist/*

check_upload:
	twine check dist/*

