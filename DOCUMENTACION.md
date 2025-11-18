# DOCUMENTACIÓN DEL PROYECTO: PIPELINE DE PREPROCESAMIENTO

## I. Introducción y Objetivo del Proyecto

El objetivo principal de este proyecto es establecer un módulo robusto, reutilizable y profesional para la etapa de preprocesamiento de datos en un flujo de trabajo de Ciencia de Datos. La adopción de la programación orientada a objetos (POO) garantiza la modularidad, mantenibilidad y escalabilidad de las transformaciones de datos, permitiendo un manejo consistente de diferentes datasets.

La funcionalidad implementada se centra en la clase `PreprocessingPipeline` ubicada en `src/preprocesamiento.py`, la cual está diseñada para orquestar de manera secuencial y configurable todas las tareas esenciales de preparación de datos:

*   **Limpieza de Datos:**
    *   Eliminación de duplicados.
    *   Gestión de valores nulos (imputación por media, mediana o moda, o eliminación de filas).
*   **Detección y Tratamiento de Outliers:**
    *   Identificación y corrección de valores atípicos mediante métodos estadísticos como el Rango Intercuartílico (IQR).
    *   Opciones para eliminar los registros o acotar (cap) sus valores.
*   **Transformación de Variables:**
    *   **Escalado:**
        *   Normalización (MinMaxScaler).
        *   Estandarización (StandardScaler) de variables numéricas para ajustar la distribución.
    *   **Codificación Categórica:**
        *   Implementación de Label Encoding.
        *   One-Hot Encoding (`crear_dummies`) para preparar las variables cualitativas para los modelos de Machine Learning.
*   **Modularidad y Encadenamiento:**
    *   Se ha optimizado la clase para que todos los métodos que modifican el DataFrame devuelvan la propia instancia (`return self`).
    *   Facilitando el encadenamiento de operaciones (`pipeline.limpiar().escalar()...`).

## II. Comandos Git Usados y Propósito
El proyecto se desarrolla bajo una metodología de GitFlow Simplificado basada en ramas de feature. Este enfoque aísla el desarrollo de nuevas funcionalidades (como el pipeline) y garantiza que la rama principal (main) se mantenga siempre estable y lista para producción.
| **Comando Git**                   | **Descripción Detallada**                                           | **Propósito Estratégico en el Proyecto**                                   |
| --------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `git clone [URL]`                 | Clona el repositorio remoto, creando un repositorio local (`.git`). | Iniciar o restablecer el entorno de trabajo desde cero.                    |
| `git config user.name/email`      | Configura la identidad del autor (nombre y correo).                 | Asociar los commits al desarrollador.                                      |
| `git checkout -b [rama]`          | Crea y cambia a una nueva rama (*ej.* `feature-preprocesamiento`).  | Aislar el desarrollo del pipeline.                                         |
| `git add .`                       | Mueve los archivos al *staging area*.                               | Preparar los cambios para un commit coherente.                             |
| `git commit -m "[mensaje]"`       | Guarda los cambios en el historial de la rama.                      | Registrar el progreso del pipeline (*ej.* `feat: Implementación inicial`). |
| `git push origin [rama]`          | Sube la rama y sus commits al remoto (GitHub).                      | Permitir revisión y creación de Pull Request.                              |
| `git pull origin main`            | Descarga y fusiona los últimos cambios de `main`.                   | Mantener la rama sincronizada.                                             |
| `git branch -d [rama]`            | Elimina una rama local fusionada.                                   | Mantener un entorno limpio.                                                |
| `git push origin --delete [rama]` | Elimina la rama remota.                                             | Limpieza final en GitHub.                                                  |

## III. 🧪 Automatización y Calidad del Código (CI)

Se implementó un workflow de Integración Continua (CI) con GitHub Actions para automatizar las pruebas y garantizar la calidad del código antes de cada fusión en la rama `main`.

| **Paso**                    | **Descripción**                                                             | **Impacto en la Calidad**                                                                              |
| --------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **1. Checkout Code**        | Obtiene el código propuesto en el Pull Request.                             | Base para la ejecución del pipeline.                                                                   |
| **2. Setup Python**         | Configura el entorno con **Python 3.10**.                                   | Garantiza la **consistencia del entorno de pruebas** en cada ejecución.                                |
| **3. Install Dependencies** | Instala las dependencias desde `requirements.txt` y `pytest`.               | Prepara el entorno para que el código sea **ejecutable y verificable**.                                |
| **4. Run Unit Tests**       | Ejecuta los tests unitarios con:<br>`pytest tests/test_preprocesamiento.py` | Verifica la **funcionalidad del pipeline**. Si algún test falla, el PR se **bloquea automáticamente**. |
| **5. Verify Doc File**      | Comprueba la existencia del archivo `DOCUMENTACION.md`.                     | Garantiza la **trazabilidad, documentación y mantenimiento** del proyecto.                             |

### 🧩 B. Cobertura de Pruebas Unitarias (Tests)

El archivo tests/test_preprocesamiento.py fue expandido para verificar los siguientes métodos clave del pipeline:

| **Método del Pipeline**               | **Funcionalidad Verificada**                                                                       |
| ------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `test_eliminar_duplicados`            | Confirma que las filas duplicadas son eliminadas, reduciendo el tamaño del dataset.                |
| `test_gestionar_nulos_imputar_media`  | Asegura que la imputación por media reemplace los valores `NaN` con la media estadística correcta. |
| `test_gestionar_nulos_eliminar_filas` | Confirma la reducción del número de filas cuando se eliminan registros con nulos.                  |
| `test_escalar_variables_minmax`       | Verifica que el escalado `MinMaxScaler` produzca valores entre 0 y 1.                              |
| `test_gestionar_outliers_acotar`      | Asegura que los valores atípicos sean correctamente acotados (*capped*).                           |

## IV. 🖥️ Evidencia de Ejecución Final

Se confirma la finalización exitosa del proyecto, con el código del pipeline fusionado en la rama main y con la automatización activa.

### 🔀 A. Creación y Fusión del Pull Request

Se inició el proceso de revisión y calidad al crear los Pull Requests correspondientes:

#### PR #2 – CI Inicial
images/image.png
feat(ci): Implementación de GitHub Actions para CI y tests unitarios iniciales ]

#### PR #3 – Tests Expandidos y Fusión Final

![alt text](<Captura de pantalla 2025-11-04 222140.png>)
feat(tests): Ampliación de la Cobertura de Pruebas Unitarias y la confirmación de "Merged"]

### 💻 B. Evidencia de Comandos y Ejecución de CI/CD

El siguiente registro muestra los comandos Git ejecutados y la verificación exitosa de la Integración Continua (CI) en GitHub:
#### Creación de la rama e implementación de CI inicial
C:\...\Preprocesamiento-ciencia-datos>git checkout -b feature-ci-automation
Switched to a new branch 'feature-ci-automation'
C:\...\Preprocesamiento-ciencia-datos>git add .
C:\...\Preprocesamiento-ciencia-datos>git commit -m "feat(ci): Implementación de GitHub Actions para CI y tests unitarios iniciales"
C:\...\Preprocesamiento-ciencia-datos>git push origin feature-ci-automation

#### Limpieza después de la fusión del PR de CI
C:\...\Preprocesamiento-ciencia-datos>git checkout main
C:\...\Preprocesamiento-ciencia-datos>git pull origin main
C:\...\Preprocesamiento-ciencia-datos>git branch -d feature-ci-automation

#### Implementación de tests expandidos
C:\...\Preprocesamiento-ciencia-datos>git checkout -b feature-ampliar-tests
C:\...\Preprocesamiento-ciencia-datos>git add tests/test_preprocesamiento.py
C:\...\Preprocesamiento-ciencia-datos>git commit -m "feat(tests): Expansión de pruebas unitarias para nulos, escalado y outliers"
C:\...\Preprocesamiento-ciencia-datos>git push origin feature-ampliar-tests
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)

## Ejecución Exitosa del Workflow de CI

El workflow CI Pipeline Execution se ejecutó correctamente en GitHub Actions para el Pull Request final, confirmando que todos los tests unitarios (incluyendo los de nulos, escalado y outliers) pasaron con éxito.

![alt text](<Captura de pantalla 2025-11-04 225123.png>)