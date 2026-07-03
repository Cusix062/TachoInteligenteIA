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
import requests
import json

matplotlib.style.use('dark_background')
st.set_page_config(page_title="Tacho Inteligente", layout="wide", page_icon="♻️")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { 
    background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%);
}
.main .block-container { padding-top: 1.5rem; }
h1 { 
    color: #e0e0e0 !important; 
    font-size: 2rem !important; 
    font-weight: 800 !important;
    background: linear-gradient(90deg, #00d09c, #00b4d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem !important;
}
h2 { color: #c0c0d0 !important; font-size: 1.3rem !important; font-weight: 700 !important; }
h3 { color: #a0a0b8 !important; font-size: 1rem !important; font-weight: 600 !important; }
p, label, .caption, .stCaption { color: #8888aa !important; }

.card { 
    background: rgba(30, 30, 60, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 1.2rem;
    transition: transform 0.2s ease;
}
.card:hover { transform: translateY(-2px); }

.result-box {
    background: rgba(25, 25, 55, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    text-align: center;
    border-left: 5px solid #00d09c;
}
.material-badge { 
    font-size: 2rem; 
    font-weight: 800; 
    letter-spacing: 3px; 
    text-transform: uppercase;
}
.metric-card { 
    background: rgba(30, 30, 65, 0.7);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; 
    padding: 1.2rem 0.8rem; 
    text-align: center; 
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    transition: all 0.2s ease;
}
.metric-card:hover {
    border-color: rgba(0, 208, 156, 0.3);
    box-shadow: 0 4px 24px rgba(0, 208, 156, 0.15);
}
.metric-card label { font-size: 0.7rem; color: #6666aa; text-transform: uppercase; letter-spacing: 1.5px; }
.metric-card .value { font-size: 1.6rem; font-weight: 800; color: #e0e0f0; }

div[data-testid="stButton"] button {
    border-radius: 10px;
    font-weight: 600;
    height: 2.8rem;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(30, 30, 60, 0.6);
    color: #c0c0d0;
    transition: all 0.2s ease;
}
div[data-testid="stButton"] button:hover {
    background: rgba(50, 50, 90, 0.8);
    border-color: rgba(0, 208, 156, 0.4);
    color: white;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #00d09c, #00b4d8);
    color: white;
    border: none;
    font-weight: 700;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background: linear-gradient(135deg, #00e8ad, #00c8ee);
    box-shadow: 0 4px 20px rgba(0, 208, 156, 0.3);
}
.stCameraInput {
    border-radius: 16px;
    overflow: hidden;
    border: 2px solid rgba(255,255,255,0.08);
}
div[data-testid="stCameraInput"] {
    border-radius: 16px;
    overflow: hidden;
}
.stCameraInput > div {
    border: none !important;
    border-radius: 16px;
}
.stSidebar {
    background: rgba(10, 10, 25, 0.95);
    border-right: 1px solid rgba(255,255,255,0.05);
}
.stSidebar .sidebar-content {
    background: transparent;
}
.stSidebar h2 {
    color: #e0e0f0 !important;
}
div[data-testid="stSidebarNav"] { display: none; }
section[data-testid="stSidebar"] div[role="radiogroup"] {
    background: transparent;
    border: none;
    gap: 4px;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(20, 20, 50, 0.5);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 12px 16px;
    transition: all 0.2s ease;
    color: #8888bb;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(30, 30, 70, 0.8);
    border-color: rgba(0, 208, 156, 0.2);
    color: #e0e0f0;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
    background: rgba(0, 208, 156, 0.15);
    border-color: rgba(0, 208, 156, 0.4);
    color: #00d09c;
}
.stAlert {
    border-radius: 12px;
    border: none;
}
div.stSuccess {
    background: rgba(0, 208, 156, 0.1);
    border: 1px solid rgba(0, 208, 156, 0.2);
    color: #00d09c;
}
div.stWarning {
    background: rgba(255, 193, 7, 0.1);
    border: 1px solid rgba(255, 193, 7, 0.2);
    color: #ffc107;
}
div.stError {
    background: rgba(220, 53, 69, 0.1);
    border: 1px solid rgba(220, 53, 69, 0.2);
    color: #dc3545;
}
div.stInfo {
    background: rgba(0, 180, 216, 0.1);
    border: 1px solid rgba(0, 180, 216, 0.2);
    color: #00b4d8;
}
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
div[data-testid="stDataFrame"] table {
    background: rgba(20, 20, 50, 0.5);
}
div[data-testid="stDataFrame"] th {
    background: rgba(0, 208, 156, 0.15);
    color: #c0c0e0;
    font-weight: 600;
}
div[data-testid="stDataFrame"] td {
    color: #a0a0c0;
    background: transparent;
}
hr {
    border-color: rgba(255,255,255,0.05);
    margin: 1.5rem 0;
}
div[data-testid="stDownloadButton"] button {
    background: rgba(30, 30, 60, 0.6);
    border: 1px solid rgba(0, 208, 156, 0.3);
    color: #00d09c;
}
div[data-testid="stDownloadButton"] button:hover {
    background: rgba(0, 208, 156, 0.15);
    border-color: #00d09c;
}
.stSpinner {
    color: #00d09c !important;
}
.stSpinner > div {
    border-color: #00d09c transparent transparent transparent !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

MODEL_PATH = "modelo/tacho_ia.h5"
CSV_PATH = "registros.csv"
CLASSES = ["glass", "metal", "paper", "plastic", "trash"]
NAMES_ES = {"glass": "Vidrio", "metal": "Metal", "paper": "Papel", "plastic": "Plástico", "trash": "Desecho"}
ICONS = {"glass": "🥃", "metal": "🔩", "paper": "📄", "plastic": "🧴", "trash": "🗑️"}
COLORS = {"glass": "#00d09c", "metal": "#00b4d8", "paper": "#f77f7f", "plastic": "#ffd93d", "trash": "#b388ff"}
BG_COLORS = {"glass": "rgba(0,208,156,0.08)", "metal": "rgba(0,180,216,0.08)", "paper": "rgba(247,127,127,0.08)", "plastic": "rgba(255,217,61,0.08)", "trash": "rgba(179,136,255,0.08)"}

API_KEY = "a4a-rLkO16xPuGROqeunvaebwxXaMdazS7Z3"
API_URL = "https://api4ai.cloud/general-cls/v1/results"

# ImageNet class -> (waste_category, confidence_weight)
IMAGENET_MAP = {
    "beer glass": ("glass", 1.0), "wine bottle": ("glass", 0.8),
    "beer bottle": ("glass", 0.8), "pop bottle": ("glass", 0.3),
    "cocktail shaker": ("glass", 0.6), "vase": ("glass", 0.6),
    "jar": ("glass", 0.7), "goblet": ("glass", 1.0),
    "wine glass": ("glass", 1.0), "cup": ("glass", 0.3),
    "bottle": ("glass", 0.5), "water bottle": ("glass", 0.2),
    "can": ("metal", 1.0), "milk can": ("metal", 1.0),
    "tin can": ("metal", 1.0), "beer can": ("metal", 1.0),
    "screw": ("metal", 0.8), "chain": ("metal", 0.7),
    "padlock": ("metal", 0.8), "key": ("metal", 0.8),
    "paper towel": ("paper", 1.0), "toilet tissue": ("paper", 1.0),
    "envelope": ("paper", 1.0), "cardboard": ("paper", 0.9),
    "carton": ("paper", 0.7), "box": ("paper", 0.4),
    "book": ("paper", 0.7), "magazine": ("paper", 0.9),
    "newspaper": ("paper", 1.0), "napkin": ("paper", 1.0),
    "paperback": ("paper", 0.7), "notebook": ("paper", 0.6),
    "plastic bag": ("plastic", 1.0), "grocery bag": ("plastic", 0.7),
    "garbage bag": ("plastic", 0.6), "bottlecap": ("plastic", 0.5),
    "bucket": ("plastic", 0.5), "straw": ("plastic", 0.8),
    "shampoo": ("plastic", 0.7), "toothbrush": ("plastic", 0.8),
    "toothpaste": ("plastic", 0.6), "balloon": ("plastic", 0.6),
    "soap dispenser": ("plastic", 0.4), "spatula": ("plastic", 0.3),
    "trash can": ("trash", 1.0), "garbage can": ("trash", 1.0),
    "dustbin": ("trash", 1.0), "cigarette": ("trash", 1.0),
    "cigarette butt": ("trash", 1.0), "diaper": ("trash", 0.9),
    "ashcan": ("trash", 1.0), "sponge": ("trash", 0.3),
    "rubber eraser": ("trash", 0.3), "face powder": ("trash", 0.2),
}

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

def predecir_local(imagen_pil):
    modelo = get_model()
    if modelo is None:
        return None, 0
    img = imagen_pil.resize((224, 224))
    arr = np.array(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    pred = modelo.predict(arr, verbose=0)
    idx = np.argmax(pred[0])
    return CLASSES[idx], float(pred[0][idx] * 100)

def predecir_api(imagen_pil):
    buf = io.BytesIO()
    imagen_pil.save(buf, format="JPEG")
    buf.seek(0)
    try:
        resp = requests.post(
            API_URL,
            headers={"X-API-KEY": API_KEY},
            files={"image": ("image.jpg", buf, "image/jpeg")},
            timeout=15
        )
        if resp.status_code != 200:
            return None, 0
        data = resp.json()
        classes = data["results"][0]["entities"][0]["classes"]
        scores = {}
        for cls, score in classes.items():
            if cls in IMAGENET_MAP:
                cat, weight = IMAGENET_MAP[cls]
                scores[cat] = scores.get(cat, 0) + score * weight
            elif "bottle" in cls or "glass" in cls:
                scores["glass"] = scores.get("glass", 0) + score * 0.3
            elif "can" in cls or "metal" in cls or "tin" in cls:
                scores["metal"] = scores.get("metal", 0) + score * 0.3
            elif "paper" in cls or "cardboard" in cls or "carton" in cls:
                scores["paper"] = scores.get("paper", 0) + score * 0.3
            elif "plastic" in cls or "bag" in cls:
                scores["plastic"] = scores.get("plastic", 0) + score * 0.3
            elif "trash" in cls or "garbage" in cls or "waste" in cls:
                scores["trash"] = scores.get("trash", 0) + score * 0.3
        if not scores:
            top_cls = max(classes, key=classes.get)
            return "trash", min(classes[top_cls] * 100, 99)
        mejor_cat = max(scores, key=scores.get)
        confianza = min(scores[mejor_cat] * 100, 99)
        return mejor_cat, confianza
    except:
        return None, 0

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

for key in ["cam_on", "captura_img", "result", "saved", "use_api"]:
    if key not in st.session_state:
        if key == "use_api":
            st.session_state[key] = not os.path.exists(MODEL_PATH)
        else:
            st.session_state[key] = False if key in ["cam_on", "saved"] else None

# ---------- NAV ----------
st.sidebar.markdown("""
<div style='text-align:center;padding:10px 0'>
    <div style='font-size:2.5rem;margin-bottom:5px'>♻️</div>
    <div style='font-size:1.2rem;font-weight:800;background:linear-gradient(90deg,#00d09c,#00b4d8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>Tacho Inteligente</div>
    <div style='font-size:0.7rem;color:#5555aa;margin-top:2px'>IA para reciclaje</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
pagina = st.sidebar.radio("", ["📷 Clasificar", "📊 Dashboard"], label_visibility="collapsed")
st.sidebar.markdown("---")

modelo_disponible = os.path.exists(MODEL_PATH)
if modelo_disponible:
    use_api = st.sidebar.toggle("☁️ Usar API en la nube", value=st.session_state.use_api)
    if use_api != st.session_state.use_api:
        st.session_state.use_api = use_api
        st.rerun()
    modo = "API ☁️" if st.session_state.use_api else "Local 🖥️"
else:
    st.session_state.use_api = True
    modo = "API ☁️"
    st.sidebar.info("📡 Modo API en la nube activado")

st.sidebar.markdown(f"<div style='font-size:0.7rem;color:#5555aa;text-align:center;padding:5px'>Modo: {modo}</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size:0.65rem;color:#444477;text-align:center;padding:10px'>API4AI + Streamlit</div>", unsafe_allow_html=True)

# ===================== CLASIFICAR =====================
def pagina_clasificar():
    st.markdown("<h1>Clasificar Residuo</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6666aa;margin-top:-10px;margin-bottom:20px'>Captura un residuo con la cámara y la IA lo identificará al instante</p>", unsafe_allow_html=True)

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
                    st.caption("📸 Listo para clasificar")
                elif st.session_state.result is not None:
                    st.caption("✅ Resultado listo")

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
                    with st.spinner("Analizando..."):
                        time.sleep(0.3)
                        if st.session_state.use_api:
                            cat, conf = predecir_api(st.session_state.captura_img)
                        else:
                            cat, conf = predecir_local(st.session_state.captura_img)
                    if cat is None:
                        st.error("No se pudo clasificar. Intenta de nuevo.")
                    else:
                        st.session_state.result = (cat, conf)
                        st.session_state.saved = False
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.8rem;color:#6666aa;text-transform:uppercase;letter-spacing:2px;margin-bottom:10px'>Resultado</div>", unsafe_allow_html=True)
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
                <div style='font-size:3.5rem;margin-bottom:5px'>{icono}</div>
                <div class='material-badge' style='color:{clr}'>{nombre_es}</div>
                <div style='color:#5555aa;text-transform:uppercase;font-size:0.75rem;letter-spacing:2px;margin-top:4px'>{cat}</div>
                <div style='margin:18px 0'>
                    <div style='font-size:0.75rem;color:#5555aa;text-transform:uppercase;letter-spacing:1px'>Confianza</div>
                    <div style='font-size:2.2rem;font-weight:800;color:{clr}'>{conf:.1f}%</div>
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
    st.markdown("<div style='font-size:1rem;font-weight:600;color:#c0c0e0;margin-bottom:10px'>📋 Últimos registros</div>", unsafe_allow_html=True)
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
    st.markdown("<h1>Dashboard de Reciclaje</h1>", unsafe_allow_html=True)
    df = cargar_datos()
    if len(df) == 0:
        st.markdown("<div class='card' style='text-align:center;padding:3rem'>", unsafe_allow_html=True)
        st.warning("No hay registros. Clasifica residuos en la sección 📷 Clasificar")
        st.markdown("</div>", unsafe_allow_html=True)
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
        st.markdown("<div style='font-size:0.9rem;font-weight:600;color:#c0c0e0;margin-bottom:10px'>Residuos por Categoría</div>", unsafe_allow_html=True)
        conteo = df["categoria"].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')
        colores_lista = [COLORS.get(c, "#888") for c in conteo.index]
        bars = ax.bar(conteo.index, conteo.values, color=colores_lista, edgecolor="none", width=0.6, alpha=0.9)
        for b, v in zip(bars, conteo.values):
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, str(v), ha="center", fontweight="bold", fontsize=13, color="#c0c0e0")
        ax.set_ylabel("Cantidad", color="#6666aa")
        ax.set_xticklabels([NAMES_ES.get(c,c) for c in conteo.index], color="#8888bb")
        ax.tick_params(colors="#6666aa")
        for spine in ax.spines.values():
            spine.set_color("rgba(255,255,255,0.05)")
        ax.yaxis.grid(True, alpha=0.1, color="#ffffff")
        fig.tight_layout()
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with cb:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.9rem;font-weight:600;color:#c0c0e0;margin-bottom:10px'>Distribución</div>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        fig2.patch.set_alpha(0)
        ax2.set_facecolor('none')
        colores_pie = [COLORS.get(c, "#888") for c in conteo.index]
        wedges, texts, autotexts = ax2.pie(
            conteo.values, labels=[NAMES_ES.get(c,c) for c in conteo.index],
            autopct="%1.1f%%", colors=colores_pie, startangle=90,
            wedgeprops={"edgecolor":"none","linewidth":0},
            textprops={'color': '#c0c0e0', 'fontweight': 'bold', 'fontsize': 11}
        )
        for at in autotexts:
            at.set_fontweight("bold")
            at.set_fontsize(11)
            at.set_color("#1a1a2e")
        ax2.axis("equal")
        fig2.tight_layout()
        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.9rem;font-weight:600;color:#c0c0e0;margin-bottom:10px'>Tendencia Temporal</div>", unsafe_allow_html=True)
    trend = df.groupby("dia").size().reset_index(name="cantidad")
    fig3, ax3 = plt.subplots(figsize=(12, 3.5))
    fig3.patch.set_alpha(0)
    ax3.set_facecolor('none')
    ax3.fill_between(range(len(trend)), trend["cantidad"], alpha=0.2, color="#00d09c")
    ax3.plot(range(len(trend)), trend["cantidad"], marker="o", color="#00b4d8", linewidth=2.5, markersize=7, markerfacecolor="#00d09c", markeredgecolor="none")
    ax3.set_xticks(range(len(trend)))
    ax3.set_xticklabels(trend["dia"].astype(str), rotation=45, ha="right", color="#8888bb")
    ax3.set_ylabel("Registros", color="#6666aa")
    ax3.tick_params(colors="#6666aa")
    for spine in ax3.spines.values():
        spine.set_color("rgba(255,255,255,0.05)")
    ax3.yaxis.grid(True, alpha=0.1, color="#ffffff")
    fig3.tight_layout()
    st.pyplot(fig3)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.9rem;font-weight:600;color:#c0c0e0;margin-bottom:10px'>Todos los Registros</div>", unsafe_allow_html=True)
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
