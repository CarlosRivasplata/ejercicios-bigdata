# Paso 4: Resultados y Analisis

**Alumno:** [Nombre Apellido]
**Pregunta de investigacion:** [Tu pregunta]

---

## 3.1 Grafico 1: [Titulo descriptivo]

![Grafico 1](capturas/grafico1.png)

### Interpretacion

[Escribe un parrafo respondiendo estas preguntas:
- Que patron o tendencia se observa en el grafico?
- Hay diferencias entre los paises? Cuales?
- Hay algun punto de inflexion o cambio notable? En que anio?
- Como se relaciona esto con tu pregunta de investigacion?]

### Prompt que usaste para generar este grafico

**Herramienta:** [ChatGPT / Claude / Copilot / otra / ninguna]

**Tu prompt exacto:**
```
[PEGA AQUI el prompt que usaste para escribir el codigo de este grafico.
Si lo escribiste tu sin IA, escribe "Codigo propio" y explica que
referencia usaste (documentacion de matplotlib, ejemplo de clase, etc.)]
```

**Que tuviste que ajustar:**
[Que cambiaste de lo que te genero la IA para que funcionara o se viera bien]

---

## 3.2 Grafico 2: [Titulo descriptivo]

![Grafico 2](capturas/grafico2.png)

### Interpretacion

[Mismo formato que el Grafico 1. Explica que muestra y que significa.]

### Prompt que usaste para generar este grafico

**Herramienta:** [ChatGPT / Claude / Copilot / otra / ninguna]

**Tu prompt exacto:**
```
[PEGA AQUI]
```

**Que tuviste que ajustar:**
[Tu respuesta]

---

## 3.3 Respuesta a mi pregunta de investigacion

[Basandote en tus graficos y datos, responde tu pregunta de investigacion
en 2-3 parrafos. Usa evidencia de tus graficos para respaldar tu respuesta.

Ejemplo: "Los datos muestran que la calidad institucional en el Cono Sur
mejoro consistentemente entre 2000-2015, especialmente en Uruguay (vdem_polyarchy
paso de 0.82 a 0.91). En contraste, el Sudeste Asiatico muestra trayectorias
divergentes: Tailandia sufrio un retroceso en 2014 (golpe de estado) mientras
que Indonesia mantuvo una mejora gradual..."]

---

## 3.4 Limitaciones

[Menciona al menos 1 limitacion de tu analisis. Ejemplo:
- "QoG no tiene datos completos para todos los anios en algunas variables"
- "5 paises no son suficientes para generalizar a toda una region"
- "El clustering con pocas variables puede no capturar toda la complejidad"]

---

## 3.5 Dashboard interactivo (opcional pero recomendado)

Puedes generar un dashboard HTML interactivo para mostrar tus resultados de forma visual.
El sistema lo detecta automaticamente y lo muestra en el ranking del curso con un boton
"Dashboard" para que cualquiera pueda verlo sin descargar nada.

### Estructura de carpetas

Pon tu dashboard en una de estas ubicaciones (el sistema busca en este orden):

```
tu_carpeta/
├── outputs/
│   └── dashboard/
│       ├── index.html         <-- Opcion 1: RECOMENDADA
│       └── assets/            <-- Archivos extras (JS, CSS, imagenes)
│           ├── datos.js
│           └── estilos.css
├── dashboard.html             <-- Opcion 2: en la raiz de tu carpeta
├── pipeline.py
├── PROMPTS.md
├── requirements.txt
└── ...
```

### Ejemplo completo con Plotly (copia y adapta)

Agrega este codigo al final de tu `pipeline.py` para generar un dashboard automaticamente:

```python
# =============================================
# GENERAR DASHBOARD HTML
# =============================================
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Crear carpeta de salida
os.makedirs("outputs/dashboard", exist_ok=True)

# Crear figura con multiples graficos
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=[
        "Grafico 1: Evolucion temporal",
        "Grafico 2: Comparativa por pais",
        "Grafico 3: Distribucion",
        "Grafico 4: Correlacion"
    ],
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "histogram"}, {"type": "scatter"}]]
)

# --- Grafico 1: Lineas temporales ---
# Adapta con tus datos reales (df es tu DataFrame)
for pais in df["pais"].unique():
    datos_pais = df[df["pais"] == pais]
    fig.add_trace(
        go.Scatter(x=datos_pais["anio"], y=datos_pais["variable"],
                   name=pais, mode="lines+markers"),
        row=1, col=1
    )

# --- Grafico 2: Barras comparativas ---
promedios = df.groupby("pais")["variable"].mean()
fig.add_trace(
    go.Bar(x=promedios.index, y=promedios.values, name="Promedio"),
    row=1, col=2
)

# --- Grafico 3: Histograma ---
fig.add_trace(
    go.Histogram(x=df["variable"], nbinsx=20, name="Distribucion"),
    row=2, col=1
)

# --- Grafico 4: Scatter ---
fig.add_trace(
    go.Scatter(x=df["variable_x"], y=df["variable_y"],
               mode="markers", name="Correlacion",
               text=df["pais"], hoverinfo="text+x+y"),
    row=2, col=2
)

# Diseno
fig.update_layout(
    title_text="Dashboard: [Tu titulo aqui]",
    title_x=0.5,
    height=800,
    template="plotly_dark",    # Tema oscuro (puedes usar "plotly_white")
    showlegend=True
)

# Guardar como HTML auto-contenido
fig.write_html(
    "outputs/dashboard/index.html",
    include_plotlyjs=True,     # IMPORTANTE: embebe Plotly en el HTML
    full_html=True
)
print("Dashboard generado en outputs/dashboard/index.html")
```

### Consejos importantes

1. **Usa `include_plotlyjs=True`** - Esto embebe Plotly dentro del HTML.
   Si usas `include_plotlyjs='cdn'` puede fallar al visualizarse online.

2. **Rutas relativas** - Si tu dashboard carga datos o imagenes, usa rutas
   relativas (`assets/datos.js`) y nunca rutas absolutas (`C:\Users\...`).

3. **Prueba local** - Antes de subir, abre el HTML en tu navegador para verificar
   que todo se ve bien.

4. **Git add** - No olvides agregar los archivos generados:
   ```bash
   git add outputs/dashboard/
   git commit -m "Agregar dashboard interactivo"
   git push
   ```

### Alternativa sin Plotly (HTML + CSS puro)

Si no usas Plotly, puedes crear un HTML manual con tablas e imagenes:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Mi Dashboard - [Tu nombre]</title>
    <style>
        body { font-family: Arial; max-width: 900px; margin: 0 auto; padding: 20px; }
        img { max-width: 100%; border-radius: 8px; margin: 10px 0; }
        h1 { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>Resultados: [Tu titulo]</h1>
    <p>[Descripcion breve de tu analisis]</p>

    <h2>Grafico 1</h2>
    <img src="assets/grafico1.png" alt="Grafico 1">
    <p>[Interpretacion del grafico]</p>

    <h2>Grafico 2</h2>
    <img src="assets/grafico2.png" alt="Grafico 2">
    <p>[Interpretacion del grafico]</p>
</body>
</html>
```

Guarda las imagenes en `outputs/dashboard/assets/` y el HTML como `outputs/dashboard/index.html`.
