import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Simulador de Café", page_icon="☕", layout="wide")

# Estilo personalizado
st.markdown("""
    <style>
    .main { background-color: #FFF8F0; }
    .stMetric { background-color: #6F4E37; color: white; border-radius: 10px; padding: 10px; }
    .stMetric label { color: #FFD59E !important; }
    .stMetric div { color: white !important; }
    h1, h2, h3 { color: #6F4E37; }
    .stButton>button { background-color: #6F4E37; color: white; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Logo y título
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.image("logo.png", width=80)
with col_titulo:
    st.title("☕ Simulador de Compra y Venta de Café")
    st.caption("Calcula tu rentabilidad por cliente de forma rápida y precisa")

st.divider()

# Configuración general
st.subheader("⚙️ Configuración general")
col1, col2 = st.columns(2)
with col1:
    precio_compra = st.number_input("Precio compra ($/kg)", min_value=0, max_value=10000, value=95, step=1)
    maquila = st.number_input("Maquila ($/kg)", min_value=0, max_value=1000, value=7, step=1)
with col2:
    merma1 = st.slider("Merma moreteado", 0.0, 0.5, 0.24, step=0.01)
    merma2 = st.slider("Merma selección", 0.0, 0.3, 0.10, step=0.01)
    merma3 = st.slider("Merma selección electrónica", 0.0, 0.3, 0.05, step=0.01)

st.divider()

# Clientes
st.subheader("👥 Clientes")
num_clientes = st.number_input("Número de clientes", min_value=1, max_value=20, value=2, step=1)

clientes = []
cols = st.columns(min(num_clientes, 3))
for i in range(num_clientes):
    with cols[i % 3]:
        st.markdown(f"**Cliente {i+1}**")
        nombre = st.text_input("Nombre", value=f"Cliente {i+1}", key=f"nombre_{i}")
        kilos = st.number_input("Kilos a entregar", min_value=0, max_value=100000, value=500, step=1, key=f"kilos_{i}")
        precio = st.number_input("Precio venta ($/kg)", min_value=0, max_value=500, value=180, step=1, key=f"precio_{i}")
        clientes.append({"nombre": nombre, "kilos": kilos, "precio": precio})

st.divider()

# Cálculos
rendimiento = (1 - merma1) * (1 - merma2) * (1 - merma3)

rows = []
for c in clientes:
    kilos_compra  = c["kilos"] / rendimiento if rendimiento > 0 else 0
    costo_compra  = kilos_compra * precio_compra
    costo_maquila = kilos_compra * maquila
    costo_total   = costo_compra + costo_maquila
    ingresos      = c["kilos"] * c["precio"]
    utilidad      = ingresos - costo_total
    margen        = utilidad / ingresos if ingresos > 0 else 0
    rows.append({
        "Cliente":                     c["nombre"],
        "Kilos a entregar":            c["kilos"],
        "Precio venta":                c["precio"],
        "Precio compra":               precio_compra,
        "Maquila":                     maquila,
        "Merma moreteado":             merma1,
        "Merma selección":             merma2,
        "Merma selección electrónica": merma3,
        "Factor rendimiento":          round(rendimiento, 4),
        "Kilos a comprar":             round(kilos_compra, 4),
        "Costo compra":                round(costo_compra, 2),
        "Costo maquila":               round(costo_maquila, 2),
        "Costo total":                 round(costo_total, 2),
        "Ingresos":                    round(ingresos, 2),
        "Utilidad":                    round(utilidad, 2),
        "Margen %":                    round(margen * 100, 4),
    })

# Totales
ingresos_total = sum(r["Ingresos"] for r in rows)
utilidad_total = sum(r["Utilidad"] for r in rows)
margen_total   = utilidad_total / ingresos_total * 100 if ingresos_total > 0 else 0

# Resultados generales
st.subheader("📊 Resultados generales")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Kilos totales",    f"{sum(r['Kilos a entregar'] for r in rows):,}")
col2.metric("Ingresos totales", f"${ingresos_total:,.2f}")
col3.metric("Utilidad total",   f"${utilidad_total:,.2f}")
col4.metric("Margen promedio",  f"{round(margen_total, 2)}%")

st.divider()

# Tabla detalle
st.subheader("📋 Detalle por cliente")
df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)

st.divider()

# Exportar a Excel
st.subheader("📥 Exportar resultados")
buffer = io.BytesIO()
df.to_excel(buffer, index=False, sheet_name="Simulador Café")
buffer.seek(0)
st.download_button(
    label="⬇️ Descargar Excel",
    data=buffer,
    file_name="simulador_cafe.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()
st.caption("Desarrollado por Landysh Ziyatdinova")
