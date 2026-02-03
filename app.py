import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración y Seguridad
st.set_page_config(page_title="Pacha Pro - Punto de Venta", layout="wide")

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 Acceso Pacha Pro")
        pwd = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if pwd == "pacha2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        return False
    return True

if check_password():
    # 2. Inicialización de Datos (Base de datos persistente)
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame({
            'Código': ['77901234', '77909876', '77911223'],
            'Producto': ['Caramelos Arcor', 'Coca Cola 500ml', 'Alfajor Jorgito'],
            'Costo ($)': [10, 800, 500],
            'Margen (%)': [100, 40, 50],
            'Stock': [100, 15, 20]
        })

    if 'clientes' not in st.session_state:
        st.session_state.clientes = pd.DataFrame({
            'Nombre': ['Consumidor Final', 'Juan Perez'],
            'Saldo Deudor ($)': [0, 1500]
        })

    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    if 'ventas_hoy' not in st.session_state:
        st.session_state.ventas_hoy = 0

    inv = st.session_state.inventario
    inv_display = inv.copy()
    inv_display['Precio Venta ($)'] = (inv_display['Costo ($)'] * (1 + inv_display['Margen (%)'] / 100)).round(0).astype(int)

    # 3. Dashboard
    st.title("🏪 Pacha Gestión Pro")
    c1, c2, c3 = st.columns(3)
    c1.metric("📦 Stock", inv['Stock'].sum())
    c2.metric("💰 Ventas Hoy", f"$ {st.session_state.ventas_hoy:,.0f}")
    c3.metric("🤝 Deuda Clientes", f"$ {st.session_state.clientes['Saldo Deudor ($)'].sum():,.0f}")

    st.divider()

    tabs = st.tabs(["🛒 CAJA (ESCÁNER)", "📋 INVENTARIO", "👤 CLIENTES", "⚙️ CONFIG"])

    # --- PESTAÑA CAJA (SOPORTE PARA LECTOR) ---
    with tabs[0]:
        col_selec, col_cart = st.columns([1, 1])
        
        with col_selec:
            st.subheader("Escanear Producto")
            # El truco: Un input de texto que captura el "Enter" que mandan los lectores de código de barras
            barcode = st.text_input("Pase el código de barras aquí 👇", key="scanner", placeholder="Esperando escaneo...")
            
            if barcode:
                # Buscar el producto por código exacto
                match = inv_display[inv_display['Código'] == barcode]
                if not match.empty:
                    prod_nom = match['Producto'].values[0]
                    p_unit = match['Precio Venta ($)'].values[0]
                    
                    # Lo agregamos al carrito automáticamente
                    st.session_state.carrito.append({
                        'Producto': prod_nom,
                        'Cantidad': 1,
                        'Subtotal': p_unit
                    })
                    st.toast(f"✅ {prod_nom} agregado")
                    # No reseteamos el campo aquí para no romper el flujo, pero el usuario puede borrarlo
                else:
                    st.error("Producto no encontrado")

        with col_cart:
            st.subheader("Carrito Actual")
            if st.session_state.carrito:
                df_cart = pd.DataFrame(st.session_state.carrito)
                st.table(df_cart)
                total_cart = df_cart['Subtotal'].sum()
                st.markdown(f"### TOTAL: ${total_cart}")
                
                if st.button("✅ FINALIZAR VENTA"):
                    for item in st.session_state.carrito:
                        idx = inv[inv['Producto'] == item['Producto']].index[0]
                        st.session_state.inventario.at[idx, 'Stock'] -= item['Cantidad']
                    
                    st.session_state.ventas_hoy += total_cart
                    st.session_state.carrito = [] 
                    st.success("Venta procesada")
                    st.rerun()
                
                if st.button("🗑️ Vaciar Carrito"):
                    st.session_state.carrito = []
                    st.rerun()

    # --- PESTAÑA INVENTARIO ---
    with tabs[1]:
        st.subheader("Control de Almacén")
        st.dataframe(inv_display, use_container_width=True)

    # --- PESTAÑA CLIENTES (RECUPERADA) ---
    with tabs[2]:
        st.subheader("Cuentas Corrientes")
        st.dataframe(st.session_state.clientes, use_container_width=True)
        
        with st.expander("💸 Registrar Pago o Deuda"):
            cli_sel = st.selectbox("Cliente", st.session_state.clientes['Nombre'].tolist())
            monto_c = st.number_input("Monto ($)", min_value=0)
            tipo_m = st.radio("Acción", ["Sumar Deuda", "Cobrar Pago"])
            if st.button("Confirmar Movimiento"):
                idx_c = st.session_state.clientes[st.session_state.clientes['Nombre'] == cli_sel].index[0]
                mod = monto_c if tipo_m == "Sumar Deuda" else -monto_c
                st.session_state.clientes.at[idx_c, 'Saldo Deudor ($)'] += mod
                st.rerun()
