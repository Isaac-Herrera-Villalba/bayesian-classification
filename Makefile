# Makefile
# -----------------------------------------------------------------------
# Descripción:
# Automatiza la ejecución del proyecto bayesian-classification.
# Incluye la creación del entorno virtual, instalación de dependencias,
# ejecución del clasificador bayesiano y generación automática del
# reporte final en PDF mediante LaTeX.
# -----------------------------------------------------------------------

PYTHON        = python3
SRC_DIR       = src
OUT_DIR       = output
INPUT_FILE    = input.txt
MAIN_FILE     = $(SRC_DIR)/main.py
PDF_READER    = okular

VENV_DIR      = .venv
PYTHON_VENV   = $(VENV_DIR)/bin/python
PIP_VENV      = $(VENV_DIR)/bin/pip

PDF_FILE      = $(OUT_DIR)/reporte.pdf

.PHONY: all help env run pdf view clean full

# -----------------------------------------------------------------------
all: help

help:
	@echo "Comandos disponibles:"
	@echo "  make env    -> Crea entorno virtual e instala dependencias"
	@echo "  make run    -> Ejecuta el clasificador bayesiano (genera PDF automático)"
	@echo "  make pdf    -> Genera solo el reporte PDF desde input.txt"
	@echo "  make view   -> Abre el PDF resultante"
	@echo "  make clean  -> Elimina archivos temporales y auxiliares de LaTeX"
	@echo "  make full   -> Ejecuta todo el flujo (run + view)"
	@echo "---------------------------------------------------------------"

# -----------------------------------------------------------------------
env:
	@echo "=== Creando entorno virtual (.venv) ==="
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "[OK] Entorno virtual creado en $(VENV_DIR)"; \
	else \
		echo "[INFO] Entorno virtual ya existe."; \
	fi
	@echo "=== Instalando dependencias ==="
	$(PIP_VENV) install --upgrade pip >/dev/null
	$(PIP_VENV) install -r requirements.txt
	@echo "[OK] Dependencias instaladas correctamente."

# -----------------------------------------------------------------------
run:
	@echo "=== Ejecutando clasificador bayesiano ==="
	mkdir -pv $(OUT_DIR)/
	$(PYTHON_VENV) -m $(SRC_DIR).main $(INPUT_FILE)

pdf:
	@echo "=== Generando reporte PDF ==="
	$(PYTHON_VENV) $(MAIN_FILE) $(INPUT_FILE)

# -----------------------------------------------------------------------
view:
	@echo "Abriendo PDF con Okular..."
	$(PDF_READER) $(PDF_FILE) &

full: run view

# -----------------------------------------------------------------------
clean:
	@echo "Eliminando archivos generados..."
	rm -rf $(OUT_DIR)/
	find . -type f -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.tex" -delete
	rm -rf $(SRC_DIR)/__pycache__
	@echo "Limpieza completada."

