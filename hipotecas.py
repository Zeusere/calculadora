import streamlit as st

st.set_page_config(page_title="Simulador de Hipoteca", layout="centered")
st.title("🏠 Simulador de Hipoteca")

st.markdown("""
Simula tu cuota mensual de hipoteca teniendo en cuenta tu ahorro, el precio de la vivienda y el tipo de interés.
El simulador añade automáticamente un 10% al precio del inmueble por los impuestos aproximados de compra en España.
""")

# Estilo uniforme y elegante
st.markdown("""
<style>
    .stSlider > div[data-baseweb="slider"] {
        background: none !important;
    }
    .stButton > button {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 16px;
        font-weight: bold;
        background-color: #0066cc;
        color: white;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #004a99;
    }
    input[type=number] {
        padding: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.header("Introduce los datos de tu hipoteca")

col1, col2 = st.columns(2)
with col1:
    precio_inmueble = st.number_input("💶 Precio del inmueble (€):", min_value=50000, max_value=2000000, value=305000, step=5000)
with col2:
    ahorro = st.number_input("💼 Ahorro aportado (€):", min_value=0, max_value=precio_inmueble, value=91500, step=1000)

plazo = st.slider("📆 Plazo en años:", min_value=5, max_value=40, value=30)

st.subheader("Tipo de interés")
tipo_interes_opcion = st.radio("Tipo de interés:", ["Fijo", "Variable"], horizontal=True)
tipo_interes = st.number_input("% Tipo de interés anual:", min_value=0.0, value=2.15, step=0.1)

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
    st.markdown(f"**🏡 Precio total del inmueble con impuestos:** {precio_total:,.2f} €")
    st.markdown(f"**💰 Importe financiado (hipoteca):** {prestamo:,.2f} €")
    st.markdown(f"**📆 Plazo:** {plazo} años ({meses} meses)")
    st.markdown(f"**💸 Cuota mensual estimada:** {cuota_mensual:,.2f} €")

    st.markdown("""
    ⚠️ Esta simulación es orientativa. No incluye gastos notariales, seguros u otros costes asociados. Consulta siempre con tu entidad financiera.
    """)
