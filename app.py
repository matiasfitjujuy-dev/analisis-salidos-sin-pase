
from pathlib import Path

import pandas as pd
import plotly.express as px

from shiny import App, ui, render
from shinywidgets import output_widget, render_widget


# ==========================================
# 1. CARGA DE DATOS
# ==========================================

carpeta = Path(__file__).parent

archivo = carpeta / "ranking_salidos_sin_pase.csv"
archivo_sector_ambito = carpeta / "sector_ambito.csv"
# Leer los resultados de los modelos de regresión
archivo_modelos = carpeta / "comparacion_modelos.csv"
archivo_distribucion = carpeta / "distribucion_salidos.csv"
datos_distribucion = pd.read_csv(archivo_distribucion)
# Datos para comparar valores reales y predichos
archivo_predicciones = carpeta / "predicciones_regresion.csv"
datos_predicciones = pd.read_csv(archivo_predicciones)

datos_modelos = pd.read_csv(archivo_modelos)

datos = pd.read_csv(archivo)
datos_sector_ambito = pd.read_csv(archivo_sector_ambito)

# Ordenar las jurisdicciones por porcentaje
datos = datos.sort_values(
    "porcentaje_ssp",
    ascending=True
)


# ==========================================
# 2. INTERFAZ DEL TABLERO
# ==========================================

# Diseño institucional: no modifica los cálculos ni los archivos CSV.
ESTILOS = """
/* Pantalla de apertura, integrada a la aplicación. */
.tab-content:has(.presentation-cover) {padding:0;border:0;background:transparent;box-shadow:none;}
.presentation-cover {min-height:650px;overflow:hidden;position:relative;color:#fff;
 background:linear-gradient(115deg,#102640 0%,#163c5d 55%,#246b9d 100%);
 padding:38px 48px 26px;border-radius:0 0 12px 12px;}
.cover-top {display:flex;align-items:center;justify-content:space-between;gap:20px;}
.cover-university {font-size:13px;font-weight:750;letter-spacing:1.2px;color:#fff;}
.cover-subject {font-size:11px;font-weight:650;letter-spacing:1.3px;color:#b7d9ec;}
.cover-body {display:grid;grid-template-columns: minmax(0,1.02fr) minmax(0,1fr);gap:30px;align-items:center;min-height:490px;}
.cover-kicker {font-size:11px;font-weight:750;letter-spacing:2px;color:#8ed0f3;margin-bottom:18px;}
.presentation-cover .cover-title {font-size:clamp(35px,3.7vw,57px);line-height:1.09;font-weight:780;
 letter-spacing:-1.5px;color:#fff;margin:0 0 20px;}
.cover-subtitle {font-size:20px;color:#dcecf7;line-height:1.5;margin:0;max-width:460px;}
.cover-rule {width:65px;height:4px;background:#e5a06a;margin:27px 0;border-radius:4px;}
.cover-stats {display:flex;gap:42px;}
.cover-number {font-size:29px;font-weight:750;line-height:1.1;color:#fff;}
.cover-stat-label {font-size:12px;color:#c4dcec;margin-top:6px;}
.cover-viz {padding:8px 0 4px;min-width:0;}
.cover-illustration {filter:drop-shadow(0 12px 22px rgba(2,15,33,.16));}
.cover-viz-title {font-size:12px;font-weight:750;letter-spacing:1.1px;color:#d7e9f5;margin-bottom:10px;}
.cover-plot {background:rgba(7,25,45,.23);border:1px solid rgba(177,215,239,.18);
 border-radius:10px;padding:7px 10px 2px;margin-bottom:13px;}
.cover-plot .shiny-bound-output {min-height:170px;}
.cover-viz-caption {font-size:11px;color:#b9d8ea;line-height:1.5;}
.cover-bottom {border-top:1px solid rgba(221,240,250,.25);padding-top:18px;
 display:flex;justify-content:space-between;align-items:center;gap:16px;}
.cover-author {font-size:13px;font-weight:750;letter-spacing:.8px;color:#fff;}
.cover-caption {font-size:11px;color:#bfd8e9;margin-top:4px;}
.cover-year {font-size:13px;color:#d9ebf7;}
@media(max-width:900px){.presentation-cover{padding:28px 25px;}
 .cover-body{grid-template-columns:1fr;gap:8px}.cover-viz{display:block;max-width:480px}
 .presentation-cover .cover-title{font-size:42px}.cover-top{flex-wrap:wrap}}

body {background:#f3f6fa; color:#183153; font-family: 'Segoe UI', Arial, sans-serif;}
.container-fluid {max-width: 1360px; padding: 20px 30px 30px;}
.hero {background:linear-gradient(115deg,#142b4c,#246b9d);color:white;
 padding:28px 32px;border-radius:16px;box-shadow:0 8px 25px rgba(17,43,76,.14);margin-bottom:20px;}
.hero .eyebrow {font-size:12px;letter-spacing:1.7px;font-weight:700;color:#c9e7fa;}
.hero h1 {font-size:31px;font-weight:700;margin:9px 0 7px;color:white;}
.hero p {color:#e1eff8;margin:0;font-size:15px;}
.kpis {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin-bottom:22px;}
.kpi {background:white;border:1px solid #e0e9f2;border-radius:13px;padding:16px 18px;
 box-shadow:0 3px 12px rgba(18,47,78,.04);}
.kpi .num {font-size:27px;font-weight:750;color:#1d628f;line-height:1.3;}
.kpi .lbl {font-size:12px;color:#65798e;margin-top:4px;}
.nav-tabs {border-bottom:1px solid #d6e2ed;gap:6px;flex-wrap:wrap;}
.nav-tabs .nav-link {color:#345a78;border-radius:10px 10px 0 0;padding:11px 16px;font-weight:600;}
.nav-tabs .nav-link.active {background:white;color:#176b9c;border-color:#d6e2ed #d6e2ed white;}
.tab-content {background:white;border:1px solid #d6e2ed;border-top:0;
 border-radius:0 0 15px 15px;padding:23px 26px 17px;box-shadow:0 5px 18px rgba(18,47,78,.05);}
.panel-title {font-size:21px;font-weight:700;color:#183153;margin:2px 0 8px;}
.panel-desc {color:#64788d;font-size:14px;margin-bottom:18px;}
.finding {background:#edf6fc;border-left:4px solid #2984b8;color:#274b65;
 border-radius:7px;padding:12px 15px;margin-top:14px;font-size:14px;}
.small-note {color:#63798e;font-size:13px;margin-top:12px;}
.footer-note {color:#66798a;font-size:12px;margin:18px 3px 0;line-height:1.65;}
.js-plotly-plot {max-width:100%;}
@media(max-width:800px){.kpis{grid-template-columns:repeat(2,1fr)}
 .container-fluid{padding:12px}.hero{padding:21px}.hero h1{font-size:24px}
 .tab-content{padding:14px}.kpi .num{font-size:22px}}
.intro {
    background: white;
    border: 1px solid #dce6f2;
    border-left: 5px solid #246b9d;
    border-radius: 12px;
    padding: 12px 20px;
    margin-bottom: 16px;
    box-shadow: 0 3px 12px rgba(17,43,76,0.05);
}
.intro h3 {
    color: #142b4c;
    margin-top: 0;
    font-size: 19px;
    margin-bottom: 7px;
}
.intro h4 {
    color: #246b9d;
    margin-bottom: 6px;
}
.intro p {
    color: #34465a;
    line-height: 1.45;
    margin-bottom: 6px;
}
"""


def tarjeta(numero, etiqueta):
    return ui.div(
        ui.div(numero, class_="num"),
        ui.div(etiqueta, class_="lbl"),
        class_="kpi"
    )


def seccion(titulo, descripcion, grafico, hallazgo):
    return ui.div(
        ui.h3(titulo, class_="panel-title"),
        ui.p(descripcion, class_="panel-desc"),
        output_widget(grafico),
        ui.div(ui.strong("Lectura del resultado: "), hallazgo, class_="finding"),
    )


app_ui = ui.page_fluid(
    ui.tags.style(ESTILOS),
    ui.navset_tab(
        ui.nav_panel(
            "Inicio",
            ui.div(
                ui.div(
                    ui.div("UNIVERSIDAD DEL GRAN ROSARIO", class_="cover-university"),
                    ui.div("INTRODUCCIÓN A LA CIENCIA DE DATOS", class_="cover-subject"),
                    class_="cover-top"
                ),
                ui.div(
                    ui.div(
                        ui.div("ANÁLISIS DE TRAYECTORIAS EDUCATIVAS", class_="cover-kicker"),
                        ui.h1("Estudiantes salidos sin pase", class_="cover-title"),
                        ui.p("Primer año de educación secundaria en Argentina", class_="cover-subtitle"),
                        ui.div(class_="cover-rule"),
                        class_="cover-copy"
                    ),
                    ui.div(
                        ui.HTML('<svg viewBox="0 0 540 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ilustración abstracta de análisis de datos; no representa resultados del estudio" style="width:100%;height:auto;display:block">\n<defs><linearGradient id="bar" x1="0" x2="0" y1="1" y2="0"><stop offset="0" stop-color="#2675ad" stop-opacity=".35"/><stop offset="1" stop-color="#7ed1f5" stop-opacity=".8"/></linearGradient><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#7ccaf2" stop-opacity=".27"/><stop offset="1" stop-color="#7ccaf2" stop-opacity="0"/></linearGradient></defs>\n<circle cx="270" cy="205" r="188" fill="none" stroke="#9fd9f3" stroke-opacity=".08" stroke-width="1"/><circle cx="270" cy="205" r="148" fill="none" stroke="#9fd9f3" stroke-opacity=".09"/><circle cx="270" cy="205" r="108" fill="none" stroke="#9fd9f3" stroke-opacity=".08"/>\n<g stroke="#c4e8fa" stroke-opacity=".12" stroke-width="1"><path d="M28 90H514 M28 148H514 M28 206H514 M28 264H514 M28 322H514 M28 380H514"/><path d="M68 58V380 M145 58V380 M222 58V380 M299 58V380 M376 58V380 M453 58V380"/></g>\n<g fill="url(#bar)"><rect x="58" y="260" width="28" height="120" rx="4"/><rect x="104" y="228" width="28" height="152" rx="4"/><rect x="150" y="278" width="28" height="102" rx="4"/><rect x="196" y="187" width="28" height="193" rx="4"/><rect x="242" y="220" width="28" height="160" rx="4"/><rect x="288" y="151" width="28" height="229" rx="4"/><rect x="334" y="197" width="28" height="183" rx="4"/><rect x="380" y="118" width="28" height="262" rx="4"/><rect x="426" y="166" width="28" height="214" rx="4"/></g>\n<path d="M42 278 C85 252 108 283 145 225 S210 250 244 185 S303 220 341 142 S404 179 450 98 S485 113 510 65 L510 380 L42 380Z" fill="url(#area)"/>\n<path d="M42 278 C85 252 108 283 145 225 S210 250 244 185 S303 220 341 142 S404 179 450 98 S485 113 510 65" fill="none" stroke="#f0ac78" stroke-width="4" stroke-linecap="round"/>\n<g fill="#f4bd93" stroke="#173b5a" stroke-width="3"><circle cx="42" cy="278" r="6"/><circle cx="145" cy="225" r="6"/><circle cx="244" cy="185" r="6"/><circle cx="341" cy="142" r="6"/><circle cx="450" cy="98" r="6"/><circle cx="510" cy="65" r="6"/></g>\n<g fill="#b8e9ff" opacity=".6"><circle cx="93" cy="112" r="3"/><circle cx="171" cy="77" r="3"/><circle cx="319" cy="85" r="3"/><circle cx="477" cy="246" r="3"/><circle cx="480" cy="290" r="2"/></g>\n</svg>'),
                        class_="cover-viz cover-illustration"
                    ),
                    class_="cover-body"
                ),
                ui.div(
                    ui.div(ui.div("LUIS MATÍAS MENDIETA", class_="cover-author"),
                           ui.div("Análisis de datos · Visualización interactiva", class_="cover-caption")),
                    ui.div("2026", class_="cover-year"),
                    class_="cover-bottom"
                ),
                class_="presentation-cover"
            ),
        ),
        ui.nav_panel(
            "01 · Distribución",
            seccion(
                "¿Cómo se distribuyen los porcentajes?",
                "Frecuencia de los porcentajes calculados en los 1.191 registros agregados válidos.",
                "grafico_distribucion",
                "La mayoría de los registros presenta porcentajes bajos, pero hay valores extremos. Cada registro representa un grupo, no un estudiante."
            )
        ),
        ui.nav_panel(
            "02 · Jurisdicciones",
            seccion(
                "¿Dónde se observan las mayores proporciones?",
                "Comparación por jurisdicción: salidos sin pase sobre matrícula inicial del primer año.",
                "grafico_provincias",
                "El ranking utiliza proporciones ponderadas por matrícula; no debe confundirse con el promedio simple de los registros."
            ),
            ui.hr(),
            ui.h4("Explorar una jurisdicción", class_="panel-title"),
            ui.input_select("provincia_elegida", "Seleccioná una jurisdicción:",
                            choices=sorted(datos["provincia"].tolist())),
            ui.output_text_verbatim("detalle_provincia")
        ),
        ui.nav_panel(
            "03 · Sector y ámbito",
            seccion(
                "¿Qué diferencias aparecen entre grupos?",
                "Comparación del porcentaje según sector de gestión y ámbito geográfico.",
                "grafico_sector_ambito",
                "En el conjunto analizado, las proporciones difieren según el sector y el ámbito; esta comparación no demuestra causalidad."
            )
        ),
        ui.nav_panel(
            "04 · Modelos",
            seccion(
                "¿Qué alternativa predice con menor error?",
                "Comparación del error absoluto medio (MAE), expresado en puntos porcentuales. Menor es mejor.",
                "grafico_modelos",
                "Las predicciones ajustadas corresponden al modelo con provincia, sector y ámbito, recortado a 0–100 %; no son un modelo nuevo."
            )
        ),
        ui.nav_panel(
            "05 · Predicciones",
            seccion(
                "¿Qué tan cerca están las predicciones de la realidad?",
                "239 registros de prueba. La diagonal representa coincidencia perfecta entre valores reales y predichos.",
                "grafico_predicciones",
                "El modelo tiene dificultades con los porcentajes extremos. Las estimaciones son exploratorias y no deben interpretarse como predicciones definitivas."
            )
        )
    ),
        ui.div(
        ui.strong("Fuente: "), "Relevamiento Anual · Base de trayectorias educativas. ",
        "Resultados exploratorios sujetos a validación metodológica. ",
        "Salidos sin pase no equivale directamente a la tasa oficial de abandono escolar.",
        class_="footer-note"
    )
)

# ==========================================
# 3. FUNCIONES DE LA APLICACIÓN
# ==========================================

def server(input, output, session):

    # GRÁFICO 1: DISTRIBUCIÓN DE PORCENTAJES
    @render_widget
    def grafico_distribucion():
        fig = px.histogram(
            datos_distribucion,
            x="porcentaje_ssp_registro",
            nbins=40,
            title="Distribución de salidos sin pase",
            labels={
                "porcentaje_ssp_registro": "Salidos sin pase (%)"
            }
        )

        fig.update_layout(
            template="plotly_white",
            font=dict(family="Segoe UI, Arial", color="#304e69"),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Porcentaje de salidos sin pase",
            yaxis_title="Cantidad de registros",
            bargap=0.05
        )

        fig.update_traces(marker_color="#2f80b7")
        return fig

    @render_widget
    def grafico_provincias():

        fig = px.bar(
            datos,
            x="porcentaje_ssp",
            y="provincia",
            orientation="h",
            labels={
                "porcentaje_ssp": "Porcentaje (%)",
                "provincia": "Jurisdicción"
            },
            hover_data={
                "matricula_primero_sec": ":,.0f",
                "salidos_primero_sec": ":,.0f",
                "porcentaje_ssp": ":.2f"
            },
            height=750
        )

        fig.update_traces(
            texttemplate="%{x:.2f}%",
            textposition="outside",
            cliponaxis=False
        )

        fig.update_layout(
            title="Salidos sin pase por jurisdicción",
            template="plotly_white",
            font=dict(family="Segoe UI, Arial", color="#304e69"),
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=20, r=85, t=60, b=40),
            xaxis=dict(
                title="Salidos sin pase respecto de la matrícula inicial (%)",
                range=[0, 7.5]
            ),
            yaxis_title="Jurisdicción"
        )

        fig.update_traces(marker_color="#2f80b7")
        return fig

    # GRÁFICO 2: SECTOR Y ÁMBITO
    @render_widget
    def grafico_sector_ambito():

        fig = px.bar(
            datos_sector_ambito,
            x="sector",
            y="porcentaje_ssp",
            color="ambito",
            barmode="group",
            color_discrete_sequence=["#2f80b7", "#70b7d9"],
            labels={
                "sector": "Sector de gestión",
                "porcentaje_ssp": "Salidos sin pase (%)",
                "ambito": "Ámbito"
            },
            title="Salidos sin pase según sector y ámbito",
            text="porcentaje_ssp"
        )

        fig.update_traces(
            texttemplate="%{y:.2f}%",
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_white",
            font=dict(family="Segoe UI, Arial", color="#304e69"),
            paper_bgcolor="white",
            plot_bgcolor="white",
            yaxis_title="Porcentaje (%)",
            xaxis_title="Sector de gestión",
            margin=dict(l=40, r=30, t=70, b=50)
        )

        return fig
    
    # GRÁFICO 3: COMPARACIÓN DE MODELOS
    @render_widget
    def grafico_modelos():

        fig = px.bar(
            datos_modelos,
            x="MAE",
            y="Modelo",
            orientation="h",
            text="MAE",
            labels={
                "MAE": "Error absoluto medio (puntos porcentuales)",
                "Modelo": "Alternativa evaluada"
            },
            title="Comparación del error de los modelos",
            hover_data={
                "MAE": ":.3f",
                "R2": ":.3f"
            }
        )

        fig.update_traces(
            texttemplate="%{x:.3f}",
            textposition="outside",
            cliponaxis=False
        )

        fig.update_layout(
            template="plotly_white",
            font=dict(family="Segoe UI, Arial", color="#304e69"),
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=420,
            margin=dict(l=30, r=80, t=70, b=50),
            xaxis=dict(
                range=[0, 3.2]
            ),
            yaxis=dict(
                autorange="reversed"
            )
        )

        fig.update_traces(marker_color="#2f80b7")
        return fig

    # GRÁFICO 5: VALORES REALES VS PREDICHOS
    @render_widget
    def grafico_predicciones():

        fig = px.scatter(
            datos_predicciones,
            x="Real",
            y="Predicho",
            title="Valores reales frente a predicciones",
            labels={
                "Real": "Porcentaje real (%)",
                "Predicho": "Porcentaje predicho (%)"
            },
            opacity=0.6,
            color_discrete_sequence=["#2f80b7"]
        )

        # Línea de predicción perfecta
        limite = max(
            datos_predicciones["Real"].max(),
            datos_predicciones["Predicho"].max()
        )

        fig.add_shape(
            type="line",
            x0=0,
            y0=0,
            x1=limite,
            y1=limite,
            line=dict(
                color="#dd7b43",
                dash="dash",
                width=2
            )
        )

        fig.update_layout(
            template="plotly_white",
            font=dict(family="Segoe UI, Arial", color="#304e69"),
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=500,
            xaxis_title="Porcentaje real (%)",
            yaxis_title="Porcentaje predicho (%)"
        )

        return fig
    # CONSULTA DE UNA JURISDICCIÓN
    @output
    @render.text
    def detalle_provincia():

        provincia = input.provincia_elegida()

        fila = datos.loc[
            datos["provincia"] == provincia
        ].iloc[0]

        matricula = int(fila["matricula_primero_sec"])
        salidos = int(fila["salidos_primero_sec"])
        porcentaje = fila["porcentaje_ssp"]

        return (
            f"Jurisdicción: {provincia}\n"
            f"Matrícula inicial: {matricula:,}\n"
            f"Salidos sin pase: {salidos:,}\n"
            f"Porcentaje: {porcentaje:.2f}%"
        )


# ==========================================
# 4. INICIAR LA APLICACIÓN
# ==========================================

app = App(app_ui, server)

