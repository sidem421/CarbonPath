import streamlit as st
import json
import os

# SAYFA AYARI
st.set_page_config(page_title="CarbonPath", page_icon="🌍")

# DOSYA YOLU (HATA ÇÖZÜMÜ BURADA)
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "data", "carbon_data.json")

# JSON YÜKLE
with open(file_path) as f:
    data = json.load(f)

# CSS
st.markdown("""
<style>
body { background-color: #0e1117; }
.title { text-align:center; font-size:40px; color:#00ffcc; }
.creator { position:fixed; top:10px; right:20px; color:white; }
</style>
""", unsafe_allow_html=True)

# SAĞ ÜST
st.markdown('<div class="creator">Melis&Azra</div>', unsafe_allow_html=True)

# SESSION
if "state" not in st.session_state:
    st.session_state.state = "start"
    st.session_state.score = 0
    st.session_state.carbon = 50

state = st.session_state.state

# BAŞLANGIÇ
if state == "start":
    st.markdown('<div class="title">🌍 CarbonPath</div>', unsafe_allow_html=True)
    st.write("Karbon döngüsünü deneyimle!")

    if st.button("🚀 Başla"):
        st.session_state.state = "atmosfer"

# ATMOSFER
elif state == "atmosfer":
    st.header("🌫️ Atmosfer")
    
    if st.button("🌱 Bitkiye git"):
        st.session_state.state = "bitki"
        st.session_state.carbon -= data["fotosentez_azalis"]
        st.session_state.score += 10

    if st.button("🌊 Okyanusa git"):
        st.session_state.state = "okyanus"
        st.session_state.carbon -= data["okyanus_emilim"]
        st.session_state.score += 5

# BİTKİ
elif state == "bitki":
    st.header("🌿 Bitki")

    if st.button("🐄 Hayvana geç"):
        st.session_state.state = "hayvan"
        st.session_state.score += 5

    if st.button("💨 Atmosfere dön"):
        st.session_state.state = "atmosfer"
        st.session_state.carbon += data["solunum_artis"]

# HAYVAN
elif state == "hayvan":
    st.header("🐾 Hayvan")

    if st.button("💀 Toprağa karış"):
        st.session_state.state = "toprak"
        st.session_state.score += 10

    if st.button("💨 Atmosfere dön"):
        st.session_state.state = "atmosfer"
        st.session_state.carbon += data["solunum_artis"]

# TOPRAK
elif state == "toprak":
    st.header("🌱 Toprak")

    if st.button("🦠 Atmosfere dön"):
        st.session_state.state = "atmosfer"
        st.session_state.carbon += data["toprak_salınım"]

# OKYANUS
elif state == "okyanus":
    st.header("🌊 Okyanus")

    if st.button("💨 Atmosfere dön"):
        st.session_state.state = "atmosfer"
        st.session_state.carbon += data["atmosfer_artis"]

# SON KONTROL
if st.session_state.score >= 40:
    st.session_state.state = "good_end"

if st.session_state.carbon >= 80:
    st.session_state.state = "bad_end"

# İYİ SON
if st.session_state.state == "good_end":
    st.success("🌱 Harika! Doğayı korudun!")
    st.write("Karbon dengede tutuldu.")

    if st.button("🔄 Tekrar Oyna"):
        st.session_state.clear()

# KÖTÜ SON
elif st.session_state.state == "bad_end":
    st.error("🔥 Karbon kontrolden çıktı!")
    st.write("Küresel ısınma arttı.")

    if st.button("🔄 Tekrar Dene"):
        st.session_state.clear()

# ALT PANEL
st.markdown("---")
st.write(f"🎯 Puan: {st.session_state.score}")
st.write(f"📊 Karbon: {round(st.session_state.carbon,1)}")

st.progress(min(int(st.session_state.carbon), 100))
