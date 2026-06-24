import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")

url_script = "https://script.google.com/macros/s/AKfycbyn0UNAvgbef9yeQm7aydTAmY7u3Pwdrh74H6YfeEvNVLEFBiwoL-xXqN7MdFseMFAj/exec"

st.title("Sistema de Pedidos")

with st.form("pedido"):
    cliente = st.text_input("Cliente")
    if st.form_submit_button("Enviar"):
        try:
            response = requests.post(url_script, json={"cliente": cliente})
            if response.status_code == 200:
                st.success("Pedido enviado correctamente a la base de datos.")
            else:
                st.error("Error al enviar el pedido.")
        except Exception as e:
            st.error(f"Error: {e}")
