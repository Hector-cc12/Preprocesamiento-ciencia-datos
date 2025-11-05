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
