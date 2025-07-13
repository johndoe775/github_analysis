env:
	python3 -m venv .venv 

activate:
	run . .venv/bin/activate

install:
	python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt
