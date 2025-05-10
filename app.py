import streamlit as st
import cv2
import tempfile
import numpy as np

st.title("Análisis de salto en video")

uploaded_file = st.file_uploader("Sube un video (.mp4)", type=["mp4"])

if uploaded_file:
    # Guardar archivo temporalmente
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    st.write(f"FPS: {fps}, Total de frames: {total_frames}")

    # Selección de frames
    frame_inicio = st.slider("Frame de despegue (inicio)", 0, total_frames - 1, 0)
    frame_fin = st.slider("Frame de aterrizaje (final)", 0, total_frames - 1, total_frames - 1)

    # Mostrar frame actual
    frame_actual = st.slider("Ver frame", 0, total_frames - 1, 0)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_actual)
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, caption=f"Frame {frame_actual}", use_column_width=True)
    cap.release()

    # Cálculo de salto
    if frame_fin > frame_inicio:
        tiempo_vuelo = (frame_fin - frame_inicio) / fps
        g = 9.81  # m/s²
        altura = (g * tiempo_vuelo**2) / 8
        st.markdown(f"**Tiempo de vuelo:** {tiempo_vuelo:.3f} segundos")
        st.markdown(f"**Altura estimada del salto:** {altura:.2f} metros")
    else:
        st.warning("El frame final debe ser posterior al inicial")