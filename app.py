import streamlit as st
import cv2
import numpy as np

# Cargar el video
video_path = "ruta_a_tu_video.mp4"  # Cambia esto a la ubicación de tu video
cap = cv2.VideoCapture(video_path)

# Comprobar si el video se cargó correctamente
if not cap.isOpened():
    st.error("Error al cargar el video. Asegúrate de que la ruta es correcta y que el video está disponible.")
    st.stop()

# Obtener el número total de frames en el video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

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
        st.error("No se puede leer el frame.")

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
st.sidebar.header("Selecciona el rango de frames")

# Validar que total_frames sea mayor que 1
if total_frames > 1:
    start_frame = st.sidebar.number_input("Frame inicial", min_value=0, max_value=total_frames-1, value=0)
    end_frame = st.sidebar.number_input("Frame final", min_value=start_frame, max_value=total_frames-1, value=total_frames-1)

    # Botón para mostrar los frames entre el rango seleccionado
    if st.sidebar.button("Mostrar frames del rango"):
        for i in range(start_frame, end_frame + 1):
            show_frame(i)
else:
    st.warning("El video no contiene suficientes frames para realizar la operación.")
