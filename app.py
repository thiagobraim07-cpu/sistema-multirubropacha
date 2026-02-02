import streamlit as st
import pandas as pd

# 1. Configuración
st.set_page_config(page_title="Pacha Gestión Pro", layout="wide")

# CSS para diseño limpio
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    div[data-testid="stMetric"] { background-color: #F0F2F6; border-radius: 10px; padding: 15px; }
    .stButton>button { background-color: #2E7D32; color: white; border-radius: 8px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización de datos (Inventario y Clientes)
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame({
        'Código': ['7790123456789', '7790987654321', '7791122334455'],
        'Producto': ['Alfajor de Chocolate', 'Gaseosa Cola 500ml', 'Galletitas Saladas'],
        'Costo ($)': [500, 800, 400],
        'Margen (%)': [50, 40, 60],
        'Stock': [24, 12, 30]
    })

if 'clientes' not in st.session_state:
    st.session_state.clientes = pd.DataFrame({
        'Nombre': ['Juan Perez', 'Maria Garcia'],
        'Saldo Deudor ($)': [1500, 0]
    })

# Procesar inventario
inv = st.session_state.inventario.copy()
inv['Precio Venta ($)'] = (inv['Costo ($)'] * (1 + inv['Margen (%)'] / 100)).round(0).astype(int)

# 3. Interfaz Principal
st.title("🏪 Pacha Gestión Pro")

col1, col2, col3 = st.columns(3)
col1.metric("📦 Productos", len(inv))
col2.metric("💰 Capital Stock", f"$ {(inv['Costo ($)'] * inv['Stock']).sum():,.0f}")
col3.metric("🤝 Deuda Clientes", f"$ {st.session_state.clientes['Saldo Deudor ($)'].sum():,.0f}")

st.divider()

tab1, tab2, tab3 = st.tabs(["📋 Inventario", "📥 Actualizar Precios", "👤 Cuentas Clientes"])

with tab1:
    st.write("### Stock Actual")
    st.dataframe(inv.style.format({'Costo ($)': '${:,.0f}', 'Precio Venta ($)': '${:,.0f}'}), use_container_width=True)

with tab2:
    st.subheader("Carga de Listas")
    archivo = st.file_uploader("Subí tu Excel", type=['xlsx', 'csv'])
    if archivo:
        st.warning("IA: Se detectó un aumento del 20% sugerido.")
        if st.button("Aplicar a todo"):
            st.session_state.inventario['Costo ($)'] = (st.session_state.inventario['Costo ($)'] * 1.2).round(0)
            st.rerun()

with tab3:
    st.subheader("Gestión de Fiados")
    
    # Formulario para nuevo cliente
    with st.expander("➕ Registrar Nuevo Cliente"):
        nuevo_nombre = st.text_input("Nombre del Cliente")
        if st.button("Guardar Cliente"):
            nuevo_cli = pd.DataFrame({'Nombre': [nuevo_nombre], 'Saldo Deudor ($)': [0]})
            st.session_state.clientes = pd.concat([st.session_state.clientes, nuevo_cli], ignore_index=True)
            st.rerun()

    st.write("---")
    
    # Tabla de saldos
    st.table(st.session_state.clientes)
    
    # Movimientos de cuenta
    st.write("### 💸 Registrar Movimiento")
    col_cli, col_monto, col_btn = st.columns([2, 1, 1])
    
    with col_cli:
        cliente_sel = st.selectbox("Seleccionar Cliente", st.session_state.clientes['Nombre'])
    with col_monto:
        monto = st.number_input("Monto ($)", step=100)
    with col_btn:
        st.write(" ") # Espaciador
        tipo = st.radio("Tipo", ["Suma Deuda", "Pagó"])
        if st.button("Registrar"):
            idx = st.session_state.clientes[st.session_state.clientes['Nombre'] == cliente_sel].index[0]
            if tipo == "Suma Deuda":
                st.session_state.clientes.at[idx, 'Saldo Deudor ($)'] += monto
            else:
                st.session_state.clientes.at[idx, 'Saldo Deudor ($)'] -= monto
            st.success("Movimiento guardado")
            st.rerun()
