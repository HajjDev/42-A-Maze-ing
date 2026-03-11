VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip
PDB = $(VENV_DIR)/bin/python3 -m pdb
FLAKE8 = $(VENV_DIR)/bin/flake8
MYPY = $(VENV_DIR)/bin/mypy

MLX_WHEEL = mlx-2.2-py3-none-any.whl


FILE ?= config.txt


PY_FILES = a_maze_ing.py \
           src/display.py \
           src/maze_generator.py \
           src/parsing/__init__.py \
           src/parsing/parse_config.py \
           src/parsing/parse_utils.py


all: install

install: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install $(MLX_WHEEL)
	$(PIP) install flake8 mypy
	touch $(VENV_DIR)/bin/activate

run: install
	$(PYTHON) a_maze_ing.py $(FILE)

debug: install
	$(PDB) a_maze_ing.py $(FILE)

lint: install
	$(FLAKE8) $(PY_FILES)
	$(MYPY) $(PY_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(FLAKE8) $(PY_FILES)
	$(MYPY) $(PY_FILES) --strict

fclean: clean
	rm -rf $(VENV_DIR)

re: fclean all

.PHONY: all install run debug clean fclean re lint lint-strict