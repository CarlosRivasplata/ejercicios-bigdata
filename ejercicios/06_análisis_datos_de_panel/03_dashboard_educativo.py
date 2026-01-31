"""
-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodologia: Cursos Avanzados de Big Data, Ciencia de Datos,
             Desarrollo de aplicaciones con IA & Econometria Aplicada.
Hash ID de Certificacion: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADEMICA PRINCIPAL:
- Wooldridge, J. M. (2010). Econometric Analysis of Cross Section and Panel Data. MIT Press.
- Stock, J. H., & Watson, M. W. (2019). Introduction to Econometrics. Pearson.
- Cameron, A. C., & Trivedi, P. K. (2005). Microeconometrics: Methods and Applications. Cambridge University Press.
-------------------------
"""

import panel as pn
import numpy as np
import pandas as pd
import altair as alt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

pn.extension('vega', template='material')

# ==============================================================================
# TEMA SITH — Oscuro + rojo sutil, profesional, elegante
# ==============================================================================
CSS_SITH = """
/* ---- BASE ---- */
body {
    background: #0c0c0f !important;
    color: #c0c0c0 !important;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* ---- CANVAS LLUVIA SITH ---- */
#sith-rain {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none; opacity: 0.08;
}

/* ---- MATERIAL TEMPLATE ---- */
.mdc-top-app-bar { background: #111114 !important; border-bottom: 1px solid #222 !important; }
.mdc-top-app-bar .mdc-top-app-bar__title { color: #ccc !important; }
.mdc-drawer { background: #0e0e11 !important; }
body .main, .pn-main-area { background: transparent !important; }
.bk-clearfix, .bk-Column, .bk-Row { position: relative; z-index: 1; }

/* ---- TIPOGRAFIA ---- */
h1 { color: #e8e8e8 !important; border-bottom: 2px solid #8b0000; padding-bottom: 6px; }
h2 { color: #ddd !important; }
h3 { color: #bbb !important; }
h4, h5 { color: #999 !important; }
p, li, span, label { color: #b8b8b8 !important; }
strong, b { color: #e0e0e0 !important; }
a { color: #d46 !important; }

/* ---- HEADER BOX ---- */
.header-box {
    background: #111114 !important;
    border: 1px solid #1c1c20 !important;
    border-left: 4px solid #8b0000 !important;
    padding: 16px 20px; border-radius: 6px; margin-bottom: 20px;
}
.header-box h3 { color: #e0e0e0 !important; text-shadow: none; margin: 0 0 6px; }
.header-box small { color: #888 !important; }
.header-box b { color: #aaa !important; }

/* ---- CARDS ---- */
.concept-card {
    background: #111114 !important;
    border: 1px solid #1c1c20 !important;
    border-top: 3px solid #8b0000 !important;
    padding: 20px; border-radius: 8px; margin: 10px 0;
}
.danger-zone {
    background: #141216 !important;
    border-left: 4px solid #b22 !important;
    padding: 15px; border-radius: 4px; margin: 10px 0;
}
.success-zone {
    background: #111414 !important;
    border-left: 4px solid #8b0000 !important;
    padding: 15px; border-radius: 4px; margin: 10px 0;
}
.warning-zone {
    background: #141311 !important;
    border-left: 4px solid #a44 !important;
    padding: 15px; border-radius: 4px; margin: 10px 0;
}

/* ---- TABLAS ---- */
table { border-collapse: collapse; width: 100%; }
th {
    background: #1a1a1e !important;
    color: #ddd !important; padding: 10px 14px;
    font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.04em;
    border-bottom: 2px solid #8b0000 !important;
}
td {
    background: #111114 !important; color: #b8b8b8 !important;
    border-bottom: 1px solid #1c1c20 !important; padding: 9px 14px;
}
tr:nth-child(even) td { background: #141418 !important; }
tr:hover td { background: #1a181c !important; }

/* ---- CODIGO ---- */
code {
    background: #18181c !important; color: #d88 !important;
    border: 1px solid #222 !important; padding: 2px 6px; border-radius: 4px;
    font-family: 'Fira Code', Consolas, monospace;
}
pre {
    background: #0a0a0d !important; color: #c0a0a0 !important;
    border: 1px solid #1c1c20 !important; border-radius: 8px;
}
pre code { background: transparent !important; border: none !important; color: inherit !important; }

/* ---- BLOCKQUOTES ---- */
blockquote {
    background: #131316 !important;
    border-left: 3px solid #8b0000 !important;
    padding: 12px 18px; border-radius: 0 6px 6px 0; margin: 10px 0;
}

/* ---- WIDGETS ---- */
.bk-input, select, input[type="text"], input[type="number"] {
    background: #141418 !important; color: #ccc !important;
    border: 1px solid #222 !important; border-radius: 4px;
}
.noUi-connect { background: #8b0000 !important; }
.noUi-handle { background: #8b0000 !important; border: 2px solid #a00 !important; }
input[type="checkbox"] { accent-color: #8b0000; }

/* ---- MATHJAX ---- */
.MathJax, .MathJax_Display, mjx-container { color: #ddb !important; }

/* ---- TABS ---- */
.bk-header .bk-tab {
    background: #111114 !important; color: #999 !important;
    border: 1px solid #1c1c20 !important; border-bottom: none !important;
}
.bk-header .bk-tab.bk-active {
    background: #161618 !important; color: #ddd !important;
    border-top: 2px solid #8b0000 !important;
}

/* ---- SEPARADORES ---- */
hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, #333, transparent); margin: 20px 0; }

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #0c0c0f; }
::-webkit-scrollbar-thumb { background: #2a2a2e; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #3a3a3e; }
"""
pn.config.raw_css.append(CSS_SITH)

# ==============================================================================
# LLUVIA SITH — Se inyecta en document.body via JS (no dentro de un pane)
# ==============================================================================
SITH_RAIN_JS = """
<div id="_sith_loader"></div>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
(function(){
    var mjT;
    var obs=new MutationObserver(function(){clearTimeout(mjT);mjT=setTimeout(function(){if(window.MathJax&&window.MathJax.typeset){try{MathJax.typeset();}catch(e){}}},400);});
    if(document.body)obs.observe(document.body,{childList:true,subtree:true});
    else document.addEventListener('DOMContentLoaded',function(){obs.observe(document.body,{childList:true,subtree:true});});
    setInterval(function(){if(window.MathJax&&window.MathJax.typeset){try{MathJax.typeset();}catch(e){}}},3000);
})();
</script>
<script>
(function(){
    if (document.getElementById('sith-rain')) return;
    var c = document.createElement('canvas');
    c.id = 'sith-rain';
    document.body.insertBefore(c, document.body.firstChild);
    var ctx = c.getContext('2d');
    c.width = window.innerWidth;
    c.height = window.innerHeight;
    var chars = '\\u16A0\\u16A1\\u16A2\\u16A3\\u16A4\\u16A5\\u16A6\\u16A7\\u16A8\\u16A9\\u16AA\\u16AB\\u16AC\\u16AD\\u16AE\\u16AF\\u16B0\\u16B1\\u16B2\\u16B3\\u16B4\\u16B5\\u16B6\\u16B7\\u16B8\\u16B9\\u16BA\\u16BB\\u16BC\\u16BD\\u16BE\\u16BF\\u16C0\\u16C1\\u16C2\\u16C3\\u16C4\\u16C5\\u16C6\\u16C7\\u16C8\\u16C9\\u16CA\\u16CB\\u16CC\\u16CD\\u2D30\\u2D31\\u2D32\\u2D33\\u2D34\\u2D35\\u2D36\\u2D37\\u2D38\\u2D39\\u2D3A\\u2D3B\\u2D3C\\u2D3D\\u2D3E\\u2D3F\\u2D40\\u2D41\\u2D42\\u2D43\\u2D44\\u2D45\\u2D46\\u2D47\\u2D48\\u2D49\\u2D4A\\u2D4B\\u2D4C\\u2D4D\\u2D4E01\\u03A3\\u03BB\\u03B2\\u0394\\u03A9';
    var sz = 15, cols = Math.floor(c.width / sz);
    var d = [];
    for (var i = 0; i < cols; i++) d[i] = Math.floor(Math.random() * c.height / sz);
    setInterval(function(){
        ctx.fillStyle = 'rgba(8,8,12,0.06)';
        ctx.fillRect(0, 0, c.width, c.height);
        ctx.fillStyle = '#aa0000';
        ctx.font = sz + 'px monospace';
        for (var i = 0; i < d.length; i++){
            var t = chars.charAt(Math.floor(Math.random() * chars.length));
            ctx.fillText(t, i * sz, d[i] * sz);
            if (d[i] * sz > c.height && Math.random() > 0.975) d[i] = 0;
            d[i]++;
        }
    }, 35);
    window.addEventListener('resize', function(){ c.width = window.innerWidth; c.height = window.innerHeight; });
})();
</script>
"""

HEADER_HTML = """
<div class="header-box">
    <h3>Masterclass: Econometria de Panel para Big Data</h3>
    <small><b>Autor:</b> @TodoEconometria | <b>Profesor:</b> Juan Marcelo Gutierrez Miranda</small><br>
    <small><b>Metodologia:</b> Big Data, AI & Econometria Aplicada | <b>ID Cert:</b> 4e8d9b1a...</small>
</div>
"""

# ==============================================================================
# FUNCIONES AUXILIARES DE VISUALIZACION
# ==============================================================================
def create_scatter_chart(df, title):
    base = alt.Chart(df).encode(
        x=alt.X('X:Q', title='Variable Explicativa (X)',
                axis=alt.Axis(labelFontSize=13, titleFontSize=15, titlePadding=10,
                              labelColor='#888', titleColor='#aaa', gridColor='#1c1c20')),
        y=alt.Y('Y:Q', title='Variable Objetivo (Y)',
                axis=alt.Axis(labelFontSize=13, titleFontSize=15, titlePadding=10,
                              labelColor='#888', titleColor='#aaa', gridColor='#1c1c20'))
    )

    points = base.mark_circle(size=90, opacity=0.85).encode(
        color=alt.Color('Entidad:N',
                        scale=alt.Scale(range=['#b33', '#d66', '#e99']),
                        legend=alt.Legend(title="Entidad", labelFontSize=13, titleFontSize=14,
                                         labelColor='#888', titleColor='#aaa')),
        tooltip=[
            alt.Tooltip('Entidad:N', title='Grupo'),
            alt.Tooltip('X:Q', title='X', format='.2f'),
            alt.Tooltip('Y:Q', title='Y', format='.2f')
        ]
    )

    line_global = base.transform_regression('X', 'Y').mark_line(
        color='#c44', strokeWidth=4, strokeDash=[5, 5]
    )

    return (points + line_global).properties(
        title=alt.TitleParams(title, fontSize=16, anchor='start', color='#ccc'),
        width='container',
        height=420,
        background='#111114'
    ).configure_view(strokeWidth=0, fill='#111114').interactive()


# ==============================================================================
# PESTANA 1: MCO y POOLED OLS
# ==============================================================================
def tab_pooled_ols():
    slider_het = pn.widgets.FloatSlider(
        name='Nivel de Heterogeneidad (Sesgo)',
        start=0, end=10, value=7, step=0.5
    )

    def plot_pooled(h_level):
        np.random.seed(42)
        xs, ys, entities = [], [], []

        x1 = np.random.normal(2, 0.5, 20)
        y1 = 2 + (-1 * x1) + np.random.normal(0, 0.5, 20)
        xs.extend(x1); ys.extend(y1); entities.extend(['Grupo A'] * 20)

        x2 = np.random.normal(5, 0.5, 20)
        y2 = (2 + h_level) + (-1 * x2) + np.random.normal(0, 0.5, 20)
        xs.extend(x2); ys.extend(y2); entities.extend(['Grupo B'] * 20)

        x3 = np.random.normal(8, 0.5, 20)
        y3 = (2 + 2 * h_level) + (-1 * x3) + np.random.normal(0, 0.5, 20)
        xs.extend(x3); ys.extend(y3); entities.extend(['Grupo C'] * 20)

        df = pd.DataFrame({'X': xs, 'Y': ys, 'Entidad': entities})
        return create_scatter_chart(df, "Visualizacion del Sesgo en Pooled OLS")

    return pn.Column(
        pn.pane.HTML(HEADER_HTML),
        pn.Row(
            pn.Column(
                pn.pane.Markdown("""
# 1. El Modelo Pooled OLS (Agrupado)

### Que es MCO (Minimos Cuadrados Ordinarios)?

MCO (en ingles OLS: Ordinary Least Squares) es el algoritmo mas fundamental
de la estadistica. Su **objetivo** es sencillo: encontrar la recta que mejor
se ajuste a una nube de puntos. "Mejor" significa que la suma de los errores
al cuadrado (la distancia vertical entre cada punto y la recta) sea la menor
posible.

Piensa en un profesor que quiere trazar la linea que mejor resuma las notas de
sus alumnos en funcion de las horas de estudio. MCO le da esa linea "optima".

### Por que se llama "Pooled"?

En datos de panel tenemos observaciones repetidas: los mismos individuos
(personas, empresas, paises) medidos en distintos momentos del tiempo.
**"Pooled"** (agrupado) significa que tomamos TODAS las observaciones y las
apilamos en un solo monton, como si vinieran de personas distintas. Ignoramos
que los datos de Juan hoy y Juan manana estan relacionados.

**Implicacion estadistica:** El modelo asume que todas las observaciones son
independientes entre si, cuando en realidad no lo son. Esto infla
artificialmente la significancia de los coeficientes (nos hace creer que un
efecto es real cuando quizas no lo es) y sesga las estimaciones.

### Que es un "Sesgo"?

Antes de continuar: un **sesgo** es simplemente un **error sistematico**.
No es un error aleatorio (que a veces va para arriba y a veces para abajo),
sino un error que siempre tira para el mismo lado. Es como una bascula que
siempre marca 2 kilos de mas: no importa cuantas veces te peses, siempre
te equivocas en la misma direccion.

### Sesgo por Heterogeneidad (El peligro del Pooled)

Imagina que estudias la relacion entre **Horas de Hospitalizacion (X)** y
**Salud Actual (Y)**.

*   Si mezclas a todos (Pooled), veras que **a mas horas en hospital, peor
    salud**. Conclusion aparente: "Los hospitales enferman".
*   Eso es **FALSO**. Lo que ocurre es que la gente que va al hospital **ya
    estaba mas enferma** de base. Esa diferencia previa (la gravedad inicial)
    es la **heterogeneidad no observada**.
*   El **efecto real**: para una misma persona, ir al hospital mejora su
    salud. Pero el Pooled OLS confunde la correlacion entre grupos con el
    efecto dentro de cada individuo.

Este es el **Sesgo por Heterogeneidad**: cuando las diferencias preexistentes
entre los individuos contaminan la relacion que intentamos medir.
                """, css_classes=['concept-card']),
                pn.pane.Markdown("**Formula del modelo Pooled OLS:**"),
                pn.pane.HTML(r'<div style="text-align:center;padding:10px 0;color:#ddb;font-size:1.3em;">$$Y_{it} = \beta_0 + \beta_1 X_{it} + \epsilon_{it}$$</div>'),
                pn.pane.Markdown("""
*Donde i = entidad, t = tiempo. El modelo NO incluye ningun termino que
capture las diferencias entre entidades.*
                """),
                width=550
            ),
            pn.Column(
                "### Laboratorio Visual",
                pn.pane.Markdown("""
Mueve el slider para cambiar la heterogeneidad. Cuando es **0**, el Pooled
OLS funciona bien (la linea roja tiene pendiente negativa correcta). A medida
que la heterogeneidad **sube**, la linea roja (Pooled) se invierte y muestra
una pendiente **positiva falsa**, cuando el efecto real dentro de cada grupo
sigue siendo negativo.

Esto es la **Paradoja de Simpson** en accion.
                """),
                slider_het,
                pn.bind(plot_pooled, h_level=slider_het)
            )
        )
    )


# ==============================================================================
# PESTANA 2: EFECTOS FIJOS Y ALEATORIOS
# ==============================================================================
def tab_fe_re():
    return pn.Column(
        pn.pane.HTML(HEADER_HTML),
        pn.Row(
            pn.Column(
                pn.pane.Markdown("""
# 2. Efectos Fijos vs. Aleatorios

### Por que se llaman "Efectos Fijos" (FE)?

Se llaman **fijos** porque asumimos que cada entidad (persona, empresa, pais)
tiene una caracteristica **constante que no cambia en el tiempo**. Es un
intercepto unico y permanente para cada individuo.

Piensa en la **cultura corporativa** de una empresa: Google y una
administracion publica tienen culturas muy distintas que afectan la
productividad de sus empleados. Esa cultura no cambia de un trimestre a otro.
Si no la controlamos, nuestro analisis confundira "trabajar en Google" con
"ser mas productivo gracias a una politica concreta".

*   **Ejemplo:** Estudias el efecto de la formacion (X) en la productividad
    (Y) de empleados en 50 empresas. Cada empresa tiene su propia cultura,
    infraestructura y liderazgo. Efectos Fijos anade un intercepto para cada
    empresa, comparando cada empleado **consigo mismo** a lo largo del tiempo.
    Asi, la cultura se "cancela" y vemos el efecto puro de la formacion.

### Por que se llaman "Efectos Aleatorios" (RE)?

Se llaman **aleatorios** porque asumimos que las diferencias entre entidades
NO son caracteristicas unicas e irrepetibles, sino variaciones **aleatorias**
extraidas de una poblacion mayor. No nos interesa cada individuo en
particular, sino la variabilidad del conjunto.

Piensa en una **encuesta a 200 restaurantes aleatorios** de una ciudad para
estudiar el efecto del tamanno del local en las ventas. No nos importa "el
restaurante de la esquina" en particular, sino el patron general. Las
diferencias entre restaurantes las tratamos como ruido estadistico.

*   **Ejemplo:** Con las mismas 50 empresas, si crees que son una muestra
    aleatoria de un universo mayor de empresas, y que sus diferencias no estan
    correlacionadas con la formacion que dan, entonces Efectos Aleatorios es
    mas eficiente (estimaciones mas precisas).

### Como decidir? El Test de Hausman

El **Test de Hausman** es el juez imparcial entre FE y RE:
                """, css_classes=['concept-card']),
                width=550
            ),
            pn.Column(
                pn.pane.Markdown("**Formula Efectos Fijos:**"),
                pn.pane.HTML(r'<div style="text-align:center;padding:8px 0;color:#ddb;font-size:1.3em;">$$Y_{it} = (\alpha + \alpha_i) + \beta X_{it} + \epsilon_{it}$$</div>'),
                pn.pane.Markdown("**Formula Efectos Aleatorios:**"),
                pn.pane.HTML(r'<div style="text-align:center;padding:8px 0;color:#ddb;font-size:1.3em;">$$Y_{it} = \alpha + \beta X_{it} + (\alpha_i + \epsilon_{it})$$</div>'),
                pn.pane.Markdown("""
### Tabla de Decision (Test de Hausman)

| Escenario | Efectos Fijos (FE) | Efectos Aleatorios (RE) |
|---|---|---|
| **Filosofia** | "Cada individuo es unico" | "Los individuos son intercambiables" |
| **Clave matematica** | Permite que X se correlacione con el efecto individual | Asume que X y el efecto individual son independientes |
| **Si Hausman P < 0.05** | **USAR ESTE** (Consistente) | Sesgado (Desechar) |
| **Si Hausman P > 0.05** | Valido pero ineficiente | **USAR ESTE** (Eficiente) |
                """),
                pn.pane.Markdown("""
> **Regla de Oro en Ciencias Sociales y Negocios**: Casi siempre se prefiere
> **Efectos Fijos**, porque es dificil creer que las caracteristicas de una
> empresa o persona no influyen en sus decisiones. Si tienes dudas, usa FE.
                """, css_classes=['success-zone'])
            )
        )
    )


# ==============================================================================
# PESTANA 3: ODDS RATIOS
# ==============================================================================
def tab_odds_ratios():
    prob_slider = pn.widgets.FloatSlider(
        name='Probabilidad del Evento (%)', start=1, end=99, value=50, step=1
    )

    def explain_odds(p_pct):
        p = p_pct / 100
        odds = p / (1 - p)

        # --- Grafico 1: Barras Probabilidad vs Odds ---
        data_bar = pd.DataFrame({
            'Metrica': ['Probabilidad', 'Odds'],
            'Valor': [p, min(odds, 20)]  # Limitar para evitar explosion visual
        })

        bar_chart = alt.Chart(data_bar).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X('Metrica:N', title=None,
                     axis=alt.Axis(labelFontSize=14, labelAngle=0, labelColor='#888')),
            y=alt.Y('Valor:Q', title='Valor',
                     axis=alt.Axis(labelFontSize=13, titleFontSize=14,
                                   labelColor='#888', titleColor='#c44', gridColor='#1a1a1e'),
                     scale=alt.Scale(domain=[0, max(min(odds, 20), 1.5)])),
            color=alt.Color('Metrica:N', scale=alt.Scale(
                domain=['Probabilidad', 'Odds'],
                range=['#b33', '#d66']
            ), legend=None),
            tooltip=[alt.Tooltip('Metrica:N'), alt.Tooltip('Valor:Q', format='.3f')]
        ).properties(
            width=250, height=300,
            title=alt.TitleParams(
                f'P = {p_pct}%  |  Odds = {odds:.2f} a 1',
                fontSize=14, color='#ccc'
            ),
            background='#111114'
        ).configure_view(fill='#111114')

        # --- Grafico 2: Curva P vs Odds ---
        p_range = np.linspace(0.01, 0.99, 100)
        odds_range = p_range / (1 - p_range)
        curve_df = pd.DataFrame({'Probabilidad': p_range, 'Odds': odds_range})

        point_df = pd.DataFrame({'Probabilidad': [p], 'Odds': [odds]})

        curve = alt.Chart(curve_df).mark_line(color='#b33', strokeWidth=2).encode(
            x=alt.X('Probabilidad:Q', title='Probabilidad',
                     axis=alt.Axis(labelFontSize=13, titleFontSize=14, format='.0%',
                                   labelColor='#888', titleColor='#aaa', gridColor='#1c1c20')),
            y=alt.Y('Odds:Q', title='Odds',
                     axis=alt.Axis(labelFontSize=13, titleFontSize=14,
                                   labelColor='#888', titleColor='#aaa', gridColor='#1c1c20'),
                     scale=alt.Scale(type='log'))
        )

        marker = alt.Chart(point_df).mark_circle(size=150, color='#c44').encode(
            x='Probabilidad:Q',
            y='Odds:Q',
            tooltip=[
                alt.Tooltip('Probabilidad:Q', format='.2f'),
                alt.Tooltip('Odds:Q', format='.2f')
            ]
        )

        curve_chart = (curve + marker).properties(
            width=300, height=300,
            title=alt.TitleParams('Relacion Probabilidad vs Odds (escala log)', fontSize=14, color='#ccc'),
            background='#111114'
        ).configure_view(fill='#111114')

        # --- Ejemplo comparativo de OR ---
        or_text = ""
        if odds > 0:
            or_text = f"""
### Ejemplo de Odds Ratio con tu valor actual

Si en un **grupo tratamiento** la probabilidad es {p_pct}% (odds = {odds:.2f})
y en un **grupo control** la probabilidad es 20% (odds = 0.25), entonces:

**OR = {odds:.2f} / 0.25 = {odds / 0.25:.2f}**

Esto significa que las chances del evento en el grupo tratamiento son
**{odds / 0.25:.1f} veces** las chances del grupo control.
            """

        return pn.Column(
            pn.Row(
                pn.pane.Vega(bar_chart, sizing_mode='fixed'),
                pn.pane.Vega(curve_chart, sizing_mode='fixed')
            ),
            pn.pane.Markdown(or_text, css_classes=['warning-zone']) if or_text else None
        )

    return pn.Column(
        pn.pane.HTML(HEADER_HTML),
        pn.pane.Markdown("""
# 3. Odds Ratios en Datos de Panel

### De donde vienen los Odds?

El concepto de **odds** viene del mundo de las **apuestas**. Cuando un
apostador dice "las chances son 4 a 1", esta usando odds. Luego la medicina
lo adopto para comparar riesgos entre grupos (fumadores vs no fumadores), y
hoy es una herramienta fundamental en ciencias sociales, marketing y negocios.

### Probabilidad vs Odds: Cual es la diferencia?

Son dos formas de medir lo mismo, pero con escalas distintas:

*   **Probabilidad** = Eventos favorables / Total de eventos. Va de 0 a 1 (o 0% a 100%).
*   **Odds (Momios)** = Eventos favorables / Eventos NO favorables. Va de 0 a infinito.

**Ejemplo concreto:** De 10 partidos, ganas 8.
*   Probabilidad = 8/10 = 0.80 (80%)
*   Odds = 8 ganados / 2 perdidos = **4 a 1**

### Que es un Odds Ratio (OR)?

El **Odds Ratio** compara los odds de DOS grupos. Responde a la pregunta:
"Las chances de que ocurra el evento, son mayores en un grupo que en otro?"

**Ejemplo en salud:** De 100 fumadores, 30 desarrollan enfermedad pulmonar.
De 100 no fumadores, 10 la desarrollan.

*   Odds fumadores = 30/70 = 0.429
*   Odds no fumadores = 10/90 = 0.111
*   **OR = 0.429 / 0.111 = 3.86**

Interpretacion correcta: "Las chances de enfermedad pulmonar entre fumadores
son **3.86 veces** las chances entre no fumadores."

**CUIDADO:** Esto **NO** significa "3.86 veces mas probable". Esa seria otra
medida (el Riesgo Relativo). Confundirlas es el error mas comun.

### Por que se usan en datos de panel?

En datos de panel con variables dependientes binarias (si/no, exito/fracaso),
los Odds Ratios permiten eliminar matematicamente los efectos fijos
individuales, lo cual es muy util cuando hay muchas entidades.

### Pros y Contras del Odds Ratio

| Aspecto | Ventaja | Desventaja |
|---|---|---|
| **Eventos raros** | Funciona muy bien (OR aproxima al Riesgo Relativo) | - |
| **Eventos comunes** | - | Exagera el tamano del efecto |
| **Interpretacion** | Matematicamente elegante y consistente | Dificil de explicar a no-estadisticos |
| **Comunicacion** | Estandar en investigacion medica | "3.86 veces las chances" confunde a gerentes |
| **Simetria** | OR para evento = 1/OR para no-evento | Puede inducir a error si no se especifica |
        """, css_classes=['concept-card']),
        pn.pane.Markdown("### Explorador interactivo: mueve el slider para ver como cambian los Odds"),
        prob_slider,
        pn.bind(explain_odds, p_pct=prob_slider)
    )


# ==============================================================================
# PESTANA 4: EFECTOS MARGINALES Y NEGOCIO
# ==============================================================================
def tab_marginal_effects():

    model_sel = pn.widgets.RadioButtonGroup(
        name='Tipo de Modelo',
        options=['Lin-Lin', 'Log-Lin', 'Log-Log'],
        value='Lin-Lin',
        button_type='danger',
        button_style='outline'
    )
    alpha_slider = pn.widgets.FloatSlider(
        name='Intercepto (alpha)', start=-5, end=15, value=5, step=0.5
    )
    beta_slider = pn.widgets.FloatSlider(
        name='Coeficiente (beta)', start=-2, end=2, value=-0.5, step=0.05
    )
    x_eval = pn.widgets.FloatSlider(
        name='Evaluar en X0', start=1, end=20, value=10, step=0.5
    )
    delta_slider = pn.widgets.FloatSlider(
        name='Cambio en X', start=0.5, end=5, value=1, step=0.5
    )

    def build_analysis(mod, alpha, beta, x0, dx):
        x = np.linspace(0.5, 25, 300)

        if mod == 'Lin-Lin':
            y = alpha + beta * x
            y0 = alpha + beta * x0
            y1 = alpha + beta * (x0 + dx)
            dy_abs = y1 - y0
            me_values = np.full_like(x, beta)
            me_at_x0 = beta
            ylabel = 'Y'
            me_label = 'dY/dX'
            formula_tex = r'\Delta Y = \beta \cdot \Delta X'
            result_html = f"<b>ΔY = {beta:.3f} x {dx:.1f} = {dy_abs:.4f} unidades</b>"
            neg_text = f'{abs(dy_abs):.2f} {"mas" if dy_abs > 0 else "menos"} por cada {dx:.1f} unidades adicionales'
        elif mod == 'Log-Lin':
            y = np.exp(alpha + beta * x)
            y0_val = np.exp(alpha + beta * x0)
            y1_val = np.exp(alpha + beta * (x0 + dx))
            dy_abs = y1_val - y0_val
            y0 = y0_val
            y1 = y1_val
            pct = (np.exp(beta * dx) - 1) * 100
            me_values = beta * np.exp(alpha + beta * x)
            me_at_x0 = beta * y0_val
            ylabel = 'Y = exp(a + bX)'
            me_label = 'dY/dX = b*Y'
            formula_tex = r'\%\Delta Y \approx (e^{\beta \cdot \Delta X} - 1) \times 100'
            result_html = f"<b>%ΔY ≈ {pct:.2f}%</b> (cambio absoluto: {dy_abs:.2f})"
            neg_text = f'{"Aumento" if pct > 0 else "Disminucion"} del {abs(pct):.1f}% en Y'
        else:
            x_safe = np.maximum(x, 0.01)
            y = np.exp(alpha + beta * np.log(x_safe))
            y0 = np.exp(alpha + beta * np.log(max(x0, 0.01)))
            y1 = np.exp(alpha + beta * np.log(max(x0 + dx, 0.01)))
            dy_abs = y1 - y0
            pct_dx = (dx / max(x0, 0.01)) * 100
            pct_dy = beta * pct_dx
            me_values = beta * np.exp(alpha + beta * np.log(x_safe)) / x_safe
            me_at_x0 = beta * y0 / max(x0, 0.01)
            ylabel = 'Y = exp(a + b*lnX)'
            me_label = 'dY/dX = b*Y/X'
            formula_tex = r'\%\Delta Y \approx \beta \cdot \%\Delta X'
            result_html = f"<b>Elasticidad: %ΔY ≈ {beta:.3f} x {pct_dx:.1f}% = {pct_dy:.2f}%</b>"
            neg_text = f'Si X sube {pct_dx:.1f}%, Y {"sube" if pct_dy > 0 else "cae"} {abs(pct_dy):.1f}%'

        # ---- GRAFICO 1: Curva de Respuesta ----
        df_curve = pd.DataFrame({'X': x, 'Y': y})
        curve_line = alt.Chart(df_curve).mark_line(color='#b33', strokeWidth=2.5).encode(
            x=alt.X('X:Q', title='X',
                     axis=alt.Axis(labelColor='#888', titleColor='#aaa',
                                   gridColor='#1c1c20', labelFontSize=12, titleFontSize=14)),
            y=alt.Y('Y:Q', title=ylabel,
                     axis=alt.Axis(labelColor='#888', titleColor='#aaa',
                                   gridColor='#1c1c20', labelFontSize=12, titleFontSize=14))
        )

        pts_df = pd.DataFrame({
            'X': [x0, x0 + dx], 'Y': [y0, y1],
            'Punto': [f'X0 = {x0:.1f}', f'X0+dX = {x0+dx:.1f}']
        })
        pts = alt.Chart(pts_df).mark_circle(size=160).encode(
            x='X:Q', y='Y:Q',
            color=alt.Color('Punto:N', scale=alt.Scale(range=['#c44', '#6ad']),
                            legend=alt.Legend(labelColor='#888', titleColor='#aaa', title='Puntos')),
            tooltip=['Punto:N', alt.Tooltip('X:Q', format='.2f'), alt.Tooltip('Y:Q', format='.4f')]
        )

        h_df = pd.DataFrame({'X': [x0, x0 + dx], 'Y': [y0, y0]})
        h_line = alt.Chart(h_df).mark_line(color='#666', strokeDash=[4, 4], strokeWidth=1.5).encode(
            x='X:Q', y='Y:Q')

        v_df = pd.DataFrame({'X': [x0 + dx, x0 + dx], 'Y': [y0, y1]})
        v_line = alt.Chart(v_df).mark_line(color='#d88', strokeWidth=2.5).encode(
            x='X:Q', y='Y:Q')

        dx_lbl = alt.Chart(pd.DataFrame({
            'X': [x0 + dx / 2], 'Y': [y0], 't': ['dX']
        })).mark_text(dy=-12, color='#888', fontSize=13).encode(x='X:Q', y='Y:Q', text='t:N')

        dy_lbl = alt.Chart(pd.DataFrame({
            'X': [x0 + dx], 'Y': [(y0 + y1) / 2], 't': ['dY']
        })).mark_text(dx=18, color='#d88', fontSize=13, fontWeight='bold').encode(
            x='X:Q', y='Y:Q', text='t:N')

        chart1 = (curve_line + pts + h_line + v_line + dx_lbl + dy_lbl).properties(
            title=alt.TitleParams('Curva de Respuesta y Efecto Marginal',
                                  fontSize=15, anchor='start', color='#ccc'),
            width=420, height=340, background='#111114'
        ).configure_view(strokeWidth=0, fill='#111114').interactive()

        # ---- GRAFICO 2: Efecto Marginal a lo largo de X ----
        df_me = pd.DataFrame({'X': x, 'ME': me_values})
        me_line = alt.Chart(df_me).mark_line(color='#d66', strokeWidth=2).encode(
            x=alt.X('X:Q', title='X',
                     axis=alt.Axis(labelColor='#888', titleColor='#aaa',
                                   gridColor='#1c1c20', labelFontSize=12, titleFontSize=14)),
            y=alt.Y('ME:Q', title=me_label,
                     axis=alt.Axis(labelColor='#888', titleColor='#aaa',
                                   gridColor='#1c1c20', labelFontSize=12, titleFontSize=14))
        )

        zero_rule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(
            color='#555', strokeDash=[3, 3]).encode(y='y:Q')

        me_pt = alt.Chart(pd.DataFrame({
            'X': [x0], 'ME': [me_at_x0]
        })).mark_circle(size=160, color='#c44').encode(
            x='X:Q', y='ME:Q',
            tooltip=[alt.Tooltip('X:Q', format='.2f', title='X0'),
                     alt.Tooltip('ME:Q', format='.4f', title='dY/dX')]
        )

        chart2 = (me_line + zero_rule + me_pt).properties(
            title=alt.TitleParams('Efecto Marginal a lo largo de X',
                                  fontSize=15, anchor='start', color='#ccc'),
            width=420, height=340, background='#111114'
        ).configure_view(strokeWidth=0, fill='#111114').interactive()

        return pn.Column(
            pn.Row(
                pn.pane.Vega(chart1, sizing_mode='fixed'),
                pn.pane.Vega(chart2, sizing_mode='fixed')
            ),
            pn.pane.HTML(
                f'<div style="text-align:center;padding:12px 0;color:#ddb;font-size:1.3em;">$${formula_tex}$$</div>',
                sizing_mode='stretch_width'),
            pn.pane.Markdown(f"""
### Resultado

{result_html}

> **Para la reunion de negocio:** "{neg_text}"
            """, css_classes=['success-zone'])
        )

    return pn.Column(
        pn.pane.HTML(HEADER_HTML),
        pn.pane.Markdown("""
# 4. Efectos Marginales e Interpretacion de Negocio

### Que es un Efecto Marginal?

El efecto marginal mide **cuanto cambia Y cuando X sube en una unidad**,
manteniendo todo lo demas constante (*Ceteris Paribus*). Es la traduccion
del coeficiente Beta a un impacto real en las unidades del problema.

En un modelo lineal, Beta ya es el efecto marginal. Pero en modelos
logaritmicos o no lineales, Beta es un numero abstracto que necesita
"traducirse" a unidades o porcentajes.

### Los 3 tipos de modelo

| Modelo | Variables | Interpretacion de Beta | Ejemplo |
|---|---|---|---|
| **Lin-Lin** | Y y X en nivel | DY por unidad de DX | "$2,500 mas de salario por ano de experiencia" |
| **Log-Lin** | ln(Y) vs X | % cambio en Y por unidad de DX | "3.2% mas salario por ano de experiencia" |
| **Log-Log** | ln(Y) vs ln(X) | Elasticidad: %DY por %DX | "Si precio sube 1%, demanda cae 0.8%" |

### Nota: "At the Mean" vs "Average Marginal Effects"

*   **MEM (At the Mean):** Evalua en el individuo "promedio". Rapido pero puede no representar a nadie real.
*   **AME (Average Marginal Effects):** Calcula para CADA individuo y promedia. Es el estandar moderno.
        """, css_classes=['concept-card']),
        pn.pane.Markdown("---"),
        pn.pane.Markdown("### Laboratorio Visual de Efectos Marginales"),
        pn.pane.Markdown(
            "Selecciona el tipo de modelo y ajusta los parametros. "
            "El grafico izquierdo muestra la **curva de respuesta** con el cambio "
            "senalado (escalera roja). El derecho muestra **como varia el efecto marginal** "
            "a lo largo de X (constante en Lin-Lin, variable en los demas)."
        ),
        model_sel,
        pn.Row(
            pn.Column(alpha_slider, beta_slider, x_eval, delta_slider, width=300),
            pn.Column(
                pn.bind(build_analysis, mod=model_sel, alpha=alpha_slider,
                        beta=beta_slider, x0=x_eval, dx=delta_slider),
                sizing_mode='stretch_width'
            )
        ),
        pn.pane.Markdown("""
> *"El valor de un Data Scientist no esta en correr el modelo, sino en
> traducir Beta en una accion de negocio clara."*
        """, css_classes=['concept-card'])
    )


# ==============================================================================
# APP PRINCIPAL
# ==============================================================================
sith_rain = pn.pane.HTML(SITH_RAIN_JS, height=0, sizing_mode='stretch_width')

dashboard = pn.Tabs(
    ('1. Pooled OLS (Concepto)', tab_pooled_ols()),
    ('2. FE vs RE (Decision)', tab_fe_re()),
    ('3. Odds Ratios (Teoria)', tab_odds_ratios()),
    ('4. Efectos Marginales (Negocio)', tab_marginal_effects()),
    dynamic=True
)

template = pn.template.MaterialTemplate(
    title="Econometria Aplicada: Masterclass",
    main=[sith_rain, dashboard],
    header_background="#0a0a0a"
)

if __name__ == '__main__':
    template.show()
