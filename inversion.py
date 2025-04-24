import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Inversiones", layout="centered")
st.title("📈 Simulador de Inversión a Largo Plazo")

st.markdown("""
Este simulador te permite visualizar cuánto podrías tener al final de tu inversión, 
eligiendo entre tres perfiles de riesgo: prudente, moderado o atrevido.
""")

# Estilos CSS para apariencia moderna
st.markdown("""
<style>
    .stButton>button {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 16px;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #004a99;
    }
</style>
""", unsafe_allow_html=True)

with st.form("form_inversion"):
    st.header("Datos de la inversión")
    aportacion_inicial = st.number_input("💰 Aportación inicial (€):", min_value=0.0, value=10000.0, step=500.0)
    aportacion_mensual = st.number_input("📆 Aportación mensual (€):", min_value=0.0, value=200.0, step=50.0)
    anos = st.slider("⏳ Años de inversión:", min_value=1, max_value=40, value=20)
    perfil = st.selectbox("📊 Perfil de inversión:", ["Prudente (3%)", "Moderado (6%)", "Atrevido (10%)"])
    simular = st.form_submit_button("Simular 🚀")

if simular:
    tasas = {"Prudente (3%)": 0.03, "Moderado (6%)": 0.06, "Atrevido (10%)": 0.10}
    tasa_anual = tasas[perfil]
    tasa_mensual = (1 + tasa_anual) ** (1 / 12) - 1

    total_invertido = aportacion_inicial
    total_no_invertido = aportacion_inicial
    datos = []

    for mes in range(anos * 12 + 1):
        datos.append((mes / 12, total_invertido, total_no_invertido))
        total_invertido = total_invertido * (1 + tasa_mensual) + aportacion_mensual
        total_no_invertido += aportacion_mensual

    df = pd.DataFrame(datos, columns=["Años", "Con inversión", "Sin inversión"])

    st.success("✅ Simulación completada")
    st.metric(label="Valor estimado al vencimiento con inversión", value=f"{df.iloc[-1]['Con inversión']:,.2f} €")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Años"], df["Con inversión"], label="Con inversión", linewidth=3)
    ax.plot(df["Años"], df["Sin inversión"], label="Sin inversión", linestyle="--", linewidth=2, color="gray")
    ax.set_ylabel("Valor acumulado (€)")
    ax.set_xlabel("Años")
    ax.set_title("Evolución del patrimonio")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("""
    Esta simulación es una estimación basada en rentabilidades constantes y no representa una garantía de rentabilidad futura. 
    Las inversiones están sujetas a riesgos.
    """)
