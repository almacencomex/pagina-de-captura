import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
url_script = "https://script.google.com/macros/s/AKfycbyZXFo8tWgYxm8Az37TNbvfHX0Ssh_Xlku0WpP0Kbf9KSRmoUVI93EnjenCZ4xBzvLU/exec"
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtbtQYSmR83sJ4BbW4QzPSXvm0eVf9rpv4e8IAZPjvz9ZQS9ZYZoUkN4iZAIHtyz588Lud5jpPTa2D/pub?output=csv"

tab1, tab2 = st.tabs(["🏢 Captura", "👨‍💻 Panel Coordinador"])

with tab1:
    st.header("Levantar Pedido / Solicitud de Movimiento")
    with st.form("pedido", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sucursal = st.selectbox("Sucursal / Área", [
                'Avenida', 'Pioneros', 'Chimalpa', 'Trejo', 'San Cristóbal', 
                'Bodegas', 'Máquinas', 'B2B', 'México Nuevo', 'Lindavista', 
                'Colinas', 'Tlazala', 'Mezquite', 'Administración', 'Operaciones'
            ])
            cliente = st.text_input("Cliente / Solicitante")
            telefono = st.text_input("Teléfono")
        with col2:
            direccion = st.text_input("Dirección / Destino")
            importe = st.number_input("Importe ($)", min_value=0.0)
            tipo = st.selectbox("Tipo Pedido / Movimiento", [
                'Recurrente', 'Perimetro suc', 'Traspaso tiendas', 'Complemento entrega', 
                'Garantia/Reposicion', 'Entrega parcial', 'Recoleccion kroma', 
                'Ruta de traspasos', 'B2B', 'Foraneo', 'Movimiento Administrativo', 'Movimiento Operativo'
            ])
        
        if st.form_submit_button("Enviar Solicitud"):
            datos = {"sucursal": sucursal, "cliente": cliente, "telefono": telefono, 
                     "direccion": direccion, "importe": importe, "tipo": tipo,
                     "chofer": "Sin asignar", "hora_salida": "", "hora_entrega": ""}
            requests.post(url_script, json=datos)
            st.success("Solicitud enviada correctamente.")

with tab2:
    st.header("Gestión de Entregas")
    clave = st.text_input("Contraseña", type="password")
    if clave == "Comex2026":
        df = pd.read_csv(csv_url)
        f = st.selectbox("Folio a gestionar", df['Folio'].unique())
        c_nuevo = st.selectbox("Asignar Chofer", ['Juan', 'Pedro', 'Luis'])
        e_nuevo = st.selectbox("Estado", ['Pendiente', 'En Ruta', 'Entregado'])
        
        # Selección de horario profesional
        hs = st.time_input("Hora Salida")
        he = st.time_input("Hora Entrega")
        
        if st.button("Confirmar y Aplicar Cambios"):
            url_edit = f"{url_script}?folio={f}&chofer={c_nuevo}&estado={e_nuevo}&h_salida={hs}&h_entrega={he}"
            res = requests.get(url_edit)
            if res.status_code == 200:
                st.success("¡Cambios aplicados correctamente!")
                st.rerun()
            else:
                st.error("Error al conectar con Google.")
        
        st.dataframe(df, use_container_width=True)
