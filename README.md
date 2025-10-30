# Inteligencia Artificial, 2026-1
## Equipo 6

### Integrantes
· Fuentes Jiménez Yasbeck Dailanny  
· Herrera Villalba Isaac  
· Juárez García Yuliana  
· Ruiz Bastián Óscar  
· Sampayo Aguilar Cinthia Gloricel  
· Velarde Valencia Josue  

---

## Proyecto: Clasificación Bayesiana

### Descripción general

Este programa implementa un **clasificador Bayesiano Naive** capaz de analizar datasets (mal llamados “bases de datos”) en formato **CSV**, **XLSX** o **ODS**, para **inferir clases probables** a partir de uno o más atributos seleccionados por el usuario.

El sistema permite al usuario especificar en un archivo de texto (`input.txt`) las características del análisis:

- Ruta y formato del dataset.  
- Columna objetivo (la variable de clase).  
- Atributos a utilizar como filtros.  
- Valores específicos de esos atributos para generar la predicción.  
- Opciones adicionales como suavizado de Laplace o discretización automática de atributos numéricos.

El programa detecta automáticamente el número de columnas y el tipo de cada atributo, permitiendo trabajar con datasets de distinta naturaleza (películas, productos, usuarios, etc.) manteniendo la misma estructura conceptual.

---

### Funcionamiento

1. **Entrada**  
   El usuario proporciona un archivo `input.txt` con la configuración y los valores de entrada.  
   Ejemplo:
   ```txt
   DATASET=./data/peliculas.xlsx
   TARGET_COLUMN=Calificación
   USE_ALL_ATTRIBUTES=true

   INSTANCE:
     Género=Acción
     Usuario=M

