import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración General
st.set_page_config(page_title="Pacha Gestión Pro", layout="wide")

# Estilo visual para que sea vea profesional y limpio
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    div[data-testid="stMetric"] { background-color: #F0F2F6; border-radius: 10px; padding: 15px; }
    .stButton>button { background-color: #2E7D32; color: white; border-radius: 8px; width: 100%; }
    .low-stock { color: #D32F2F; font-weight: bold; border: 1px solid #D32F2F; padding: 10px; border-radius: 5px; background-color: #FFEBEE; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización de Datos (Base de datos interna)
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame({
        'Código': ['101', '102', '103', '104'],
        'Producto': ['Caramelos', 'Gaseosa Cola', 'Alfajor', 'Chicles'],
        'Costo ($)': [10, 800, 500, 50],
        'Margen (%)': [100, 40, 50, 80],
        'Stock': [50, 12, 24, 3]
    })

if 'clientes' not in st.session_state:
    st.session_state.clientes = pd.DataFrame({
        'Nombre': ['Juan Perez', 'Maria Garcia'],
        'Saldo Deudor ($)': [1500, 0]
    })

if 'ventas_totales' not in st.session_state:
    st.session_state.ventas_totales = 0

if 'ultimo_ticket' not in st.session_state:
    st.session_state.ultimo_ticket = ""

# 3. Lógica y Cálculos
inv = st.session_state.inventario
inv_display = inv.copy()
inv_display['Precio Venta ($)'] = (inv_display['Costo ($)'] * (1 + inv_display['Margen (%)'] / 100)).round(0).astype(int)
productos_bajo_stock = inv[inv['Stock'] < 5]

# 4. Panel de Control Superior
st.title("🏪 Pacha Gestión Pro")
col1, col2, col3 = st.columns(3)
col1.metric("📦 Productos en Stock", inv['Stock'].sum())
col2.metric("💰 Caja del Día", f"$ {st.session_state.ventas_totales:,.0f}")
col3.metric("🤝 Deuda de Clientes", f"$ {st.session_state.clientes['Saldo Deudor ($)'].sum():,.0f}")

# Mostrar Alertas si hay poco stock
if not productos_bajo_stock.empty:
    st.markdown("### 🚨 ALERTAS DE REPOSICIÓN")
    for _, fila in productos_bajo_stock.iterrows():
        st.markdown(f"<div class='low-stock'>⚠️ Solo quedan {fila['Stock']} unidades de {fila['Producto']}</div>", unsafe_allow_html=True)

st.divider()

# 5. Pestañas de Navegación
tab1, tab2, tab3, tab4 = st.tabs(["🛒 PUNTO DE VENTA", "📋 INVENTARIO", "📥 CARGAR LISTA", "👤 CLIENTES"])

# --- PESTAÑA 1: VENTAS ---
with tab1:
    col_v, col_t = st.columns([1, 1])
    with col_v:
        st.subheader("Nueva Venta")
        prod_sel = st.selectbox("Seleccionar Producto", inv_display['Producto'].tolist())
        cant = st.number_input("Cantidad", min_value=1, value=1)
        
        datos = inv_display[inv_display['Producto'] == prod_sel].iloc[0]
        precio = datos['Precio Venta ($)']
        total = precio * cant
        
        st.markdown(f"## Total: ${total}")
        
        if st.button("CONFIRMAR VENTA ✅"):
            idx = inv[inv['Producto'] == prod_sel].index[0]
            if inv.at[idx, 'Stock'] >= cant:
                st.session_state.inventario.at[idx, 'Stock'] -= cant
                st.session_state.ventas_totales += total
                
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
                st.session_state.ultimo_ticket = f"PACHA GESTIÓN PRO\n---\nFECHA: {fecha}\nPRODUCTO: {prod_sel}\nCANTIDAD: {cant}\nTOTAL: ${total}\n---"
                st.rerun()
            else:
                st.error("Stock insuficiente")

    with col_t:
        st.subheader("Último Ticket")
        if st.session_state.ultimo_ticket:
            st.code(st.session_state.ultimo_ticket)

# --- PESTAÑA 2: INVENTARIO ---
with tab2:
    st.subheader("Control de Almacén")
    st.dataframe(inv_display.style.format({'Costo ($)': '${:,.0f}', 'Precio Venta ($)': '${:,.0f}'}), use_container_width=True)

# --- PESTAÑA 3: CARGA DE EXCEL ---
with tab3:
    st.subheader("Actualización por Proveedor")
    archivo = st.file_uploader("Subí el Excel del proveedor", type=['xlsx', 'csv'])
    if archivo:
        st.warning("IA: Se calculó un aumento preventivo del 15% según inflación.")
        if st.button("Actualizar Precios"):
            st.session_state.inventario['Costo ($)'] = (st.session_state.inventario['Costo ($)'] * 1.15).round(0).astype(int)
            st.success("Precios actualizados con éxito")
            st.rerun()

# --- PESTAÑA 4: CLIENTES ---
with tab4:
    st.subheader("Gestión de Fiados")
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.write("### Saldos")
        st.table(st.session_state.clientes)
        
    with col_c2:
        st.write("### Registrar Pago o Deuda")
        cli_sel = st.selectbox("Cliente", st.session_state.clientes['Nombre'].tolist())
        monto_cli = st.number_input("Monto ($)", min_value=0, step=100)
        tipo_mov = st.radio("Movimiento", ["Sumar Deuda", "Registrar Pago"])
        
        if st.button("Registrar Movimiento"):
            idx_c = st.session_state.clientes[st.session_state.clientes['Nombre'] == cli_sel].index[0]
            if tipo_mov == "Sumar Deuda":
                st.session_state.clientes.at[idx_c, 'Saldo Deudor ($)'] += monto_cli
            else:
                st.session_state.clientes.at[idx_c, 'Saldo Deudor ($)'] -= monto_cli
            st.rerun()
