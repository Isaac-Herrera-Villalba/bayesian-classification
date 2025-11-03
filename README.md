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
- Hoja (en caso de archivos de tipo hoja de cálculo).  
- Columna objetivo (la variable de clase).  
- Atributos a utilizar como filtros o predictores.  
- Valores específicos de esos atributos para generar la predicción.  
- Opciones adicionales como suavizado de Laplace (`LAPLACE_ALPHA`) o discretización automática (`DISCRETIZE_STRATEGY`) de atributos numéricos.

El programa detecta automáticamente el número de columnas, el tipo de dato de cada atributo y se adapta a distintos contextos (películas, música, videojuegos, comida, etc.), manteniendo una estructura de clasificación coherente y reutilizable.

---

### Funcionamiento

#### 1. Entrada

El archivo `input.txt` actúa como **fuente de configuración principal** del sistema.  
Define el dataset a analizar, la hoja (si aplica), la columna objetivo, los atributos a considerar y la instancia que se desea clasificar.

Cada bloque puede corresponder a un dataset diferente.  
Solo **una configuración activa** debe estar descomentada al ejecutar el programa.

##### Estructura general

| Clave | Descripción |
|-------|--------------|
| `DATASET` | Ruta del archivo de datos (`.ods`, `.xlsx`, `.csv`). |
| `SHEET` | Nombre de la hoja dentro del dataset (ej. `Sheet1`, `Sheet4`). |
| `TARGET_COLUMN` | Columna que representa la clase o etiqueta a predecir. |
| `USE_ALL_ATTRIBUTES` | Define si se emplearán todos los atributos (`true` / `false`). |
| `REPORT` | Ruta y nombre del archivo PDF de salida. |
| `LAPLACE_ALPHA` | *(Opcional)* Valor del suavizado de Laplace (por defecto `1`). |
| `INSTANCE` | Atributos y valores que conforman la instancia a clasificar. |

##### Ejemplo de configuración activa

```txt
DATASET=data/musica.ods
SHEET=Sheet4
TARGET_COLUMN=Popularidad
USE_ALL_ATTRIBUTES=true
REPORT=output/reporte.pdf

INSTANCE:
  Artista=Queen
  Plataforma=Spotify
  Oyente=M
  Género=Rock

