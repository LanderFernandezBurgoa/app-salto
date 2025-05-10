import streamlit as st
import cv2
import numpy as np

# Ruta al archivo de video
st.title("Análisis de salto en video")

uploaded_file = st.file_uploader("Sube un video (.mp4)", type=["mp4"])

# Intentar abrir el video
cap = cv2.VideoCapture(video_path)

# Verificar si el video se abrió correctamente
if not cap.isOpened():
    st.error("Error al cargar el video. Asegúrate de que la ruta sea correcta y el video esté accesible.")
    st.stop()

# Obtener el número total de frames en el video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Comprobar si el video tiene frames válidos
if total_frames <= 0:
    st.error("El video no contiene frames o no se puede leer correctamente.")
    st.stop()

# Función para mostrar un frame específico
def show_frame(frame_idx):
    # Establecer la posición del frame en el video
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()

    if ret:
        # Convertir el frame de BGR a RGB (OpenCV usa BGR por defecto)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, channels="RGB", use_column_width=True)
    else:
        st.error("No se pudo leer el frame en el índice: " + str(frame_idx))

# Inicializar el índice del frame
frame_idx = 0

# Mostrar el primer frame al inicio
show_frame(frame_idx)

# Controles para avanzar y retroceder en los frames
col1, col2 = st.columns(2)

with col1:
    if st.button("Retroceder") and frame_idx > 0:
        frame_idx -= 1
        show_frame(frame_idx)

with col2:
    if st.button("Avanzar") and frame_idx < total_frames - 1:
        frame_idx += 1
        show_frame(frame_idx)

# Seleccionar el rango de frames en el sidebar
st.sidebar.header("Selecciona un rango de frames")

# Seleccionar frame inicial y final con validaciones
start_frame = st.sidebar.number_input("Frame inicial", min_value=0, max_value=total_frames-1, value=0)
end_frame = st.sidebar.number_input("Frame final", min_value=start_frame, max_value=total_frames-1, value=total_frames-1)

# Botón para mostrar frames entre el rango
if st.sidebar.button("Mostrar frames en el rango"):
    for i in range(start_frame, end_frame + 1):
        show_frame(i)

# Cerrar el objeto de captura de video cuando terminamos
cap.release()
