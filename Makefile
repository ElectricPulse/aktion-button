ARGS = keepalive headful

run-headful:
	python3 main.py ${ARGS}

run:
	python3 main.py

debug:
	python3 -m pdb main.py ${ARGS}


