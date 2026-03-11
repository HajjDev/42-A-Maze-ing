# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip
PDB = $(VENV_DIR)/bin/python3 -m pdb
FLAKE8 = $(VENV_DIR)/bin/flake8
MYPY = $(VENV_DIR)/bin/mypy

MLX_WHEEL = mlx-2.2-py3-none-any.whl

# Le fichier de configuration par défaut (peut être modifié via le terminal: make run FILE=autre.txt)
FILE ?= config.txt

# Liste EXPLICITE de tous les fichiers Python (Zéro wildcard comme demandé)
PY_FILES = a_maze_ing.py \
           src/display.py \
           src/maze_generator.py \
           src/parsing/__init__.py \
           src/parsing/parse_config.py \
           src/parsing/parse_utils.py

# Règle par défaut
all: install

# ==============================================================================
# RÈGLES OBLIGATOIRES DU SUJET (Chapitre III.2)
# ==============================================================================

# 1. install : Installe les dépendances
install: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install $(MLX_WHEEL)
	$(PIP) install flake8 mypy
	touch $(VENV_DIR)/bin/activate

# 2. run : Exécute le programme principal
run: install
	$(PYTHON) a_maze_ing.py $(FILE)

# 3. debug : Exécute le programme en mode debug avec pdb
debug: install
	$(PDB) a_maze_ing.py $(FILE)

# 5. lint : Exécute flake8 et mypy
lint: install
	$(FLAKE8) $(PY_FILES)
	$(MYPY) $(PY_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# 6. lint-strict (Optionnel dans le sujet) : Vérification stricte
lint-strict: install
	$(FLAKE8) $(PY_FILES)
	$(MYPY) $(PY_FILES) --strict

# ==============================================================================
# RÈGLES CLASSIQUES 42 (Non précisées mais indispensables pour le venv)
# ==============================================================================

fclean: clean
	rm -rf $(VENV_DIR)

re: fclean all

.PHONY: all install run debug clean fclean re lint lint-strict