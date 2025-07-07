
import streamlit as st
import pandas as pd
import os
import sys
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from geopy.distance import geodesic


# Yol ayarları
sys.path.append('C:\\Users\\ASUS\\Documents\\afet-analiz')
from utils.pipeline import process_dataframe
from utils.map_utils import lat_lon_bul_fast, create_map, filter_by_date, filter_by_label

# Telegram mesajlarının CSV dosya yolu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join("streamlit_app", "data", "messages.csv")

# Sayfa ayarları
st.set_page_config(layout="wide")
st.title("🆘 Afet Tweet ve Telegram Verisi Haritalama")

# Sayfayı otomatik yenile (Telegram için)
st_autorefresh(interval=15 * 10000, key="refresh-telegram")

# Tweet verisi başta boş
df_upload = pd.DataFrame()

# ---- 1. Kullanıcının yüklediği Tweet CSV dosyası ----
st.header("📤 Yüklenen Tweet Verisi")
uploaded_file = st.file_uploader("Tweet CSV dosyasını yükleyin", type=["csv"])

if uploaded_file:
    df_upload = pd.read_csv(uploaded_file)

    if "content" not in df_upload.columns:
        st.error("❌ 'content' sütunu eksik!")
    else:
        df_upload = process_dataframe(df_upload)
        df_upload['lat'], df_upload['lon'] = zip(*df_upload['city'].apply(lat_lon_bul_fast))
        df_upload["source"] = "Tweet"

        st.success("✅ Tweet verisi işlendi.")
        st.write(df_upload[["content", "city", "label"]].head())

# ---- 2. Telegram'dan gelen veriler ----
st.header("🤖 Telegram Üzerinden Gelen Veriler")

@st.cache_data(ttl=1)
def load_telegram_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame(columns=["timestamp", "city", "label", "content"])

df_telegram = load_telegram_data()

if not df_telegram.empty:
    expected_cols = ["timestamp", "city", "label", "content"]
    if not all(col in df_telegram.columns for col in expected_cols):
        st.error("❌ 'messages.csv' dosyasında eksik sütunlar var.")
        st.stop()

    df_telegram["date"] = pd.to_datetime(df_telegram["timestamp"], errors="coerce")
    df_telegram["lat"], df_telegram["lon"] = zip(*df_telegram["city"].apply(lat_lon_bul_fast))
    df_telegram["source"] = "Telegram"

    st.success("✅ Telegram verisi yüklendi.")
else:
    st.info("Henüz Telegram'dan gelen veri yok.")
    df_telegram = pd.DataFrame()

# ---- 3. Tweet + Telegram birleşik harita ve grafikler ----
st.header("🌐 Birleşik Afet Haritası ve Analizi")

# Verileri birleştir
all_data = pd.DataFrame()
if not df_upload.empty:
    all_data = pd.concat([all_data, df_upload], ignore_index=True)
if not df_telegram.empty:
    all_data = pd.concat([all_data, df_telegram], ignore_index=True)

if not all_data.empty:
    all_data = filter_by_date(all_data, st)
    all_data = filter_by_label(all_data, st)

    st.subheader("🗺️ Tüm Afet Noktaları (Tweet + Telegram)")
    combined_map = create_map(all_data)
    st_folium(combined_map, width=1000)

    st.subheader("📊 Etiket Dağılımı")
    st.bar_chart(all_data["label"].value_counts())

    if "date" in all_data.columns:
        st.subheader("📈 Zaman Serisi")
        ts = all_data.groupby([all_data["date"].dt.date, "label"]).size().unstack(fill_value=0)
        st.line_chart(ts)
else:
    st.info("Henüz gösterilecek birleşik afet verisi yok.")

from utils.help_view import show_help_section
if not all_data.empty:
    show_help_section(all_data)
