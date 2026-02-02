import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión de Kiosco IA", layout="wide")

st.title("🏪 Sistema de Gestión Multirubro")
st.subheader("Control de Stock y Precios Inteligente")

# Datos de ejemplo que definimos antes
data = {
    'Código': ['7790123456789', '7790987654321', '7791122334455', '7795544332211'],
    'Producto': ['Alfajor de Chocolate', 'Gaseosa Cola 500ml', 'Galletitas Saladas', 'Encendedor'],
    'Costo ($)': [500.0, 800.0, 400.0, 300.0],
    'Margen (%)': [50, 40, 60, 100],
    'Stock': [24, 12, 30, 10]
}

df = pd.DataFrame(data)

# Calcular Precio de Venta automáticamente
df['Precio Venta ($)'] = df['Costo ($)'] * (1 + df['Margen (%)'] / 100)

# Interfaz de usuario
st.write("### Inventario Actual")
st.dataframe(df, use_container_width=True)

# Sección de Carga (Simulando lo que pediste en el audio)
st.divider()
st.write("### 📤 Actualizar Precios por Excel")
archivo = st.file_uploader("Subí el Excel de tu proveedor aquí", type=['xlsx', 'csv'])

if archivo:
    st.success("¡Archivo recibido! La IA está analizando los nuevos costos...")
    # Aquí irá la lógica de comparación que mencionamos
