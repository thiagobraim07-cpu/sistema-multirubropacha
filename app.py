import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de Seguridad
st.set_page_config(page_title="Pacha Pro - Punto de Venta", layout="wide")

def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔐 Acceso Pacha Pro")
        pwd = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if pwd == "pacha2026": # Contraseña configurada
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        return False
    return True

if check_password():
    # Estilos CSS
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; }
        div[data-testid="stMetric"] { background-color: #F0F2F6; border-radius: 10px; padding: 15px; }
        .stButton>button { border-radius: 8px; width: 100%; }
        </style>
        """, unsafe_allow_html=True)

    # 2. Base de Datos Inicial
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame({
            'Código': ['77901234', '77909876', '77911223'],
            'Producto': ['Caramelos Arcor', 'Coca Cola 500ml', 'Alfajor Jorgito'],
            'Costo ($)': [10, 800, 500],
            'Margen (%)': [100, 40, 50],
            'Stock': [100, 15, 20]
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
    c3.metric("⚠️ Críticos", len(inv[inv['Stock'] < 5]))

    st.divider()

    tabs = st.tabs(["🛒 VENTA RÁPIDA", "📋 INVENTARIO", "👤 CLIENTES", "⚙️ CONFIG"])

    with tabs[0]: # PUNTO DE VENTA
        col_selec, col_cart = st.columns([1, 1])
        
        with col_selec:
            st.subheader("Añadir al Carrito")
            # El buscador ahora permite escribir código o nombre
            opcion = st.selectbox("Buscar por Nombre o Código", inv_display['Producto'] + " (" + inv_display['Código'] + ")")
            prod_nom = opcion.split(" (")[0]
            cant_v = st.number_input("Cantidad", min_value=1, value=1)
            
            p_unit = inv_display[inv_display['Producto'] == prod_nom]['Precio Venta ($)'].values[0]
            
            if st.button("➕ AGREGAR"):
                st.session_state.carrito.append({
                    'Producto': prod_nom,
                    'Cantidad': cant_v,
                    'Subtotal': p_unit * cant_v
                })
                st.toast(f"Agregado: {prod_nom}")

        with col_cart:
            st.subheader("Ticket Actual")
            if st.session_state.carrito:
                df_cart = pd.DataFrame(st.session_state.carrito)
                st.table(df_cart)
                total_cart = df_cart['Subtotal'].sum()
                st.markdown(f"### TOTAL: ${total_cart}")
                
                if st.button("✅ FINALIZAR Y COBRAR"):
                    for item in st.session_state.carrito:
                        idx = inv[inv['Producto'] == item['Producto']].index[0]
                        st.session_state.inventario.at[idx, 'Stock'] -= item['Cantidad']
                    
                    st.session_state.ventas_hoy += total_cart
                    st.session_state.carrito = [] 
                    st.success("Venta procesada")
                    st.balloons()
                    st.rerun()
                
                if st.button("🗑️ Vaciar Carrito"):
                    st.session_state.carrito = []
                    st.rerun()

    with tabs[1]: # INVENTARIO
        st.subheader("Control de Almacén")
        st.dataframe(inv_display, use_container_width=True)

    with tabs[3]: # CONFIG
        if st.button("Cerrar Sesión"):
            del st.session_state["password_correct"]
            st.rerun()
