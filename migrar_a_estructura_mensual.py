#!/usr/bin/env python3
"""
Script de Migración - Organización Mensual de Reportes
=======================================================

Este script reorganiza los reportes existentes en la carpeta data/
creando subcarpetas por mes (formato YYYY-MM).

USO:
    python migrar_a_estructura_mensual.py

ANTES:
    data/
    ├── reporte_fenomenos_20260130.xlsx
    ├── reporte_fenomenos_20260131.xlsx
    └── reporte_fenomenos_20260201.xlsx

DESPUÉS:
    data/
    ├── 2026-01/
    │   ├── reporte_fenomenos_20260130.xlsx
    │   └── reporte_fenomenos_20260131.xlsx
    └── 2026-02/
        └── reporte_fenomenos_20260201.xlsx
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

DATA_DIR = "data"


def extraer_fecha_del_nombre(nombre_archivo):
    """
    Extrae la fecha del nombre del archivo
    Ej: reporte_fenomenos_20260130.xlsx -> 2026-01
    """
    try:
        # Buscar el patrón YYYYMMDD en el nombre
        partes = nombre_archivo.split("_")
        for parte in partes:
            if len(parte) == 12 and parte[:8].isdigit():  # 20260130.xlsx
                fecha_str = parte[:8]  # 20260130
                year = fecha_str[:4]
                mes = fecha_str[4:6]
                return f"{year}-{mes}"
    except:
        pass
    return None


def migrar_archivos():
    """Reorganiza los archivos existentes en carpetas mensuales"""

    if not os.path.exists(DATA_DIR):
        print(f"❌ No se encuentra el directorio {DATA_DIR}")
        return

    # Listar todos los archivos .xlsx en el directorio raíz de data/
    archivos = [
        f
        for f in os.listdir(DATA_DIR)
        if f.endswith(".xlsx") and os.path.isfile(os.path.join(DATA_DIR, f))
    ]

    if not archivos:
        print(f"✅ No hay archivos para migrar en {DATA_DIR}")
        return

    print(f"📁 Encontrados {len(archivos)} archivos para migrar\n")

    migrados = 0
    errores = 0

    for archivo in archivos:
        mes_carpeta = extraer_fecha_del_nombre(archivo)

        if not mes_carpeta:
            print(f"⚠️  Saltando {archivo} (no se pudo extraer fecha)")
            errores += 1
            continue

        # Crear directorio del mes si no existe
        ruta_mes = os.path.join(DATA_DIR, mes_carpeta)
        if not os.path.exists(ruta_mes):
            os.makedirs(ruta_mes)
            print(f"📂 Creada carpeta: {ruta_mes}")

        # Mover archivo
        ruta_origen = os.path.join(DATA_DIR, archivo)
        ruta_destino = os.path.join(ruta_mes, archivo)

        try:
            shutil.move(ruta_origen, ruta_destino)
            print(f"✅ Migrado: {archivo} -> {mes_carpeta}/")
            migrados += 1
        except Exception as e:
            print(f"❌ Error al migrar {archivo}: {e}")
            errores += 1

    print(f"\n{'=' * 50}")
    print(f"RESUMEN DE MIGRACIÓN")
    print(f"{'=' * 50}")
    print(f"✅ Archivos migrados: {migrados}")
    print(f"❌ Errores: {errores}")
    print(f"📂 Estructura actualizada en: {os.path.abspath(DATA_DIR)}")
    print(f"\n¡Listo! Ahora puedes ejecutar dashboard.py")


def verificar_estructura():
    """Muestra la estructura actual de carpetas"""
    print(f"\n{'=' * 50}")
    print(f"ESTRUCTURA ACTUAL DE {DATA_DIR}/")
    print(f"{'=' * 50}\n")

    if not os.path.exists(DATA_DIR):
        print(f"❌ Directorio {DATA_DIR} no existe")
        return

    for item in sorted(os.listdir(DATA_DIR)):
        item_path = os.path.join(DATA_DIR, item)
        if os.path.isdir(item_path):
            archivos_mes = [f for f in os.listdir(item_path) if f.endswith(".xlsx")]
            print(f"📁 {item}/ ({len(archivos_mes)} reportes)")
            for archivo in sorted(archivos_mes):
                print(f"   └─ {archivo}")
        elif item.endswith(".xlsx"):
            print(f"📄 {item} (sin organizar)")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════╗
    ║  MIGRACIÓN A ESTRUCTURA MENSUAL                    ║
    ║  Monitor de Fenómenos Corruptivos                  ║
    ╚════════════════════════════════════════════════════╝
    """)

    # Mostrar estructura actual
    verificar_estructura()

    # Confirmar migración
    print(f"\n{'=' * 50}")
    respuesta = input("¿Desea continuar con la migración? (s/n): ").lower().strip()

    if respuesta in ["s", "si", "sí", "y", "yes"]:
        print(f"\n🚀 Iniciando migración...\n")
        migrar_archivos()

        # Mostrar estructura final
        verificar_estructura()
    else:
        print("\n❌ Migración cancelada")