import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import os

st.set_page_config(page_title="Tacho Inteligente", layout="wide")
st.title("Tacho Inteligente con IA")
st.markdown("Dashboard de monitoreo de residuos reciclables")

csv_path = "registros.csv"
if not os.path.exists(csv_path):
    st.warning("No hay registros todavia. Usa camara.py para clasificar residuos.")
    st.stop()

df = pd.read_csv(csv_path, names=["fecha", "categoria", "confianza"], header=None)
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
df = df.dropna(subset=["fecha"])
df["confianza"] = pd.to_numeric(df["confianza"], errors="coerce")
df["dia"] = df["fecha"].dt.date
df["hora"] = df["fecha"].dt.hour

total = len(df)
prom_conf = df["confianza"].mean()
hoy = datetime.now().date()
count_hoy = len(df[df["dia"] == hoy])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Registros", total)
col2.metric("Confianza Promedio", f"{prom_conf:.1f}%")
col3.metric("Registros Hoy", count_hoy)

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Residuos por Categoria")
    conteo = df["categoria"].value_counts()
    fig, ax = plt.subplots()
    bars = ax.bar(conteo.index, conteo.values, color=["#4ECDC4", "#95E1D3", "#F38181", "#FFE156", "#AA96DA"])
    for bar, val in zip(bars, conteo.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, str(val), ha="center", fontweight="bold")
    fig.tight_layout()
    st.pyplot(fig)

with col_b:
    st.subheader("Distribucion")
    fig2, ax2 = plt.subplots()
    ax2.pie(conteo.values, labels=conteo.index, autopct="%1.1f%%",
            colors=["#4ECDC4", "#95E1D3", "#F38181", "#FFE156", "#AA96DA"])
    fig2.tight_layout()
    st.pyplot(fig2)

st.divider()

st.subheader("Registros")
st.dataframe(df[["fecha", "categoria", "confianza"]].sort_values("fecha", ascending=False), width=700)
