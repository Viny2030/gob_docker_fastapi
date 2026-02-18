import pytest
import pandas as pd
from analisis import analizar_boletin, REGLAS_CLASIFICACION

# ==========================================
# DEFINICIÓN DE GRUPOS DEMOGRÁFICOS / SECTORES
# ==========================================
# Para el stress testing, simulamos textos que afectan a distintos grupos
# para ver si el algoritmo los "ve" a todos por igual.

CASOS_STRESS_TEST = [
    # GRUPO 1: JUBILADOS (Sector Vulnerable)
    # Prueba: ¿Detecta eufemismos técnicos como "ajuste de movilidad"?
    {
        "texto": "Se decreta la nueva fórmula de movilidad jubilatoria con ajuste trimestral.",
        "grupo": "Jubilados",
        "esperado": "Jubilaciones / Pensiones",
    },
    # GRUPO 2: USUARIOS DE SERVICIOS (Población General)
    # Prueba: ¿Detecta aumentos disfrazados de "revisión"?
    {
        "texto": "Apruébase el nuevo cuadro tarifario para la distribución de energía eléctrica.",
        "grupo": "Usuarios",
        "esperado": "Tarifas Servicios Públicos",
    },
    # GRUPO 3: EMPRESAS CONTRATISTAS (Sector Privilegiado)
    # Prueba: ¿Detecta beneficios corporativos?
    {
        "texto": "Autorízase la redeterminación de precios en la obra pública de saneamiento.",
        "grupo": "Empresas",
        "esperado": "Obra Pública / Contratos",
    },
    # GRUPO 4: CASOS CONFUSOS (Borde)
    # Prueba de Falso Positivo: Texto que parece corrupción pero no lo es.
    {
        "texto": "Declaración de interés cultural a la obra de teatro local.",
        "grupo": "Cultura",
        "esperado": "No identificado",  # NO debe marcarlo como Obra Pública
    },
]

# ==========================================
# EJECUCIÓN DEL TEST (Pytest)
# ==========================================


@pytest.mark.parametrize("caso", CASOS_STRESS_TEST)
def test_cobertura_demografica(caso):
    """
    Stress Test: Verifica que el algoritmo funcione equitativamente
    para diferentes sectores (Jubilados vs Empresas).
    """
    # 1. Preparamos el dato simulado
    df_simulado = pd.DataFrame(
        [
            {
                "fecha": "2024-01-01",
                "seccion": "primera",
                "detalle": caso["texto"],
                "tipo_decision": "No identificado",  # Estado inicial
                "link": "http://test",
            }
        ]
    )

    # 2. Ejecutamos el núcleo de análisis (Tu cerebro teórico)
    df_procesado, _, _ = analizar_boletin(df_simulado)

    resultado_obtenido = df_procesado.iloc[0]["tipo_decision"]

    # 3. Validación (Assert)
    mensaje_error = (
        f"\n[FALLO DE SESGO EN GRUPO: {caso['grupo']}]\n"
        f"Texto: '{caso['texto']}'\n"
        f"Esperaba clasificar como: '{caso['esperado']}'\n"
        f"Pero el algoritmo dijo: '{resultado_obtenido}'\n"
        f"-> RIESGO: El sistema está ciego ante este sector."
    )

    assert resultado_obtenido == caso["esperado"], mensaje_error


def test_auditoria_diccionario_completo():
    """
    Verifica la integridad del diccionario de reglas.
    Asegura que no hayamos borrado reglas críticas accidentalmente.
    """
    sectores_criticos = [
        "Jubilaciones / Pensiones",
        "Privatización / Concesión",
        "Tarifas Servicios Públicos",
    ]

    for sector in sectores_criticos:
        assert sector in REGLAS_CLASIFICACION, (
            f"¡ALERTA CRÍTICA! Se borró la categoría '{sector}'."
        )
        assert len(REGLAS_CLASIFICACION[sector]) > 0, (
            f"La categoría '{sector}' está vacía (sin palabras clave)."
        )


# ==========================================
# INSTRUCCIONES DE USO
# ==========================================
# Para correr esta auditoría, abre tu terminal y escribe:
# pip install pytest
# pytest tests_auditoria.py -v