# 7.3 Hadoop y HDFS: Almacenamiento Distribuido

**Curso:** Big Data con Python - Prof. Juan Marcelo Gutierrez Miranda (@TodoEconometria)

Nivel: Intermedio-Avanzado

---

> **"No puedes procesar lo que no puedes almacenar."**
>
> Antes de Spark, antes de los DataFrames, antes del machine learning distribuido...
> alguien tuvo que resolver el problema de **donde guardar petabytes de datos**.
> Esa solucion se llama HDFS, y nacio dentro del ecosistema Hadoop.

---

## Indice

- [7.3.1 El origen: Google y los 3 papers](#731-el-origen-google-y-los-3-papers)
- [7.3.2 Ecosistema Hadoop: vista panoramica](#732-ecosistema-hadoop-vista-panoramica)
- [7.3.3 HDFS: Arquitectura del sistema de archivos distribuido](#733-hdfs-arquitectura-del-sistema-de-archivos-distribuido)
- [7.3.4 Flujo de escritura en HDFS](#734-flujo-de-escritura-en-hdfs)
- [7.3.5 Flujo de lectura en HDFS](#735-flujo-de-lectura-en-hdfs)
- [7.3.6 Comandos HDFS: referencia completa](#736-comandos-hdfs-referencia-completa)
- [7.3.7 Montando Hadoop con Docker](#737-montando-hadoop-con-docker)
- [7.3.8 HDFS vs sistemas de archivos locales](#738-hdfs-vs-sistemas-de-archivos-locales)
- [7.3.9 YARN: gestion de recursos del cluster](#739-yarn-gestion-de-recursos-del-cluster)
- [7.3.10 Spark sobre HDFS](#7310-spark-sobre-hdfs)
- [7.3.11 Tolerancia a fallos](#7311-tolerancia-a-fallos)
- [7.3.12 Hadoop en la nube](#7312-hadoop-en-la-nube)
- [7.3.13 Hadoop vs Spark: no son competidores](#7313-hadoop-vs-spark-no-son-competidores)
- [7.3.14 Referencias](#7314-referencias)

---

## 7.3.1 El origen: Google y los 3 papers

### El problema de Google (circa 2000)

A principios de los 2000, Google enfrentaba un problema que nadie mas tenia:
indexar **toda la web**. Hablamos de miles de millones de paginas web que debian
ser almacenadas, procesadas y servidas a millones de usuarios. Ningun sistema
existente podia manejar esa escala.

La solucion de Google no fue comprar computadoras mas potentes (scale up), sino
usar **miles de computadoras baratas trabajando juntas** (scale out). Para lograrlo,
publicaron tres papers academicos que cambiaron la industria para siempre:

### Los 3 papers fundamentales

| Anio | Paper | Problema que resuelve | Equivalente Open Source |
|------|-------|----------------------|------------------------|
| 2003 | **Google File System (GFS)** | Almacenar petabytes en miles de discos baratos | HDFS |
| 2004 | **MapReduce** | Procesar petabytes en paralelo de forma simple | Hadoop MapReduce |
| 2006 | **BigTable** | Base de datos NoSQL sobre GFS | HBase |

**GFS (2003):** Describe como distribuir archivos enormes en miles de servidores
commodity (baratos, no especializados). Introduce conceptos como chunking (partir
archivos en bloques), replicacion automatica y un master centralizado que conoce
la ubicacion de cada bloque.

**MapReduce (2004):** Define un modelo de programacion donde cualquier problema
se descompone en dos fases: **Map** (transformar datos en paralelo) y **Reduce**
(agregar resultados). El framework se encarga de distribuir el trabajo, manejar
fallos y coordinar los nodos.

**BigTable (2006):** Una base de datos distribuida, columnar y sparse (dispersa),
construida sobre GFS. Optimizada para lecturas y escrituras aleatorias a gran
escala. Es la base conceptual de HBase, Cassandra y muchas bases NoSQL modernas.

### De Google a Hadoop: Doug Cutting

**Doug Cutting**, un ingeniero de software que trabajaba en el proyecto de busqueda
open source **Nutch**, leyo los papers de Google y penso: *"Puedo construir esto
de forma abierta"*. Junto con **Mike Cafarella**, implemento versiones open source
de GFS y MapReduce.

En 2006, estas implementaciones se separaron de Nutch y se convirtieron en un
proyecto independiente de la Apache Software Foundation: **Hadoop**.

> **El nombre "Hadoop"** viene del elefante amarillo de peluche de su hijo.
> Doug Cutting eligio el nombre porque era facil de pronunciar, de recordar
> y de buscar en Google. No tiene ningun significado tecnico.

Yahoo! fue la primera gran empresa en adoptar Hadoop a escala, financiando
gran parte de su desarrollo inicial. Para 2008, Hadoop ya procesaba petabytes
de datos en clusters de miles de nodos.

---

## 7.3.2 Ecosistema Hadoop: vista panoramica

Hadoop no es una sola herramienta. Es un **ecosistema completo** de proyectos
que trabajan juntos para almacenar, procesar y analizar datos a gran escala.

### Diagrama del ecosistema

```
+=========================================================================+
|                      ECOSISTEMA HADOOP                                  |
+=========================================================================+
|                                                                         |
|  +-------------------+  +-------------------+  +-------------------+    |
|  |       HIVE        |  |       PIG         |  |     SPARK SQL     |    |
|  |  (SQL sobre HDFS) |  |  (Scripting ETL)  |  |  (SQL en memoria) |    |
|  +-------------------+  +-------------------+  +-------------------+    |
|                                                                         |
|  +-------------------+  +-------------------+  +-------------------+    |
|  |      HBase        |  |     SQOOP         |  |      FLUME        |    |
|  | (NoSQL columnar)  |  | (Import/Export    |  |  (Ingesta logs    |    |
|  |                   |  |  RDBMS <-> HDFS)  |  |   en streaming)   |    |
|  +-------------------+  +-------------------+  +-------------------+    |
|                                                                         |
|  +-------------------+  +-------------------+                           |
|  |     OOZIE         |  |    ZOOKEEPER      |                           |
|  |  (Orquestacion    |  |  (Coordinacion    |                           |
|  |   de workflows)   |  |   distribuida)    |                           |
|  +-------------------+  +-------------------+                           |
|                                                                         |
+=========================== CAPA DE PROCESO ==============================+
|                                                                         |
|  +-------------------------------+  +-------------------------------+   |
|  |        MapReduce              |  |          SPARK                |   |
|  |   (Proceso batch original)    |  |   (Proceso en memoria,       |   |
|  |   Disco a disco, lento        |  |    10-100x mas rapido)       |   |
|  +-------------------------------+  +-------------------------------+   |
|                                                                         |
+=========================== CAPA DE RECURSOS =============================+
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |                        YARN                                        | |
|  |          (Yet Another Resource Negotiator)                         | |
|  |   Gestiona CPU, memoria y scheduling de aplicaciones en el cluster | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
+=========================== CAPA DE ALMACENAMIENTO =======================+
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |                        HDFS                                        | |
|  |          (Hadoop Distributed File System)                          | |
|  |   Almacena datos en bloques replicados a traves del cluster        | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
+=========================================================================+
```

### Componentes principales

**HDFS (almacenamiento):** El sistema de archivos distribuido. Almacena datos
partidos en bloques de 128 MB, replicados en multiples nodos. Es la "base"
sobre la que todo lo demas se construye. Lo veremos en detalle en la seccion 7.3.3.

**YARN (gestion de recursos):** El "sistema operativo" del cluster. Decide
cuanta CPU y memoria recibe cada aplicacion. Permite que MapReduce, Spark,
Hive y otros motores compartan el mismo cluster. Seccion 7.3.9.

**MapReduce (procesamiento original):** El primer motor de procesamiento de
Hadoop. Escribe resultados intermedios a disco entre las fases Map y Reduce,
lo que lo hace lento pero muy tolerante a fallos. **En la practica, Spark lo
ha reemplazado casi por completo.**

**Hive:** Permite escribir consultas SQL que se traducen automaticamente a
trabajos MapReduce (o Spark). Ideal para analistas que conocen SQL pero no
quieren programar en Java. Facebook lo creo internamente y luego lo abrio.

**HBase:** Base de datos NoSQL columnar construida sobre HDFS. Inspirada en
BigTable de Google. Permite lecturas y escrituras aleatorias rapidas sobre
datos almacenados en HDFS (que normalmente solo permite escritura secuencial).

**Pig:** Lenguaje de scripting de alto nivel para crear pipelines ETL. Fue
popular antes de Spark pero hoy esta en desuso.

**Sqoop:** Herramienta para importar datos de bases de datos relacionales
(MySQL, PostgreSQL, Oracle) a HDFS y viceversa. Genera trabajos MapReduce
internamente.

**Flume:** Sistema de ingesta de logs y datos en streaming hacia HDFS.
Diseñado para mover grandes volumenes de datos de eventos en tiempo real.

**Oozie:** Orquestador de workflows. Permite encadenar trabajos MapReduce,
Spark, Hive, etc. Similar a Airflow pero especifico del ecosistema Hadoop.

**ZooKeeper:** Servicio de coordinacion distribuida. Maneja eleccion de
lideres, configuracion compartida y locks distribuidos. Esencial para
Hadoop HA (High Availability).

### Por que Spark reemplazo a MapReduce (pero HDFS sigue vivo)

MapReduce escribe a disco despues de cada fase. Si tienes un pipeline de
5 pasos, hay 5 escrituras y lecturas a disco. Spark mantiene los datos
**en memoria RAM** entre operaciones, lo que lo hace 10-100x mas rapido.

Sin embargo, HDFS **no fue reemplazado**. Spark necesita leer datos de
algun lugar y escribir resultados en algun lugar. HDFS sigue siendo el
sistema de almacenamiento distribuido mas usado en clusters on-premise.

```
ANTES (2008-2014):         AHORA (2015+):
HDFS + MapReduce           HDFS + YARN + Spark
(lento pero funciona)      (lo mejor de ambos mundos)
```

---

## 7.3.3 HDFS: Arquitectura del sistema de archivos distribuido

HDFS (Hadoop Distributed File System) es un sistema de archivos diseñado para
almacenar archivos **muy grandes** (gigabytes a terabytes) distribuyendolos en
multiples servidores commodity.

### Componentes principales

```
+================================================================+
|                    CLUSTER HDFS                                 |
+================================================================+
|                                                                 |
|   +---------------------------+                                 |
|   |        NameNode           |    (MAESTRO - solo 1 activo)    |
|   |---------------------------|                                 |
|   |  - Metadata del sistema   |                                 |
|   |  - Namespace (arbol de    |                                 |
|   |    directorios/archivos)  |                                 |
|   |  - Mapa: archivo -> lista |                                 |
|   |    de bloques             |                                 |
|   |  - Mapa: bloque -> lista  |                                 |
|   |    de DataNodes           |                                 |
|   |  - NO almacena datos      |                                 |
|   +---------------------------+                                 |
|           |         |         |                                  |
|     heartbeat  heartbeat  heartbeat  (cada 3 segundos)          |
|           |         |         |                                  |
|   +-------+---------+---------+------+                          |
|   |       |         |         |      |                          |
|   v       v         v         v      v                          |
| +------+ +------+ +------+ +------+ +------+                   |
| | Data | | Data | | Data | | Data | | Data |                   |
| | Node | | Node | | Node | | Node | | Node |                   |
| |  01  | |  02  | |  03  | |  04  | |  05  |                   |
| |------| |------| |------| |------| |------|                   |
| |[B1]  | |[B1]  | |[B2]  | |[B2]  | |[B3]  |                   |
| |[B3]  | |[B4]  | |[B3]  | |[B5]  | |[B1]  |                   |
| |[B5]  | |[B6]  | |[B4]  | |[B6]  | |[B2]  |                   |
| +------+ +------+ +------+ +------+ +------+                   |
|  (ESCLAVOS - almacenan los bloques reales de datos)             |
|                                                                 |
+================================================================+
```

### NameNode (el maestro)

El NameNode es el **cerebro** del cluster HDFS. Mantiene toda la metadata:

- **Namespace:** El arbol de directorios y archivos (como `/datos/ventas/2024.csv`).
- **Mapa de bloques:** Sabe que el archivo `2024.csv` esta compuesto por los
  bloques B1, B2, B3.
- **Ubicacion de bloques:** Sabe que B1 esta en DataNode01, DataNode02 y
  DataNode05 (tres copias).
- **Permisos:** Propietario, grupo, permisos rwx (similar a Linux).

**Importante:** El NameNode **NO almacena datos de usuario**. Solo metadata.
Toda la metadata vive en RAM para acceso rapido. Por eso el NameNode necesita
mucha memoria RAM (pero poco disco).

La metadata se persiste en dos archivos:
- **FsImage:** Snapshot completo del namespace en un momento dado.
- **EditLog:** Log de todas las operaciones desde el ultimo FsImage.

### DataNode (los esclavos)

Los DataNodes son los **obreros** del cluster. Cada DataNode:

- Almacena bloques de datos en su disco local.
- Envia **heartbeats** al NameNode cada 3 segundos ("estoy vivo").
- Envia **block reports** periodicamente (lista completa de bloques que tiene).
- Ejecuta operaciones de lectura/escritura ordenadas por el NameNode.

Un cluster tipico tiene entre 10 y miles de DataNodes.

### Secondary NameNode (NO es un backup)

Este es uno de los conceptos mas confusos de Hadoop. El Secondary NameNode
**NO es un respaldo del NameNode**. Su unica funcion es:

- Periodicamente descargar el FsImage y el EditLog del NameNode.
- Fusionarlos (merge) para crear un nuevo FsImage compacto.
- Enviar el FsImage compactado de vuelta al NameNode.

Este proceso se llama **checkpointing** y evita que el EditLog crezca
indefinidamente. Si el NameNode muere, los datos del Secondary NameNode
pueden ayudar en la recuperacion, pero NO es un failover automatico.

Para alta disponibilidad real se usa un **Standby NameNode** con ZooKeeper
(ver seccion 7.3.11).

### Bloques: la unidad fundamental

Cuando subes un archivo a HDFS, este se divide en **bloques** de tamanio fijo:

```
Archivo original: ventas_2024.csv (400 MB)
                       |
         +-------------+-------------+
         |             |             |
     Bloque 1      Bloque 2      Bloque 3
     (128 MB)      (128 MB)      (144 MB)
                                  [ultimo bloque puede
                                   ser menor a 128 MB]
```

**Tamanio por defecto:** 128 MB (antes era 64 MB en versiones antiguas de Hadoop).

**Por que bloques tan grandes?** A diferencia de un sistema de archivos local
(donde los bloques son de 4 KB), HDFS usa bloques enormes por dos razones:

1. **Minimizar overhead de metadata:** Si tuvieras bloques de 4 KB para un
   archivo de 1 TB, el NameNode tendria que trackear 250 millones de bloques.
   Con bloques de 128 MB, solo necesita trackear ~8,000 bloques.

2. **Maximizar throughput de disco:** Leer un archivo secuencialmente es
   mucho mas rapido que hacer muchas lecturas pequeñas. Con bloques de 128 MB,
   el tiempo de seek del disco es insignificante comparado con el tiempo
   de transferencia.

### Factor de replicacion

Cada bloque se replica en **3 DataNodes diferentes** (por defecto). Esto
significa que un archivo de 400 MB ocupa realmente 1.2 GB en el cluster
(400 MB x 3 copias).

```
Archivo: datos.csv -> 2 bloques (B1, B2)
Factor de replicacion: 3

+----------+  +----------+  +----------+  +----------+  +----------+
| DataNode |  | DataNode |  | DataNode |  | DataNode |  | DataNode |
|    01    |  |    02    |  |    03    |  |    04    |  |    05    |
|----------|  |----------|  |----------|  |----------|  |----------|
|  [B1*]   |  |  [B1]    |  |  [B2*]   |  |          |  |  [B1]    |
|  [B2]    |  |          |  |  [B2]    |  |  [B2]    |  |          |
+----------+  +----------+  +----------+  +----------+  +----------+

B1 esta en: DataNode01, DataNode02, DataNode05  (3 copias)
B2 esta en: DataNode01, DataNode03, DataNode04  (3 copias)

* = replica primaria (primera en ser escrita)
```

**Ventajas de la replicacion:**
- Si un DataNode muere, los datos siguen disponibles en otros 2 nodos.
- Las lecturas se pueden hacer desde el nodo mas cercano al cliente.
- Mayor ancho de banda de lectura (3 nodos pueden servir el mismo bloque).

**Desventaja:** Triplicar el uso de disco. Para 1 PB de datos, necesitas 3 PB
de almacenamiento fisico. (Las versiones modernas ofrecen **erasure coding**
como alternativa mas eficiente: ~1.5x en lugar de 3x.)

### Rack Awareness

En un datacenter real, los servidores estan organizados en **racks** (estantes).
Los servidores del mismo rack comparten un switch de red, por lo que la
comunicacion dentro del rack es mas rapida que entre racks.

HDFS es "rack-aware": sabe en que rack esta cada DataNode y distribuye las
replicas inteligentemente:

```
Rack Awareness: Estrategia de colocacion de replicas (por defecto)

+-------------------+    +-------------------+    +-------------------+
|     RACK 1        |    |     RACK 2        |    |     RACK 3        |
|                   |    |                   |    |                   |
| +-----+ +-----+  |    | +-----+ +-----+  |    | +-----+ +-----+  |
| | DN1 | | DN2 |  |    | | DN3 | | DN4 |  |    | | DN5 | | DN6 |  |
| |     | |     |  |    | |     | |     |  |    | |     | |     |  |
| |[B1] | |     |  |    | |[B1] | |[B1] |  |    | |     | |     |  |
| +-----+ +-----+  |    | +-----+ +-----+  |    | +-----+ +-----+  |
+-------------------+    +-------------------+    +-------------------+

Regla para 3 replicas:
  - Replica 1: en el nodo local (mismo rack del escritor)
  - Replica 2: en un nodo de un rack DIFERENTE
  - Replica 3: en otro nodo del MISMO rack que la replica 2

Esto garantiza que si un rack entero falla (switch muerto, corte de
energia), al menos 1 replica sobrevive en otro rack.
```

---

## 7.3.4 Flujo de escritura en HDFS

Cuando un cliente escribe un archivo en HDFS, ocurre un proceso coordinado
entre el cliente, el NameNode y multiples DataNodes.

### Diagrama paso a paso

```
ESCRITURA DE UN ARCHIVO EN HDFS (Pipeline)
===========================================

    Cliente                NameNode             DataNode1   DataNode2   DataNode3
       |                      |                     |           |           |
       |  1. create("a.csv")  |                     |           |           |
       |--------------------->|                     |           |           |
       |                      |                     |           |           |
       |  2. OK + lista de    |                     |           |           |
       |     DataNodes para   |                     |           |           |
       |     bloque 1:        |                     |           |           |
       |     [DN1, DN2, DN3]  |                     |           |           |
       |<---------------------|                     |           |           |
       |                                            |           |           |
       |  3. Establecer pipeline de escritura        |           |           |
       |==========================================>|           |           |
       |                                            |=========>|           |
       |                                            |           |=========>|
       |                                                                   |
       |  4. Pipeline confirmado                                           |
       |<==================================================================|
       |                                                                   |
       |  5. Enviar datos en "packets" (64 KB cada uno)                    |
       |  +--------+--------+--------+--------+                           |
       |  |pkt 1   |pkt 2   |pkt 3   |pkt N   |                           |
       |  +--------+--------+--------+--------+                           |
       |============> DN1 ==========> DN2 ==========> DN3                  |
       |              (escribe)       (escribe)        (escribe)           |
       |                                                                   |
       |  6. ACK (acknowledgement) en sentido inverso                      |
       |              DN1 <========== DN2 <========== DN3                  |
       |<=============                                                     |
       |                                                                   |
       |  7. Bloque completado.                                            |
       |     Repetir pasos 2-6 para cada bloque.                           |
       |                                                                   |
       |  8. close()          |                     |           |           |
       |--------------------->|                     |           |           |
       |                      |  Confirma recepcion |           |           |
       |                      |  de todos los       |           |           |
       |                      |  bloques            |           |           |
       |  9. OK               |                     |           |           |
       |<---------------------|                     |           |           |
```

### Pasos detallados

1. **El cliente llama a `create()`:** Contacta al NameNode solicitando crear
   un archivo nuevo en una ruta determinada.

2. **El NameNode responde:** Verifica permisos, verifica que el archivo no
   exista, y devuelve una lista de DataNodes para el primer bloque (elegidos
   segun rack awareness y carga actual de cada nodo).

3. **Se establece el pipeline:** El cliente se conecta al primer DataNode (DN1).
   DN1 se conecta a DN2, y DN2 se conecta a DN3. Se forma una cadena.

4. **Confirmacion del pipeline:** DN3 confirma a DN2, DN2 a DN1, DN1 al cliente.
   El pipeline esta listo.

5. **Envio de datos:** El cliente envia datos en paquetes de 64 KB. Cada
   paquete viaja por el pipeline: cliente -> DN1 -> DN2 -> DN3. DN1 escribe
   a disco Y al mismo tiempo reenvia a DN2 (no espera a terminar de escribir).

6. **Acknowledgement:** Cuando DN3 escribe exitosamente un paquete, envia ACK
   a DN2, que envia ACK a DN1, que envia ACK al cliente.

7. **Repeticion:** Se repite para todos los bloques del archivo.

8. **Cierre:** El cliente llama a `close()`. El NameNode confirma que todos los
   bloques fueron recibidos y replica correctamente.

**Dato clave:** El NameNode NO participa en la transferencia de datos. Solo
coordina. Los datos viajan directamente entre el cliente y los DataNodes.

---

## 7.3.5 Flujo de lectura en HDFS

La lectura es mas simple que la escritura y aprovecha el principio de
**data locality** (leer desde el nodo mas cercano).

### Diagrama paso a paso

```
LECTURA DE UN ARCHIVO EN HDFS
===============================

    Cliente                NameNode             DataNode1   DataNode2   DataNode3
       |                      |                     |           |           |
       |  1. open("a.csv")   |                     |           |           |
       |--------------------->|                     |           |           |
       |                      |                     |           |           |
       |  2. Mapa de bloques: |                     |           |           |
       |     B1: [DN1, DN5]   |                     |           |           |
       |     B2: [DN3, DN2]   |                     |           |           |
       |     B3: [DN2, DN4]   |                     |           |           |
       |     (ordenados por   |                     |           |           |
       |      proximidad al   |                     |           |           |
       |      cliente)        |                     |           |           |
       |<---------------------|                     |           |           |
       |                                            |           |           |
       |  3. Leer bloque B1 directamente            |           |           |
       |==========================================>|           |           |
       |                                            |           |           |
       |  4. Datos del bloque B1                    |           |           |
       |<===========================================|           |           |
       |                                                        |           |
       |  5. Leer bloque B2 directamente                        |           |
       |========================================================|=========>|
       |                                                        |           |
       |  6. Datos del bloque B2                                |           |
       |<=======================================================|<==========|
       |                                            |           |           |
       |  [... continua para cada bloque ...]       |           |           |
       |                                            |           |           |
       |  7. close()                                |           |           |
```

### Pasos detallados

1. **El cliente llama a `open()`:** Contacta al NameNode pidiendo leer un archivo.

2. **El NameNode responde:** Devuelve la lista de bloques que componen el archivo
   y, para cada bloque, la lista de DataNodes que tienen una copia. Los DataNodes
   se ordenan por **proximidad al cliente** (mismo nodo > mismo rack > otro rack).

3. **Lectura directa:** El cliente lee el bloque B1 directamente del DataNode
   mas cercano. **El NameNode NO participa en la transferencia de datos.**

4. **Data locality:** Si el cliente esta ejecutandose en un DataNode que tiene
   una copia del bloque, lee directamente del disco local (0 transferencia de red).
   Esto es lo que hace Spark tan rapido: programa las tareas en los nodos que
   ya tienen los datos.

5. **Verificacion:** Cada bloque tiene un **checksum**. El cliente verifica la
   integridad de cada bloque despues de leerlo. Si el checksum falla, lee de
   otra replica.

6. **Secuencial:** El cliente lee los bloques en orden (B1, B2, B3...) para
   reconstruir el archivo completo.

**Data locality es la clave del rendimiento en Big Data:** En lugar de mover
terabytes de datos hacia el programa, mueves el programa hacia donde estan los
datos. Spark aprovecha esto al maximo.

---

## 7.3.6 Comandos HDFS: referencia completa

Los comandos HDFS siguen una sintaxis similar a los comandos Unix. Se invocan
con `hdfs dfs` seguido del comando.

### Navegacion y listado

```bash
# Listar contenido de un directorio
hdfs dfs -ls /
hdfs dfs -ls /user/hadoop/datos/

# Listar recursivamente
hdfs dfs -ls -R /user/hadoop/

# Crear un directorio
hdfs dfs -mkdir /user/hadoop/output

# Crear directorios anidados (como mkdir -p)
hdfs dfs -mkdir -p /user/hadoop/datos/ventas/2024
```

### Subir y bajar archivos

```bash
# Subir archivo local a HDFS
hdfs dfs -put archivo_local.csv /user/hadoop/datos/
# Equivalente:
hdfs dfs -copyFromLocal archivo_local.csv /user/hadoop/datos/

# Subir y borrar el archivo local (mover a HDFS)
hdfs dfs -moveFromLocal archivo_local.csv /user/hadoop/datos/

# Descargar archivo de HDFS a local
hdfs dfs -get /user/hadoop/datos/resultado.csv ./local/
# Equivalente:
hdfs dfs -copyToLocal /user/hadoop/datos/resultado.csv ./local/

# Copiar archivos dentro de HDFS
hdfs dfs -cp /datos/origen.csv /datos/backup/origen.csv

# Mover archivos dentro de HDFS
hdfs dfs -mv /datos/temp.csv /datos/procesados/temp.csv
```

### Leer contenido

```bash
# Ver contenido de un archivo (como cat)
hdfs dfs -cat /user/hadoop/datos/muestra.csv

# Ver las primeras lineas (piping con head)
hdfs dfs -cat /user/hadoop/datos/grande.csv | head -20

# Ver las ultimas lineas
hdfs dfs -tail /user/hadoop/datos/log.txt

# Contar lineas, palabras, bytes
hdfs dfs -cat /user/hadoop/datos/muestra.csv | wc -l
```

### Eliminar archivos

```bash
# Eliminar un archivo
hdfs dfs -rm /user/hadoop/datos/temporal.csv

# Eliminar un directorio (recursivo)
hdfs dfs -rm -r /user/hadoop/datos/temp/

# Eliminar sin mover a la papelera (permanente)
hdfs dfs -rm -skipTrash /user/hadoop/datos/temporal.csv

# Vaciar la papelera
hdfs dfs -expunge
```

### Informacion y estadisticas

```bash
# Ver espacio usado por un directorio
hdfs dfs -du /user/hadoop/datos/
# Version legible (human-readable)
hdfs dfs -du -h /user/hadoop/datos/
# Con resumen total
hdfs dfs -du -s -h /user/hadoop/datos/

# Ver factor de replicacion y tamanio de bloques
hdfs dfs -stat "%r %o %n" /user/hadoop/datos/archivo.csv
# %r = factor de replicacion
# %o = tamanio de bloque
# %n = nombre del archivo

# Contar archivos, directorios y bytes
hdfs dfs -count /user/hadoop/datos/
```

### Permisos

```bash
# Cambiar permisos (como chmod en Linux)
hdfs dfs -chmod 755 /user/hadoop/datos/script.sh
hdfs dfs -chmod -R 644 /user/hadoop/datos/

# Cambiar propietario
hdfs dfs -chown hadoop:hadoop /user/hadoop/datos/
hdfs dfs -chown -R hadoop:hadoop /user/hadoop/
```

### Administracion del cluster

```bash
# Reporte del estado del cluster
hdfs dfsadmin -report
# Muestra: capacidad total, espacio usado, DataNodes activos, etc.

# Verificar integridad del sistema de archivos
hdfs fsck /
# Muestra: bloques perdidos, sub-replicados, corruptos

# Verificar un directorio especifico con detalle
hdfs fsck /user/hadoop/datos/ -files -blocks -locations

# Ver la topologia del cluster (racks)
hdfs dfsadmin -printTopology

# Modo seguro (safe mode): el NameNode no permite escrituras
hdfs dfsadmin -safemode get     # Consultar estado
hdfs dfsadmin -safemode enter   # Entrar en modo seguro
hdfs dfsadmin -safemode leave   # Salir de modo seguro
```

### Ejemplo practico completo

```bash
# 1. Crear estructura de directorios
hdfs dfs -mkdir -p /proyecto/datos/raw
hdfs dfs -mkdir -p /proyecto/datos/processed
hdfs dfs -mkdir -p /proyecto/output

# 2. Subir datos
hdfs dfs -put ventas_2024.csv /proyecto/datos/raw/

# 3. Verificar que se subio correctamente
hdfs dfs -ls /proyecto/datos/raw/
hdfs dfs -du -h /proyecto/datos/raw/

# 4. Ver las primeras lineas
hdfs dfs -cat /proyecto/datos/raw/ventas_2024.csv | head -5

# 5. (Spark o MapReduce procesan los datos y escriben en /proyecto/output/)

# 6. Descargar resultados
hdfs dfs -get /proyecto/output/resultados.parquet ./resultados_local/

# 7. Verificar integridad
hdfs fsck /proyecto/ -files
```

---

## 7.3.7 Montando Hadoop con Docker

Para experimentar con HDFS sin necesitar un cluster real, podemos levantar
un mini-cluster usando Docker Compose.

### docker-compose.yml

```yaml
# docker-compose.yml - Mini cluster Hadoop (NameNode + 2 DataNodes)
# Basado en la imagen oficial de Apache Hadoop
version: "3.8"

services:
  # ============================================================
  # NameNode: El maestro del cluster HDFS
  # Almacena metadata, namespace y ubicacion de bloques
  # ============================================================
  namenode:
    image: apache/hadoop:3.3.6
    hostname: namenode
    container_name: namenode
    command: ["hdfs", "namenode"]
    ports:
      - "9870:9870"   # Web UI del NameNode (http://localhost:9870)
      - "9000:9000"   # Puerto RPC (usado por clientes y DataNodes)
    environment:
      # Directorio donde el NameNode guarda su metadata
      HADOOP_HOME: /opt/hadoop
      # Configuraciones de HDFS (se pasan como variables de entorno)
      ENSURE_NAMENODE_DIR: /tmp/hadoop-root/dfs/name
    env_file:
      - ./hadoop.env
    volumes:
      # Persistir metadata del NameNode entre reinicios
      - namenode_data:/tmp/hadoop-root/dfs/name
    networks:
      - hadoop_network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9870/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ============================================================
  # DataNode 1: Almacena bloques reales de datos
  # ============================================================
  datanode1:
    image: apache/hadoop:3.3.6
    hostname: datanode1
    container_name: datanode1
    command: ["hdfs", "datanode"]
    ports:
      - "9864:9864"   # Web UI del DataNode 1 (http://localhost:9864)
    environment:
      HADOOP_HOME: /opt/hadoop
    env_file:
      - ./hadoop.env
    volumes:
      # Persistir bloques de datos
      - datanode1_data:/tmp/hadoop-root/dfs/data
    networks:
      - hadoop_network
    depends_on:
      namenode:
        condition: service_healthy

  # ============================================================
  # DataNode 2: Segundo nodo de almacenamiento
  # ============================================================
  datanode2:
    image: apache/hadoop:3.3.6
    hostname: datanode2
    container_name: datanode2
    command: ["hdfs", "datanode"]
    ports:
      - "9865:9864"   # Web UI del DataNode 2 (http://localhost:9865)
    environment:
      HADOOP_HOME: /opt/hadoop
    env_file:
      - ./hadoop.env
    volumes:
      - datanode2_data:/tmp/hadoop-root/dfs/data
    networks:
      - hadoop_network
    depends_on:
      namenode:
        condition: service_healthy

  # ============================================================
  # ResourceManager (YARN): Gestion de recursos del cluster
  # ============================================================
  resourcemanager:
    image: apache/hadoop:3.3.6
    hostname: resourcemanager
    container_name: resourcemanager
    command: ["yarn", "resourcemanager"]
    ports:
      - "8088:8088"   # Web UI de YARN (http://localhost:8088)
    environment:
      HADOOP_HOME: /opt/hadoop
    env_file:
      - ./hadoop.env
    networks:
      - hadoop_network
    depends_on:
      namenode:
        condition: service_healthy

volumes:
  namenode_data:
    driver: local
  datanode1_data:
    driver: local
  datanode2_data:
    driver: local

networks:
  hadoop_network:
    driver: bridge
```

### Archivo de configuracion hadoop.env

```bash
# hadoop.env - Variables de entorno compartidas por todos los servicios

# --- core-site.xml ---
CORE-SITE.XML_fs.defaultFS=hdfs://namenode:9000
CORE-SITE.XML_hadoop.http.staticuser.user=root

# --- hdfs-site.xml ---
HDFS-SITE.XML_dfs.replication=2
# Usamos factor 2 (no 3) porque solo tenemos 2 DataNodes
HDFS-SITE.XML_dfs.namenode.name.dir=/tmp/hadoop-root/dfs/name
HDFS-SITE.XML_dfs.datanode.data.dir=/tmp/hadoop-root/dfs/data
HDFS-SITE.XML_dfs.permissions.enabled=false
# Deshabilitamos permisos para simplificar en desarrollo

# --- yarn-site.xml ---
YARN-SITE.XML_yarn.resourcemanager.hostname=resourcemanager
YARN-SITE.XML_yarn.nodemanager.aux-services=mapreduce_shuffle
YARN-SITE.XML_yarn.nodemanager.resource.memory-mb=2048
YARN-SITE.XML_yarn.scheduler.maximum-allocation-mb=2048
YARN-SITE.XML_yarn.nodemanager.resource.cpu-vcores=2

# --- mapred-site.xml ---
MAPRED-SITE.XML_mapreduce.framework.name=yarn
```

### Puertos importantes

| Puerto | Servicio | URL | Que muestra |
|--------|----------|-----|-------------|
| 9870 | NameNode UI | http://localhost:9870 | Estado del cluster, DataNodes activos, uso de disco |
| 9864 | DataNode 1 UI | http://localhost:9864 | Estado del DataNode, bloques almacenados |
| 9865 | DataNode 2 UI | http://localhost:9865 | Estado del DataNode 2 |
| 8088 | YARN ResourceManager | http://localhost:8088 | Aplicaciones en ejecucion, recursos del cluster |
| 9000 | HDFS RPC | (no web) | Puerto para clientes y DataNodes |

### Levantar y verificar

```bash
# 1. Levantar el cluster
docker compose up -d

# 2. Esperar ~30 segundos a que todo arranque

# 3. Verificar que los DataNodes se registraron
docker exec -it namenode hdfs dfsadmin -report

# Deberia mostrar algo como:
# Configured Capacity: ...
# Live datanodes (2):
#   Name: datanode1:9866
#   Name: datanode2:9866

# 4. Probar subir un archivo
docker exec -it namenode bash -c "echo 'Hola HDFS' > /tmp/test.txt"
docker exec -it namenode hdfs dfs -mkdir -p /test
docker exec -it namenode hdfs dfs -put /tmp/test.txt /test/
docker exec -it namenode hdfs dfs -cat /test/test.txt

# 5. Verificar en la UI: http://localhost:9870
#    Ir a "Utilities" -> "Browse the file system"

# 6. Detener el cluster
docker compose down

# 7. Detener y eliminar volumenes (borra datos)
docker compose down -v
```

---

## 7.3.8 HDFS vs sistemas de archivos locales

HDFS no es un reemplazo de ext4, NTFS o APFS. Es un sistema especializado
con compromisos de disenio muy diferentes.

### Tabla comparativa

| Caracteristica | Sistema local (ext4/NTFS) | HDFS |
|---------------|--------------------------|------|
| **Tamanio de bloque** | 4 KB | 128 MB |
| **Optimizado para** | Archivos pequeños y medianos | Archivos MUY grandes (GB-TB) |
| **Patron de acceso** | Lectura y escritura aleatoria | Write-once, read-many |
| **Edicion in-place** | Si (puedes modificar un byte) | No (reemplazas el archivo completo) |
| **Latencia** | Muy baja (microsegundos) | Alta (milisegundos a segundos) |
| **Throughput** | Limitado a 1 disco | Alto (lee de N discos en paralelo) |
| **Tolerancia a fallos** | Un disco muere = datos perdidos | 3 copias en diferentes nodos |
| **Escalabilidad** | 1 maquina | Miles de maquinas |
| **Archivos pequeños** | Eficiente | MUY ineficiente |

### Write-once, read-many

HDFS esta diseñado bajo el principio de que los datos se **escriben una vez**
y se **leen muchas veces**. No puedes abrir un archivo y editar la linea 47.
Si necesitas modificar un archivo, lo reemplazas completamente.

Esto simplifica enormemente el disenio (no hay locks de escritura, no hay
problemas de concurrencia en escritura) y es perfecto para datos analiticos:
logs, datasets, resultados de ETL, etc.

### El "small file problem"

El problema mas grave de HDFS es el manejo de **archivos pequeños**. Cada
archivo, sin importar su tamanio, ocupa al menos una entrada en la metadata
del NameNode (~150 bytes de RAM).

```
Escenario A: 1 archivo de 1 TB
  -> 8,192 bloques de 128 MB
  -> ~8,192 entradas en NameNode
  -> Funciona perfectamente

Escenario B: 1 millon de archivos de 1 KB cada uno
  -> 1 millon de bloques (1 por archivo)
  -> ~1 millon de entradas en NameNode
  -> 150 MB de RAM SOLO para metadata
  -> Rendimiento degradado severamente

Escenario C: 1,000 millones de archivos de 1 KB
  -> NameNode necesita ~150 GB de RAM solo para metadata
  -> IMPOSIBLE de operar
```

**Solucion:** Si tienes muchos archivos pequeños, combinalos en archivos
grandes antes de subirlos a HDFS. Formatos como **Parquet**, **Avro** o
**SequenceFile** permiten empaquetar millones de registros en pocos archivos
grandes y eficientes.

---

## 7.3.9 YARN: gestion de recursos del cluster

YARN (Yet Another Resource Negotiator) es el "sistema operativo" del cluster
Hadoop. Gestiona CPU y memoria, y permite que multiples aplicaciones
(MapReduce, Spark, Hive, etc.) compartan el mismo cluster.

### Arquitectura de YARN

```
+================================================================+
|                     CLUSTER YARN                                |
+================================================================+
|                                                                 |
|   +---------------------------+                                 |
|   |    ResourceManager (RM)   |   (MAESTRO - 1 por cluster)    |
|   |---------------------------|                                 |
|   |  - Scheduler: decide      |                                 |
|   |    quien recibe recursos  |                                 |
|   |  - ApplicationsManager:   |                                 |
|   |    acepta trabajos,       |                                 |
|   |    lanza AppMasters       |                                 |
|   +---------------------------+                                 |
|        |           |           |                                 |
|        v           v           v                                 |
|   +---------+ +---------+ +---------+                           |
|   |NodeMgr 1| |NodeMgr 2| |NodeMgr 3|  (1 por nodo del cluster)|
|   |---------|	|---------|	|---------| 			  |
|   |Container| |Container| |Container|                           |
|   |Container| |Container| |Container|                           |
|   |   AM    | |Container| |Container|                           |
|   +---------+ +---------+ +---------+                           |
|                                                                 |
|   AM = ApplicationMaster (1 por aplicacion Spark/MR)            |
|   Container = unidad de recurso (CPU + RAM asignada)            |
+================================================================+
```

### Componentes

**ResourceManager (RM):** El maestro de YARN. Tiene dos partes:
- **Scheduler:** Asigna recursos a las aplicaciones segun politicas configuradas
  (FIFO, Fair Scheduler, Capacity Scheduler).
- **ApplicationsManager:** Acepta nuevos trabajos y lanza un ApplicationMaster
  para cada uno.

**NodeManager (NM):** Un agente que corre en cada nodo del cluster.
- Monitorea los recursos locales (CPU, RAM, disco).
- Lanza y supervisa Containers.
- Reporta al ResourceManager.

**ApplicationMaster (AM):** Uno por cada aplicacion enviada al cluster.
- Negocia recursos con el ResourceManager.
- Coordina la ejecucion de las tareas dentro de sus Containers.
- En Spark, el ApplicationMaster es el **Driver** (o un proceso que lanza el Driver).

**Container:** La unidad de recurso en YARN. Un Container es un conjunto de
CPU y RAM asignado en un NodeManager especifico. Por ejemplo: 2 cores + 4 GB RAM.
Los Executors de Spark corren dentro de Containers.

### Como Spark usa YARN

Cuando ejecutas Spark sobre YARN:

```bash
# Enviar una aplicacion Spark al cluster YARN
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 10 \
  --executor-memory 4g \
  --executor-cores 2 \
  mi_aplicacion.py
```

Lo que sucede internamente:

1. `spark-submit` contacta al ResourceManager de YARN.
2. YARN lanza un ApplicationMaster (el Spark Driver en modo `cluster`).
3. El ApplicationMaster pide 10 Containers al ResourceManager (para los Executors).
4. YARN asigna Containers en los NodeManagers disponibles.
5. El Driver coordina la ejecucion de tareas en los Executors.
6. Al terminar, los Containers se liberan.

**Deploy modes:**
- `--deploy-mode client`: El Driver corre en tu maquina local. Util para
  desarrollo interactivo (notebooks, spark-shell).
- `--deploy-mode cluster`: El Driver corre dentro del cluster YARN. Util para
  produccion (el trabajo no depende de tu maquina).

---

## 7.3.10 Spark sobre HDFS

La combinacion **HDFS + YARN + Spark** es la arquitectura mas comun en clusters
de Big Data en produccion. Cada componente hace lo que mejor sabe hacer:

```
+-------------------------------------------------------------------+
|  SPARK (procesamiento en memoria)                                 |
|  - Lee datos de HDFS                                              |
|  - Procesa en RAM (transformaciones, joins, ML)                   |
|  - Escribe resultados a HDFS o a una base de datos                |
+-------------------------------------------------------------------+
         |                              |
         | lee de                       | escribe a
         v                              v
+-------------------------------------------------------------------+
|  HDFS (almacenamiento distribuido)                                |
|  - Datos particionados en bloques de 128 MB                      |
|  - Replicados en 3 nodos                                         |
|  - Optimizado para lecturas secuenciales                          |
+-------------------------------------------------------------------+
         |
         | gestionado por
         v
+-------------------------------------------------------------------+
|  YARN (gestion de recursos)                                       |
|  - Asigna CPU y RAM a Spark                                       |
|  - Permite que multiples aplicaciones compartan el cluster        |
+-------------------------------------------------------------------+
```

### Lectura desde HDFS en Spark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Lectura desde HDFS") \
    .master("yarn") \
    .getOrCreate()

# Leer un CSV desde HDFS
df = spark.read.csv("hdfs://namenode:9000/datos/ventas_2024.csv",
                     header=True, inferSchema=True)

# Leer un directorio completo de archivos Parquet
df = spark.read.parquet("hdfs://namenode:9000/datos/ventas_parquet/")

# Leer con particiones (Spark detecta automaticamente la estructura)
df = spark.read.parquet("hdfs://namenode:9000/datos/ventas/year=2024/")

# Procesar
resultado = df.groupBy("region").agg({"monto": "sum"})

# Escribir resultado de vuelta a HDFS
resultado.write.parquet("hdfs://namenode:9000/output/ventas_por_region/")

# O escribir a una base de datos
resultado.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://db:5432/analytics") \
    .option("dbtable", "ventas_resumen") \
    .save()
```

### Data locality en accion

Cuando Spark lee de HDFS, el Spark Driver consulta al NameNode para saber
en que DataNodes estan los bloques. Luego, YARN intenta programar los
Executors de Spark **en los mismos nodos** que tienen los datos:

```
Sin data locality:                  Con data locality (HDFS + YARN):

DataNode1 [datos] ---red--->        DataNode1 [datos] --> Executor 1
                           |           (procesamiento local, sin red!)
DataNode2 [datos] ---red--->  Executor
                           |        DataNode2 [datos] --> Executor 2
DataNode3 [datos] ---red--->           (procesamiento local, sin red!)

Cuello de botella: RED              Sin cuello de botella de red
```

Esto es lo que hace que Spark + HDFS sea tan eficiente: **mueves el computo
hacia los datos**, no los datos hacia el computo.

### Ventajas sobre leer desde disco local

| Aspecto | Disco local | HDFS |
|---------|-------------|------|
| Paralelismo de lectura | 1 disco | N discos en paralelo |
| Tolerancia a fallos | Disco muere = datos perdidos | 3 copias automaticas |
| Escala | Limitado a 1 maquina | Petabytes en miles de maquinas |
| Data locality con Spark | No aplica | Executor lee de disco local del DataNode |
| Compartir datos | Copiar manualmente a cada maquina | Todos leen del mismo HDFS |

---

## 7.3.11 Tolerancia a fallos

En un cluster de miles de maquinas, **los fallos son la norma, no la excepcion**.
Google estimo que en un cluster de 10,000 nodos, al menos un disco falla
por dia. HDFS fue diseñado desde el principio para manejar esto.

### Escenario 1: Muere un DataNode

```
ANTES:                          DESPUES (automatico):

DN1: [B1] [B3] [B5]            DN1: MUERTO (sin heartbeat por 10 min)
DN2: [B1] [B4] [B6]            DN2: [B1] [B4] [B6]
DN3: [B2] [B3] [B4]            DN3: [B2] [B3] [B4] [B5] <-- re-replica
DN4: [B2] [B5] [B6]            DN4: [B2] [B5] [B6] [B3] <-- re-replica
DN5: [B1] [B2] [B3]            DN5: [B1] [B2] [B3] [B5] <-- re-replica

NameNode detecta que DN1 no envia heartbeat durante 10 minutos.
Lo marca como muerto. Verifica que bloques estaban en DN1 (B1, B3, B5).
Comprueba que cada bloque tenga al menos 3 replicas.
Ordena re-replicacion de los bloques sub-replicados a otros DataNodes.

TODO ESTO OCURRE AUTOMATICAMENTE. No se necesita intervencion humana.
```

**Proceso detallado:**

1. Cada DataNode envia un **heartbeat** al NameNode cada 3 segundos.
2. Si el NameNode no recibe heartbeat durante 10 minutos (configurable),
   marca al DataNode como muerto.
3. El NameNode revisa su tabla de bloques: identifica que bloques estaban
   en el DataNode muerto.
4. Para cada bloque que ahora tiene menos de 3 replicas, el NameNode
   ordena a otro DataNode que tenga una copia que la replique a un
   DataNode que no la tenga.
5. El factor de replicacion se restaura automaticamente.

### Escenario 2: Muere el NameNode

Este es el punto debil de HDFS: el NameNode es un **Single Point of Failure (SPOF)**.
Si el NameNode muere, **todo el cluster HDFS se detiene**. Nadie puede leer
ni escribir porque nadie sabe donde estan los bloques.

**Solucion: HDFS High Availability (HA) con ZooKeeper**

```
+------------------+         +------------------+
|  NameNode        |         |  NameNode        |
|  (ACTIVO)        |  <----> |  (STANDBY)       |
|                  |  sync   |                  |
| Sirve peticiones |         | Listo para tomar |
| de clientes      |         | el control       |
+------------------+         +------------------+
        |                           |
        +----------+----------------+
                   |
          +------------------+
          |   ZOOKEEPER      |
          |  (3-5 nodos)     |
          |                  |
          | - Detecta fallo  |
          | - Hace failover  |
          |   automatico     |
          +------------------+
```

- Se configuran **dos NameNodes**: uno Activo y uno Standby.
- Ambos mantienen la metadata sincronizada a traves de un Journal compartido
  (JournalNodes o NFS compartido).
- ZooKeeper monitorea la salud del NameNode Activo.
- Si el Activo falla, ZooKeeper automaticamente promueve al Standby a Activo.
- El failover toma solo unos segundos.

### Escenario 3: Disco corrupto / datos corruptos

Cada bloque en HDFS tiene un **checksum** (por defecto CRC32C). Cuando un
cliente lee un bloque:

1. Lee los datos y el checksum almacenado.
2. Calcula el checksum de los datos recibidos.
3. Si no coinciden: el bloque esta corrupto.
4. El cliente notifica al NameNode.
5. El NameNode marca esa replica como corrupta.
6. El NameNode ordena re-replicacion desde una replica sana.
7. El cliente lee de otra replica automaticamente.

Los DataNodes tambien verifican checksums periodicamente en segundo plano
(proceso llamado **DataBlockScanner**), detectando corrupcion silenciosa antes
de que un cliente la encuentre.

---

## 7.3.12 Hadoop en la nube

Hoy en dia, muchas empresas no operan clusters Hadoop fisicos. En su lugar,
usan servicios gestionados en la nube que ofrecen la misma funcionalidad
sin la complejidad operativa.

### Servicios gestionados

| Proveedor | Servicio | Descripcion |
|-----------|----------|-------------|
| **AWS** | Amazon EMR (Elastic MapReduce) | Cluster Hadoop/Spark gestionado, se levanta en minutos |
| **Google Cloud** | Dataproc | Cluster Hadoop/Spark con integracion nativa a BigQuery |
| **Azure** | HDInsight | Cluster Hadoop/Spark gestionado en Azure |

### Object Storage como "HDFS en la nube"

El cambio mas importante en la nube es que **HDFS se reemplaza por Object Storage**:

| HDFS (on-premise) | Object Storage (nube) |
|-------------------|-----------------------|
| `hdfs://namenode:9000/datos/` | `s3://mi-bucket/datos/` (AWS) |
| | `gs://mi-bucket/datos/` (Google Cloud) |
| | `abfss://container@account/datos/` (Azure) |

```python
# Lectura en Spark desde S3 (en lugar de HDFS)
df = spark.read.parquet("s3a://mi-bucket/datos/ventas/")

# Lectura desde Google Cloud Storage
df = spark.read.parquet("gs://mi-bucket/datos/ventas/")
```

### El patron moderno: computo efimero + almacenamiento persistente

```
PATRON CLASICO (on-premise):        PATRON MODERNO (nube):

+-------------------------+          +-------------------------+
| Cluster permanente      |          | Object Storage (S3/GCS) |
|  HDFS + YARN + Spark    |          | (siempre encendido,     |
|  (siempre encendido,    |          |  centavos por GB/mes)   |
|  costoso 24/7)          |          +-------------------------+
+-------------------------+                    |
                                               v
                                    +-------------------------+
                                    | Cluster Spark efimero   |
                                    | (se levanta para un job,|
                                    |  se destruye al terminar|
                                    |  pagas solo por uso)    |
                                    +-------------------------+
```

**Ventajas del patron moderno:**
- **Costo:** Solo pagas computo cuando lo necesitas.
- **Escalabilidad:** Puedes crear un cluster de 100 nodos para un job de 2 horas
  y destruirlo. Con Hadoop on-premise, esos 100 nodos estarian ociosos el resto
  del tiempo.
- **Separacion storage/compute:** Los datos persisten en S3 independientemente
  del cluster. Puedes tener multiples clusters leyendo los mismos datos.

**Desventaja principal:** La latencia de red entre computo y storage es mayor
que con HDFS (donde el dato esta en el disco local). Se compensa con el ancho
de banda masivo de la red interna de los proveedores cloud.

---

## 7.3.13 Hadoop vs Spark: no son competidores

Esta es una de las confusiones mas comunes en Big Data. Hay que aclararlo
de una vez:

### La analogia del auto

```
HADOOP = El auto completo              SPARK = Un motor nuevo
  - HDFS    = el tanque de gasolina      - Reemplaza a MapReduce
  - YARN    = la transmision               (el motor viejo)
  - MapReduce = el motor (original)      - PERO necesita tanque (HDFS/S3)
                                         - Y necesita transmision (YARN/K8s)
```

### Comparacion precisa

| Aspecto | Hadoop | Spark |
|---------|--------|-------|
| **Que es** | Ecosistema completo (storage + compute + resource mgmt) | Motor de procesamiento |
| **Almacenamiento** | HDFS | NO tiene (usa HDFS, S3, GCS, local, etc.) |
| **Gestion de recursos** | YARN | NO tiene (usa YARN, Kubernetes, Mesos, Standalone) |
| **Procesamiento** | MapReduce (disco a disco) | En memoria (10-100x mas rapido) |
| **Lenguajes** | Java (principalmente) | Python, Scala, Java, R, SQL |
| **Interactividad** | No (solo batch) | Si (spark-shell, notebooks, streaming) |

### En produccion real

La combinacion mas usada en empresas es:

```
+-------------------+
|      SPARK        |  <-- Motor de procesamiento (reemplazo de MapReduce)
+-------------------+
         |
+-------------------+
|       YARN        |  <-- Gestion de recursos (parte de Hadoop)
+-------------------+
         |
+-------------------+
|       HDFS        |  <-- Almacenamiento (parte de Hadoop)
+-------------------+

Esto es "Spark sobre Hadoop" y es la configuracion estandar.
```

### Spark sin Hadoop: es posible pero...

Spark puede funcionar sin ningun componente de Hadoop:

```python
# Spark "standalone" leyendo de disco local
spark = SparkSession.builder \
    .master("local[*]") \
    .getOrCreate()

df = spark.read.csv("/home/user/datos/archivo.csv")
```

Pero en produccion real, siempre necesitas:
1. **Un storage distribuido:** HDFS, S3, GCS, Azure Blob.
2. **Un cluster manager:** YARN, Kubernetes, Mesos, o Spark Standalone.

Spark sin storage distribuido es como un auto de carreras sin pista:
tecnicamente funciona, pero no puedes aprovechar su potencial.

### Resumen final

```
NO DIGAS: "Usamos Spark en vez de Hadoop"
SI DIGAS: "Usamos Spark en vez de MapReduce, sobre HDFS y YARN"

NO DIGAS: "Hadoop esta muerto"
SI DIGAS: "MapReduce esta en desuso, pero HDFS y YARN siguen muy vivos"
```

---

## 7.3.14 Referencias

### Papers originales (lectura recomendada)

1. **Ghemawat, S., Gobioff, H., & Leung, S.-T. (2003).** The Google File System.
   *19th ACM Symposium on Operating Systems Principles (SOSP)*.
   https://research.google/pubs/pub51/

2. **Dean, J., & Ghemawat, S. (2004).** MapReduce: Simplified Data Processing
   on Large Clusters. *6th USENIX Symposium on Operating Systems Design and
   Implementation (OSDI)*.
   https://research.google/pubs/pub62/

3. **Chang, F., et al. (2006).** Bigtable: A Distributed Storage System for
   Structured Data. *7th USENIX Symposium on Operating Systems Design and
   Implementation (OSDI)*.
   https://research.google/pubs/pub27898/

### Libros

4. **White, T. (2015).** *Hadoop: The Definitive Guide (4th Edition)*. O'Reilly Media.
   El libro de referencia para Hadoop.

5. **Kleppmann, M. (2017).** *Designing Data-Intensive Applications*. O'Reilly Media.
   Capitulos 5 (Replication) y 6 (Partitioning) son especialmente relevantes.

### Documentacion oficial

6. **Apache Hadoop:** https://hadoop.apache.org/docs/current/
7. **HDFS Architecture:** https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
8. **YARN Architecture:** https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html
9. **Apache Spark on YARN:** https://spark.apache.org/docs/3.5.4/running-on-yarn.html

### Articulos academicos complementarios

10. **Shvachko, K., et al. (2010).** The Hadoop Distributed File System.
    *IEEE 26th Symposium on Mass Storage Systems and Technologies (MSST)*.

11. **Zaharia, M., et al. (2016).** Apache Spark: A unified engine for big data
    processing. *Communications of the ACM, 59(11)*, 56-65.

---

## Resumen visual del modulo

```
+===================================================================+
|                                                                    |
|   Google (2003-2006)                                               |
|     |                                                              |
|     | publica 3 papers                                             |
|     v                                                              |
|   Doug Cutting (2006)                                              |
|     |                                                              |
|     | implementa open source                                       |
|     v                                                              |
|   HADOOP = HDFS + MapReduce + YARN                                 |
|              |        |         |                                   |
|              |        |         +-> gestiona CPU y RAM              |
|              |        |                                             |
|              |        +-> procesamiento batch (REEMPLAZADO por      |
|              |            Spark en 2015+)                           |
|              |                                                     |
|              +-> almacenamiento distribuido (SIGUE VIGENTE)        |
|                  - Bloques de 128 MB                               |
|                  - 3 replicas por bloque                           |
|                  - NameNode (metadata) + DataNodes (datos)         |
|                  - Tolerante a fallos                              |
|                                                                    |
|   HOY (2025+):                                                     |
|     On-premise: HDFS + YARN + Spark                                |
|     Nube: S3/GCS + Kubernetes/YARN + Spark                         |
|                                                                    |
+===================================================================+
```

---

Volver a: [Modulo 07 - Infraestructura Big Data](../README.md)

---

-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA:
- Dean, J. & Ghemawat, S. (2004). MapReduce: Simplified Data Processing on Large Clusters. OSDI'04, 137-150.
- Ghemawat, S., Gobioff, H. & Leung, S.T. (2003). The Google File System. SOSP'03, 29-43.
- Shvachko, K., et al. (2010). The Hadoop Distributed File System. IEEE MSST, 1-10.
- White, T. (2015). Hadoop: The Definitive Guide (4th ed.). O'Reilly Media.
- Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media.
- Apache Hadoop Documentation. https://hadoop.apache.org/docs/current/
-------------------------
