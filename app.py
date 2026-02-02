import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión de Kiosco IA", layout="wide")

st.title("🏪 Sistema de Gestión Multirubro")
st.subheader("Control de Stock y Precios Inteligente")

# 1. Base de datos interna (Lo que ya tenemos)
if 'inventario' not in st.session_state:
    data = {
        'Código': ['7790123456789', '7790987654321', '7791122334455', '7795544332211'],
        'Producto': ['Alfajor de Chocolate', 'Gaseosa Cola 500ml', 'Galletitas Saladas', 'Encendedor'],
        'Costo Anterior ($)': [500.0, 800.0, 400.0, 300.0],
        'Margen (%)': [50, 40, 60, 100],
        'Stock': [24, 12, 30, 10]
    }
    st.session_state.inventario = pd.DataFrame(data)

inv = st.session_state.inventario

# 2. Interfaz Principal
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 📋 Inventario Actual")
    # Calculamos precio de venta actual
    inv['Precio Venta ($)'] = inv['Costo Anterior ($)'] * (1 + inv['Margen (%)'] / 100)
    st.dataframe(inv, use_container_width=True)

with col2:
    st.write("### 📤 Cargar Lista de Proveedor")
    archivo = st.file_uploader("Subí el Excel nuevo", type=['xlsx', 'csv'])

# 3. Lógica de Comparación (La magia)
if archivo:
    st.divider()
    st.warning("⚠️ Se detectaron cambios en la lista del proveedor")
    
    # Simulamos que el Excel subido tiene costos nuevos (un 10% más caros)
    nuevos_costos = inv[['Código', 'Producto']].copy()
    nuevos_costos['Nuevo Costo ($)'] = inv['Costo Anterior ($)'] * 1.10
    
    st.write("### 📉 Comparativa de Aumentos")
    comparativa = pd.merge(inv, nuevos_costos, on=['Código', 'Producto'])
    comparativa['Nuevo Precio Venta ($)'] = comparativa['Nuevo Costo ($)'] * (1 + comparativa['Margen (%)'] / 100)
    
    # Mostramos solo lo relevante para el dueño del kiosco
    st.table(comparativa[['Producto', 'Costo Anterior ($)', 'Nuevo Costo ($)', 'Nuevo Precio Venta ($)']])
    
    if st.button("✅ Aplicar todos los aumentos"):
        st.session_state.inventario['Costo Anterior ($)'] = nuevos_costos['Nuevo Costo ($)']
        st.success("¡Precios actualizados con éxito!")
        st.rerun()
