# En analisis.py
import os
import unicodedata
from datetime import datetime

# Cambia esto en analisis.py y dashboard.py
# Ahora la carpeta 'data' está directamente en la raíz
BASE_PATH = os.getcwd()
DATA_DIR = os.path.join(os.getcwd(), "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

# Crea la estructura jerárquica si no existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"📁 Directorio de datos preparado en: {DATA_DIR}")

# MATRIZ TEÓRICA - Ph.D. Vicente Humberto Monteverde
MATRIZ_TEORICA = {
    "Privatización / Concesión": {
        "keywords": ["concesion", "privatizacion", "venta de pliegos", "subvaluacion"],
        "transferencia": "Estado a Privados",
        "peso": 9.0
    },
    "Obra Pública / Contratos": {
        "keywords": ["obra publica", "licitacion", "contratacion directa", "sobreprecio", "redeterminacion"],
        "transferencia": "Estado a Empresas",
        "peso": 8.5
    },
    "Tarifas Servicios Públicos": {
        "keywords": ["cuadro tarifario", "aumento de tarifa", "revision tarifaria", "peaje"],
        "transferencia": "Usuarios a Concesionarias",
        "peso": 7.5
    },
    "Precios de Consumo Regulados": {
        "keywords": ["precios justos", "canasta basica", "viveres", "alimento"],
        "transferencia": "Consumidores a Productores",
        "peso": 6.5
    },
    "Salarios y Paritarias": {
        "keywords": ["paritaria", "salario minimo", "ajuste salarial", "convenio colectivo"],
        "transferencia": "Asalariados a Empleadores",
        "peso": 5.5
    },
    "Jubilaciones / Pensiones": {
        "keywords": ["movilidad jubilatoria", "haber minimo", "anses", "ajuste previsional"],
        "transferencia": "Jubilados al Estado",
        "peso": 10.0
    },
    "Traslado de Impuestos": {
        "keywords": ["iva", "ingresos brutos", "doble imposicion", "presion tributaria"],
        "transferencia": "Contribuyentes al Estado",
        "peso": 9.5
    },
}

def limpiar_texto_curado(texto):
    """Limpia y normaliza texto para análisis"""
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    # Remover acentos
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

def evaluar_riesgo(score):
    """Clasifica el riesgo según el índice"""
    if score >= 8:
        return "Alto"
    elif score >= 5:
        return "Medio"
    else:
        return "Bajo"

def analizar_boletin(df, directorio_destino=None):
    """
    Analiza licitaciones aplicando la matriz teórica de Monteverde
    
    Args:
        df: DataFrame con las licitaciones
        directorio_destino: Carpeta donde guardar el reporte (opcional)
    
    Returns:
        tuple: (df_analizado, path_excel, df_vacio)
    """
    if df.empty:
        print("⚠️ DataFrame vacío recibido")
        return df, None, pd.DataFrame()
    
    # Copiar para no modificar el original
    df = df.copy()
    
    # Limpiar texto para análisis
    df["texto_clean"] = df["detalle"].apply(limpiar_texto_curado)
    
    # Inicializar columnas
    df["tipo_decision"] = "No identificado"
    df["transferencia"] = "No identificado"
    df["indice_fenomeno_corruptivo"] = 0.0

    # Aplicar matriz teórica
    for categoria, info in MATRIZ_TEORICA.items():
        # Crear pattern de búsqueda
        pattern = "|".join(info["keywords"])
        mask = df["texto_clean"].str.contains(pattern, na=False, regex=True)
        
        # Asignar valores
        df.loc[mask, "tipo_decision"] = categoria
        df.loc[mask, "transferencia"] = info["transferencia"]
        df.loc[mask, "indice_fenomeno_corruptivo"] = info["peso"]

    # Clasificar nivel de riesgo
    df["nivel_riesgo_teorico"] = df["indice_fenomeno_corruptivo"].apply(evaluar_riesgo)
    
    # Determinar directorio de guardado
    if directorio_destino and os.path.exists(directorio_destino):
        save_dir = directorio_destino
    else:
        save_dir = DATA_DIR
    
    # Generar nombre de archivo con timestamp
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"reporte_fenomenos_{fecha_str}.xlsx"
    path_excel = os.path.join(save_dir, nombre_archivo)
    
    # Guardar Excel
    try:
        # Seleccionar columnas importantes para el reporte
        columnas_reporte = [
            'fecha', 'nro_proceso', 'detalle', 'tipo_proceso', 
            'fecha_apertura', 'tipo_decision', 'transferencia',
            'indice_fenomeno_corruptivo', 'nivel_riesgo_teorico', 'link'
        ]
        
        # Filtrar solo columnas que existen
        columnas_existentes = [col for col in columnas_reporte if col in df.columns]
        df_exportar = df[columnas_existentes]
        
        # Exportar con formato
        with pd.ExcelWriter(path_excel, engine='openpyxl') as writer:
            df_exportar.to_excel(writer, sheet_name='Analisis', index=False)
            
            # Ajustar ancho de columnas
            worksheet = writer.sheets['Analisis']
            for idx, col in enumerate(df_exportar.columns, 1):
                max_length = max(
                    df_exportar[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(64 + idx)].width = min(max_length + 2, 50)
        
        print(f"✅ Reporte guardado: {path_excel}")
        
    except Exception as e:
        print(f"❌ Error al guardar Excel: {e}")
        # Fallback: guardar CSV
        path_excel = path_excel.replace('.xlsx', '.csv')
        df.to_csv(path_excel, index=False)
        print(f"⚠️ Guardado como CSV alternativo: {path_excel}")
    
    return df, path_excel, pd.DataFrame()
