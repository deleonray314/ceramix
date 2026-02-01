# Guía de Implementación de Pronósticos: Tendencia y Suavizado

Este documento detalla paso a paso cómo implementar modelos de pronóstico ("Forecasting") utilizando Python, enfocándose en **Suavizado Exponencial** y **Regresión Lineal**, adecuado para un historial de datos limitado (aprox. 1 año).

## 1. Preparación del Entorno

Necesitaremos librerías adicionales para el análisis estadístico.

```bash
pip install pandas statsmodels scikit-learn matplotlib
```

## 2. Preprocesamiento de Datos

Antes de pronosticar, los datos deben estar estructurados temporalmente.

**Suposiciones:**

- `df` es tu DataFrame limpio.
- Columna de fecha: `'FECHA'` (u otro nombre).
- Columna de valor: `'TOTAL'` (o `'VENTA'`).

### Paso 2.1: Conversión y Agrupación

Los datos diarios suelen ser muy ruidosos. Agrupar por **Semanas (W)** o **Meses (M)** ayuda a ver mejor la tendencia.

```python
import pandas as pd
import matplotlib.pyplot as plt

# 1. Convertir a datetime
df['FECHA'] = pd.to_datetime(df['FECHA'])

# 2. Ordenar cronológicamente
df = df.sort_values('FECHA')

# 3. Agrupar (Ejemplo: Semanal 'W-MON' para semanas que inician en lunes)
# Sumar ventas por semana
df_resampled = df.set_index('FECHA').resample('W-MON')['TOTAL'].sum().reset_index()

# Manejar valores nulos (semanas sin ventas)
df_resampled['TOTAL'] = df_resampled['TOTAL'].fillna(0)

# Establecer la fecha como índice para los modelos
data_series = df_resampled.set_index('FECHA')['TOTAL']
```

---

## 3. Método 1: Suavizado Exponencial (Holt-Winters)

Ideal para capturar el nivel actual y la tendencia local. Al tener solo 1 año, la "estacionalidad" es difícil de detectar, por lo que nos enfocamos en el modelo **Holt**.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Paso 3.1: Entrenar el modelo
# trend='add' asume una tendencia lineal aditiva (crece/decrece constantemente)
# seasonal=None porque con 1 año no hay ciclos repetidos claros para validar
modelo_hw = ExponentialSmoothing(
    data_series,
    trend='add',
    seasonal=None,
    initialization_method="estimated"
).fit()

# Paso 3.2: Pronosticar
# Predecir las próximas 4 semanas (aprox. 1 mes, ej: Febrero 2026)
prediccion_hw = modelo_hw.forecast(steps=4)

print("Pronóstico Holt-Winters (Próximas 4 semanas):")
print(prediccion_hw)
```

---

## 4. Método 2: Regresión Lineal (Tendencia Pura)

Dibuja una línea recta basada en la historia completa. Útil para ver la dirección general a largo plazo.

```python
from sklearn.linear_model import LinearRegression
import numpy as np

# Paso 4.1: Preparar variables X (tiempo) y y (ventas)
# Creamos una secuencia numérica para el tiempo: 0, 1, 2...
df_resampled['periodo_idx'] = np.arange(len(df_resampled))

X = df_resampled[['periodo_idx']] # Features
y = df_resampled['TOTAL']         # Target

# Paso 4.2: Entrenar
modelo_lr = LinearRegression()
modelo_lr.fit(X, y)

# Paso 4.3: Pronosticar futuro
# Crear índices para los siguientes 4 periodos
ultimo_idx = df_resampled['periodo_idx'].max()
periodos_futuros = np.array([[ultimo_idx + 1], [ultimo_idx + 2], [ultimo_idx + 3], [ultimo_idx + 4]])

prediccion_lr = modelo_lr.predict(periodos_futuros)

print("Pronóstico Regresión Lineal:")
print(prediccion_lr)
```

---

## 5. Visualización Comparativa

Cómo ver los resultados gráficamente dentro de Python o Streamlit/Looker.

```python
# Graficar Historia (asegúrate de tener matplotlib)
plt.figure(figsize=(10, 6))
plt.plot(data_series.index, data_series.values, label='Histórico Real', marker='o')

# Graficar Holt-Winters
# Necesitamos las fechas futuras para graficar
fechas_futuras = pd.date_range(start=data_series.index[-1], periods=5, freq='W-MON')[1:]
plt.plot(fechas_futuras, prediccion_hw, label='Pronóstico Holt-Winters', linestyle='--', color='orange')

# Graficar Regresión
plt.plot(fechas_futuras, prediccion_lr, label='Pronóstico Regresión', linestyle=':', color='green')

plt.title('Comparación de Pronósticos: Feb 2026')
plt.legend()
plt.show()
```

## 6. Integración con tu Proyecto (Próximos Pasos)

1.  **Limpiar datos**: Asegurar que `cerammix.py` elimine las filas sucias ('TOTAL', etc.) correctamente.
2.  **Generar el DataFrame "Forecast"**: Crear un nuevo DataFrame que contenga:
    - Columna `Fecha`: Fechas futuras.
    - Columna `Tipo`: 'Prediccion'.
    - Columna `Monto`: Valor predicho.
3.  **Unir**: Concatenar el histórico (marcado como `Tipo='Real'`) con el forecast.
4.  **Subir a Drive**: Guardar este dataset "aumentado" para que Looker Studio pueda mostrar líneas continuas (Real -> Predicción).
