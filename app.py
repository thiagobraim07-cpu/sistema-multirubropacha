import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Estilo White Neon Profesional
st.set_page_config(page_title="Pacha Pro AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E1E1E; }
    /* Estilo del Asistente Superior */
    .ai-container {
        background: linear-gradient(90deg, #00F2FF, #FF00E5);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] {
        border: 2px solid #00F2FF;
        border-radius: 15px;
        padding: 10px;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización de Datos (Base de datos centralizada)
if 'inv' not in st.session_state:
    st.session_state.inv = pd.DataFrame({
        'Código': ['77901234', '77909876', '101'],
        'Producto': ['Alfajor Arcor', 'Coca Cola 500ml', 'Caramelos'],
        'Costo ($)': [500, 800, 10],
        'Margen (%)': [50, 40, 100],
        'Stock': [20, 15, 100]
    })

if 'cli' not in st.session_state:
    st.session_state.cli = pd.DataFrame({'Nombre': ['Consumidor Final', 'Juan Perez'], 'Deuda ($)': [0, 1500]})

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

if 'ventas_total' not in st.session_state:
    st.session_state.ventas_total = 0

# --- 🤖 3. ASISTENTE IA SUPERIOR (Control Total) ---
st.markdown('<div class="ai-container">', unsafe_allow_html=True)
st.subheader("🤖 Asistente Pacha Pro")
comando = st.text_input("¿Qué querés hacer? (Ej: 'Vender 2 cocas', 'Costo alfajor 600', 'Deuda Juan 2000')", placeholder="Escribí una orden...")
st.markdown('</div>', unsafe_allow_html=True)

if comando:
    cmd = comando.lower()
    # Lógica de procesamiento de órdenes
    for i, row in st.session_state.inv.iterrows():
        if row['Producto'].lower() in cmd:
            nums = [int(s) for s in cmd.split() if s.isdigit()]
            if nums:
                val = nums[0]
                if "vend" in cmd:
                    if st.session_state.inv.at[i, 'Stock'] >= val:
                        st.session_state.inv.at[i, 'Stock'] -= val
                        precio = int(row['Costo ($)'] * (1 + row['Margen (%)'] / 100))
                        st.session_state.ventas_total += (precio * val)
                        st.success(f"✅ Venta procesada: {val}x {row['Producto']}")
                    else: st.error("Stock insuficiente")
                elif "costo" in cmd or "vale" in cmd:
                    st.session_state.inv.at[i, 'Costo ($)'] = val
                    st.success(f"✅ Nuevo costo para {row['Producto']}: ${val}")
                elif "stock" in cmd or "tengo" in cmd:
                    st.session_state.inv.at[i, 'Stock'] = val
                    st.success(f"✅ Stock de {row['Producto']} actualizado a {val}")
    st.divider()

# 4. Dashboard de Métricas
c1, c2, c3 = st.columns(3)
c1.metric("💰 Ventas Hoy", f"$ {st.session_state.ventas_total:,.0f}")
c2.metric("📦 Productos", len(st.session_state.inv))
c3.metric("🤝 Deuda Clientes", f"$ {st.session_state.cli['Deuda ($)'].sum():,.0f}")

st.divider()

# 5. Módulos del Sistema
tabs = st.tabs(["🛒 CAJA RÁPIDA", "📋 INVENTARIO", "👥 CLIENTES", "📥 CARGA MASIVA"])

with tabs[0]: # CAJA
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Selección de Productos")
        prod = st.selectbox("Producto", st.session_state.inv['Producto'])
        cant = st.number_input("Cantidad", min_value=1, value=1)
        if st.button("➕ Agregar al Carrito"):
            match = st.session_state.inv[st.session_state.inv['Producto'] == prod].iloc[0]
            precio_v = int(match['Costo ($)'] * (1 + match['Margen (%)'] / 100))
            st.session_state.carrito.append({'Prod': prod, 'Cant': cant, 'Sub': precio_v * cant})
    with col_b:
        st.subheader("Ticket")
        if st.session_state.carrito:
            st.table(pd.DataFrame(st.session_state.carrito))
            if st.button("Finalizar Venta"):
                for it in st.session_state.carrito:
                    idx = st.session_state.inv[st.session_state.inv['Producto'] == it['Prod']].index[0]
                    st.session_state.inv.at[idx, 'Stock'] -= it['Cant']
                    st.session_state.ventas_total += it['Sub']
                st.session_state.carrito = []
                st.rerun()

with tabs[1]: # INVENTARIO
    st.subheader("Control de Stock")
    df_inv = st.session_state.inv.copy()
    df_inv['Venta ($)'] = (df_inv['Costo ($)'] * (1 + df_inv['Margen (%)'] / 100)).round(0)
    st.dataframe(df_inv, use_container_width=True)

with tabs[2]: # CLIENTES
    st.subheader("Cuentas de Fiados")
    st.dataframe(st.session_state.cli, use_container_width=True)
    with st.expander("Modificar Deuda"):
        c_sel = st.selectbox("Elegir Cliente", st.session_state.cli['Nombre'])
        monto = st.number_input("Monto ($)", min_value=0)
        if st.button("Registrar Movimiento"):
            idx_c = st.session_state.cli[st.session_state.cli['Nombre'] == c_sel].index[0]
            st.session_state.cli.at[idx_c, 'Deuda ($)'] += monto # Podés cambiar a resta si paga
            st.rerun()

with tabs[3]: # CARGA MASIVA
    st.subheader("Importar desde Excel/CSV")
    file = st.file_uploader("Subí tu lista de precios", type=['xlsx', 'csv'])
    if file:
        st.info("La IA está lista para procesar los datos.")
