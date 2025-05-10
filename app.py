import streamlit as st
import cv2
import tempfile
import numpy as np

st.title("Análisis de salto en video")

uploaded_file = st.file_uploader("Sube un video (.mp4)", type=["mp4"])

if uploaded_file is not None:
    # Guardar archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        video_path = tmp_file.name

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    st.write(f"FPS: {fps}, Total de frames: {total_frames}")

    # Inicializar session_state si no existe
    for key, default in [("frame_inicio", 0), ("frame_fin", total_frames - 1), ("frame_actual", 0)]:
        if key not in st.session_state:
            st.session_state[key] = default

    # Función para controlar los sliders con botones
    def frame_control(label, key):
        col1, col2, col3 = st.columns([1, 6, 1])

        with col1:
            if st.button("◀", key=key + "_menos"):
                if st.session_state[key] > 0:
                    st.session_state[key] -= 1

        # Mostramos slider con valor temporal (sin vincular directamente a session_state)
        with col2:
            temp_val = st.slider(
                label,
                0,
                total_frames - 1,
                st.session_state[key],
                key=key + "_slider"
            )
            st.session_state[key] = temp_val

        with col3:
            if st.button("▶", key=key + "_mas"):
                if st.session_state[key] < total_frames - 1:
                    st.session_state[key] += 1

    # Usamos la función para los tres controles
    frame_control("Frame de despegue (inicio)", "frame_inicio")
    frame_control("Frame de aterrizaje (final)", "frame_fin")
    frame_control("Ver frame", "frame_actual")

    # Mostrar frame actual
    cap.set(cv2.CAP_PROP_POS_FRAMES, st.session_state.frame_actual)
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, caption=f"Frame {st.session_state.frame_actual}", use_column_width=True)
    cap.release()

    # Cálculo del salto
    if st.session_state.frame_fin > st.session_state.frame_inicio:
        tiempo_vuelo = (st.session_state.frame_fin - st.session_state.frame_inicio) / fps
        g = 9.81
        altura = (g * tiempo_vuelo ** 2) / 8
        st.markdown(f"**Tiempo de vuelo:** {tiempo_vuelo:.3f} segundos")
        st.markdown(f"**Altura estimada del salto:** {altura:.2f} metros")
    else:
        st.warning("El frame final debe ser posterior al inicial")
else:
    st.info("Por favor, sube un video en formato .mp4 para comenzar.")
