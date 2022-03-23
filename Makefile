PROGRAM_NAME := tachi-local
PROJECT_DIR  := tachi_local

VERSION := $(shell sed -nE 's/__version__[ ]+= "([0-9.]+)"/\1/p' $(PROJECT_DIR)/version.py)
FILES := $(shell find $(PROJECT_DIR) -name "*.py")

SHEBANG := "\#!/usr/bin/env python"


.PHONY: all get-version \
		dist upload \
		pyi-exe pyi-spec \
        clean clean-pycache clean-output clean-dist clean-build clean-egg clean-pyi


all: $(PROGRAM_NAME)

$(PROGRAM_NAME): $(FILES)
	mv $(PROJECT_DIR)/__main__.py .
	zip $(PROJECT_DIR).zip -r -0 $(PROJECT_DIR)/{,**/}*.py __main__.py
	mv __main__.py $(PROJECT_DIR)
	echo $(SHEBANG) > $(PROGRAM_NAME)
	cat $(PROJECT_DIR).zip >> $(PROGRAM_NAME)
	rm $(PROJECT_DIR).zip
	chmod +x $(PROGRAM_NAME)


get-version: ; @echo $(VERSION)


dist: clean-dist ; python -m build
upload: ; python -m twine check dist/* && python -m twine upload dist/*


pyi-exe:
	python pyi_create_version_info.py
	pyinstaller pyi_$(PROGRAM_NAME).spec \
				--distpath pyinstaller/dist \
				--workpath pyinstaller/build
pyi-spec:
	pyi-makespec pyi_entry.py \
	             --name $(PROGRAM_NAME) \
				 --onefile \
				 --icon NONE \
				 --version-file pyi_win_version_info.py
	mv $(PROGRAM_NAME).spec pyi_$(PROGRAM_NAME).spec


clean: clean-pycache clean-output clean-dist clean-build clean-pyi

clean-pycache: ; find . -type f -name "*.py[co]" -delete -o -type d -name __pycache__ -delete
clean-output:  ; rm -f $(PROGRAM_NAME)
clean-dist:    ; rm -rf dist
clean-build:   ; rm -rf build
clean-egg:     ; rm -rf $(PROJECT_DIR).egg-info
clean-pyi:     ; rm -rf pyinstaller
