import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Almacén Comex", layout="wide")

url_script = "https://script.google.com/macros/s/AKfycbyZXFo8tWgYxm8Az37TNbvfHX0Ssh_Xlku0WpP0Kbf9KSRmoUVI93EnjenCZ4xBzvLU/exec"
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtbtQYSmR83sJ4BbW4QzPSXvm0eVf9rpv4e8IAZPjvz9ZQS9ZYZoUkN4iZAIHtyz588Lud5jpPTa2D/pub?output=csv"

tab1, tab2 = st.tabs(["🏢 Captura", "👨‍💻 Panel Coordinador"])

with tab1:
    st.header("Levantar Pedido")
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
            datos = {"sucursal": sucursal, "cliente": cliente, "telefono": telefono, "direccion": direccion, "colonia": colonia, "cp": cp, "importe": importe, "tipo": tipo, "prioridad": prioridad, "notas": notas}
            resp = requests.post(url_script, json=datos)
            if resp.status_code == 200:
                st.success("Pedido enviado correctamente.")

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
            
            st.subheader("Actualizar Estado")
            col_f, col_e = st.columns(2)
            folio_a_editar = col_f.selectbox("Selecciona Folio", df['Folio'].unique())
            nuevo_status = col_e.selectbox("Nuevo Estado", ['Pendiente', 'En Ruta', 'Entregado'])
            
            url_edit = f"{url_script}?folio={folio_a_editar}&estado={nuevo_status}"
            st.link_button("Confirmar cambio de estado en Google", url_edit)
            
            st.dataframe(df, use_container_width=True)
        except:
            st.error("Error al cargar datos. Verifica la URL CSV y que la hoja esté publicada.")
