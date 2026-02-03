import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de Estilo "White Neon"
st.set_page_config(page_title="Pacha Pro AI", layout="wide")

st.markdown("""
    <style>
    /* Fondo Blanco y Texto Oscuro */
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    
    /* Barra Lateral con Degradado Neón */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F2F6 100%);
        border-right: 3px solid #00F2FF;
    }
    
    /* Tarjetas y Contenedores con Glow Neón */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 2px solid #FF00E5;
        box-shadow: 0 0 10px #FF00E5;
        border-radius: 15px;
    }
    
    /* Botones Neón */
    .stButton>button {
        background: linear-gradient(90deg, #00F2FF, #FF00E5);
        color: white;
        border: none;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(255, 0, 229, 0.4);
    }
    
    /* Pestañas (Tabs) */
    button[data-baseweb="tab"] { color: #1E1E1E; }
    button[aria-selected="true"] { color: #FF00E5 !important; border-bottom-color: #FF00E5 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame({
        'Código': ['101', '102'],
        'Producto': ['Caramelos Arcor', 'Coca Cola'],
        'Costo ($)': [10, 800],
        'Margen (%)': [100, 40],
        'Stock': [100, 15]
    })

# 3. Asistente Pacha IA (Mejorado para ser más humano)
with st.sidebar:
    st.title("🤖 Asistente Pacha")
    user_input = st.text_input("¿En qué te ayudo hoy?", placeholder="Ej: Cambiá el costo de la coca a 900")
    
    if st.button("Enviar"):
        query = user_input.lower()
        inv = st.session_state.inventario
        updated = False
        
        # Lógica de acción natural
        for i, row in inv.iterrows():
            if row['Producto'].lower() in query:
                # Extraer el número de la frase
                nums = [int(s) for s in query.split() if s.isdigit()]
                if nums:
                    val = nums[0]
                    if "costo" in query or "precio" in query or "vale" in query:
                        st.session_state.inventario.at[i, 'Costo ($)'] = val
                        st.success(f"¡Entendido! Ya actualicé el costo de {row['Producto']} a ${val}. ¿Algo más?")
                        updated = True
                    elif "stock" in query or "cantidad" in query or "tengo" in query:
                        st.session_state.inventario.at[i, 'Stock'] = val
                        st.success(f"¡Listo! Ahora figuran {val} unidades de {row['Producto']} en el sistema.")
                        updated = True
        
        if not updated:
            st.info("Hola! Soy tu asistente. Decime qué producto querés modificar y el nuevo valor (ej: 'Stock de alfajor a 50').")
        else:
            st.balloons()
            st.rerun()

# 4. Interfaz Principal
st.title("Pacha Pro + AI Assistant")
inv_disp = st.session_state.inventario.copy()
inv_disp['Venta ($)'] = (inv_disp['Costo ($)'] * (1 + inv_disp['Margen (%)'] / 100)).round(0).astype(int)

c1, c2, c3 = st.columns(3)
c1.metric("📦 Productos", len(inv_disp))
c2.metric("💰 Valor Inventario", f"$ {(inv_disp['Costo ($)'] * inv_disp['Stock']).sum():,.0f}")
c3.metric("📈 Margen Promedio", f"{int(inv_disp['Margen (%)'].mean())}%")

tabs = st.tabs(["🛒 VENTAS", "📋 INVENTARIO", "👤 CLIENTES"])

with tabs[1]:
    st.subheader("Control de Stock")
    st.dataframe(inv_disp, use_container_width=True)
    with tabs[2]:
        st.subheader("Fiados")
        # (Aquí va el código de clientes anterior...)
        st.write("Gestión de deudas activa.")
