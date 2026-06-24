import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Almacén Comex", layout="wide")

url = "TU_URL_DE_GOOGLE_SHEET_AQUI"
csv_url = url.replace('/edit#gid=', '/export?format=csv&gid=')

def cargar_datos():
    return pd.read_csv(csv_url)

def guardar_datos(df_actualizado):
    st.warning("Para guardar cambios, asegúrate de tener configurada la API de Google Sheets.")

SUCURSALES = ['Avenida', 'Pioneros', 'Chimalpa', 'Trejo', 'San Cristóbal', 'Bodegas', 'Máquinas', 'B2B', 'México Nuevo', 'Lindavista', 'Colinas', 'Tlazala', 'Mezquite']
TIPOS_PEDIDO = ['Recurrente', 'Perimetro suc', 'Traspaso tiendas', 'Complemento entrega', 'Garantia/Reposicion', 'Entrega parcial', 'Recoleccion kroma', 'Ruta de traspasos', 'B2B', 'Foraneo']
PRIORIDADES = ['A', 'B', 'C']
REPARTIDORES = ['Juan Luis', 'Jorge', 'Issac', 'Sin Asignar']
ESTADOS = ['Pendiente', 'Preparando', 'Asignado', 'En Ruta', 'Entregado']

st.title("📦 Sistema Interno de Logística - Almacén Comex")

tab1, tab2 = st.tabs(["🏢 Panel de Sucursales (Captura)", "👨‍💻 Panel del Coordinador (Entregas)"])

with tab1:
    st.header("Levantar Nuevo Pedido de Reparto")
    with st.form("formulario_pedido", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sucursal = st.selectbox("Sucursal Origen", SUCURSALES)
            cliente = st.text_input("Nombre del Cliente")
            telefono = st.text_input("Teléfono del Cliente") 
            direccion = st.text_input("Dirección Completa")
            colonia = st.text_input("Colonia")
            codigo_postal = st.text_input("Código Postal")
            importe = st.number_input("Importe ($)", min_value=0.0, step=50.0)
        with col2:
            tipo_pedido = st.selectbox("Tipo de Pedido", TIPOS_PEDIDO)
            prioridad = st.selectbox("Prioridad", PRIORIDADES)
            notas = st.text_area("Notas / Indicaciones Especiales")
            
        enviar = st.form_submit_button("Enviar Pedido")
        if enviar:
            st.success("Pedido enviado (Configura los permisos de escritura para persistencia).")

with tab2:
    st.header("Gestión de Entregas")
    clave = st.text_input("Contraseña:", type="password")
    if clave == "Comex2026":
        df_coordinador = cargar_datos()
        st.dataframe(df_coordinador, use_container_width=True)
        st.subheader("Actualizar Estatus")
        with st.form("actualizar"):
            folio_editar = st.selectbox("Folio", df_coordinador['Folio'].tolist())
            nuevo_estado = st.selectbox("Estado", ESTADOS)
            if st.form_submit_button("Guardar"):
                st.info("Función de escritura disponible tras configuración de API.")
