# Trabajo Final: Pipeline de Big Data con Infraestructura Docker

**Alumno:** Carlos Rivasplata  
**Docente:** Juan Marcelo Gutiérrez  
**Curso:** ESPECIALISTA EN BIG DATA

**🚀 Ver Dashboard Interactivo:** [https://carlosrivasplata.github.io/ejercicios-bigdata/](https://carlosrivasplata.github.io/ejercicios-bigdata/)

---

## Índice

1.  [Tema de Investigación y Metodología](#1-tema-de-investigación-y-metodología)
2.  [Arquitectura de Infraestructura](#2-arquitectura-de-infraestructura)
3.  [Análisis de Datos y Hallazgos](#3-análisis-de-datos-y-hallazgos)
4.  [Discusión Teórica y Preguntas](#4-discusión-teórica-y-preguntas)
5.  [Cómo Ejecutar este Proyecto](#5-cómo-ejecutar-este-proyecto)

---

## 1. Tema de Investigación y Metodología

### 1.1 Pregunta de Investigación
**Título:** Desarrollo Político-Económico en el Magreb: Autoritarismo vs Democracia

**Pregunta:** ¿Existe una relación directa entre el desarrollo económico (PIB per cápita) y el nivel de democracia electoral en los países del Magreb? ¿Los países más ricos de la región tienden a ser más democráticos o el autoritarismo persiste independientemente de la riqueza?

### 1.2 Fuente de Datos: The Quality of Government (QoG) Institute
Para este análisis, se ha seleccionado el **Standard Dataset (Cross-Section)** del **QoG Institute**. Esta fuente de datos es una de las más completas y respetadas en ciencias sociales, ya que agrega y estandariza cientos de variables de fuentes primarias (como el Banco Mundial, V-Dem, etc.) en un único dataset coherente.

### 1.3 Selección de Modelo de Análisis
El enunciado del trabajo final propone tres enfoques metodológicos: **Series Temporales**, **Clustering (K-Means)**, y **Análisis Comparativo**.

Dado que el dataset QoG utilizado es de tipo **Cross-Section** (una "fotografía" de un único año) y la muestra se limita a 5 países:
*   Se **descarta** el enfoque de **Series Temporales**, ya que no existe la dimensión temporal necesaria.
*   Se **descarta** el enfoque de **Clustering**, ya que 5 observaciones son insuficientes para un agrupamiento estadístico robusto.

Por lo tanto, se ha seleccionado el **Análisis Comparativo y Correlacional** como el modelo más adecuado y riguroso.

---

## 2. Arquitectura de Infraestructura

### 2.1 Diagrama de Arquitectura (Docker)

```mermaid
graph TD
    subgraph Host_Machine ["Tu Computadora (Host)"]
        CSV[("📂 Datos CSV (QoG)")]
        Code["📜 pipeline.py"]
        Output_Local["📂 outputs/ (Gráficos)"]
    end

    subgraph Docker_Environment ["🐳 Docker Compose Cluster"]
        direction TB
        
        subgraph Spark_Cluster ["Apache Spark Cluster"]
            Master["🧠 Spark Master<br>(Puerto 8080)"]
            Worker["💪 Spark Worker<br>(2GB RAM, 2 Cores)"]
        end
        
        Postgres[("🐘 PostgreSQL<br>(Puerto 5432)")]
    end

    %% Conexiones de Volúmenes
    CSV -.-> |Volumen /workspace/datos| Master
    Code -.-> |Volumen /workspace/src| Master
    
    %% Flujo de Datos
    Master --> |Asigna Tareas| Worker
    Worker --> |Procesa Datos| Master
    Master --> |Guarda Resultados| Output_Local
    Master -.-> |"Conexión JDBC (Opcional)"| Postgres

    %% Estilos
    style Host_Machine fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Docker_Environment fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    style Spark_Cluster fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style Master fill:#ffcc80,stroke:#ef6c00
    style Worker fill:#ffe0b2,stroke:#ef6c00
    style Postgres fill:#b2dfdb,stroke:#00695c
```

### 2.2 Diagrama de Flujo del Pipeline (ETL)

```mermaid
graph LR
    subgraph ETL_Process ["Pipeline de Datos (pipeline.py)"]
        direction LR
        A[("📥 Carga Datos<br>(CSV QoG)")] --> B{"🌍 Filtrado<br>(Solo Magreb)"}
        B --> C["🧹 Limpieza<br>(Nulos & Tipos)"]
        C --> D["🧮 Transformación<br>(Variables Derivadas)"]
        D --> E[("💾 Guardar<br>(Parquet)")]
        D --> F["📊 Visualización<br>(Matplotlib/Seaborn)"]
        F --> G[("🖼️ Exportar<br>(5 Gráficos PNG)")]
    end
    
    style ETL_Process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style A fill:#e1bee7,stroke:#4a148c
    style E fill:#b2dfdb,stroke:#004d40
    style G fill:#ffccbc,stroke:#bf360c
```

### 2.3 Descripción General
Esta infraestructura despliega un **cluster de procesamiento de Big Data** utilizando contenedores Docker. El objetivo es crear un entorno aislado y reproducible para ejecutar tareas de ETL y análisis con Apache Spark. El cluster consta de tres servicios principales: un nodo maestro de Spark, un nodo trabajador y una base de datos PostgreSQL.

### 2.4 Servicios y Volúmenes
- **PostgreSQL (`postgres:16-alpine`):** Sirve como almacén de datos persistente.
- **Spark Master/Worker (`apache/spark:3.5.4-python3`):** Orquestan y ejecutan el procesamiento de datos. La UI del Master se expone en el puerto `8080`.
- **Volúmenes:** Se utilizan para mapear las carpetas locales (`datos/`, `outputs/`) y los archivos de código (`pipeline.py`, `requirements.txt`) al entorno de Docker, permitiendo una interacción fluida y la persistencia de los resultados.

### 2.5 Captura de Pantalla (Spark UI)
![Spark UI](outputs/graficos/spark_ui.jpeg)

---

## 3. Análisis de Datos y Hallazgos

### 3.1 Gráfico 1: Nivel de Democracia en el Magreb
![Gráfico 1](outputs/graficos/01_comparacion_democracia.png)
**Interpretación:** El gráfico muestra una heterogeneidad significativa. **Mauritania (MRT)** emerge como el país con el índice más alto, mientras que **Argelia, Marruecos y Libia** se agrupan en la categoría de "autoritarios".

### 3.2 Gráfico 2: Relación Democracia vs. Riqueza
![Gráfico 2](outputs/graficos/02_democracia_vs_pib.png)
**Interpretación:** Este gráfico **desafía la hipótesis inicial**. No se observa una correlación positiva clara. **Argelia y Libia** son "outliers": alto PIB (petróleo) pero baja democracia, sugiriendo un patrón de **estado rentista**.

### 3.3 Gráfico 3: Mapa de Calor de Correlación
![Gráfico 3](outputs/graficos/03_heatmap_correlacion.png)
**Interpretación:** La correlación entre **Democracia y PIB** es negativa (-0.21). En cambio, **Esperanza de Vida y PIB** tienen una fuerte correlación positiva (0.79), y **Democracia y Estabilidad** una fuerte correlación negativa (-0.81).

### 3.4 Gráfico 4 y 5: Análisis Institucional y Social
![Gráfico 4](outputs/graficos/04_estabilidad_vs_corrupcion.png)
![Gráfico 5](outputs/graficos/05_bubble_social.png)
**Interpretación:** El control de la corrupción es bajo en toda la región. El desarrollo social (esperanza de vida) parece estar más ligado a la riqueza económica que al tipo de régimen político.

### 3.5 Conclusiones del Análisis
La hipótesis de que el desarrollo económico fomenta la democracia **es rechazada** para el Magreb. La riqueza de recursos naturales parece sostener el autoritarismo, mientras que el desarrollo social depende más del PIB que de la libertad política.

---

## 4. Discusión Teórica y Preguntas

### 4.1 Infraestructura y Escalabilidad
Un worker de 2GB con un CSV de 3GB causaría un error `OutOfMemoryError`. La solución es escalar el cluster, aumentar particiones o usar formatos optimizados como Parquet. Para 50GB, se requeriría un cluster en la nube (AWS/Databricks) y almacenamiento distribuido (S3).

### 4.2 ETL y Lazy Evaluation
Spark usa **evaluación perezosa**: `spark.read.csv()` solo define un plan. La ejecución real solo ocurre cuando una **acción** (`.count()`, `.write()`) lo requiere, permitiendo optimizaciones.

---

## 5. Cómo Ejecutar este Proyecto

1.  **Levantar la infraestructura:**
    ```sh
    docker compose up -d
    ```
2.  **Instalar dependencias:**
    ```sh
    docker compose exec -u 0 spark-master pip install -r /workspace/requirements.txt
    ```
3.  **Ejecutar el pipeline completo:**
    ```sh
    docker compose exec spark-master /opt/spark/bin/spark-submit /workspace/pipeline.py
    ```
4.  **Ver los resultados:** Los gráficos generados se encontrarán en la carpeta `outputs/graficos`.
