import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")

url_script = "https://script.google.com/macros/s/AKfycbyZXFo8tWgYxm8Az37TNbvfHX0Ssh_Xlku0WpP0Kbf9KSRmoUVI93EnjenCZ4xBzvLU/exec"

st.title("📦 Sistema Interno de Logística - Almacén Comex")

tab1, tab2 = st.tabs(["🏢 Panel de Sucursales (Captura)", "👨‍💻 Panel del Coordinador (Entregas)"])

with tab1:
    st.header("Levantar Nuevo Pedido")
    with st.form("pedido", clear_on_submit=True):
        sucursal = st.selectbox("Sucursal", ['Avenida', 'Pioneros', 'Chimalpa'])
        cliente = st.text_input("Cliente")
        if st.form_submit_button("Enviar Pedido"):
            datos = {"sucursal": sucursal, "cliente": cliente}
            resp = requests.post(url_script, json=datos)
            if resp.status_code == 200:
                st.success(f"¡Éxito! Pedido de {cliente} recibido en {sucursal}.")

with tab2:
    st.header("Gestión de Entregas")
    clave = st.text_input("Contraseña:", type="password")
    if clave == "Comex2026":
        try:
            df = pd.read_csv("TU_URL_CSV_DE_GOOGLE_SHEETS")
            
            # --- Contadores (Dashboard) ---
            c1, c2, c3 = st.columns(3)
            c1.metric("Pendientes", len(df[df['Estado'] == 'Pendiente']))
            c2.metric("En Ruta", len(df[df['Estado'] == 'En Ruta']))
            c3.metric("Entregados hoy", len(df[df['Estado'] == 'Entregado']))
            
            st.dataframe(df, use_container_width=True)
        except:
            st.warning("Cargando datos o base vacía...")
