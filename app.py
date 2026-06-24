import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

url = "TU_URL_AQUI"
csv_url = url.replace('/edit#gid=', '/export?format=csv&gid=')

st.title("Sistema de Pedidos")

if st.button("Cargar Datos"):
    try:
        df = pd.read_csv(csv_url)
        st.dataframe(df)
    except:
        st.error("No pude leer la hoja. Asegúrate de que es pública.")

st.subheader("Captura Nuevo Pedido")
with st.form("pedido"):
    cliente = st.text_input("Cliente")
    if st.form_submit_button("Enviar"):
        st.write("Pedido enviado a:", cliente)
