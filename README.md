# CERAMIX Sales Analysis Project 📊

## 📋 Descripción del Proyecto

Este proyecto se centra en la **ingeniería y limpieza de datos** de las ventas de la empresa **CERAMIX** (2025).

El objetivo principal es procesar los datos brutos alojados en **Google Drive**, realizar un Análisis Exploratorio de Datos (EDA) preliminar y preparar un dataset limpio y estructurado para alimentar un tablero de control en **Looker Studio**.

## 🎯 Objetivos de Negocio

El tablero final en Looker Studio permitirá responder interactivamente a:

- **Rendimiento Temporal:** Identificación de Meses, Semanas, Días y Trimestres con mejor y peor desempeño.
- **Análisis Financiero:** Visualización de ingresos a lo largo del 2025.
- **Forecasting:** (Opcional) Proyección básica para Febrero 2026 y meses subsiguientes. (La opción de meses subsiguientes dependerá de la disponibilidad de datos históricos del año corriente)

## 🔄 Flujo de Trabajo (Pipeline)

1.  **Conexión API Google Drive:**
    - Autenticación segura (Service Account / OAuth).
    - **Lectura y Escritura directa:** El script modificará los archivos directamente en la nube.
2.  **Procesamiento (Python):**
    - Limpieza de datos (Manejo de duplicados, valores nulos, formatos de fecha).
    - Validación de calidad (QA).
3.  **Visualización (Looker Studio):**
    - Los datos limpios se actualizan en Drive para reflejarse automáticamente en Looker.

## 🛠️ Requisitos Técnicos

- **Google Drive API V3** habilitada.
- **Google Sheets API** (si el archivo es una hoja de cálculo).
- Credenciales de acceso (JSON key).

## 📊 Estructura de Datos Requerida

Para el análisis, se espera que los datos limpios cumplan con:

| Variable    | Descripción          | Uso en Looker                          |
| :---------- | :------------------- | :------------------------------------- |
| **Cliente** | Nombre normalizado   | Filtros                                |
| **Fecha**   | Formato `YYYY-MM-DD` | Series de tiempo, drill-down (Mes/Día) |
| **Ingreso** | Numérico (Moneda)    | Métricas (Suma, Promedio)              |

## 🛠️ Stack Tecnológico

- **Fuente:** Google Drive.
- **Procesamiento:** Python (Pandas).
- **Visualización:** Looker Studio.
