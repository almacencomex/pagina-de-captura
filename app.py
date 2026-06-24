import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
url_script = "https://script.google.com/macros/s/AKfycbyZXFo8tWgYxm8Az37TNbvfHX0Ssh_Xlku0WpP0Kbf9KSRmoUVI93EnjenCZ4xBzvLU/exec"
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtbtQYSmR83sJ4BbW4QzPSXvm0eVf9rpv4e8IAZPjvz9ZQS9ZYZoUkN4iZAIHtyz588Lud5jpPTa2D/pub?output=csv"

tab1, tab2 = st.tabs(["🏢 Captura", "👨‍💻 Panel Coordinador"])

with tab1:
    with st.form("pedido", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sucursal = st.selectbox("Sucursal", ['Avenida', 'Pioneros', 'Chimalpa'])
            cliente = st.text_input("Cliente")
            chofer = st.selectbox("Chofer", ['Juan', 'Pedro', 'Luis', 'Sin asignar'])
        with col2:
            h_salida = st.text_input("Hora Salida (HH:MM)")
            h_entrega = st.text_input("Hora Entrega (HH:MM)")
            if st.form_submit_button("Enviar Pedido"):
                datos = {"sucursal": sucursal, "cliente": cliente, "chofer": chofer, 
                         "hora_salida": h_salida, "hora_entrega": h_entrega}
                requests.post(url_script, json=datos)
                st.success("Pedido registrado.")

with tab2:
    st.header("Gestión de Entregas")
    clave = st.text_input("Contraseña", type="password")
    
    if clave == "Comex2026":
        try:
            df = pd.read_csv(csv_url)
            f = st.selectbox("Folio a gestionar", df['Folio'].unique())
            c_nuevo = st.selectbox("Asignar Chofer", ['Juan', 'Pedro', 'Luis'])
            e_nuevo = st.selectbox("Estado", ['Pendiente', 'En Ruta', 'Entregado'])
            hs = st.text_input("H. Salida")
            he = st.text_input("H. Entrega")
            
            if st.button("Actualizar"):
                url_edit = f"{url_script}?folio={f}&chofer={c_nuevo}&estado={e_nuevo}&h_salida={hs}&h_entrega={he}"
                st.link_button("Confirmar cambios en Google", url_edit)
            
            st.dataframe(df, use_container_width=True)
        except:
            st.error("Error al cargar datos. Verifica la URL CSV y que la hoja esté publicada.")
    else:
        st.warning("Por favor, ingresa la contraseña para acceder al panel de gestión.")
