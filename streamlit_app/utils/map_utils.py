# utils/map_utils.py

import folium
import pandas as pd

# Şehir koordinatları sözlüğü
sehir_koordinat = {
    "Ankara": (39.9208, 32.8541),
    "İstanbul": (41.0082, 28.9784),
    "İzmir": (38.4192, 27.1287),
    "Gaziantep": (37.0662, 37.3833),
    "Malatya": (38.3552, 38.3095),
    "Hatay": (36.2028, 36.1608),
    "Kahramanmaraş": (37.5736, 36.9371),
    "Adana": (37.0, 35.3213),
    "Diyarbakır": (37.9144, 40.2306),
    "Şanlıurfa": (37.1674, 38.7955),
    "Elazığ": (38.6750, 39.2200),
    "Mersin": (36.8000, 34.6333),
    "Van": (38.4891, 43.4089),
    "Batman": (37.8812, 41.1351),
    "Osmaniye": (37.0742, 36.2476),
    "Adıyaman": (37.7648, 38.2786),
}

label_colors = {
    "yemek": "green",
    "utilities": "purple",
    "yangın": "red",
    "kurtarma": "orange",
    "su": "blue",
    "other": "gray"
}

def lat_lon_bul_fast(sehir):
    return sehir_koordinat.get(sehir, (None, None))

def create_map(df_filtered):
    m = folium.Map(location=[39, 35], zoom_start=6)
    for _, row in df_filtered.dropna(subset=["lat", "lon"]).iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(
                f"{row['city']} - {row['label']}<br><b>Tweet:</b> {row['content']}",
                max_width=300
            ),
            icon=folium.Icon(color=label_colors.get(row["label"], "gray"))
        ).add_to(m)
    return m

from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

def filter_by_date(df, st):
    # timestamp sütununu datetime formatına çevir
    if 'timestamp' in df.columns and not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=["timestamp"])
        if not df.empty:
            min_date = df['timestamp'].min().date()
            max_date = df['timestamp'].max().date()
            # Eğer min_date ve max_date aynıysa, max_date'e bir gün ekle
            if min_date == max_date:
                max_date = (pd.to_datetime(max_date) + timedelta(days=1)).date()
        else:
            # Veri seti boşsa varsayılan tarihler
            min_date = datetime(2025, 1, 1).date()
            max_date = datetime.now().date()
    else:
        # timestamp sütunu yoksa veya veri seti boşsa varsayılan tarihler
        min_date = datetime(2025, 1, 1).date()
        max_date = datetime.now().date()

    # Slider oluştur
    date_range = st.slider(
        "Tarih aralığını seçin",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )
    # Veriyi tarih aralığına göre filtrele
    if 'timestamp' in df.columns and not df.empty:
        df = df[(df['timestamp'].dt.date >= date_range[0]) & (df['timestamp'].dt.date <= date_range[1])]
    
    # lat ve lon sütunlarını ekle
    df['lat'] = df['city'].apply(lambda x: lat_lon_bul_fast(x)[0])
    df['lon'] = df['city'].apply(lambda x: lat_lon_bul_fast(x)[1])
    return df

'''
def filter_by_date(df, st):
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=["date"])
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        date_range = st.slider("Tarih aralığını seçin", min_value=min_date, max_value=max_date, value=(min_date, max_date))
        df = df[(df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])]
    return df
'''
def filter_by_label(df, st):
    unique_labels = df['label'].dropna().unique().tolist()
    selected = st.multiselect("Gösterilecek etiketler:", options=unique_labels, default=unique_labels)
    return df[df['label'].isin(selected)]
