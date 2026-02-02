import streamlit as st
import pandas as pd

# Configuración de página con estilo moderno
st.set_page_config(page_title="Pacha Gestion Pro", layout="wide", initial_sidebar_state="collapsed")

# CSS Personalizado para que se vea "Pro" e innovador
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #4CAF50; color: white; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #45a049; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Pacha Gestión Pro")
st.write("Sistema inteligente para el comercio moderno.")

# 1. Base de datos con precios redondeados
if 'inventario' not in st.session_state:
    data = {
        'Código': ['7790123456789', '7790987654321', '7791122334455', '7795544332211'],
        'Producto': ['Alfajor de Chocolate', 'Gaseosa Cola 500ml', 'Galletitas Saladas', 'Encendedor'],
        'Costo ($)': [500.0, 800.0, 400.0, 300.0],
        'Margen (%)': [50, 40, 60, 100],
        'Stock': [24, 12, 30, 10]
    }
    st.session_state.inventario = pd.DataFrame(data)

# Cálculos base
df = st.session_state.inventario.copy()
df['Precio Venta ($)'] = (df['Costo ($)'] * (1 + df['Margen (%)'] / 100)).round(0) # Redondeo a entero

# 2. Dashboard de indicadores (Innovador)
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("📦 Productos", len(df))
with col_b:
    valor_stock = (df['Costo ($)'] * df['Stock']).sum()
    st.metric("💰 Valor Stock (Costo)", f"$ {valor_stock:,.0f}")
with col_c:
    st.metric("🔥 Margen Promedio", f"{df['Margen (%)'].mean():.1f}%")

st.divider()

# 3. Interfaz de Gestión
tab1, tab2 = st.tabs(["📊 Inventario en Vivo", "📥 Carga de Listas"])

with tab1:
    st.write("### Vista General de Productos")
    # Tabla con diseño mejorado
    st.dataframe(df.style.format({
        "Costo ($)": "${:.0f}",
        "Precio Venta ($)": "${:.0f}",
        "Margen (%)": "{}%"
    }), use_container_width=True)

with tab2:
    st.subheader("Actualización Inteligente")
    col_file, col_info = st.columns([1, 1])
    
    with col_file:
        archivo = st.file_uploader("Arrastrá el Excel del proveedor", type=['xlsx', 'csv'])
    
    with col_info:
        st.info("La IA detectará automáticamente aumentos y mantendrá tus márgenes de ganancia intactos.")

    if archivo:
        # Simulamos detección de aumento para la demo
        st.warning("⚠️ Se detectó un aumento general del 15% en los costos.")
        df_new = df.copy()
        df_new['Nuevo Costo'] = (df_new['Costo ($)'] * 1.15).round(0)
        df_new['Nuevo Precio'] = (df_new['Nuevo Costo'] * (1 + df_new['Margen (%)'] / 100)).round(0)
        
        st.write("#### Comparativa de Precios")
        st.table(df_new[['Producto', 'Costo ($)', 'Nuevo Costo', 'Nuevo Precio']])
        
        if st.button("🔥 ACTUALIZAR TODOS LOS PRECIOS"):
            st.session_state.inventario['Costo ($)'] = df_new['Nuevo Costo']
            st.success("¡Precios actualizados y redondeados!")
            st.balloons()
            st.rerun()
    
    if st.button("✅ Aplicar todos los aumentos"):
        st.session_state.inventario['Costo Anterior ($)'] = nuevos_costos['Nuevo Costo ($)']
        st.success("¡Precios actualizados con éxito!")
        st.rerun()
