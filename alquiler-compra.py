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
    summary {
        font-weight: bold;
        margin-top: 1rem;
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

    tasa_inversion = st.slider("Rentabilidad esperada del ahorro si alquilas (% anual):", 0.0, 15.0, 2.0, step=0.1)
    calcular = st.form_submit_button("Calcular 📊")

if calcular:
    hipoteca = precio_vivienda - ahorro
    meses = anios * 12
    interes_mensual = interes_hipoteca / 100 / 12

    if interes_mensual > 0:
        cuota_mensual = hipoteca * interes_mensual / (1 - (1 + interes_mensual)**(-meses))
    else:
        cuota_mensual = hipoteca / meses

    alquiler_total = 0
    alquiler_actual = alquiler_mensual

    hipoteca_acumulada = 0
    valor_vivienda = precio_vivienda
    valor_neto_acumulado = []

    ahorro_invertido = ahorro
    tasa_inversion /= 100

    for anio in range(1, anios + 1):
        total_anual_alquiler = alquiler_actual * 12
        alquiler_total += total_anual_alquiler
        alquiler_actual *= (1 + incremento_alquiler / 100)

        hipoteca_acumulada += cuota_mensual * 12
        valor_vivienda *= (1 + 0.02)
        ahorro_invertido *= (1 + tasa_inversion)

        valor_neto = valor_vivienda - hipoteca_acumulada
        riqueza_alquilar = ahorro_invertido - alquiler_total

        valor_neto_acumulado.append((anio, alquiler_total, hipoteca_acumulada, valor_vivienda, valor_neto, ahorro_invertido, riqueza_alquilar))

    df = pd.DataFrame(valor_neto_acumulado, columns=["Año", "Coste de Alquilar", "Pagado en Hipoteca", "Valor Vivienda", "Valor Neto Compra", "Ahorro Invertido Alquilando", "Riqueza Alquilando"])

    st.success("Resultado comparativo")
    st.markdown(f"**💸 Coste total de alquilar durante {anios} años:** {alquiler_total:,.2f} €")
    st.markdown(f"**💰 Pagos totales de hipoteca en {anios} años:** {hipoteca_acumulada:,.2f} €")
    st.markdown(f"**📈 Valor estimado de la vivienda tras {anios} años (2% anual):** {valor_vivienda:,.2f} €")
    st.markdown(f"**💼 Valor neto acumulado por compra (valor - pagos):** {df.iloc[-1]['Valor Neto Compra']:,.2f} €")
    st.markdown(f"**📊 Valor del ahorro invertido si se alquila:** {df.iloc[-1]['Ahorro Invertido Alquilando']:,.2f} €")
    st.markdown(f"**🧮 Riqueza neta alquilando (ahorro - alquiler):** {df.iloc[-1]['Riqueza Alquilando']:,.2f} €")

    chart_df = df.set_index("Año")[["Valor Neto Compra", "Riqueza Alquilando"]]
    st.line_chart(chart_df)

    riqueza_comprar = df.iloc[-1]['Valor Neto Compra']
    riqueza_alquilar = df.iloc[-1]['Riqueza Alquilando']

    if riqueza_comprar > riqueza_alquilar:
        st.success("✅ Según estos datos, **comprar** parece más rentable a largo plazo que alquilar, considerando la rentabilidad del ahorro.")
    else:
        st.warning("⚠️ Según estos datos, **alquilar** podría ser más rentable que comprar, considerando la rentabilidad del ahorro disponible.")

    st.markdown("""
    ⚠️ Esta comparativa es estimativa. No incluye gastos de compra, impuestos, seguros, mantenimiento, ni beneficios por revalorización real futura.
    """)

    st.subheader("📋 Tabla resumen de resultados año a año")
    st.dataframe(df.style.format("{:.2f}"))

    st.subheader("❓ Preguntas frecuentes sobre esta simulación")
    with st.expander("¿Qué es 'Valor Neto Compra'?"):
        st.markdown("Es la diferencia entre el valor estimado de la vivienda en el futuro y el total pagado en cuotas de hipoteca. Representa el patrimonio acumulado al comprar.")

    with st.expander("¿Qué significa 'Riqueza Alquilando'?"):
        st.markdown("Es el resultado de invertir el ahorro inicial y restar todos los pagos de alquiler. Representa el patrimonio neto acumulado si decides alquilar.")

    with st.expander("¿Por qué se descuenta el ahorro inicial en el caso de compra?"):
        st.markdown("Ese dinero deja de estar disponible (liquidez) porque se utiliza como entrada. Se incorpora en el valor de la vivienda, pero ya no puede invertirse como en el caso de alquilar.")

    with st.expander("¿Puedo confiar en esta simulación?"):
        st.markdown("Esta herramienta está basada en cálculos matemáticos estándar, pero **no sustituye asesoramiento financiero profesional**. Considera esta simulación como una orientación inicial para tomar decisiones.")

