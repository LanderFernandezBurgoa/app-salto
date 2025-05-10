import streamlit as st
import cv2
import numpy as np

# Cargar el video
video_path = "ruta_a_tu_video.mp4"  # Cambia esto a la ubicación de tu video
cap = cv2.VideoCapture(video_path)

# Inicializar el contador de frames
frame_idx = 0

# Obtener el número total de frames en el video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

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
