import streamlit as st
import pandas as pd

# 1. Configuración de página con tema oscuro forzado
st.set_page_config(page_title="Pacha Pro Neon", layout="wide")

# 2. CSS para el estilo NEÓN e INNOVADOR
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp { background-color: #0E1117; color: #00FFC8; }
    
    /* Tarjetas de métricas con borde neón */
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #00FFC8;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 0 10px #00FFC8;
    }
    
    /* Estilo de los títulos */
    h1, h2, h3 { color: #00FFC8 !important; text-shadow: 0 0 15px #00FFC8; }
    
    /* Botones Neón */
    .stButton>button {
        background-color: transparent;
        color: #00FFC8;
        border: 2px solid #00FFC8;
        border-radius: 20px;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 0 5px #00FFC8;
    }
    .stButton>button:hover {
        background-color: #00FFC8;
        color: #0E1117;
        box-shadow: 0 0 20px #00FFC8;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ PACHA GESTIÓN NEÓN")
st.write("---")

# 3. Base de datos con redondeo forzado desde el inicio
if 'inventario' not in st.session_state:
    data = {
        'Código': ['7790123456789', '7790987654321', '7791122334455', '7795544332211'],
        'Producto': ['Alfajor de Chocolate', 'Gaseosa Cola 500ml', 'Galletitas Saladas', 'Encendedor'],
        'Costo ($)': [500, 800, 400, 300],
        'Margen (%)': [50, 40, 60, 100],
        'Stock': [24, 12, 30, 10]
    }
    st.session_state.inventario = pd.DataFrame(data)

# Procesamiento de datos sin decimales
df = st.session_state.inventario.copy()
df['Costo ($)'] = df['Costo ($)'].astype(int)
df['Precio Venta ($)'] = (df['Costo ($)'] * (1 + df['Margen (%)'] / 100)).round(0).astype(int)

# 4. Dashboard de métricas
col1, col2, col3 = st.columns(3)
col1.metric("📦 PRODUCTOS", f"{len(df)}")
col2.metric("💰 CAPITAL", f"$ {(df['Costo ($)'] * df['Stock']).sum():,.0f}")
col3.metric("📈 MARGEN", f"{int(df['Margen (%)'].mean())}%")

# 5. Pestañas de Navegación
tab1, tab2, tab3 = st.tabs(["💎 INVENTARIO", "🔋 ACTUALIZAR", "👤 CLIENTES (PRÓXIMAMENTE)"])

with tab1:
    st.write("### Stock Disponible")
    # Mostramos la tabla formateada para que no tenga puntos decimales
    st.dataframe(df.style.format({
        'Costo ($)': '${:,.0f}',
        'Precio Venta ($)': '${:,.0f}',
        'Margen (%)': '{}%'
    }), use_container_width=True)

with tab2:
    st.subheader("Subida de Listas de Proveedores")
    archivo = st.file_uploader("Arrastrá tu archivo aquí", type=['xlsx', 'csv'])
    
    if archivo:
        st.warning("🚀 IA: Calculando nuevos precios sin centavos...")
        # Simulamos un aumento del 20%
        df_update = df.copy()
        df_update['Nuevo Costo'] = (df_update['Costo ($)'] * 1.20).round(0).astype(int)
        df_update['Nuevo Precio'] = (df_update['Nuevo Costo'] * (1 + df_update['Margen (%)'] / 100)).round(0).astype(int)
        
        st.table(df_update[['Producto', 'Costo ($)', 'Nuevo Costo', 'Nuevo Precio']])
        
        if st.button("APLICAR CAMBIOS NEÓN"):
            st.session_state.inventario['Costo ($)'] = df_update['Nuevo Costo']
            st.balloons()
            st.rerun()
    
    if st.button("✅ Aplicar todos los aumentos"):
        st.session_state.inventario['Costo Anterior ($)'] = nuevos_costos['Nuevo Costo ($)']
        st.success("¡Precios actualizados con éxito!")
        st.rerun()
