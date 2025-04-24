import streamlit as st
import pandas as pd

st.set_page_config(page_title="¿Comprar o Alquilar?", layout="centered")
st.title("🏠 Comparador: ¿Comprar o Alquilar?")

st.markdown("""
Esta herramienta te ayuda a comparar el coste a largo plazo entre comprar una vivienda o seguir alquilando.
Ten en cuenta factores como precio, alquiler, crecimiento anual, hipoteca, revalorización...
""")

# Estilos
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

with st.form("comparador"):
    st.header("🔢 Introduce los datos")
    col1, col2 = st.columns(2)
    with col1:
        precio_vivienda = st.number_input("Precio de la vivienda (€):", value=250000, step=10000)
        ahorro = st.number_input("Ahorro inicial aportado (€):", value=50000, step=1000)
        interes_hipoteca = st.number_input("Interés hipotecario anual (%):", value=3.0, step=0.1)
    with col2:
        alquiler_mensual = st.number_input("Alquiler mensual actual (€):", value=900, step=50)
        incremento_alquiler = st.slider("% incremento anual del alquiler:", 0.0, 10.0, 2.0, step=0.1)
        anios = st.slider("Años de análisis:", 5, 40, 25)

    calcular = st.form_submit_button("Calcular 📊")

if calcular:
    hipoteca = precio_vivienda - ahorro
    meses = anios * 12
    interes_mensual = interes_hipoteca / 100 / 12

    if interes_mensual > 0:
        cuota_mensual = hipoteca * interes_mensual / (1 - (1 + interes_mensual)**(-meses))
    else:
        cuota_mensual = hipoteca / meses

    total_comprar = cuota_mensual * meses
    valor_futuro_inmueble = precio_vivienda * ((1 + 0.02) ** anios)
    valor_neto_comprar = valor_futuro_inmueble - total_comprar

    alquiler_total = 0
    alquiler_actual = alquiler_mensual
    alquiler_evolucion = []

    for anio in range(anios):
        total_anual = alquiler_actual * 12
        alquiler_total += total_anual
        alquiler_evolucion.append((anio + 1, alquiler_total, total_comprar / anios * (anio + 1)))
        alquiler_actual *= (1 + incremento_alquiler / 100)

    df = pd.DataFrame(alquiler_evolucion, columns=["Año", "Coste de Alquilar", "Coste de Comprar"])

    st.success("Resultado comparativo")
    st.markdown(f"**💸 Coste total de alquilar durante {anios} años:** {alquiler_total:,.2f} €")
    st.markdown(f"**🏠 Coste total de hipoteca (sin impuestos, seguros, etc):** {total_comprar:,.2f} €")
    st.markdown(f"**📈 Valor estimado de la vivienda tras {anios} años (2% anual):** {valor_futuro_inmueble:,.2f} €")
    st.markdown(f"**💼 Valor neto acumulado por compra (valor futuro - pagos):** {valor_neto_comprar:,.2f} €")

    st.line_chart(df.set_index("Año"))

    st.markdown("""
    ⚠️ Esta comparativa es estimativa. No incluye gastos de compra, impuestos, seguros, mantenimiento, ni beneficios por revalorización real futura.
    """)
