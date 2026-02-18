import pandas as pd
from collections import Counter
import os
from analisis import limpiar_texto_curado

# Palabras vacías (Stopwords) que no nos importan porque son conectores
STOPWORDS = [
    "el",
    "la",
    "los",
    "las",
    "un",
    "una",
    "unos",
    "unas",
    "de",
    "del",
    "al",
    "a",
    "en",
    "y",
    "o",
    "que",
    "se",
    "por",
    "con",
    "para",
    "su",
    "sus",
    "es",
    "son",
    "fue",
    "boletín",
    "oficial",
    "resolución",
    "decreto",
    "ley",
    "artículo",
    "n°",
    "fecha",
    "visto",
    "considerando",
]


def analizar_frecuencias(archivo_excel):
    """
    Lee el Excel generado, busca en la categoría 'No identificado'
    y cuenta qué palabras se repiten más.
    """
    try:
        df = pd.read_excel(archivo_excel, sheet_name="Analisis")
    except Exception as e:
        print(f"Error al leer el Excel: {e}")
        return

    # 1. Filtramos solo lo que el sistema NO entendió (La "Caja Negra")
    df_desconocido = df[df["tipo_decision"] == "No identificado"]

    if df_desconocido.empty:
        print(
            "¡Excelente! No hay registros sin identificar. Tu diccionario cubre todo."
        )
        return

    print(f"Analizando {len(df_desconocido)} registros no identificados...")

    palabras_candidatas = []

    # 2. Procesamos el texto
    for texto in df_desconocido["detalle"]:
        # Limpiamos (sacamos tildes raras) y pasamos a minúsculas
        texto_limpio = limpiar_texto_curado(str(texto)).lower()

        # Separamos en palabras
        tokens = texto_limpio.split()

        # Guardamos solo las palabras que NO son conectores (stopwords) y tienen longitud decente
        for palabra in tokens:
            # Quitamos signos de puntuación pegados
            palabra = palabra.strip(".,;:()\"'")
            if len(palabra) > 4 and palabra not in STOPWORDS:
                palabras_candidatas.append(palabra)

    # 3. Contamos las frecuencias
    conteo = Counter(palabras_candidatas)

    # 4. Mostramos el TOP 20
    print("\n=== REPORTE DE SUGERENCIAS PARA NUEVAS REGLAS ===")
    print("Estas palabras se repiten mucho en lo que estás ignorando.")
    print("Si ves términos de dinero o poder aquí, agrégalos a 'analisis.py'.\n")

    print(f"{'PALABRA':<20} | {'FRECUENCIA':<10}")
    print("-" * 35)

    for palabra, cantidad in conteo.most_common(20):
        print(f"{palabra:<20} | {cantidad:<10}")

    print("-" * 35)


# --- EJECUCIÓN ---
if __name__ == "__main__":
    # Busca automáticamente el último Excel generado en la carpeta data
    data_dir = "data"
    archivos = [
        f
        for f in os.listdir(data_dir)
        if f.startswith("reporte_fenomenos") and f.endswith(".xlsx")
    ]

    if archivos:
        # Ordenamos para obtener el más reciente
        archivos.sort(reverse=True)
        ultimo_reporte = os.path.join(data_dir, archivos[0])
        print(f"Analizando reporte: {ultimo_reporte}")
        analizar_frecuencias(ultimo_reporte)
    else:
        print("No encontré reportes Excel en la carpeta /data")