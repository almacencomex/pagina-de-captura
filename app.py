import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

url_script = "https://script.google.com/macros/s/AKfycbyZXFo8tWgYxm8Az37TNbvfHX0Ssh_Xlku0WpP0Kbf9KSRmoUVI93EnjenCZ4xBzvLU/exec
"
url_csv = "https://docs.google.com/spreadsheets/d/1qnZGiiCG6Y82YS-NSU05AHQ9VO3b_7EAlMKpmDBIc2k/edit?gid=0#gid=0"
csv_url = url_csv.replace('/edit#gid=', '/export?format=csv&gid=')

tab1, tab2 = st.tabs(["🏢 Captura", "👨‍💻 Panel Coordinador"])

with tab1:
    st.header("Levantar Pedido")
    with st.form("pedido", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sucursal = st.selectbox("Sucursal", ['Avenida', 'Pioneros', 'Chimalpa'])
            cliente = st.text_input("Cliente")
            telefono = st.text_input("Teléfono")
            direccion = st.text_input("Dirección")
            colonia = st.text_input("Colonia")
            cp = st.text_input("Código Postal")
        with col2:
            importe = st.number_input("Importe ($)", min_value=0.0)
            tipo = st.selectbox("Tipo", ['Recurrente', 'Traspaso'])
            prioridad = st.selectbox("Prioridad", ['A', 'B', 'C'])
            notas = st.text_area("Notas")
        
        if st.form_submit_button("Enviar Pedido"):
            datos = {"sucursal": sucursal, "cliente": cliente, "telefono": telefono, "direccion": direccion, "colonia": colonia, "cp": cp, "importe": importe, "tipo": tipo, "prioridad": prioridad, "notas": notas}
            requests.post(url_script, json=datos)
            st.success("Pedido enviado.")

with tab2:
    st.header("Panel de Control")
    clave = st.text_input("Contraseña", type="password")
    if clave == "Comex2026":
        try:
            df = pd.read_csv(csv_url)
            c1, c2, c3 = st.columns(3)
            c1.metric("Pendientes", len(df[df['Estado'] == 'Pendiente']))
            c2.metric("En Ruta", len(df[df['Estado'] == 'En Ruta']))
            c3.metric("Entregados", len(df[df['Estado'] == 'Entregado']))
            st.dataframe(df, use_container_width=True)
        except:
            st.error("Error al cargar datos. Verifica que la hoja esté pública.")
