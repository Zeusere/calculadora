import streamlit as st

st.set_page_config(page_title="Calculadora de Retribución", layout="centered")
st.title("💼 Calculadora de Retribución del Representante")

st.markdown("""
Esta herramienta te permite calcular la retribución anual de un representante 
según los saldos gestionados, el margen de la distribuidora y el cumplimiento de variables cualitativas.
""")

# Formulario dinámico con inputs
with st.form("formulario_retribucion"):
    st.header("Datos Cuantitativos")
    saldos_asesoramiento = st.number_input("Saldos medios asesoramiento no independiente (€):", min_value=0.0, value=7000000.0, step=100000.0)
    saldos_rto = st.number_input("Saldos medios servicio RTO (€):", min_value=0.0, value=3000000.0, step=100000.0)
    margen_pct = st.number_input("Margen de la distribuidora (%):", min_value=0.0, value=1.0, step=0.1)

    st.header("Variables Cuantitativas")
    v1 = st.selectbox("¿Variable 1 (saldos medios 2024 ≥ 3.000.000 €) cumplida?", ["No", "Sí"])
    v2 = st.selectbox("¿Variable 2 (cobertura ≥ 95%) cumplida?", ["No", "Sí"])
    v3 = st.selectbox("¿Variable 3 (≥ 30 cuentas con saldo a cierre de 2024) cumplida?", ["No", "Sí"])

    submit = st.form_submit_button("Calcular Retribución")

if submit:
    suma_variables = int(v1 == "Sí") + int(v2 == "Sí") + int(v3 == "Sí")
    adicional_por_variables = {0: 0.00, 1: 0.0010, 2: 0.0040, 3: 0.0060}
    porcentaje_adicional = adicional_por_variables.get(suma_variables, 0.0)

    margen_total = (margen_pct / 100) * (saldos_asesoramiento + saldos_rto)
    comision_maxima = 0.75 * margen_total

    retrib_asesoramiento = saldos_asesoramiento * (0.0030 + porcentaje_adicional)
    retrib_rto = saldos_rto * 0.0020
    retrib_total_cuantitativa = retrib_asesoramiento + retrib_rto

    retribucion_total = min(retrib_total_cuantitativa, comision_maxima)
    retrib_cualitativa = (retrib_total_cuantitativa * 0.30) / 0.70
    retrib_cualitativa = min(retrib_cualitativa, comision_maxima - retribucion_total)

    retribucion_final = retribucion_total + retrib_cualitativa

    st.success("\U0001F4B0 Resultado de la Retribución")
    st.write(f"**Margen bruto de la Distribuidora:** {margen_total:,.2f} €")
    st.write(f"**Límite 75% para el agente:** {comision_maxima:,.2f} €")
    st.write(f"**Retribución por asesoramiento:** {retrib_asesoramiento:,.2f} €")
    st.write(f"**Retribución por RTO:** {retrib_rto:,.2f} €")
    st.write(f"**Total cuantitativa (sin límite):** {retrib_total_cuantitativa:,.2f} €")
    st.write(f"**Total cuantitativa (con límite):** {retribucion_total:,.2f} €")
    st.write(f"**Retribución cualitativa estimada:** {retrib_cualitativa:,.2f} €")
    st.markdown(f"### \U0001F389 **TOTAL A PERCIBIR: {retribucion_final:,.2f} €**")
