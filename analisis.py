import os
import unicodedata
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS DINÁMICAS ---
# Detecta la raíz del proyecto para que funcione en Docker/Railway y Local
BASE_PATH = os.getcwd()
DATA_DIR = os.path.join(BASE_PATH, "data")

# Asegura que la carpeta 'data' exista para evitar errores de guardado
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except Exception as e:
        print(f"⚠️ No se pudo crear DATA_DIR: {e}")

# --- MATRIZ TEÓRICA - Ph.D. Vicente Humberto Monteverde ---
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
    """Normaliza texto eliminando acentos y convirtiendo a minúsculas"""
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

def evaluar_riesgo(score):
    """Clasifica el nivel de riesgo según el peso de la matriz"""
    if score >= 8: return "Alto"
    if score >= 5: return "Medio"
    return "Bajo"

def analizar_boletin(df, directorio_destino=None):
    """
    Aplica la matriz de Monteverde y guarda el reporte resultante.
    """
    if df is None or df.empty:
        return pd.DataFrame(), None, pd.DataFrame()
    
    df = df.copy()
    
    # 1. Limpieza y preparación
    df["texto_clean"] = df["detalle"].apply(limpiar_texto_curado)
    df["tipo_decision"] = "No identificado"
    df["transferencia"] = "No identificado"
    df["indice_fenomeno_corruptivo"] = 0.0

    # 2. Aplicación de la Matriz Teórica
    for categoria, info in MATRIZ_TEORICA.items():
        pattern = "|".join(info["keywords"])
        mask = df["texto_clean"].str.contains(pattern, na=False, regex=True)
        
        df.loc[mask, "tipo_decision"] = categoria
        df.loc[mask, "transferencia"] = info["transferencia"]
        df.loc[mask, "indice_fenomeno_corruptivo"] = info["peso"]

    df["nivel_riesgo_teorico"] = df["indice_fenomeno_corruptivo"].apply(evaluar_riesgo)
    
    # 3. Gestión de guardado de archivos
    save_dir = directorio_destino if (directorio_destino and os.path.exists(directorio_destino)) else DATA_DIR
    
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_base = f"reporte_fenomenos_{fecha_str}"
    path_excel = os.path.join(save_dir, f"{nombre_base}.xlsx")
    
    try:
        # Columnas deseadas para el reporte final
        cols = ['fecha', 'nro_proceso', 'detalle', 'tipo_proceso', 'tipo_decision', 
                'transferencia', 'indice_fenomeno_corruptivo', 'nivel_riesgo_teorico', 'link']
        
        # Filtrar solo las columnas que realmente existen en el DF
        df_export = df[[c for c in cols if c in df.columns]]
        
        # Guardar Excel con motor openpyxl
        df_export.to_excel(path_excel, index=False, engine='openpyxl')
        print(f"✅ Reporte generado exitosamente: {path_excel}")
        
    except Exception as e:
        print(f"❌ Error al guardar Excel: {e}. Intentando CSV...")
        path_excel = os.path.join(save_dir, f"{nombre_base}.csv")
        df.to_csv(path_excel, index=False)
    
    # Retornar el DataFrame analizado, la ruta del archivo y un DF vacío para compatibilidad con main.py
    return df, path_excel, pd.DataFrame()
