import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Almacén Comex - Control de Reparto", layout="wide")

EXCEL_FILE = 'Control_Nuevo.xlsx'

# CONFIGURACIÓN DE SEGURIDAD: Cambia aquí la contraseña del coordinador
CLAVE_COORDINADOR = "Comex2026"

def cargar_datos():
    if os.path.exists(EXCEL_FILE):
        try:
            return pd.read_excel(EXCEL_FILE, sheet_name='Captura Pedidos')
        except:
            return pd.DataFrame(columns=['Folio', 'Fecha', 'Hora Pedido', 'Sucursal', 'Cliente', 'Telefono', 'Direccion', 'Colonia', 'Codigo Postal', 'Importe', 'Tipo Pedido', 'Prioridad', 'Repartidor', 'Estado', 'Notas'])
    else:
        return pd.DataFrame(columns=['Folio', 'Fecha', 'Hora Pedido', 'Sucursal', 'Cliente', 'Telefono', 'Direccion', 'Colonia', 'Codigo Postal', 'Importe', 'Tipo Pedido', 'Prioridad', 'Repartidor', 'Estado', 'Notas'])

def guardar_datos(df_nuevos):
    df_nuevos.to_excel(EXCEL_FILE, sheet_name='Captura Pedidos', index=False)

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
            direccion = st.text_input("Dirección Completa (Calle y Número)")
            colonia = st.text_input("Colonia")
            codigo_postal = st.text_input("Código Postal (C.P.)")
            importe = st.number_input("Importe del Pedido ($)", min_value=0.0, step=50.0)
        with col2:
            tipo_pedido = st.selectbox("Tipo de Pedido", TIPOS_PEDIDO)
            prioridad = st.selectbox("Prioridad", PRIORIDADES)
            notas = st.text_area("Notas / Indicaciones Especiales")
            
        enviar = st.form_submit_button("Enviar Pedido al Coordinador")
        if enviar:
            if not cliente or not telefono or not direccion or not colonia:
                st.error("Por favor, llena los campos obligatorios (Cliente, Teléfono, Dirección y Colonia).")
            else:
                df_actual = cargar_datos()
                nuevo_id = len(df_actual) + 1
                folio = f"P{nuevo_id:03d}"
                nuevo_pedido = {
                    'Folio': folio, 'Fecha': datetime.now().strftime('%Y-%m-%d'), 'Hora Pedido': datetime.now().strftime('%H:%M:%S'),
                    'Sucursal': sucursal, 'Cliente': cliente, 'Telefono': telefono, 'Direccion': direccion, 'Colonia': colonia, 'Codigo Postal': codigo_postal, 'Importe': importe, 'Tipo Pedido': tipo_pedido,
                    'Prioridad': prioridad, 'Repartidor': 'Sin Asignar', 'Estado': 'Pendiente', 'Notas': notas
                }
                df_actual = pd.concat([df_actual, pd.DataFrame([nuevo_pedido])], ignore_index=True)
                guardar_datos(df_actual)
                st.success(f"¡Pedido guardado con éxito! Folio: {folio}")

with tab2:
    st.header("Gestión y Despacho de Entregas")
    
    # CANDADO DE SEGURIDAD: Solicitar contraseña
    clave_ingresada = st.text_input("🔑 Ingrese la contraseña de Coordinador para desbloquear este panel:", type="password")
    
    if clave_ingresada == CLAVE_COORDINADOR:
        st.success("🔓 Acceso concedido al Panel de Gestión.")
        df_coordinador = cargar_datos()
        
        if df_coordinador.empty:
            st.info("No hay pedidos registrados por el momento.")
        else:
            col_filtro1, col_filtro2 = st.columns(2)
            
            with col_filtro1:
                fecha_seleccionada = st.date_input("📅 Seleccionar Día de Trabajo:", datetime.now().date())
                fecha_str = fecha_seleccionada.strftime('%Y-%m-%d')
                
            with col_filtro2:
                estado_filtro = st.multiselect("Filtrar por Estado:", ESTADOS, default=['Pendiente', 'Preparando', 'Asignado', 'En Ruta'])
            
            df_filtrado = df_coordinador[df_coordinador['Fecha'] == fecha_str]
            df_filtrado = df_filtrado[df_filtrado['Estado'].isin(estado_filtro)]
            
            st.dataframe(df_filtrado, use_container_width=True)
            
            st.markdown("---")
            st.subheader("⚙️ Actualizar Estatus de Reparto")
            with st.form("actualizar_logistica"):
                col_f, col_r, col_e = st.columns(3)
                with col_f:
                    folios_disponibles = df_filtrado['Folio'].tolist() if not df_filtrado.empty else ["No hay folios en esta fecha"]
                    folio_a_editar = st.selectbox("Selecciona el Folio del Pedido", folios_disponibles)
                with col_r:
                    repartidor_asignado = st.selectbox("Asignar Repartidor", REPARTIDORES)
                with col_e:
                    nuevo_estado = st.selectbox("Cambiar Estado", ESTADOS)
                
                actualizar_btn = st.form_submit_button("Guardar Cambios de Logística")
                if actualizar_btn and folio_a_editar != "No hay folios en esta fecha":
                    df_coordinador.loc[df_coordinador['Folio'] == folio_a_editar, 'Repartidor'] = repartidor_asignado
                    df_coordinador.loc[df_coordinador['Folio'] == folio_a_editar, 'Estado'] = nuevo_estado
                    ahora = datetime.now().strftime('%H:%M:%S')
                    if nuevo_estado == 'En Ruta':
                        df_coordinador.loc[df_coordinador['Folio'] == folio_a_editar, 'Hora Salida'] = ahora
                    elif nuevo_estado == 'Entregado':
                        df_coordinador.loc[df_coordinador['Folio'] == folio_a_editar, 'Hora Entrega'] = ahora
                    guardar_datos(df_coordinador)
                    st.success(f"Pedido {folio_a_editar} actualizado.")
                    st.rerun()
                elif actualizar_btn:
                    st.warning("No hay ningún folio seleccionado para actualizar.")
                    
    elif clave_ingresada != "":
        st.error("❌ Contraseña incorrecta. Acceso denegado a las funciones de despacho.")