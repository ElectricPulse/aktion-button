ARGS = --headful

run:
	python3 main.py ${ARGS}

debug:
	python3 -m pdb main.py ${ARGS}


