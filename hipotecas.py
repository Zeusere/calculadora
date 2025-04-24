import streamlit as st

st.set_page_config(page_title="Simulador de Hipoteca", layout="centered")
st.title("🏠 Simulador de Hipoteca")

st.markdown("""
Calcula tu hipoteca estimada con este simulador. Ten en cuenta que al precio del inmueble se añade un 10% de impuestos.
""")

# Estilos para sliders y controles
st.markdown("""
<style>
    .stSlider > div[data-baseweb="slider"] {
        background: #d1e231;
    }
    .stButton > button {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 16px;
        font-weight: bold;
        background-color: #a61576;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #860c5f;
    }
</style>
""", unsafe_allow_html=True)

st.header("Detalles de tu hipoteca")

precio_inmueble = st.slider("💶 Precio del inmueble (€)", 50000, 1000000, 305000, step=10000)
ahorro = st.slider("💼 Ahorro aportado (€)", 0, precio_inmueble, 91500, step=1000)
plazo = st.slider("📆 Plazo en años", 5, 40, 30)

tipo_interes_fijo = st.radio("💡 Tipo de interés", ["Fijo", "Variable"], horizontal=True)
tipo_interes = st.number_input("% Tipo de interés anual", min_value=0.0, value=2.15, step=0.1)

if st.button("Calcular cuota mensual 💸"):
    precio_total = precio_inmueble * 1.10  # incluye el 10% de impuestos
    prestamo = precio_total - ahorro
    meses = plazo * 12
    interes_mensual = tipo_interes / 100 / 12

    if interes_mensual > 0:
        cuota_mensual = prestamo * interes_mensual / (1 - (1 + interes_mensual)**(-meses))
    else:
        cuota_mensual = prestamo / meses

    st.success("📊 Resultado de la simulación")
    st.write(f"**Precio total con impuestos:** {precio_total:,.2f} €")
    st.write(f"**Importe del préstamo:** {prestamo:,.2f} €")
    st.write(f"**Cuota mensual estimada:** {cuota_mensual:,.2f} € durante {meses} meses")

    st.markdown("""
    ⚠️ Esta simulación es orientativa. No incluye gastos notariales, seguros u otros costes asociados.
    """)
