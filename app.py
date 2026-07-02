# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import os
import csv
from PIL import Image
import io
import time
import sys

matplotlib.style.use('ggplot')
st.set_page_config(page_title="Tacho Inteligente", layout="wide", page_icon="♻️")

CSS = """
<style>
.stApp { background: #f0f2f6; }
.main .block-container { padding-top: 1.5rem; }
h1 { color: #2C3E50; font-size: 2rem; }
h2 { color: #2C3E50; font-size: 1.3rem; }
.card { background: white; border-radius: 12px; padding: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem; }
.result-box { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,0.1); text-align: center; border-left: 5px solid #4ECDC4; }
.material-badge { font-size: 1.8rem; font-weight: 800; letter-spacing: 2px; }
.metric-card { background: white; border-radius: 10px; padding: 0.8rem; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.metric-card label { font-size: 0.75rem; color: #888; }
.metric-card .value { font-size: 1.4rem; font-weight: 700; color: #2C3E50; }
div[data-testid="stButton"] button { border-radius: 8px; font-weight: 600; height: 2.8rem; }
div[data-testid="stButton"] button[kind="primary"] { background: #2C3E50; color: white; border: none; }
div[data-testid="stButton"] button[kind="primary"]:hover { background: #1a252f; }
.stCameraInput { border-radius: 12px; overflow: hidden; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

MODEL_PATH = "modelo/tacho_ia.h5"
CSV_PATH = "registros.csv"
CLASSES = ["glass", "metal", "paper", "plastic", "trash"]
NAMES_ES = {"glass": "Vidrio", "metal": "Metal", "paper": "Papel", "plastic": "Plástico", "trash": "Desecho"}
ICONS = {"glass": "🥃", "metal": "🔩", "paper": "📄", "plastic": "🧴", "trash": "🗑️"}
COLORS = {"glass": "#4ECDC4", "metal": "#95E1D3", "paper": "#F38181", "plastic": "#FFE156", "trash": "#AA96DA"}
BG_COLORS = {"glass": "#E8F8F5", "metal": "#F0FDF9", "paper": "#FEF0EF", "plastic": "#FFFBE6", "trash": "#F5F0FF"}

def load_model_lazy():
    if not os.path.exists(MODEL_PATH):
        return None
    import tensorflow as tf
    return tf.keras.models.load_model(MODEL_PATH)

_model = None
def get_model():
    global _model
    if _model is None:
        _model = load_model_lazy()
    return _model

def predecir(imagen_pil):
    modelo = get_model()
    if modelo is None:
        return None, 0
    img = imagen_pil.resize((224, 224))
    arr = np.array(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    pred = modelo.predict(arr, verbose=0)
    idx = np.argmax(pred[0])
    return CLASSES[idx], float(pred[0][idx] * 100)

def guardar_registro(categoria, confianza):
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.now(), categoria, f"{confianza:.1f}"])

def cargar_datos():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    df = pd.read_csv(CSV_PATH, names=["fecha", "categoria", "confianza"], header=None)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df.dropna(subset=["fecha"])
    df["confianza"] = pd.to_numeric(df["confianza"], errors="coerce")
    df["dia"] = df["fecha"].dt.date
    df["hora"] = df["fecha"].dt.hour
    return df

for key in ["cam_on", "captura_img", "result", "saved"]:
    if key not in st.session_state:
        st.session_state[key] = False if key in ["cam_on", "saved"] else None

# ---------- NAV ----------
st.sidebar.markdown("<h2 style='text-align:center;color:#2C3E50;'>♻️ Tacho<br>Inteligente</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
pagina = st.sidebar.radio("", ["📷 Clasificar", "📊 Dashboard"], label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.caption("IA para reciclaje")

# ===================== CLASIFICAR =====================
def pagina_clasificar():
    st.markdown("<h1>📷 Clasificar Residuo</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666;margin-top:-10px'>Captura un residuo con la cámara y la IA lo identificará</p>", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if not st.session_state.cam_on:
            if st.button("📷 Activar cámara", type="primary", use_container_width=True):
                st.session_state.cam_on = True
                st.rerun()
        else:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("❌ Cerrar cámara", use_container_width=True):
                    st.session_state.cam_on = False
                    st.session_state.captura_img = None
                    st.session_state.result = None
                    st.session_state.saved = False
                    st.rerun()
            with col_b:
                if st.session_state.captura_img is not None and st.session_state.result is None:
                    st.caption("Listo para clasificar")
                elif st.session_state.result is not None:
                    st.caption("Resultado listo")

            st.caption("Enfoca el residuo y presiona el botón circular 📸")
            img_data = st.camera_input("", key="cam_feed")
            if img_data is not None:
                st.session_state.captura_img = Image.open(io.BytesIO(img_data.getvalue()))
                st.session_state.result = None
                st.session_state.saved = False

        if st.session_state.captura_img is not None:
            st.image(st.session_state.captura_img, width=280, caption="Captura")
            if st.session_state.result is None:
                if st.button("🔍 Clasificar material", type="primary", use_container_width=True):
                    with st.spinner("Cargando modelo y analizando..."):
                        time.sleep(0.5)
                        cat, conf = predecir(st.session_state.captura_img)
                    if cat is None:
                        st.error("Modelo no encontrado. Ejecuta 'entrenar.py' primero.")
                    else:
                        st.session_state.result = (cat, conf)
                        st.session_state.saved = False
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Resultado")
        if st.session_state.result is None:
            if not st.session_state.cam_on:
                st.info("👆 Activa la cámara")
            elif st.session_state.captura_img is None:
                st.info("📸 Captura un residuo")
            else:
                st.info("🔍 Presiona 'Clasificar material'")
        else:
            cat, conf = st.session_state.result
            clr = COLORS.get(cat, "#888")
            bg = BG_COLORS.get(cat, "#fff")
            nombre_es = NAMES_ES.get(cat, cat)
            icono = ICONS.get(cat, "♻️")

            st.markdown(f"""
            <div class='result-box' style='border-left-color:{clr};background:{bg}'>
                <div style='font-size:3rem'>{icono}</div>
                <div class='material-badge' style='color:{clr}'>{nombre_es}</div>
                <div style='color:#999;text-transform:uppercase;font-size:0.8rem;letter-spacing:2px'>{cat}</div>
                <div style='margin:15px 0'>
                    <div style='font-size:0.8rem;color:#888'>Confianza</div>
                    <div style='font-size:2rem;font-weight:800;color:{clr}'>{conf:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if conf >= 70:
                st.success("✅ Clasificación confiable")
            elif conf >= 40:
                st.warning("⚠️ Confianza media, verifica")
            else:
                st.error("❌ Baja confianza, intenta de nuevo")

            if not st.session_state.saved:
                if st.button("💾 Guardar registro", type="primary", use_container_width=True):
                    guardar_registro(cat, conf)
                    st.session_state.saved = True
                    st.rerun()
            else:
                st.success("✔️ Guardado en el Dashboard")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📋 Últimos registros")
    df = cargar_datos()
    if len(df) > 0:
        ult = df.tail(5).iloc[::-1][["fecha", "categoria", "confianza"]].copy()
        ult["categoria"] = ult["categoria"].map(lambda c: f"{ICONS.get(c,'')} {NAMES_ES.get(c,c)}")
        ult["confianza"] = ult["confianza"].apply(lambda x: f"{x:.1f}%")
        ult["fecha"] = ult["fecha"].dt.strftime("%H:%M  %d/%m/%Y")
        ult.columns = ["Fecha", "Material", "Confianza"]
        st.dataframe(ult, width=550)
    else:
        st.caption("Sin registros todavía")

# ===================== DASHBOARD =====================
def pagina_dashboard():
    st.markdown("<h1>📊 Dashboard de Reciclaje</h1>", unsafe_allow_html=True)
    df = cargar_datos()
    if len(df) == 0:
        st.warning("No hay registros. Clasifica residuos en la sección 📷 Clasificar")
        return

    total = len(df)
    prom_conf = df["confianza"].mean()
    count_hoy = len(df[df["dia"] == datetime.now().date()])
    mejor_cat = df["categoria"].mode().iloc[0]
    nombre_top = NAMES_ES.get(mejor_cat, mejor_cat)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='metric-card'><label>Total</label><div class='value'>{total}</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><label>Confianza Prom.</label><div class='value'>{prom_conf:.1f}%</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><label>Registros Hoy</label><div class='value'>{count_hoy}</div></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='metric-card'><label>Más Reciclado</label><div class='value'>{nombre_top}</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    ca, cb = st.columns(2)

    with ca:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Residuos por Categoría")
        conteo = df["categoria"].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        colores_lista = [COLORS.get(c, "#888") for c in conteo.index]
        bars = ax.bar(conteo.index, conteo.values, color=colores_lista, edgecolor="white", linewidth=0.5, width=0.6)
        for b, v in zip(bars, conteo.values):
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, str(v), ha="center", fontweight="bold", fontsize=12)
        ax.set_ylabel("Cantidad")
        ax.set_xticklabels([NAMES_ES.get(c,c) for c in conteo.index])
        fig.tight_layout()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with cb:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Distribución")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        colores_pie = [COLORS.get(c, "#888") for c in conteo.index]
        wedges, texts, autotexts = ax2.pie(
            conteo.values, labels=[NAMES_ES.get(c,c) for c in conteo.index],
            autopct="%1.1f%%", colors=colores_pie, startangle=90,
            wedgeprops={"edgecolor":"white","linewidth":1}
        )
        for at in autotexts:
            at.set_fontweight("bold")
            at.set_fontsize(11)
        ax2.axis("equal")
        fig2.tight_layout()
        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Tendencia Temporal")
    trend = df.groupby("dia").size().reset_index(name="cantidad")
    fig3, ax3 = plt.subplots(figsize=(12, 3.5))
    ax3.fill_between(range(len(trend)), trend["cantidad"], alpha=0.25, color="#4ECDC4")
    ax3.plot(range(len(trend)), trend["cantidad"], marker="o", color="#2C3E50", linewidth=2.5, markersize=7)
    ax3.set_xticks(range(len(trend)))
    ax3.set_xticklabels(trend["dia"].astype(str), rotation=45, ha="right")
    ax3.set_ylabel("Registros")
    fig3.tight_layout()
    st.pyplot(fig3)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Todos los Registros")
    show = df[["fecha", "categoria", "confianza"]].sort_values("fecha", ascending=False).copy()
    show["categoria"] = show["categoria"].map(lambda c: f"{ICONS.get(c,'')} {NAMES_ES.get(c,c)}")
    show["confianza"] = show["confianza"].apply(lambda x: f"{x:.1f}%")
    show["fecha"] = show["fecha"].dt.strftime("%Y-%m-%d %H:%M:%S")
    show.columns = ["Fecha", "Material", "Confianza"]
    st.dataframe(show, width=700)
    csv_data = show.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar CSV", data=csv_data, file_name="registros.csv", mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

if pagina == "📷 Clasificar":
    pagina_clasificar()
else:
    pagina_dashboard()
