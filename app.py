import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Almacén Comex", layout="wide")

conn = st.connection("gsheets", type="gsheets")

def cargar_datos():
    return conn.read(spreadsheet="Base_Entregas_Comex", worksheet="Captura Pedidos")

def guardar_datos(df_actualizado):
    conn.update(spreadsheet="Base_Entregas_Comex", worksheet="Captura Pedidos", data=df_actualizado)

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
            df_actual = cargar_datos()
            nuevo_id = len(df_actual) + 1
            folio = f"P{nuevo_id:03d}"
            nuevo_pedido = {
                'Folio': folio, 'Fecha': datetime.now().strftime('%Y-%m-%d'), 'Hora Pedido': datetime.now().strftime('%H:%M:%S'),
                'Sucursal': sucursal, 'Cliente': cliente, 'Telefono': telefono, 'Direccion': direccion, 'Colonia': colonia, 'Codigo Postal': codigo_postal, 'Importe': importe, 'Tipo Pedido': tipo_pedido,
                'Prioridad': prioridad, 'Repartidor': 'Sin Asignar', 'Estado': 'Pendiente', 'Notas': notas,
                'Hora Salida': '', 'Hora Entrega': ''
            }
            df_actual = pd.concat([df_actual, pd.DataFrame([nuevo_pedido])], ignore_index=True)
            guardar_datos(df_actual)
            st.success(f"Pedido {folio} guardado.")

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
                idx = df_coordinador[df_coordinador['Folio'] == folio_editar].index[0]
                df_coordinador.at[idx, 'Estado'] = nuevo_estado
                guardar_datos(df_coordinador)
                st.rerun()
