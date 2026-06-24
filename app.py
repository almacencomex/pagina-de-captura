import streamlit as st
import requests

st.set_page_config(layout="wide")

url_script = "https://script.google.com/macros/s/AKfycbyZXFo8tWgYxm8Az37TNbvfHX0Ssh_Xlku0WpP0Kbf9KSRmoUVI93EnjenCZ4xBzvLU/exec"

st.title("📦 Sistema Interno - Almacén Comex")

with st.form("pedido", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        sucursal = st.selectbox("Sucursal", ['Avenida', 'Pioneros', 'Chimalpa', 'Trejo', 'San Cristóbal', 'Bodegas', 'Máquinas', 'B2B', 'México Nuevo', 'Lindavista', 'Colinas', 'Tlazala', 'Mezquite'])
        cliente = st.text_input("Cliente")
        telefono = st.text_input("Teléfono")
        direccion = st.text_input("Dirección")
        colonia = st.text_input("Colonia")
        cp = st.text_input("Código Postal")
    with col2:
        importe = st.number_input("Importe ($)", min_value=0.0)
        tipo = st.selectbox("Tipo Pedido", ['Recurrente', 'Perimetro suc', 'Traspaso tiendas', 'Complemento entrega', 'Garantia/Reposicion', 'Entrega parcial', 'Recoleccion kroma', 'Ruta de traspasos', 'B2B', 'Foraneo'])
        prioridad = st.selectbox("Prioridad", ['A', 'B', 'C'])
        notas = st.text_area("Notas")
    
    if st.form_submit_button("Enviar Pedido"):
        datos = {
            "sucursal": sucursal, "cliente": cliente, "telefono": telefono,
            "direccion": direccion, "colonia": colonia, "cp": cp,
            "importe": importe, "tipo": tipo, "prioridad": prioridad, "notas": notas
        }
        resp = requests.post(url_script, json=datos)
        if resp.status_code == 200:
            st.success("Pedido registrado con éxito.")
