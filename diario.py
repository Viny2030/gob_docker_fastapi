import os
import re
import time
import shutil
import warnings
import requests
import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from analisis import analizar_boletin

# Suprimir warnings de SSL (portal gubernamental con certificado problemático)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# ==========================================
# CONFIGURACIÓN DE RUTAS CON ARCHIVADO MENSUAL
# ==========================================
DATA_DIR = os.path.join(os.getcwd(), "data")

def obtener_directorio_mes_actual():
    ahora = datetime.now()
    mes_carpeta = ahora.strftime("%Y-%m")
    ruta_mes = os.path.join(DATA_DIR, mes_carpeta)
    if not os.path.exists(ruta_mes):
        os.makedirs(ruta_mes)
        print(f"📁 Creada nueva carpeta mensual: {ruta_mes}")
    return ruta_mes

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ==========================================
# HEADERS ACTUALIZADOS (Chrome 120, 2024)
# ==========================================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.argentina.gob.ar/",
}

# ==========================================
# FUNCIÓN DE REQUEST CON REINTENTOS
# ==========================================
def get_con_reintentos(url, intentos=3, timeout=60, espera=10, verify_ssl=False):
    """
    GET con reintentos. verify_ssl=False necesario para comprar.gob.ar
    cuya cadena de certificados está rota desde ~feb 2026.
    """
    ultimo_error = None
    for i in range(1, intentos + 1):
        try:
            print(f"   🔄 Intento {i}/{intentos}: {url[:65]}...")
            resp = requests.get(url, headers=HEADERS, timeout=timeout, verify=verify_ssl)
            resp.raise_for_status()
            return resp
        except Exception as e:
            ultimo_error = e
            print(f"   ⚠️ Intento {i} fallido: {type(e).__name__}: {str(e)[:100]}")
            if i < intentos:
                print(f"   ⏳ Esperando {espera}s antes de reintentar...")
                time.sleep(espera)
    raise ultimo_error

# ==========================================
# FUENTE 1: SCRAPER COMPRAR.GOB.AR
# ==========================================
def extraer_licitaciones_scraper():
    url = "https://comprar.gob.ar/Compras.aspx?qs=W1HXHGHtH10="
    try:
        response = get_con_reintentos(url, intentos=3, timeout=60, espera=15, verify_ssl=False)
        soup = BeautifulSoup(response.text, "html.parser")
        tabla = soup.find("table", {"id": "ctl00_CPH1_GridLicitaciones"})
        if not tabla:
            tabla = soup.find("table")
        if not tabla:
            print("   ❌ Tabla de licitaciones no encontrada en el HTML.")
            return pd.DataFrame()
        rows = tabla.find_all("tr")
        datos = []
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) > 4:
                link_tag = cols[2].find("a")
                datos.append({
                    "fecha":          datetime.now().strftime("%Y-%m-%d"),
                    "nro_proceso":    cols[1].text.strip(),
                    "detalle":        cols[2].text.strip(),
                    "tipo_proceso":   cols[3].text.strip(),
                    "fecha_apertura": cols[4].text.strip(),
                    "link":           "https://comprar.gob.ar" + link_tag["href"] if link_tag else url,
                    "fuente":         "Scraper Comprar.gob.ar",
                })
        print(f"   ✅ Scraper OK: {len(datos)} procesos extraídos.")
        return pd.DataFrame(datos)
    except Exception as e:
        print(f"❌ Scraper falló: {e}")
        return pd.DataFrame()

# ==========================================
# FUENTE 2: API OFICIAL DATOS.GOB.AR (ONC)
# ==========================================
def extraer_api_datos_gob():
    print("🔁 FALLBACK 1: API datos.gob.ar (ONC)...")
    # Datasets públicos de la Oficina Nacional de Contrataciones
    endpoints = [
        "https://datos.gob.ar/api/3/action/datastore_search?resource_id=6b5d4940-5e87-4f2d-8de1-c5583ef4a243&limit=50",
        "https://datos.gob.ar/api/3/action/datastore_search?resource_id=99db6631-d1cf-470c-a73d-afa948d53f35&limit=50",
    ]
    for url in endpoints:
        try:
            resp = get_con_reintentos(url, intentos=2, timeout=30, espera=5, verify_ssl=True)
            records = resp.json().get("result", {}).get("records", [])
            if records:
                datos = [{
                    "fecha":          datetime.now().strftime("%Y-%m-%d"),
                    "nro_proceso":    str(r.get("nro_proceso", r.get("_id", "n/a"))),
                    "detalle":        r.get("descripcion", r.get("objeto", r.get("detalle", "Sin descripción"))),
                    "tipo_proceso":   r.get("tipo_procedimiento", r.get("modalidad", "n/a")),
                    "fecha_apertura": r.get("fecha_apertura", r.get("fecha", "n/a")),
                    "link":           r.get("enlace", r.get("url", "https://comprar.gob.ar")),
                    "fuente":         "API datos.gob.ar",
                } for r in records]
                print(f"   ✅ API OK: {len(datos)} registros.")
                return pd.DataFrame(datos)
        except Exception as e:
            print(f"   ⚠️ Endpoint fallido: {e}")
    print("   ❌ API datos.gob.ar: sin datos.")
    return pd.DataFrame()

# ==========================================
# FUENTE 3: BOLETÍN OFICIAL - SECCIÓN CONTRATACIONES
# ==========================================
def extraer_boletin_oficial():
    print("🔁 FALLBACK 2: Boletín Oficial - Contrataciones...")
    palabras_clave = [
        "licitaci", "contrat", "adjudicaci", "obra p", "concurso",
        "compra", "adquisici", "subasta", "locaci", "llamado a",
        "pliego", "presupuesto oficial",
    ]
    urls_rss = [
        "https://www.boletinoficial.gob.ar/rss/3",  # Tercera sección (contrataciones)
        "https://www.boletinoficial.gob.ar/rss/2",  # Segunda sección
        "https://www.boletinoficial.gob.ar/rss/1",  # Primera sección
    ]
    datos = []
    for url in urls_rss:
        try:
            resp = get_con_reintentos(url, intentos=2, timeout=30, espera=5, verify_ssl=True)
            items = re.findall(r"<item>(.*?)</item>", resp.text, re.DOTALL)
            for item in items[:100]:
                titulo_m = re.search(r"<title[^>]*>(.*?)</title>", item, re.DOTALL)
                link_m   = re.search(r"<link>(.*?)</link>",         item, re.DOTALL)
                desc_m   = re.search(r"<description[^>]*>(.*?)</description>", item, re.DOTALL)
                titulo = re.sub(r"<[^>]+>|<!\[CDATA\[|\]\]>", "", titulo_m.group(1) if titulo_m else "").strip()
                link   = (link_m.group(1) if link_m else "").strip()
                desc   = re.sub(r"<[^>]+>|<!\[CDATA\[|\]\]>", "", desc_m.group(1) if desc_m else "").strip()
                texto  = (titulo + " " + desc).lower()
                if any(p in texto for p in palabras_clave) and titulo:
                    datos.append({
                        "fecha":          datetime.now().strftime("%Y-%m-%d"),
                        "nro_proceso":    "BOL-" + datetime.now().strftime("%H%M%S"),
                        "detalle":        titulo,
                        "tipo_proceso":   "Boletín Oficial",
                        "fecha_apertura": "n/a",
                        "link":           link,
                        "fuente":         "Boletín Oficial",
                    })
        except Exception as e:
            print(f"   ⚠️ RSS {url[-20:]}: {e}")
    if datos:
        print(f"   ✅ Boletín Oficial: {len(datos)} items.")
        return pd.DataFrame(datos)
    print("   ❌ Boletín Oficial: sin items relevantes.")
    return pd.DataFrame()

# ==========================================
# FUENTE 4: ARGENTINACOMPRA (portal alternativo)
# ==========================================
def extraer_argentinacompra():
    print("🔁 FALLBACK 3: argentinacompra.gov.ar...")
    url = "https://www.argentinacompra.gov.ar/"
    try:
        resp = get_con_reintentos(url, intentos=2, timeout=30, espera=5, verify_ssl=False)
        soup = BeautifulSoup(resp.text, "html.parser")
        datos = []
        for tabla in soup.find_all("table")[:3]:
            for row in tabla.find_all("tr")[1:20]:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    link_tag = row.find("a")
                    datos.append({
                        "fecha":          datetime.now().strftime("%Y-%m-%d"),
                        "nro_proceso":    cols[0].text.strip() if cols else "n/a",
                        "detalle":        cols[1].text.strip() if len(cols) > 1 else "n/a",
                        "tipo_proceso":   cols[2].text.strip() if len(cols) > 2 else "n/a",
                        "fecha_apertura": cols[3].text.strip() if len(cols) > 3 else "n/a",
                        "link":           link_tag["href"] if link_tag else url,
                        "fuente":         "ArgentinaCompra",
                    })
        if datos:
            print(f"   ✅ ArgentinaCompra: {len(datos)} registros.")
        else:
            print("   ❌ ArgentinaCompra: sin datos estructurados.")
        return pd.DataFrame(datos)
    except Exception as e:
        print(f"   ❌ ArgentinaCompra falló: {e}")
        return pd.DataFrame()

# ==========================================
# ORQUESTADOR: CASCADA DE 4 FUENTES
# ==========================================
def extraer_licitaciones():
    print("🔍 Conectando con Comprar.gob.ar...")
    fuentes = [
        ("Comprar.gob.ar (scraper)", extraer_licitaciones_scraper),
        ("API datos.gob.ar",         extraer_api_datos_gob),
        ("Boletín Oficial",          extraer_boletin_oficial),
        ("ArgentinaCompra",          extraer_argentinacompra),
    ]
    for nombre, funcion in fuentes:
        df = funcion()
        if not df.empty:
            print(f"✅ Fuente activa: {nombre} ({len(df)} registros)")
            return df
        print(f"   → {nombre}: sin datos, probando siguiente fuente...")
    print("❌ Todas las fuentes fallaron.")
    return pd.DataFrame()

# ==========================================
# PROCESO PRINCIPAL
# ==========================================
def ejecutar_robot():
    start_time = datetime.now()
    print(f"\n--- INICIO PROCESO DIARIO: {start_time.strftime('%Y-%m-%d %H:%M')} ---")

    directorio_mes = obtener_directorio_mes_actual()
    df_portal = extraer_licitaciones()

    if df_portal.empty:
        print("⚠️ Todas las fuentes fallaron. Generando registro de control vacío.")
        df_portal = pd.DataFrame([{
            "fecha":          datetime.now().strftime("%Y-%m-%d"),
            "detalle":        "Sin datos - todas las fuentes fallaron",
            "link":           "n/a",
            "tipo_proceso":   "n/a",
            "fecha_apertura": "n/a",
            "fuente":         "ninguna",
        }])
    else:
        df_portal["detalle"] = df_portal["detalle"].fillna("Sin descripción")
        print(f"📊 Total registros a analizar: {len(df_portal)}")

    print("🧠 Aplicando Matriz de Análisis XAI (Ph.D. Monteverde)...")

    try:
        df_final, path_excel, _ = analizar_boletin(df_portal, directorio_mes)
    except TypeError:
        print("⚠️ Usando modo compatibilidad (analisis.py antiguo).")
        df_final, path_excel, _ = analizar_boletin(df_portal)
        if path_excel and os.path.exists(path_excel):
            nombre_archivo = os.path.basename(path_excel)
            nueva_ruta     = os.path.join(directorio_mes, nombre_archivo)
            shutil.move(path_excel, nueva_ruta)
            path_excel = nueva_ruta
            print(f"📦 Archivo organizado en: {path_excel}")

    if path_excel and os.path.exists(path_excel):
        print(f"\n✨ REPORTE GENERADO: {path_excel}")
        if "indice_fenomeno_corruptivo" in df_final.columns:
            top_riesgo = df_final.sort_values(
                by="indice_fenomeno_corruptivo", ascending=False
            ).head(3)
            print("\n🚨 ALERTAS DE MAYOR RIESGO DETECTADAS:")
            print(top_riesgo[["detalle", "indice_fenomeno_corruptivo"]])
    else:
        print("❌ Error crítico: El reporte no pudo ser generado.")

    elapsed = (datetime.now() - start_time).seconds
    print(f"\n⏱️ Tiempo total: {elapsed} segundos.")
    print("--- FIN DEL PROCESO ---")

if __name__ == "__main__":
    ejecutar_robot()
