import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Pacha Gestión Pro", layout="wide")

# 2. CSS para diseño limpio y profesional (Fondo claro)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    div[data-testid="stMetric"] {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 15px;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏪 Pacha Gestión Pro")
st.write("Administración eficiente para tu negocio")

# 3. Base de datos con precios redondeados (sin decimales)
if 'inventario' not in st.session_state:
    data = {
        'Código': ['7790123456789', '7790987654321', '7791122334455', '7795544332211'],
        'Producto': ['Alfajor de Chocolate', 'Gaseosa Cola 500ml', 'Galletitas Saladas', 'Encendedor'],
        'Costo ($)': [500, 800, 400, 300],
        'Margen (%)': [50, 40, 60, 100],
        'Stock': [24, 12, 30, 10]
    }
    st.session_state.inventario = pd.DataFrame(data)

# Procesar datos para visualización limpia
df = st.session_state.inventario.copy()
df['Costo ($)'] = df['Costo ($)'].astype(int)
df['Precio Venta ($)'] = (df['Costo ($)'] * (1 + df['Margen (%)'] / 100)).round(0).astype(int)

# 4. Dashboard de métricas
col1, col2, col3 = st.columns(3)
col1.metric("📦 Productos", f"{len(df)}")
col2.metric("💰 Capital en Stock", f"$ {(df['Costo ($)'] * df['Stock']).sum():,.0f}")
col3.metric("📈 Margen Promedio", f"{int(df['Margen (%)'].mean())}%")

st.divider()

# 5. Pestañas
tab1, tab2, tab3 = st.tabs(["📋 Inventario", "📥 Cargar Lista", "👥 Clientes"])

with tab1:
    st.write("### Stock Actual")
    st.dataframe(df.style.format({
        'Costo ($)': '${:,.0f}',
        'Precio Venta ($)': '${:,.0f}',
        'Margen (%)': '{}%'
    }), use_container_width=True)

with tab2:
    st.subheader("Actualizar por Proveedor")
    archivo = st.file_uploader("Subí tu Excel de precios", type=['xlsx', 'csv'])
    
    if archivo:
        # Simulamos detección de aumento (ej. 20%)
        df_update = df.copy()
        df_update['Nuevo Costo'] = (df_update['Costo ($)'] * 1.20).round(0).astype(int)
        df_update['Nuevo Precio'] = (df_update['Nuevo Costo'] * (1 + df_update['Margen (%)'] / 100)).round(0).astype(int)
        
        st.write("#### Comparativa de Nuevos Precios")
        st.table(df_update[['Producto', 'Costo ($)', 'Nuevo Costo', 'Nuevo Precio']])
        
        if st.button("Actualizar Todo el Sistema"):
            st.session_state.inventario['Costo ($)'] = df_update['Nuevo Costo']
            st.success("¡Precios actualizados!")
            st.rerun()

with tab3:
    st.write("### Control de Cuentas Corrientes")
    st.info("Aquí vamos a programar el sistema de 'Fiados' para que puedas anotar quién debe plata.")
    
    if st.button("✅ Aplicar todos los aumentos"):
        st.session_state.inventario['Costo Anterior ($)'] = nuevos_costos['Nuevo Costo ($)']
        st.success("¡Precios actualizados con éxito!")
        st.rerun()
