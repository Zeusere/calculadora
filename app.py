import streamlit as st
import time

st.set_page_config(page_title="Calculadora de Retribución", layout="centered")
st.title("📋 Calculadora Retributiva Paso a Paso")

# Inicializar estados
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'saldos_asesoramiento' not in st.session_state:
    st.session_state.saldos_asesoramiento = 0.0
if 'saldos_rto' not in st.session_state:
    st.session_state.saldos_rto = 0.0
if 'margen_pct' not in st.session_state:
    st.session_state.margen_pct = 0.0
if 'v1' not in st.session_state:
    st.session_state.v1 = "No"
if 'v2' not in st.session_state:
    st.session_state.v2 = "No"
if 'v3' not in st.session_state:
    st.session_state.v3 = "No"

# Estilos CSS para efecto tipo Typeform
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 1rem;
        padding: 0.75rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Paso 1: Introducción de saldos
if st.session_state.step == 1:
    st.subheader("Paso 1: Saldos Gestionados")
    st.session_state.saldos_asesoramiento = st.number_input("Saldos medios asesoramiento no independiente (€):", min_value=0.0, value=st.session_state.saldos_asesoramiento, step=100000.0)
    st.session_state.saldos_rto = st.number_input("Saldos medios servicio RTO (€):", min_value=0.0, value=st.session_state.saldos_rto, step=100000.0)
    if st.button("Siguiente ➡️"):
        st.session_state.step = 2
        time.sleep(0.3)
        st.experimental_rerun()

# Paso 2: Margen de MAPFRE
elif st.session_state.step == 2:
    st.subheader("Paso 2: Margen de MAPFRE")
    st.session_state.margen_pct = st.number_input("Margen neto aplicado por MAPFRE (%):", min_value=0.0, value=st.session_state.margen_pct, step=0.1)
    if st.button("⬅️ Volver"):
        st.session_state.step = 1
        time.sleep(0.3)
        st.experimental_rerun()
    if st.button("Siguiente ➡️"):
        st.session_state.step = 3
        time.sleep(0.3)
        st.experimental_rerun()

# Paso 3: Variables Cuantitativas
elif st.session_state.step == 3:
    st.subheader("Paso 3: Cumplimiento de Variables Cuantitativas")
    st.session_state.v1 = st.selectbox("¿Saldos medios 2024 ≥ 3.000.000 €?", ["No", "Sí"], index=1 if st.session_state.v1 == "Sí" else 0)
    st.session_state.v2 = st.selectbox("¿Cobertura ≥ 95% en criterios cualitativos?", ["No", "Sí"], index=1 if st.session_state.v2 == "Sí" else 0)
    st.session_state.v3 = st.selectbox("¿≥ 30 cuentas con saldo a cierre de 2024?", ["No", "Sí"], index=1 if st.session_state.v3 == "Sí" else 0)

    if st.button("⬅️ Volver"):
        st.session_state.step = 2
        time.sleep(0.3)
        st.experimental_rerun()
    if st.button("Calcular Retribución 💰"):
        st.session_state.step = 4
        time.sleep(0.3)
        st.experimental_rerun()

# Paso 4: Resultados
elif st.session_state.step == 4:
    v1 = st.session_state.v1
    v2 = st.session_state.v2
    v3 = st.session_state.v3

    suma_variables = int(v1 == "Sí") + int(v2 == "Sí") + int(v3 == "Sí")
    adicional_por_variables = {0: 0.00, 1: 0.0010, 2: 0.0040, 3: 0.0060}
    porcentaje_adicional = adicional_por_variables.get(suma_variables, 0.0)

    saldos_asesoramiento = st.session_state.saldos_asesoramiento
    saldos_rto = st.session_state.saldos_rto
    margen_pct = st.session_state.margen_pct

    margen_total = (margen_pct / 100) * (saldos_asesoramiento + saldos_rto)
    comision_maxima = 0.75 * margen_total

    retrib_asesoramiento = saldos_asesoramiento * (0.0030 + porcentaje_adicional)
    retrib_rto = saldos_rto * 0.0020
    retrib_total_cuantitativa = retrib_asesoramiento + retrib_rto

    retribucion_total = min(retrib_total_cuantitativa, comision_maxima)
    retrib_cualitativa = (retrib_total_cuantitativa * 0.30) / 0.70
    retrib_cualitativa = min(retrib_cualitativa, comision_maxima - retribucion_total)

    retribucion_final = retribucion_total + retrib_cualitativa

    st.success("🎉 Resultado de la Retribución")
    st.markdown(f"**Saldos asesoramiento:** {saldos_asesoramiento:,.2f} €  ")
    st.markdown(f"**Saldos RTO:** {saldos_rto:,.2f} €  ")
    st.markdown(f"**Margen MAPFRE:** {margen_pct}%  ")
    st.markdown(f"**Variables cuantitativas cumplidas:** {suma_variables}  ")
    st.divider()
    st.markdown(f"**➡️ Margen bruto de MAPFRE:** {margen_total:,.2f} €")
    st.markdown(f"**➡️ Límite 75% para el agente:** {comision_maxima:,.2f} €")
    st.markdown(f"**➡️ Retribución por asesoramiento:** {retrib_asesoramiento:,.2f} €")
    st.markdown(f"**➡️ Retribución por RTO:** {retrib_rto:,.2f} €")
    st.markdown(f"**➡️ Total cuantitativa (sin límite):** {retrib_total_cuantitativa:,.2f} €")
    st.markdown(f"**➡️ Total cuantitativa (con límite):** {retribucion_total:,.2f} €")
    st.markdown(f"**➡️ Retribución cualitativa estimada:** {retrib_cualitativa:,.2f} €")
    st.markdown(f"## 🏆 TOTAL A PERCIBIR: {retribucion_final:,.2f} €")

    if st.button("🔁 Volver al inicio"):
        st.session_state.step = 1
        st.experimental_rerun()
