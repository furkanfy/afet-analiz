import streamlit as st
import pandas as pd
import os
from streamlit_folium import st_folium
import sys
sys.path.append('C:\\Users\\ASUS\\Documents\\afet-analiz')
from streamlit_app.utils.pipeline import process_dataframe
from streamlit_app.utils.map_utils import lat_lon_bul_fast, create_map, filter_by_date, filter_by_label
# Telegram mesajlarının CSV dosya yolu
DATA_PATH = os.path.join("streamlit_app", "data", "messages.csv")

st.set_page_config(layout="wide")
st.title("🆘 Afet Tweet Analizi ve Haritalama")

# ---- 1. Kullanıcının yüklediği CSV ----
st.header("📤 Yüklenen Tweet Verisi")
uploaded_file = st.file_uploader("Tweet CSV dosyasını yükleyin", type=["csv"])

if uploaded_file:
    df_upload = pd.read_csv(uploaded_file)

    if "content" not in df_upload.columns:
        st.error("❌ 'content' sütunu eksik!")
    else:
        df_upload = process_dataframe(df_upload)
        df_upload['lat'], df_upload['lon'] = zip(*df_upload['city'].apply(lat_lon_bul_fast))

        st.success("✅ Dosya işlendi.")
        st.write(df_upload[["content", "city", "label"]].head())

        # Harita
        df_upload = filter_by_date(df_upload, st)
        df_upload = filter_by_label(df_upload, st)

        st.subheader("🗺️ Yüklenen Tweet Haritası")
        m1 = create_map(df_upload)
        st_folium(m1, width=1000)

        st.subheader("📊 Etiket Dağılımı")
        st.bar_chart(df_upload["label"].value_counts())

        if "date" in df_upload.columns:
            st.subheader("📈 Günlük Etiket Dağılımı")
            ts_data = df_upload.groupby([df_upload["date"].dt.date, "label"]).size().unstack(fill_value=0)
            st.line_chart(ts_data)

# ---- 2. Telegram'dan gelen veriler ----
st.header("🤖 Telegram Üzerinden Gelen Veriler")

if os.path.exists(DATA_PATH):
    df_telegram = pd.read_csv(DATA_PATH)
    st.write(df_telegram.columns)

    # Eksik kolon varsa uyar
    expected_cols = ["timestamp", "city", "label", "content"]
    if not all(col in df_telegram.columns for col in expected_cols):
        st.error("❌ 'messages.csv' dosyasında eksik sütunlar var. 'timestamp', 'city', 'label', 'content' bekleniyor.")
        st.stop()
        
    

    # Pipeline değil çünkü Telegram zaten işlenmiş metin verisi içeriyor
    df_telegram["date"] = pd.to_datetime(df_telegram["timestamp"], errors="coerce")
    df_telegram["lat"], df_telegram["lon"] = zip(*df_telegram["city"].apply(lat_lon_bul_fast))

    df_telegram = filter_by_date(df_telegram, st)
    df_telegram = filter_by_label(df_telegram, st)

    st.subheader("🗺️ Telegram Afet Haritası")
    m2 = create_map(df_telegram)
    st_folium(m2, width=1000)

    st.subheader("📊 Telegram Etiket Dağılımı")
    st.bar_chart(df_telegram["label"].value_counts())

    st.subheader("📈 Telegram Zaman Serisi")
    ts = df_telegram.groupby([df_telegram["date"].dt.date, "label"]).size().unstack(fill_value=0)
    st.line_chart(ts)



'''




DATA_PATH = "data/messages.csv"
if os.path.exists(DATA_PATH):
    df_telegram = pd.read_csv(DATA_PATH)
    df_telegram['date'] = pd.to_datetime(df_telegram['timestamp'], errors='coerce')

    df_telegram['lat'], df_telegram['lon'] = zip(*df_telegram['city'].apply(lat_lon_bul_fast))

    df_telegram = filter_by_date(df_telegram, st)
    df_telegram = filter_by_label(df_telegram, st)

    st.subheader("🗺️ Telegram Afet Haritası")
    m2 = create_map(df_telegram)
    st_folium(m2, width=1000)

    st.subheader("📊 Telegram Etiket Dağılımı")
    st.bar_chart(df_telegram["label"].value_counts())

    st.subheader("📈 Telegram Zaman Serisi")
    ts = df_telegram.groupby([df_telegram["date"].dt.date, "label"]).size().unstack(fill_value=0)
    st.line_chart(ts)
else:
    st.warning("Telegram'dan henüz kayıt alınmadı.")




'''
