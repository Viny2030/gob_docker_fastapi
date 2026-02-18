import streamlit as st
import pandas as pd
import os
from datetime import datetime
from analisis import analizar_boletin, MATRIZ_TEORICA

# ===============================
# 1. CONFIGURACIÓN UI Y ESTILO
# ===============================
st.set_page_config(
    page_title="Monitor XAI - Ph.D. Monteverde",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stDataFrame {border: 1px solid #e6e9ef;}
    .st-emotion-cache-1ghh6m {font-weight: bold; color: #1f77b4;}
    .css-1kyxreq {justify-content: center;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ===============================
# RUTAS Y CARGA DE ARCHIVOS
# ===============================
DATA_DIR = "/app/data" if os.path.exists("/app/data") else "data"
ARTICULO_DOCX = "articulo_monteverde_español.docx"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def buscar_todos_los_xlsx(base_dir):
    """
    Busca TODOS los archivos .xlsx en el directorio base
    y en todas sus subcarpetas (ej: data/2026-01/, data/2026-02/)
    Retorna lista de rutas completas ordenadas por fecha descendente.
    """
    archivos = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".xlsx"):
                ruta_completa = os.path.join(root, f)
                archivos.append(ruta_completa)
    # Ordenar por fecha de modificación, más reciente primero
    archivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return archivos

def etiqueta_archivo(ruta):
    """Genera etiqueta legible: '2026-02 / reporte_fenomenos_20260217.xlsx'"""
    partes = ruta.replace("\\", "/").split("/")
    if len(partes) >= 3:
        return f"{partes[-2]} / {partes[-1]}"
    return partes[-1]

# ===============================
# 2. HEADER PRINCIPAL
# ===============================
st.title("⚖️ Monitor de Fenómenos Corruptivos")
st.subheader("Algoritmos contra la Corrupción - Ph.D. Vicente Humberto Monteverde")
st.write("---")

# ===============================
# PESTAÑAS
# ===============================
tab_monitor, tab_analisis, tab_documentacion = st.tabs([
    "📊 Monitor Histórico",
    "🚀 Análisis en Vivo (Paso 1-2-3)",
    "📖 Instructivo y Documentación",
])

# --- PESTAÑA 1: MONITOR HISTÓRICO ---
with tab_monitor:
    st.header("Visualización de Reportes Generados")

    # Buscar en todas las subcarpetas mensuales
    todos_los_archivos = buscar_todos_los_xlsx(DATA_DIR)

    if not todos_los_archivos:
        st.info("No se encontraron reportes. Ejecute el robot o realice un análisis en vivo.")
    else:
        # Mostrar estadística rápida
        st.caption(f"📁 {len(todos_los_archivos)} reportes encontrados en total")

        # Selectbox con etiqueta legible
        etiquetas = [etiqueta_archivo(r) for r in todos_los_archivos]
        idx = st.selectbox(
            "Seleccioná un reporte para auditar:",
            range(len(etiquetas)),
            format_func=lambda i: etiquetas[i]
        )
        ruta = todos_los_archivos[idx]

        try:
            xl = pd.ExcelFile(ruta)
            # Intentar leer la hoja correcta
            hoja = "Sheet1" if "Sheet1" in xl.sheet_names else xl.sheet_names[0]
            df = xl.parse(hoja)

            # Dashboard de métricas
            m1, m2, m3 = st.columns(3)
            m1.metric("Procesos Analizados", len(df))

            if "indice_fenomeno_corruptivo" in df.columns:
                m2.metric(
                    "Intensidad Promedio",
                    f"{df['indice_fenomeno_corruptivo'].mean():.1f} / 10",
                )
                if "nivel_riesgo_teorico" in df.columns:
                    riesgo_alto = len(df[df["nivel_riesgo_teorico"] == "Alto"])
                    m3.metric("Alertas de Riesgo Alto", riesgo_alto, delta_color="inverse")

            st.write("### Detalle del Análisis Algorítmico")
            st.dataframe(df, width="stretch", hide_index=True)

            st.divider()
            col_g, col_m = st.columns([1, 2])

            with col_g:
                st.subheader("📖 Glosario de Variables")
                glosario_data = {
                    "Variable": [
                        "indice_fenomeno_corruptivo",
                        "nivel_riesgo_teorico",
                        "tipo_decision",
                        "transferencia"
                    ],
                    "Descripción": [
                        "Índice 0-10 según teoría Monteverde",
                        "Clasificación Alto/Medio/Bajo",
                        "Categoría del fenómeno detectado",
                        "Dirección de la transferencia de ingresos"
                    ]
                }
                st.table(pd.DataFrame(glosario_data))

            with col_m:
                st.subheader("🔬 Marco Teórico: Los 7 Escenarios")
                resumen_teorico = []
                for k, v in MATRIZ_TEORICA.items():
                    resumen_teorico.append({
                        "Escenario": k,
                        "Mecanismo de Transferencia": v.get("transferencia", "Sin descripción"),
                    })
                st.table(pd.DataFrame(resumen_teorico))

        except Exception as e:
            st.error(f"Error al procesar el archivo Excel: {e}")

# --- PESTAÑA 2: ANÁLISIS EN VIVO ---
with tab_analisis:
    st.header("🔗 Conexión Directa: Comprar.gob.ar")
    st.info("Este proceso ejecuta el scraper sobre el portal de compras y aplica la matriz XAI de inmediato.")

    if st.button("🚀 Iniciar Ciclo de Análisis Completo"):
        with st.spinner("Ejecutando Paso 1-2-3 (Scraping + Matriz + Relación)..."):
            try:
                import diario
                df_nuevo = diario.extraer_licitaciones()

                if not df_nuevo.empty:
                    df_res, path_excel, _ = analizar_boletin(df_nuevo)
                    st.success(f"✅ Éxito: Reporte generado en {os.path.basename(path_excel)}")

                    col_res1, col_res2 = st.columns(2)
                    col_res1.metric(
                        "Índice de Riesgo Promedio",
                        f"{df_res['indice_fenomeno_corruptivo'].mean():.1f}",
                    )
                    col_res2.write("Visualice el detalle completo en la pestaña 'Monitor Histórico'.")
                    st.dataframe(df_res, width="stretch", hide_index=True)
                else:
                    st.error("No se pudieron obtener datos del portal. Verifique la conexión.")
            except Exception as e:
                st.error(f"Error inesperado: {e}")
                st.exception(e)

# --- PESTAÑA 3: DOCUMENTACIÓN ---
with tab_documentacion:
    st.header("📖 Guía de Uso del Monitor XAI")
    st.info("Siga estos pasos para auditar los procesos de contratación y detectar fenómenos corruptivos.")

    col_inst1, col_inst2 = st.columns(2)

    with col_inst1:
        st.markdown("""
        ### 🚀 Operación del Sistema
        1. **Generación de Datos:** Vaya a la pestaña **'Análisis en Vivo'** y pulse el botón 🚀.
        2. **Selección de Reporte:** En **'Monitor Histórico'**, use el desplegable para elegir el reporte por fecha.
        3. **Auditoría:** Ordene la tabla por **'Índice'** para identificar casos críticos.
        """)

    with col_inst2:
        st.markdown("""
        ### 🔍 Interpretación de Riesgo
        * **Índice (0-10):** Nivel de discrecionalidad detectado.
        * **🔴 Alto (8-10):** Probabilidad elevada de irregularidad (requiere auditoría).
        * **🟡 Medio (5-7):** Requiere revisión de antecedentes.
        * **🔵 Bajo (0-4):** Estándares de competencia normales.
        """)

    st.divider()
    st.header("📄 Fundamentación Académica")
    st.markdown("""
    Esta herramienta implementa la investigación del **Ph.D. Vicente Humberto Monteverde** sobre la 
    **Transferencia Regresiva de Ingresos**. El sistema busca patrones anómalos en el gasto público.
    
    **Referencias:**
    - Monteverde, V.H. (2021). "Great corruption - theory of corrupt phenomena", *Journal of Financial Crime*, Vol. 28 No. 2, pp. 580-592.
    - DOI: [10.1108/JFC-03-2020-0054](https://doi.org/10.1108/JFC-03-2020-0054)
    """)

    if os.path.exists(ARTICULO_DOCX):
        with open(ARTICULO_DOCX, "rb") as f:
            st.download_button(
                label="📥 Descargar Artículo Original (Ph.D. Monteverde)",
                data=f,
                file_name=ARTICULO_DOCX,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
    else:
        st.info("📄 Documentación académica disponible en el enlace de referencia arriba.")
