# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 voter_db.py
	./$(VENV)/bin/python3 registrar.py
	./$(VENV)/bin/python3 voting_block.py
	./$(VENV)/bin/python3 transaction.py
	./$(VENV)/bin/python3 blockchain.py
	./$(VENV)/bin/python3 Testing/unittesting.py
	./$(VENV)/bin/python3 Testing/registration_sim.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean