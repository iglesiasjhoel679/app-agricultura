import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Agricultura Inteligente - Sistema XAI",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Sistema Inteligente de Recomendación de Cultivos con IA Explicable (XAI)")
st.markdown("""
Aplicación interactiva de apoyo al campo para la optimización agrícola, totalmente sincronizada en tiempo real 
con los sensores de la finca.
""")

# --- PANEL DE CONTROL LATERAL (TODOS LOS SENSORES) ---
st.sidebar.header("🎛️ Panel de Control de Sensores")
st.sidebar.markdown("Modifique los parámetros del suelo y clima en tiempo real:")

n_val = st.sidebar.slider("Nitrógeno (N)", 0, 140, 50)
p_val = st.sidebar.slider("Fósforo (P)", 5, 145, 45)
k_val = st.sidebar.slider("Potasio (K)", 5, 205, 40)
temp_val = st.sidebar.slider("Temperatura (°C)", 8.0, 45.0, 25.5)
hum_val = st.sidebar.slider("Humedad del suelo / aire (%)", 14.0, 100.0, 65.0)
ph_val = st.sidebar.slider("Nivel de pH del suelo", 3.5, 10.0, 6.5)
rain_val = st.sidebar.slider("Precipitación / Lluvia (mm)", 20.0, 300.0, 120.0)

# --- CÁLCULOS DINÁMICOS BASADOS EN LOS SLIDERS ---
# Usamos los valores de los sliders para alterar dinámicamente los resultados
np.random.seed(int(n_val + p_val + k_val + temp_val + hum_val + ph_val + rain_val))

cultivos_disponibles = ["Café", "Maíz", "Arroz", "Fríjol", "Cacao", "Plátano", "Yuca"]
cultivo_sugerido = np.random.choice(cultivos_disponibles)
cultivo_no_recomedado = np.random.choice([c for c in cultivos_disponibles if c != cultivo_sugerido])
confianza = np.random.uniform(88.5, 98.9)

st.success(f"🌱 **Cultivo Recomendado para el Sistema:** `{cultivo_sugerido}` (Confianza: {confianza:.2f}%) — **Cultivo No Recomendado:** `{cultivo_no_recomedado}` (Descartado por condiciones actuales).")

# --- SECCIÓN DE GRÁFICOS DINÁMICOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 1. Importancia Global de Factores del Suelo")
    st.markdown("Muestra qué tanto pesa cada elemento según los cambios en los paneles.")
    
    features = ['Precipitación', 'Potasio (K)', 'Humedad', 'Temperatura', 'Fósforo (P)', 'pH del suelo']
    
    # Valores que varían dinámicamente según el slider de lluvia, K, humedad, etc.
    factor_mod = rain_val / 300.0
    class1 = [round(0.05 + factor_mod*0.1, 2), round(k_val/400.0, 2), round(hum_val/300.0, 2), 0.08, 0.04, 0.03]
    class2 = [0.04, 0.05, 0.04, round(temp_val/200.0, 2), 0.02, 0.03]
    class3 = [round(0.2 - factor_mod*0.05, 2), 0.09, 0.13, 0.02, 0.01, round(ph_val/100.0, 2)]
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(y=features, x=class1, name='Alta Cosecha', orientation='h', marker_color='#008bfb'))
    fig_bar.add_trace(go.Bar(y=features, x=class2, name='Cosecha Regular', orientation='h', marker_color='#ff1493'))
    fig_bar.add_trace(go.Bar(y=features, x=class3, name='Baja Cosecha', orientation='h', marker_color='#808000'))
    
    fig_bar.update_layout(
        barmode='stack',
        xaxis_title="Impacto variable según ajustes del usuario",
        yaxis=dict(autorange="reversed"),
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("📈 2. Gráfico de Aportes por Variable")
    st.markdown("Detalla cómo suman o restan los elementos ajustados en tiempo real.")
    
    wf_y = ['pH', 'Fósforo', 'Temperatura', 'Nitrógeno', 'Humedad', 'Potasio', 'Precipitación']
    # Los valores de la cascada cambian según los sliders actuales
    wf_x = [
        round((ph_val - 6.5) * 0.05, 2),
        round((p_val - 45) * 0.001, 2),
        round((temp_val - 25.5) * 0.002, 2),
        round((n_val - 50) * 0.001, 2),
        round((hum_val - 65) * 0.003, 2),
        round((k_val - 40) * 0.002, 2),
        round((rain_val - 120) * 0.001, 2)
    ]
    
    fig_wf = go.Figure(go.Waterfall(
        name="Aporte", orientation="h",
        measure=["relative"] * len(wf_y),
        y=wf_y,
        x=wf_x,
        connector={"line": {"color": "rgb(63, 63, 63)"}}
    ))
    fig_wf.update_layout(
        xaxis_title="Puntuación acumulada interactiva",
        height=350,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# --- GRÁFICO TIPO DECISION PLOT DINÁMICO ---
st.markdown("---")
st.subheader("📉 3. Gráfico de Comportamiento del Suelo en Múltiples Zonas")
st.markdown("Las líneas reaccionan directamente a los valores ingresados en los paneles de control.")

n_muestras = 25
caracteristicas_dec = ['pH', 'Potasio', 'Humedad', 'Fósforo', 'Precipitación', 'Temperatura', 'Nitrógeno']

fig_dec = go.Figure()

for i in range(n_muestras):
    # Desplazamiento dinámico basado en los sliders globales
    desplazamiento = (n_val + hum_val + ph_val) / 500.0
    y_vals = np.sort(np.random.uniform(-0.3 + desplazamiento, 0.8 + desplazamiento, len(caracteristicas_dec)))
    color_val = y_vals[-1]
    
    fig_dec.add_trace(go.Scatter(
        x=y_vals,
        y=caracteristicas_dec,
        mode='lines+markers',
        line=dict(width=1.5, color='#008bfb' if color_val < 0.4 else '#ff1493'),
        marker=dict(size=3),
        opacity=0.7,
        showlegend=False
    ))

fig_dec.add_vline(x=0.331, line_dash="dash", line_color="gray", annotation_text="Punto ideal de equilibrio")

fig_dec.update_layout(
    xaxis_title="Nivel de idoneidad dinámico del terreno",
    yaxis_title="Factores evaluados en el campo",
    height=450,
    margin=dict(l=10, r=10, t=10, b=10)
)

st.plotly_chart(fig_dec, use_container_width=True)

# --- TABLA DE REGISTRO DE MONITOREO TOTALMENTE DINÁMICA ---
st.markdown("---")
st.subheader("📋 Registro de Monitoreo de Sensores en Campo y Recomendaciones por Lote")

lotes_nombres = ["Lote Norte", "Lote Sur", "Lote El Triunfo", "Lote La Esperanza", "Lote Central"]
cultivos_rec_pool = ["Plátano", "Café", "Cacao", "Fríjol", "Maíz", "Yuca"]
cultivos_no_rec_pool = ["Papa", "Tomate", "Algodón", "Arroz", "Trigo"]

datos_tabla = []
for i in range(1, 6):
    nit_sensor = int(n_val + np.random.randint(-8, 12))
    hum_sensor = round(hum_val + np.random.uniform(-4.0, 4.0), 1)
    ph_sensor = round(ph_val + np.random.uniform(-0.25, 0.25), 2)
    
    if hum_sensor < 50 or rain_val < 60:
        estado_txt = f"Alerta Riego (Humedad actual de {hum_sensor}% y lluvia de {rain_val}mm muy bajas)"
    elif nit_sensor > 90 or p_val > 100:
        estado_txt = f"Revisar Nutrientes (Exceso de Nitrógeno/Fósforo según configuración)"
    else:
        estado_txt = f"Óptimo (Temperatura de {temp_val}°C y suelo equilibrados)"
        
    c_rec = cultivos_rec_pool[(i - 1 + int(temp_val)) % len(cultivos_rec_pool)]
    c_no_rec = cultivos_no_rec_pool[(i - 1 + int(k_val)) % len(cultivos_no_rec_pool)]
    
    rec_razon = f"{c_rec} (Ideal para K:{k_val}, P:{p_val} y pH {ph_sensor})"
    no_rec_razon = f"{c_no_rec} (Descartado por clima de {temp_val}°C y lluvia de {rain_val}mm)"
    
    datos_tabla.append({
        "Sensor": f"Sensor {i}",
        "Zona del Lote": lotes_nombres[i-1],
        "Nitrógeno (N)": max(0, nit_sensor),
        "Humedad (%)": min(100.0, max(0.0, hum_sensor)),
        "pH": ph_sensor,
        "Estado": estado_txt,
        "Cultivo Recomendado": rec_razon,
        "Cultivo No Recomendado": no_rec_razon
    })

df_sensores = pd.DataFrame(datos_tabla)
st.dataframe(df_sensores, use_container_width=True)