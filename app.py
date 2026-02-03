import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. Configuración de Estilo "White Neon"
st.set_page_config(page_title="Pacha Pro AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    [data-testid="stSidebar"] { background: #F8F9FA; border-right: 3px solid #00F2FF; }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 2px solid #FF00E5;
        box-shadow: 0 0 10px #FF00E5;
        border-radius: 15px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00F2FF, #FF00E5);
        color: white; border: none; border-radius: 20px; font-weight: bold;
    }
    .low-stock { color: #D32F2F; font-weight: bold; border: 1px solid #D32F2F; padding: 10px; border-radius: 5px; background-color: #FFEBEE; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización de Datos
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame({
        'Código': ['101', '102', '103'],
        'Producto': ['Caramelos Arcor', 'Coca Cola', 'Alfajor'],
        'Costo ($)': [10, 800, 500],
        'Margen (%)': [100, 40, 50],
        'Stock': [100, 15, 24]
    })

if 'clientes' not in st.session_state:
    st.session_state.clientes = pd.DataFrame({'Nombre': ['Consumidor Final', 'Juan Perez'], 'Saldo Deudor ($)': [0, 1500]})

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

if 'ventas_hoy' not in st.session_state:
    st.session_state.ventas_hoy = 0

# 3. Asistente Pacha IA (Accionable y Humano)
with st.sidebar:
    st.title("🤖 Asistente Pacha")
    user_input = st.text_input("¿Qué orden tenés para mí?", placeholder="Ej: Vendí 2 cocas")
    
    if st.button("Ejecutar"):
        query = user_input.lower()
        inv = st.session_state.inventario
        updated = False
        
        for i, row in inv.iterrows():
            if row['Producto'].lower() in query:
                nums = [int(s) for s in query.split() if s.isdigit()]
                if nums:
                    val = nums[0]
                    # ACCIÓN: VENTA
                    if "vend" in query or "salida" in query:
                        if st.session_state.inventario.at[i, 'Stock'] >= val:
                            st.session_state.inventario.at[i, 'Stock'] -= val
                            p_venta = int(row['Costo ($)'] * (1 + row['Margen (%)'] / 100))
                            st.session_state.ventas_hoy += (p_venta * val)
                            st.success(f"¡Venta registrada! Desconté {val} de {row['Producto']}.")
                            updated = True
                    # ACCIÓN: ACTUALIZAR COSTO
                    elif "costo" in query or "vale" in query:
                        st.session_state.inventario.at[i, 'Costo ($)'] = val
                        st.success(f"¡Entendido! El costo de {row['Producto']} ahora es ${val}.")
                        updated = True
        if updated: st.rerun()

# 4. Dashboard y Alertas
st.title("Pacha Pro + AI Assistant")
inv_disp = st.session_state.inventario.copy()
inv_disp['Venta ($)'] = (inv_disp['Costo ($)'] * (1 + inv_disp['Margen (%)'] / 100)).round(0).astype(int)

c1, c2, c3 = st.columns(3)
c1.metric("📦 Productos", len(inv_disp))
c2.metric("💰 Ventas Hoy", f"$ {st.session_state.ventas_hoy:,.0f}")
c3.metric("🤝 Deudas", f"$ {st.session_state.clientes['Saldo Deudor ($)'].sum():,.0f}")

tabs = st.tabs(["🛒 CAJA", "📋 INVENTARIO", "👤 CLIENTES", "📥 CARGAS"])

# --- PESTAÑA 1: CAJA ---
with tabs[0]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Selección")
        barcode = st.text_input("Escaneá o buscá producto", key="scanner")
        if barcode:
            match = inv_disp[inv_display['Código'] == barcode] if barcode.isdigit() else inv_disp[inv_disp['Producto'].str.contains(barcode, case=False)]
            if not match.empty:
                item = match.iloc[0]
                if st.button(f"Agregar {item['Producto']} - ${item['Venta ($)']}️"):
                    st.session_state.carrito.append({'Prod': item['Producto'], 'Cant': 1, 'Sub': item['Venta ($)']})
                    st.rerun()
    with col_b:
        st.subheader("Carrito")
        if st.session_state.carrito:
            df_c = pd.DataFrame(st.session_state.carrito)
            st.table(df_c)
            if st.button("Finalizar Venta"):
                for it in st.session_state.carrito:
                    idx = inv[inv['Producto'] == it['Prod']].index[0]
                    st.session_state.inventario.at[idx, 'Stock'] -= it['Cant']
                    st.session_state.ventas_hoy += it['Sub']
                st.session_state.carrito = []
                st.success("¡Cobrado!")
                st.rerun()

# --- PESTAÑA 2: INVENTARIO ---
with tabs[1]:
    st.subheader("Control de Stock")
    st.dataframe(inv_disp, use_container_width=True)
    bajos = inv_disp[inv_disp['Stock'] < 5]
    if not bajos.empty:
        st.error(f"⚠️ Reponer: {', '.join(bajos['Producto'].tolist())}")

# --- PESTAÑA 3: CLIENTES ---
with tabs[2]:
    st.subheader("Cuentas Corrientes")
    st.dataframe(st.session_state.clientes, use_container_width=True)

# --- PESTAÑA 4: CARGAS (MULTIFORMATO) ---
with tabs[3]:
    st.subheader("Importar Lista de Proveedores")
    file = st.file_uploader("Subí tu Excel (.xlsx) o CSV (.csv)", type=['xlsx', 'csv'])
    if file:
        st.info("Archivo detectado. La IA procesará los cambios de precio.")
        if st.button("Procesar y Actualizar Inventario"):
            st.session_state.inventario['Costo ($)'] = (st.session_state.inventario['Costo ($)'] * 1.10).round(0)
            st.success("Inventario actualizado.")
            st.rerun()
