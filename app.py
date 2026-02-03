import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Pacha Pro - AI Edition", layout="wide")

# 1. Seguridad (Contraseña: pacha2026)
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
    # 2. Base de Datos
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame({
            'Código': ['101', '102'],
            'Producto': ['Caramelos', 'Gaseosa'],
            'Costo ($)': [10, 800],
            'Margen (%)': [100, 40],
            'Stock': [100, 15]
        })

    # 3. Interfaz
    st.title("🏪 Pacha Pro + AI Assistant")
    
    # --- 🤖 NUEVO: ASISTENTE DE IA (ACCIONABLE) ---
    with st.sidebar:
        st.header("🤖 Asistente Pacha IA")
        st.write("Pedime cambios en lenguaje natural.")
        query = st.text_input("Ej: 'Costo del caramelo a 20'", key="ai_query")
        
        if st.button("Ejecutar Orden"):
            query = query.lower()
            inv = st.session_state.inventario
            success_action = False
            
            # Lógica de detección de órdenes (Simulación de IA procesadora)
            for i, row in inv.iterrows():
                prod_name = row['Producto'].lower()
                if prod_name in query:
                    # Detectar si quiere cambiar COSTO
                    if "costo" in query or "vale" in query:
                        new_val = [int(s) for s in query.split() if s.isdigit()][0]
                        st.session_state.inventario.at[i, 'Costo ($)'] = new_val
                        st.success(f"✅ Costo de {row['Producto']} actualizado a ${new_val}")
                        success_action = True
                    # Detectar si quiere cambiar STOCK
                    elif "stock" in query or "cantidad" in query:
                        new_val = [int(s) for s in query.split() if s.isdigit()][0]
                        st.session_state.inventario.at[i, 'Stock'] = new_val
                        st.success(f"✅ Stock de {row['Producto']} actualizado a {new_val}")
                        success_action = True
            
            if success_action:
                st.rerun()
            else:
                st.error("No entendí la orden. Intentá: '[Producto] [campo] [valor]'")

    # 4. Pestañas de siempre
    tabs = st.tabs(["🛒 VENTAS", "📋 INVENTARIO", "👤 CLIENTES"])

    with tabs[0]:
        st.subheader("Caja Rápida")
        # (Aquí va el código de ventas anterior...)
        st.info("Escanear producto para vender.")

    with tabs[1]:
        st.subheader("Control de Stock")
        st.dataframe(st.session_state.inventario, use_container_width=True)

    with tabs[2]:
        st.subheader("Fiados")
        # (Aquí va el código de clientes anterior...)
        st.write("Gestión de deudas activa.")index[0]
                mod = monto_c if tipo_m == "Sumar Deuda" else -monto_c
                st.session_state.clientes.at[idx_c, 'Saldo Deudor ($)'] += mod
                st.rerun()
