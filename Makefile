ARGS = --headful
SRC = src
ENTRY = src/main.py

run:
	python3 "${ENTRY}" ${ARGS}

daemon:
	python3 "${ENTRY}"

debug:
	python3 -m pdb "${ENTRY}" ${ARGS}


