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

Version simplificada del dashboard educativo (sin calculadora interactiva en Tab 4).
Para la version completa con calculadora, ver 03_dashboard_educativo.py
"""

import panel as pn
import numpy as np
import pandas as pd
import altair as alt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

pn.extension('katex', 'vega', template='material')

# ==============================================================================
# ESTILOS CSS PROFESIONALES
# ==============================================================================
CSS_CUSTOM = """
.bk-root { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
.header-box {
    background-color: #2C3E50;
    color: #ECF0F1;
    padding: 15px;
    border-radius: 5px;
    border-left: 6px solid #E74C3C;
    margin-bottom: 20px;
}
.concept-card {
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-top: 4px solid #3498DB;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    margin: 10px 0;
}
.danger-zone {
    background-color: #FDEDEC;
    border-left: 5px solid #E74C3C;
    padding: 15px;
    border-radius: 4px;
    margin: 10px 0;
}
.success-zone {
    background-color: #EAFAF1;
    border-left: 5px solid #2ECC71;
    padding: 15px;
    border-radius: 4px;
    margin: 10px 0;
}
.warning-zone {
    background-color: #FEF9E7;
    border-left: 5px solid #F39C12;
    padding: 15px;
    border-radius: 4px;
    margin: 10px 0;
}
.interpretation-text {
    font-size: 1.1em;
    color: #2c3e50;
    line-height: 1.6;
}
"""
pn.config.raw_css.append(CSS_CUSTOM)

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
                axis=alt.Axis(labelFontSize=13, titleFontSize=15, titlePadding=10)),
        y=alt.Y('Y:Q', title='Variable Objetivo (Y)',
                axis=alt.Axis(labelFontSize=13, titleFontSize=15, titlePadding=10))
    )

    points = base.mark_circle(size=90, opacity=0.7).encode(
        color=alt.Color('Entidad:N', legend=alt.Legend(title="Entidad", labelFontSize=13, titleFontSize=14)),
        tooltip=[
            alt.Tooltip('Entidad:N', title='Grupo'),
            alt.Tooltip('X:Q', title='X', format='.2f'),
            alt.Tooltip('Y:Q', title='Y', format='.2f')
        ]
    )

    line_global = base.transform_regression('X', 'Y').mark_line(
        color='#E74C3C', strokeWidth=4, strokeDash=[5, 5]
    )

    return (points + line_global).properties(
        title=alt.TitleParams(title, fontSize=16, anchor='start'),
        width='container',
        height=420
    ).configure_view(strokeWidth=0).interactive()


# ==============================================================================
# PESTANA 1: MCO y POOLED OLS
# ==============================================================================
def tab_pooled_ols():
    slider_het = pn.widgets.FloatSlider(
        name='Nivel de Heterogeneidad (Sesgo)',
        start=0, end=10, value=7, step=0.5
    )

    def plot_pooled(h_level):
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
artificialmente la significancia de los coeficientes y sesga las estimaciones.

### Que es un "Sesgo"?

Un **sesgo** es simplemente un **error sistematico**. No es un error aleatorio
(que a veces va para arriba y a veces para abajo), sino un error que siempre
tira para el mismo lado. Es como una bascula que siempre marca 2 kilos de
mas: no importa cuantas veces te peses, siempre te equivocas en la misma
direccion.

### Sesgo por Heterogeneidad (El peligro del Pooled)

Imagina que estudias la relacion entre **Horas de Hospitalizacion (X)** y
**Salud Actual (Y)**.

*   Si mezclas a todos (Pooled), veras que **a mas horas en hospital, peor
    salud**. Conclusion aparente: "Los hospitales enferman".
*   Eso es **FALSO**. La gente que va al hospital **ya estaba mas enferma**
    de base. Esa diferencia previa es la **heterogeneidad no observada**.
*   El **efecto real**: para una misma persona, ir al hospital mejora su
    salud. Pero el Pooled OLS confunde la correlacion entre grupos con el
    efecto dentro de cada individuo.

Este es el **Sesgo por Heterogeneidad**: cuando las diferencias preexistentes
entre los individuos contaminan la relacion que intentamos medir.
                """, css_classes=['concept-card']),
                pn.pane.Markdown("**Formula del modelo Pooled OLS:**"),
                pn.pane.LaTeX(
                    r"Y_{it} = \beta_0 + \beta_1 X_{it} + \epsilon_{it}",
                    styles={'font-size': '1.5em', 'text-align': 'center', 'margin': '10px 0'}
                ),
                pn.pane.Markdown("*Donde i = entidad, t = tiempo. Sin termino de heterogeneidad.*"),
                width=550
            ),
            pn.Column(
                "### Laboratorio Visual",
                pn.pane.Markdown("""
Mueve el slider. Si la heterogeneidad es **0**, Pooled funciona. Si sube,
**la linea roja se invierte** incorrectamente (Paradoja de Simpson).
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

Se llaman **fijos** porque asumimos que cada entidad tiene una caracteristica
**constante que no cambia en el tiempo**. Es un intercepto unico y permanente.

Piensa en la **cultura corporativa**: Google y una administracion publica
tienen culturas muy distintas que afectan la productividad. Esa cultura no
cambia de un trimestre a otro. FE la controla dando un intercepto propio a
cada empresa, comparando cada empleado **consigo mismo** en el tiempo.

*   **Ejemplo:** Estudias formacion (X) vs productividad (Y) en 50 empresas.
    Cada empresa tiene su cultura y liderazgo. FE anade un intercepto por
    empresa, la cultura se "cancela" y vemos el efecto puro de la formacion.

### Por que se llaman "Efectos Aleatorios" (RE)?

Se llaman **aleatorios** porque asumimos que las diferencias entre entidades
son variaciones **aleatorias** extraidas de una poblacion mayor. No nos
interesa cada individuo, sino la variabilidad general.

Piensa en una **encuesta a 200 restaurantes aleatorios** de una ciudad. No
nos importa "el restaurante de la esquina", sino el patron general. Las
diferencias entre restaurantes las tratamos como ruido estadistico.

*   **Ejemplo:** Las mismas 50 empresas, pero si crees que son una muestra
    aleatoria y sus diferencias no correlacionan con la formacion, RE es mas
    eficiente (estimaciones mas precisas).

### Como decidir? El Test de Hausman
                """, css_classes=['concept-card']),
                width=550
            ),
            pn.Column(
                pn.pane.Markdown("**Formula Efectos Fijos:**"),
                pn.pane.LaTeX(
                    r"Y_{it} = (\alpha + \alpha_i) + \beta X_{it} + \epsilon_{it}",
                    styles={'font-size': '1.3em', 'text-align': 'center', 'margin': '8px 0'}
                ),
                pn.pane.Markdown("**Formula Efectos Aleatorios:**"),
                pn.pane.LaTeX(
                    r"Y_{it} = \alpha + \beta X_{it} + (\alpha_i + \epsilon_{it})",
                    styles={'font-size': '1.3em', 'text-align': 'center', 'margin': '8px 0'}
                ),
                pn.pane.Markdown("""
### Tabla de Decision (Test de Hausman)

| Escenario | Efectos Fijos (FE) | Efectos Aleatorios (RE) |
|---|---|---|
| **Filosofia** | "Cada individuo es unico" | "Los individuos son intercambiables" |
| **Clave matematica** | Permite correlacion entre X y el efecto individual | Asume independencia entre X y el efecto individual |
| **Si Hausman P < 0.05** | **USAR ESTE** (Consistente) | Sesgado (Desechar) |
| **Si Hausman P > 0.05** | Valido pero ineficiente | **USAR ESTE** (Eficiente) |
                """),
                pn.pane.Markdown("""
> **Regla de Oro**: Casi siempre se prefiere **Efectos Fijos** en ciencias
> sociales y negocios, porque es dificil creer que las caracteristicas de
> una empresa no influyen en sus decisiones. Si tienes dudas, usa FE.
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

        data = pd.DataFrame({
            'Metrica': ['Probabilidad', 'Odds'],
            'Valor': [p, min(odds, 20)]
        })

        chart = alt.Chart(data).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X('Metrica:N', title=None, axis=alt.Axis(labelFontSize=14, labelAngle=0)),
            y=alt.Y('Valor:Q', title='Valor',
                     axis=alt.Axis(labelFontSize=13, titleFontSize=14),
                     scale=alt.Scale(domain=[0, max(min(odds, 20), 1.5)])),
            color=alt.Color('Metrica:N', scale=alt.Scale(
                domain=['Probabilidad', 'Odds'], range=['#3498DB', '#E74C3C']
            ), legend=None),
            tooltip=[alt.Tooltip('Metrica:N'), alt.Tooltip('Valor:Q', format='.3f')]
        ).properties(
            height=300, width=280,
            title=alt.TitleParams(f'P = {p_pct}%  |  Odds = {odds:.2f} a 1', fontSize=14)
        )

        pros_cons = f"""
### Pros y Contras del Odds Ratio

*   **Pro**: Es matematicamente constante en modelos con variables binarias. No depende del nivel base de X.
*   **Contra**: Es dificil de intuir. Un OR de 3.0 **NO** significa "3 veces mas probable" (eso es Riesgo Relativo).
*   **Contra**: Exagera el efecto cuando el evento es comun (probabilidad > 50%).
*   **Pro**: Funciona muy bien con eventos raros (donde aproxima al Riesgo Relativo).
*   **Pro**: Es simetrico: OR del evento = 1 / OR del no-evento.
        """
        return pn.Row(chart, pn.pane.Markdown(pros_cons, css_classes=['danger-zone']))

    return pn.Column(
        pn.pane.HTML(HEADER_HTML),
        pn.pane.Markdown("""
# 3. Odds Ratios en Datos de Panel

### De donde vienen los Odds?

El concepto de **odds** viene del mundo de las **apuestas**. Cuando un
apostador dice "las chances son 4 a 1", esta usando odds. Luego la medicina
lo adopto para comparar riesgos entre grupos, y hoy es una herramienta
fundamental en ciencias sociales, marketing y negocios.

### Probabilidad vs Odds

*   **Probabilidad** = Eventos favorables / Total de eventos (0 a 1).
*   **Odds (Momios)** = Eventos favorables / Eventos NO favorables (0 a infinito).

**Ejemplo:** De 10 partidos, ganas 8.
*   Probabilidad = 8/10 = 80%
*   Odds = 8/2 = **4 a 1**

### Que es un Odds Ratio (OR)?

Compara los odds de DOS grupos:

**Ejemplo:** De 100 fumadores, 30 enferman. De 100 no fumadores, 10 enferman.
*   Odds fumadores = 30/70 = 0.429
*   Odds no fumadores = 10/90 = 0.111
*   **OR = 0.429 / 0.111 = 3.86**

Interpretacion: "Las chances de enfermedad entre fumadores son **3.86 veces**
las chances entre no fumadores." **NO** significa "3.86 veces mas probable".

### Por que se usan en datos de panel?

En datos de panel con variables binarias (si/no), los Odds Ratios permiten
eliminar matematicamente los efectos fijos individuales, lo cual es muy util
cuando hay muchas entidades.
        """, css_classes=['concept-card']),
        prob_slider,
        pn.bind(explain_odds, p_pct=prob_slider)
    )


# ==============================================================================
# PESTANA 4: EFECTOS MARGINALES Y NEGOCIO
# ==============================================================================
def tab_marginal_effects():
    return pn.Column(
        pn.pane.HTML(HEADER_HTML),
        pn.pane.Markdown("""
# 4. Efectos Marginales e Interpretacion de Negocio

### Que es un Efecto Marginal?

Imagina un **termostato**: el efecto marginal es cuanto sube la temperatura
de la habitacion si giras la perilla **un grado mas**. En econometria, es
exactamente lo mismo: cuanto cambia Y (resultado) si X (causa) sube en una
unidad, manteniendo todo lo demas igual.

En terminos tecnicos, es la **derivada parcial** de Y con respecto a X. Pero
no necesitas saber calculo para entenderlo: es "el impacto de mover una
palanca".

### Por que no basta con mirar el coeficiente Beta?

En un modelo **lineal simple**, Beta ya ES el efecto marginal. Pero en
modelos mas complejos (logaritmicos, logisticos), **Beta es un numero
abstracto** sin interpretacion directa. Necesitamos "traducirlo".

Es como tener la velocidad en millas/hora cuando tu jefe necesita km/hora.
        """, css_classes=['concept-card']),
        pn.Row(
            pn.Column(
                pn.pane.Markdown("""
### Los 3 tipos de interpretacion

**1. Lineal-Lineal (Nivel-Nivel)**

X e Y en unidades originales.

*   "Un ano mas de experiencia aumenta el salario en **2,500 dolares**."
*   Uso: Salarios, precios, cantidades fisicas.

**2. Log-Lineal (Semi-Elasticidad)**

Y en logaritmo, X en nivel. Comun en salarios y crimen.

*   "Un ano mas de experiencia aumenta el salario en **3.2%**."
*   Uso: Retornos a educacion, impacto de politicas.

**3. Log-Log (Elasticidad Constante)**

X e Y en logaritmo. Estandar en economia de precios.

*   "Si el precio sube 1%, la demanda cae **0.8%**."
*   Uso: Elasticidades precio-demanda.
                """)
            ),
            pn.Column(
                pn.pane.Markdown("**Formulas:**"),
                pn.pane.Markdown("Lin-Lin:"),
                pn.pane.LaTeX(r"\Delta Y = \beta \cdot \Delta X",
                              styles={'font-size': '1.2em', 'text-align': 'center', 'margin': '5px 0'}),
                pn.pane.Markdown("Log-Lin:"),
                pn.pane.LaTeX(r"\%\Delta Y \approx (e^{\beta \cdot \Delta X} - 1) \times 100",
                              styles={'font-size': '1.2em', 'text-align': 'center', 'margin': '5px 0'}),
                pn.pane.Markdown("Log-Log:"),
                pn.pane.LaTeX(r"\%\Delta Y \approx \beta \cdot \%\Delta X",
                              styles={'font-size': '1.2em', 'text-align': 'center', 'margin': '5px 0'}),
                css_classes=['success-zone']
            )
        ),
        pn.pane.Markdown("""
### Nota tecnica: "At the Mean" vs "Average Marginal Effects"

*   **At the Mean (MEM):** Se evalua en el individuo "promedio". Rapido pero
    puede no representar a nadie real.
*   **Average Marginal Effects (AME):** Se calcula para CADA individuo y se
    promedia. Es mas robusto y es el estandar moderno. Usa AME siempre que
    puedas.

### Insight Profesional

> "El valor de un Data Scientist no esta en correr el modelo, sino en
> traducir Beta en una accion de negocio clara. Un coeficiente que nadie
> entiende es un coeficiente que nadie usa."
        """, css_classes=['concept-card'])
    )


# ==============================================================================
# APP PRINCIPAL
# ==============================================================================
dashboard = pn.Tabs(
    ('1. Pooled OLS (Concepto)', tab_pooled_ols()),
    ('2. Efectos Fijos vs Aleatorios', tab_fe_re()),
    ('3. Odds Ratios (Teoria)', tab_odds_ratios()),
    ('4. Efectos Marginales (Negocio)', tab_marginal_effects()),
    dynamic=True
)

template = pn.template.MaterialTemplate(
    title="Econometria Aplicada: Masterclass",
    main=[dashboard],
    header_background="#2C3E50"
)

if __name__ == '__main__':
    template.show()
