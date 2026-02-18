📘# 🏛️ Monitor de Fenómenos Corruptivos

## Sistema de Detección Automática de Transferencias Regresivas de Ingresos

Sistema automatizado de análisis de decisiones estatales basado en la **Teoría de Fenómenos Corruptivos** del **Ph.D. Vicente Humberto Monteverde** (Journal of Financial Crime, 2020).

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Fundamento Teórico](#-fundamento-teórico)
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Arquitectura Mensual](#-arquitectura-mensual)
- [Componentes Principales](#-componentes-principales)
- [Dashboard Interactivo](#-dashboard-interactivo)
- [Matriz de Análisis XAI](#-matriz-de-análisis-xai)
- [Migración de Datos](#-migración-de-datos)
- [Dockerización](#-dockerización)
- [Desarrollo y Contribución](#-desarrollo-y-contribución)
- [Referencias Académicas](#-referencias-académicas)
- [Licencia](#-licencia)

---

## 🎯 Descripción

Este sistema realiza **auditoría automatizada de decisiones estatales legales** publicadas en:
- Boletín Oficial de la República Argentina (BORA)
- Portal Comprar.gob.ar

**No detecta delitos penales**, sino **fenómenos corruptivos legales** que generan transferencias regresivas de ingresos según la taxonomía científica del Dr. Monteverde.

### ¿Qué NO es este sistema?

❌ Un detector de sobornos o malversación  
❌ Un sistema de denuncia penal  
❌ Un análisis de corrupción individual  

### ¿Qué SÍ es?

✅ Analizador de decisiones discrecionales del Estado  
✅ Detector de transferencias económicas regresivas  
✅ Herramienta de transparencia basada en evidencia científica  
✅ Sistema de alertas tempranas sobre decisiones de alto impacto social  

---

## 🔬 Fundamento Teórico

### Teoría de Fenómenos Corruptivos (Monteverde, 2020)

La **Gran Corrupción** no se limita a actos ilegales. La corrupción moderna se ha diversificado en **fenómenos legales** que producen las mismas consecuencias económicas:

> *"La corrupción muta y se diversifica, volviéndose legal a través de decisiones discrecionales del Estado que generan situaciones de desigualdad económica e injusticia."*

### Los 7 Escenarios Críticos

| Escenario | Descripción | Peso XAI | Dirección de Transferencia |
|-----------|-------------|----------|----------------------------|
| **Privatización/Concesión** | Venta o adjudicación de activos estatales potencialmente subvaluados | 9.0 | Estado → Privados |
| **Obra Pública/Contratos** | Redeterminaciones, contratos directos, sobreprecios | 8.0 | Estado → Empresas Contratistas |
| **Tarifas Servicios Públicos** | Aumentos tarifarios sin considerar ingresos de la población | 7.0 | Usuarios → Concesionarias |
| **Precios Regulados** | Fijación de precios en canasta básica | 6.0 | Consumidores → Productores |
| **Salarios y Paritarias** | Ajustes salariales por debajo de inflación | 5.0 | Asalariados → Empleadores/Estado |
| **Jubilaciones/Pensiones** | Modificaciones en fórmula de movilidad jubilatoria | **10.0** | Jubilados → Estado |
| **Traslado de Impuestos** | Impuestos corporativos trasladados al precio final | 9.0 | Contribuyentes → Estado |

**Referencia:** Monteverde, V. H. (2020). *Great corruption – theory of corrupt phenomena*. Journal of Financial Crime, Vol. 28 No. 2, pp. 580-595.

---

## ✨ Características

### 🤖 Automatización Completa
- ✅ Web scraping diario de Comprar.gob.ar
- ✅ Análisis automático con matriz XAI (Explainable AI)
- ✅ Generación de reportes Excel
- ✅ Archivado mensual automático

### 📊 Dashboard Interactivo
- ✅ Visualización con Streamlit
- ✅ Gráficos interactivos (Plotly)
- ✅ Navegación histórica por mes
- ✅ Análisis avanzados (ICC, matriz de riesgo)
- ✅ Exportación de datos

### 🔍 Transparencia Científica
- ✅ Matriz XAI explicable
- ✅ Citas académicas incluidas
- ✅ Metodología reproducible
- ✅ Código abierto

### 🐳 Listo para Producción
- ✅ Compatible con Docker
- ✅ Variables de entorno configurables
- ✅ Estructura escalable
- ✅ Logs detallados

---

## 📁 Estructura del Proyecto

```
monitor-fenomenos-corruptivos/
│
├── data/                              # Datos y reportes (organizados por mes)
│   ├── 2026-01/                      # Reportes de Enero 2026
│   │   ├── reporte_fenomenos_20260130.xlsx
│   │   └── reporte_fenomenos_20260131.xlsx
│   ├── 2026-02/                      # Reportes de Febrero 2026
│   │   └── reporte_fenomenos_20260201.xlsx
│   └── ...
│
├── diario.py                          # Script principal de recolección
├── analisis.py                        # Motor de análisis (Matriz XAI)
├── dashboard.py                       # Dashboard interactivo (Streamlit)
├── migrar_a_estructura_mensual.py     # Script de migración
│
├── requirements.txt                   # Dependencias Python
├── Dockerfile                         # Contenedor Docker
├── docker-compose.yml                 # Orquestación
│
├── articulo_monteverde_español.docx   # Paper académico original
├── instructivo_dashboard.docx         # Manual de usuario
│
└── README.md                          # Este archivo
```

---

## 💻 Requisitos del Sistema

### Software Necesario

| Componente | Versión Mínima | Recomendada |
|------------|----------------|-------------|
| Python | 3.8+ | 3.10+ |
| pip | 20.0+ | 23.0+ |
| Docker (opcional) | 20.0+ | 24.0+ |

### Dependencias Python

```
pandas>=1.3.0
requests>=2.28.0
beautifulsoup4>=4.11.0
streamlit>=1.25.0
plotly>=5.14.0
openpyxl>=3.0.0
```

---

## 🚀 Instalación

### Método 1: Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/monitor-fenomenos-corruptivos.git
cd monitor-fenomenos-corruptivos

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python analisis.py  # Debe ejecutar un test rápido
```

### Método 2: Docker

```bash
# 1. Construir la imagen
docker build -t monitor-corrupcion .

# 2. Ejecutar contenedor
docker run -p 8501:8501 -v $(pwd)/data:/app/data monitor-corrupcion

# 3. Acceder al dashboard
# Abrir navegador en: http://localhost:8501
```

---

## 📖 Uso

### Ejecución Diaria (Recolección de Datos)

```bash
# Ejecutar análisis del día
python diario.py
```

**Salida esperada:**
```
--- INICIO PROCESO DIARIO: 2026-02-01 08:00 ---
📁 Creada nueva carpeta mensual: data/2026-02
📂 Directorio de almacenamiento: data/2026-02
Conectando con Comprar.gob.ar...
Éxito: Se extrajeron 45 procesos del portal.
Aplicando Matriz de Análisis XAI (Ph.D. Monteverde)...
✅ REPORTE GENERADO EXITOSAMENTE: data/2026-02/reporte_fenomenos_20260201.xlsx

Top Alertas detectadas:
                                          detalle  indice_total
0  Adjudicación de obra pública sin licitación...          8.0
1  Redeterminación de precios contrato vial...             8.0
2  Aumento tarifario servicio eléctrico...                 7.0

📦 Reporte archivado en: data/2026-02
⏱️ Tiempo de ejecución: 12 segundos
```

### Visualización (Dashboard)

```bash
# Iniciar el dashboard interactivo
streamlit run dashboard.py
```

**El dashboard se abrirá automáticamente en:** `http://localhost:8501`

### Navegación en el Dashboard

1. **Sidebar → Navegación**: Elegir entre "Dashboard Principal" o "Instructivo"
2. **Sidebar → Mes a analizar**: Seleccionar el período (Ej: "Febrero 2026")
3. **Sidebar → Reporte Diario**: Elegir el día específico
4. **Explorar**: Métricas, gráficos, tabla de auditoría, análisis avanzados

---

## 📅 Arquitectura Mensual

### ¿Por qué archivado mensual?

A partir de Febrero 2026, el sistema organiza automáticamente los reportes en carpetas mensuales para:

✅ Facilitar navegación histórica  
✅ Mejorar rendimiento con grandes volúmenes  
✅ Permitir análisis comparativos mensuales  
✅ Escalabilidad a largo plazo (años de datos)  

### Estructura de Archivado

```
data/
├── 2026-01/  ← Carpeta automática del mes
│   ├── reporte_fenomenos_20260101.xlsx
│   ├── reporte_fenomenos_20260102.xlsx
│   └── ... (31 archivos)
├── 2026-02/
│   ├── reporte_fenomenos_20260201.xlsx
│   └── ...
└── 2026-03/
    └── ...
```

### Funcionamiento Automático

Cada vez que ejecutas `diario.py`:

1. **Detecta** el mes actual (ejemplo: `2026-02`)
2. **Crea** la carpeta `data/2026-02/` si no existe
3. **Guarda** el reporte del día en esa carpeta
4. **Registra** en logs el archivado exitoso

**No requiere configuración manual** - todo es automático.

---

## 🧩 Componentes Principales

### 1. `diario.py` - Recolector Automático

**Responsabilidades:**
- Scraping de Comprar.gob.ar
- Extracción de licitaciones y contrataciones
- Invocación del motor de análisis
- Archivado mensual automático

**Configuración:**

```python
# Variables importantes
DATA_DIR = "data"  # Directorio base
url = "https://comprar.gob.ar/Compras.aspx?qs=W1HXHGHtH10="
```

### 2. `analisis.py` - Motor de Análisis

**Responsabilidades:**
- Aplicación de la Matriz XAI
- Clasificación de fenómenos
- Cálculo de índices de riesgo
- Generación de reportes Excel

**Matriz XAI (Snippet):**

```python
MATRIZ_TEORICA = {
    "Privatización / Concesión": {
        "keywords": ["concesion", "privatizacion", "venta de pliegos", ...],
        "transferencia": "Estado a Privados",
        "peso": 9,
    },
    "Jubilaciones / Pensiones": {
        "keywords": ["movilidad jubilatoria", "haber minimo", "anses", ...],
        "transferencia": "Jubilados al Estado",
        "peso": 10,  # ¡Peso máximo!
    },
    # ... 7 escenarios en total
}
```

### 3. `dashboard.py` - Interfaz de Usuario

**Secciones:**

1. **Header y Métricas**
   - Total de normas analizadas
   - Fenómenos detectados
   - Índice máximo de riesgo
   - Fecha del reporte

2. **Visualizaciones Interactivas**
   - Gráfico de barras: Intensidad por escenario
   - Gráfico circular: Sectores de transferencia

3. **Tabla de Auditoría**
   - Explorador de decisiones estatales
   - Columnas: Fecha, Tipo, Transferencia, Índice, Riesgo, Link

4. **Análisis Avanzados**
   - Acumulación temporal
   - Matriz de riesgo (scatter plot)
   - Concentración de riesgo
   - Índice de Concentración Corruptiva (ICC)
   - Recomendaciones basadas en teoría

5. **Fundamento Científico**
   - Explicación de la teoría
   - Los 7 escenarios
   - Citas académicas

### 4. `migrar_a_estructura_mensual.py` - Migración

Script one-time para reorganizar datos existentes:

```bash
python migrar_a_estructura_mensual.py
```

**Funciones:**
- Detecta archivos sueltos en `data/`
- Extrae fecha del nombre de archivo
- Crea carpetas por mes
- Mueve archivos automáticamente
- Muestra resumen de migración

---

## 📊 Dashboard Interactivo

### Métricas Principales

| Métrica | Descripción |
|---------|-------------|
| **Normas Analizadas** | Total de decisiones procesadas en el día |
| **Fenómenos Detectados** | Decisiones clasificadas en algún escenario |
| **Riesgo Máximo** | Índice más alto detectado (escala 0-10) |
| **Fecha del Reporte** | Día del análisis |

### Gráficos Interactivos

#### 1. Intensidad por Escenario Teórico
- **Tipo:** Barras horizontales
- **Eje X:** Índice de intensidad (0-10)
- **Eje Y:** Escenario de la teoría
- **Color:** Nivel de riesgo (Alto=Rojo, Medio=Naranja, Bajo=Azul)

#### 2. Sectores de Transferencia Regresiva
- **Tipo:** Pie chart (dona)
- **Datos:** Distribución de impacto económico por sector

### Tabla de Auditoría

Explorador filtrable y ordenable con:
- **Fecha:** Publicación de la norma
- **Tipo de Decisión:** Escenario clasificado
- **Transferencia:** Dirección del flujo económico
- **Índice:** Barra de progreso (0-10)
- **Nivel de Riesgo:** Calificación cualitativa
- **Link:** Enlace directo a la norma en BORA/Comprar

### Análisis Avanzados

#### Índice de Concentración Corruptiva (ICC)

Mide si pocos escenarios concentran la mayoría de los casos (Principio de Pareto):

- **ICC Alto (≥80%)**: Pocos escenarios concentran fenómenos → Alerta estratégica
- **ICC Moderado (60-79%)**: Distribución desigual
- **ICC Bajo (<60%)**: Fenómenos distribuidos

#### Matriz de Riesgo

Scatter plot que cruza:
- **Eje X:** Intensidad del fenómeno
- **Eje Y:** Dirección de transferencia
- **Tamaño:** Magnitud del índice
- **Color:** Nivel de riesgo

---

## 🔍 Matriz de Análisis XAI

### Proceso de Clasificación

```
1. ENTRADA
   ↓
   Texto de la decisión estatal
   ↓
2. LIMPIEZA
   ↓
   Normalización Unicode (eliminar tildes)
   Conversión a minúsculas
   ↓
3. MATCHING
   ↓
   Búsqueda de keywords por escenario
   (Regex case-insensitive)
   ↓
4. CLASIFICACIÓN
   ↓
   Asignación de:
   - Tipo de decisión
   - Transferencia económica
   - Peso XAI (0-10)
   ↓
5. EVALUACIÓN
   ↓
   Nivel de riesgo:
   - Alto: ≥8
   - Medio: 5-7
   - Bajo: <5
   ↓
6. SALIDA
   ↓
   Reporte Excel con clasificación
```

### Ejemplo de Clasificación

**Entrada:**
```
"Adjudicación de contrato de obra pública para construcción de autopista 
con cláusula de redeterminación de precios."
```

**Proceso:**
1. Limpieza: `"adjudicacion de contrato de obra publica para construccion..."`
2. Match: Encuentra `"obra publica"` y `"redeterminacion de precios"`
3. Clasificación:
   - **Tipo:** Obra Pública / Contratos
   - **Transferencia:** Estado a Empresas Contratistas
   - **Peso:** 8.0
   - **Riesgo:** Alto

**Salida:**
| Campo | Valor |
|-------|-------|
| tipo_decision | Obra Pública / Contratos |
| transferencia | Estado a Empresas Contratistas |
| indice_fenomeno_corruptivo | 8.0 |
| nivel_riesgo_teorico | Alto |

---

## 🔄 Migración de Datos

### Si ya tienes datos de enero en `data/`

Ejecuta el script de migración una sola vez:

```bash
python migrar_a_estructura_mensual.py
```

### Proceso de Migración

```
ANTES:
data/
├── reporte_fenomenos_20260130.xlsx
├── reporte_fenomenos_20260131.xlsx
└── (30+ archivos sueltos)

DESPUÉS:
data/
└── 2026-01/
    ├── reporte_fenomenos_20260130.xlsx
    ├── reporte_fenomenos_20260131.xlsx
    └── (31 archivos organizados)
```

### Seguridad

El script:
✅ Muestra preview antes de ejecutar  
✅ Pide confirmación  
✅ Mueve archivos (no los copia, ahorra espacio)  
✅ Muestra resumen de éxitos y errores  

**Recomendación:** Haz backup antes de migrar:
```bash
cp -r data data_backup_20260131
```

---

## 🐳 Dockerización

### Dockerfile Incluido

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - TZ=America/Argentina/Buenos_Aires
```

### Comandos Docker

```bash
# Construir
docker-compose build

# Ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 👨‍💻 Desarrollo y Contribución

### Agregar Nuevos Escenarios

Editar `analisis.py`:

```python
MATRIZ_TEORICA = {
    # ... escenarios existentes ...
    
    "Nuevo Escenario": {
        "keywords": ["palabra1", "palabra2", "frase completa"],
        "transferencia": "Sector A a Sector B",
        "peso": 7,  # Entre 1-10
    },
}
```

### Testing

```bash
# Test del motor de análisis
python analisis.py

# Test del scraper
python diario.py
```

### Estructura de Commits

```
feat: Agregar escenario de subsidios energéticos
fix: Corregir encoding en scraping BORA
docs: Actualizar README con ejemplos
refactor: Optimizar carga de archivos grandes
```

---

## 📚 Referencias Académicas

### Publicación Original

**Monteverde, V. H. (2020)**  
*Great corruption – theory of corrupt phenomena*  
Journal of Financial Crime, Vol. 28 No. 2, pp. 580-595  
https://doi.org/10.1108/JFC-04-2020-0062

### Conceptos Clave Citados

- **Rent Seeking** (Búsqueda de Rentas): Obtención de ingresos mediante privilegios estatales en lugar de actividad productiva
- **Legalidad como Escudo**: La corrupción moderna opera dentro de marcos normativos legales
- **Transferencias Regresivas**: Flujo de ingresos desde sectores vulnerables hacia sectores concentrados
- **Discrecionalidad Estatal**: Decisiones sin transparencia ni criterios técnicos públicos

### Descarga del Paper

Incluido en el proyecto como:
- `articulo_monteverde_español.docx`
- También disponible para descarga desde el dashboard

---

## 📄 Licencia

Este proyecto se distribuye bajo licencia **MIT**.

```
MIT License

Copyright (c) 2026 Monitor de Fenómenos Corruptivos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🙏 Agradecimientos

- **Ph.D. Vicente Humberto Monteverde** - Por la teoría científica fundamental
- **Journal of Financial Crime** - Publicación del paper académico
- **Comunidad Open Source** - Bibliotecas Python utilizadas

---

## 📞 Contacto y Soporte

- **Issues:** [GitHub Issues](https://github.com/tu-usuario/monitor-fenomenos-corruptivos/issues)
- **Documentación:** Ver `instructivo_dashboard.docx` incluido
- **Email:** soporte@proyecto.org (si aplica)

---

## 🗺️ Roadmap

### v1.0 (Actual)
- ✅ Scraping automatizado
- ✅ Análisis con Matriz XAI
- ✅ Dashboard interactivo
- ✅ Archivado mensual

### v1.1 (En desarrollo)
- ⏳ API RESTful para integraciones
- ⏳ Alertas por email
- ⏳ Análisis comparativo multi-mes
- ⏳ Export a PDF de reportes

### v2.0 (Futuro)
- 📋 Machine Learning para mejora de clasificación
- 📋 Integración con otros BOE de Latinoamérica
- 📋 Dashboard público en tiempo real
- 📋 App móvil

---

**Última actualización:** 31 de Enero, 2026  
**Versión:** 2.0 (Archivado Mensual)  
**Mantenedor:** [Tu Nombre/Organización]

---

<p align="center">
  <strong>Monitor de Fenómenos Corruptivos</strong><br>
  <em>Transparencia basada en evidencia científica</em>
</p>