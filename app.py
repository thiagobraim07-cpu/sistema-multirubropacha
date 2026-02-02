import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración
st.set_page_config(page_title="Pacha Gestión Pro", layout="wide")

# 2. Base de Datos
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame({
        'Código': ['101', '102', '103'],
        'Producto': ['Caramelos', 'Gaseosa Cola', 'Alfajor'],
        'Costo ($)': [10, 800, 500],
        'Margen (%)': [100, 40, 50],
        'Stock': [100, 12, 24]
    })

if 'ventas_totales' not in st.session_state:
    st.session_state.ventas_totales = 0

if 'ultimo_ticket' not in st.session_state:
    st.session_state.ultimo_ticket = ""

# 3. Interfaz Superior
st.title("🏪 Pacha Gestión Pro")
inv = st.session_state.inventario
productos_bajo_stock = inv[inv['Stock'] < 5]

col1, col2, col3 = st.columns(3)
col1.metric("📦 Stock Total", inv['Stock'].sum())
col2.metric("💰 Ventas del Día", f"$ {st.session_state.ventas_totales:,.0f}")
col3.metric("⚠️ Alertas de Reposición", len(productos_bajo_stock))

if not productos_bajo_stock.empty:
    with st.expander("🚨 VER PRODUCTOS A REPONER"):
        st.write(productos_bajo_stock[['Producto', 'Stock']])

st.divider()

# 4. Pestañas
tab1, tab2, tab3 = st.tabs(["🛒 VENTA", "📋 INVENTARIO", "👤 CLIENTES"])

with tab1:
    col_v, col_t = st.columns([1, 1])
    
    with col_v:
        st.subheader("Caja")
        prod_sel = st.selectbox("Producto", inv['Producto'].tolist())
        cant = st.number_input("Cantidad", min_value=1, value=1)
        
        datos = inv[inv['Producto'] == prod_sel].iloc[0]
        precio = int(datos['Costo ($)'] * (1 + datos['Margen (%)'] / 100))
        total = precio * cant
        
        st.markdown(f"### Total: ${total}")
        
        if st.button("CONFIRMAR Y GENERAR TICKET"):
            idx = inv[inv['Producto'] == prod_sel].index[0]
            if inv.at[idx, 'Stock'] >= cant:
                # Restar stock
                st.session_state.inventario.at[idx, 'Stock'] -= cant
                st.session_state.ventas_totales += total
                
                # Crear Ticket
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
                st.session_state.ultimo_ticket = f"""
                PACHA GESTIÓN PRO
                ---------------------------
                FECHA: {fecha}
                PRODUCTO: {prod_sel}
                CANTIDAD: {cant}
                PRECIO UNIT: ${precio}
                ---------------------------
                TOTAL: ${total}
                ¡Gracias por su compra!
                """
                st.success("Venta realizada")
                st.rerun()
            else:
                st.error("No hay stock suficiente")

    with col_t:
        st.subheader("Ticket de Venta")
        if st.session_state.ultimo_ticket:
            st.code(st.session_state.ultimo_ticket)
            st.button("Imprimir (Simulado)")
        else:
            st.info("El ticket aparecerá aquí después de la venta.")

with tab2:
    st.write("### Control de Stock")
    st.dataframe(st.session_state.inventario, use_container_width=True)

with tab3:
    st.write("### Cuentas Corrientes")
    st.info("Módulo de Clientes activo.")
