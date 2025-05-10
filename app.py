import streamlit as st
import cv2
import numpy as np

# Cargar el video
video_path = "video.mp4"  # Cambia esto a la ubicación de tu video
cap = cv2.VideoCapture(video_path)

# Comprobar si el video se cargó correctamente
if not cap.isOpened():
    st.error("Error al cargar el video. Asegúrate de que la ruta es correcta y que el video está disponible.")
    st.stop()

# Obtener el número total de frames en el video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Comprobar si el número total de frames es válido
if total_frames <= 0:
    st.error("El video no tiene frames o no se puede leer correctamente.")
    st.stop()

# Inicializar el contador de frames
frame_idx = 0

# Función para mostrar el frame en la aplicación
def show_frame(frame_idx):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if ret:
        # Convertir el frame de BGR a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, channels="RGB", use_column_width=True)
    else:
        st.error("No se puede leer el frame. Intenta con otro video o verifica el archivo.")
        st.stop()

# Mostrar el primer frame
show_frame(frame_idx)

# Botones para avanzar y retroceder
col1, col2 = st.columns(2)

with col1:
    if st.button("Retroceder"):
        if frame_idx > 0:
            frame_idx -= 1
            show_frame(frame_idx)

with col2:
    if st.button("Avanzar"):
        if frame_idx < total_frames - 1:
            frame_idx += 1
            show_frame(frame_idx)

# Opción para seleccionar el frame inicial y final
st.sidebar.header("Selecciona el
