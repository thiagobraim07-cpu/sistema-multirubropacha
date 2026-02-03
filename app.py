import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración General y Seguridad
st.set_page_config(page_title="Pacha Gestión Pro", layout="wide")

def check_password():
    """Retorna True si el usuario ingresó la contraseña correcta."""
    def password_entered():
        if st.session_state["password"] == "pacha2026": # <-- CAMBIA TU CONTRASEÑA AQUÍ
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔐 Acceso Restringido")
        st.text_input("Ingresá la contraseña para continuar", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Contraseña incorrecta, intentá de nuevo", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

if check_password():
    # Estilo visual
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; }
        div[data-testid="stMetric"] { background-color: #F0F2F6; border-radius: 10px; padding: 15px; }
        .stButton>button { background-color: #2E7D32; color: white; border-radius: 8px; width: 100%; }
        .low-stock { color: #D32F2F; font-weight: bold; border: 1px solid #D32F2F; padding: 10px; border-radius: 5px; background-color: #FFEBEE; }
        </style>
        """, unsafe_allow_html=True)

    # 2. Inicialización de Datos
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

    # 3. Lógica
    inv = st.session_state.inventario
    inv_display = inv.copy()
    inv_display['Precio Venta ($)'] = (inv_display['Costo ($)'] * (1 + inv_display['Margen (%)'] / 100)).round(0).astype(int)
    productos_bajo_stock = inv[inv['Stock'] < 5]

    # 4. Dashboard Principal
    st.title("🏪 Pacha Gestión Pro")
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Stock Total", inv['Stock'].sum())
    col2.metric("💰 Caja Hoy", f"$ {st.session_state.ventas_totales:,.0f}")
    col3.metric("🤝 Deuda Total", f"$ {st.session_state.clientes['Saldo Deudor ($)'].sum():,.0f}")

    if not productos_bajo_stock.empty:
        st.markdown("### 🚨 ALERTAS DE REPOSICIÓN")
        for _, fila in productos_bajo_stock.iterrows():
            st.markdown(f"<div class='low-stock'>⚠️ Solo quedan {fila['Stock']} de {fila['Producto']}</div>", unsafe_allow_html=True)

    st.divider()

    # 5. Pestañas
    tabs = st.tabs(["🛒 PUNTO DE VENTA", "📋 INVENTARIO", "📥 CARGAR LISTA", "👤 CLIENTES"])

    with tabs[0]: # VENTAS
        col_v, col_t = st.columns([1, 1])
        with col_v:
            st.subheader("Caja Rápida")
            prod_sel = st.selectbox("Producto", inv_display['Producto'].tolist())
            cant = st.number_input("Cantidad", min_value=1, value=1)
            datos = inv_display[inv_display['Producto'] == prod_sel].iloc[0]
            total = datos['Precio Venta ($)'] * cant
            st.markdown(f"## Total: ${total}")
            if st.button("COBRAR ✅"):
                idx = inv[inv['Producto'] == prod_sel].index[0]
                if inv.at[idx, 'Stock'] >= cant:
                    st.session_state.inventario.at[idx, 'Stock'] -= cant
                    st.session_state.ventas_totales += total
                    st.session_state.ultimo_ticket = f"PACHA GESTIÓN PRO\n---\nFECHA: {datetime.now().strftime('%d/%m/%Y %H:%M')}\nPRODUCTO: {prod_sel}\nCANTIDAD: {cant}\nTOTAL: ${total}\n---"
                    st.rerun()

        with col_t:
            st.subheader("Ticket")
            if st.session_state.ultimo_ticket:
                st.code(st.session_state.ultimo_ticket)

    with tabs[1]: # INVENTARIO
        st.subheader("Stock Actual")
        st.dataframe(inv_display.style.format({'Costo ($)': '${:,.0f}', 'Precio Venta ($)': '${:,.0f}'}), use_container_width=True)

    with tabs[2]: # CARGA EXCEL
        st.subheader("Cargar Lista de Proveedor")
        archivo = st.file_uploader("Arrastrá el archivo", type=['xlsx', 'csv'])
        if archivo:
            if st.button("Aplicar Aumento General (15%)"):
                st.session_state.inventario['Costo ($)'] = (st.session_state.inventario['Costo ($)'] * 1.15).round(0).astype(int)
                st.rerun()

    with tabs[3]: # CLIENTES
        st.subheader("Cuentas Corrientes")
        st.write("### Saldos")
        st.table(st.session_state.clientes)
        cli_sel = st.selectbox("Elegir Cliente", st.session_state.clientes['Nombre'].tolist())
        monto_cli = st.number_input("Monto ($)", min_value=0)
        tipo_mov = st.radio("Acción", ["Sumar Deuda", "Cobrar Pago"])
        if st.button("Guardar Movimiento"):
            idx_c = st.session_state.clientes[st.session_state.clientes['Nombre'] == cli_sel].index[0]
            st.session_state.clientes.at[idx_c, 'Saldo Deudor ($)'] += (monto_cli if tipo_mov == "Sumar Deuda" else -monto_cli)
            st.rerun()
