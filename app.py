import streamlit as st
import pandas as pd

st.title("Simulador de Café")

num_clientes = st.number_input("Número de clientes", min_value=1, max_value=10, value=2, step=1)

clientes = []
for i in range(num_clientes):
    st.markdown(f"**Cliente {i+1}**")
    nombre = st.text_input(f"Nombre cliente {i+1}", value=f"Cliente {i+1}", key=f"nombre_{i}")
    kilos = st.number_input(f"Kilos {nombre}", min_value=0, max_value=10000, value=500, step=1, key=f"kilos_{i}")
    precio = st.number_input(f"Precio venta {nombre}", min_value=0, max_value=500, value=180, step=1, key=f"precio_{i}")
    clientes.append({
        "nombre": nombre,
        "kilos": kilos,
        "precio": precio
    })

st.divider()

precio_compra = st.number_input("Precio compra ($/kg)", min_value=0, max_value=10000, value=95, step=1)
maquila = st.number_input("Maquila ($/kg)", min_value=0, max_value=1000, value=7, step=1)
merma1 = st.slider("Merma moreteado", 0.0, 0.5, 0.24)
merma2 = st.slider("Merma selección", 0.0, 0.3, 0.10)

# Cálculos
rendimiento = (1 - merma1) * (1 - merma2)
kilos_total = sum(c["kilos"] for c in clientes)
ingresos_total = sum(c["kilos"] * c["precio"] for c in clientes)
kilos_compra = kilos_total / rendimiento if rendimiento > 0 else 0
costo_total = kilos_compra * (precio_compra + maquila)
utilidad = ingresos_total - costo_total
margen = utilidad / ingresos_total if ingresos_total > 0 else 0

# Resultados
st.subheader("Resultados")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Kilos totales", f"{kilos_total:,}")
col2.metric("Ingresos", f"${ingresos_total:,.2f}")
col3.metric("Utilidad", f"${utilidad:,.2f}")
col4.metric("Margen", f"{round(margen * 100, 2)}%")

# Detalle por cliente
st.subheader("Detalle por cliente")
df = pd.DataFrame(clientes)
df["ingresos"] = df["kilos"] * df["precio"]
df.columns = ["Nombre", "Kilos", "Precio unitario", "Ingresos"]
st.dataframe(df, use_container_width=True)
