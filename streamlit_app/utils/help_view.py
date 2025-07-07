# streamlit_app/utils/help_view.py

import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import sys
sys.path.append('C:\\Users\\ASUS\\Documents\\afet-analiz')
from utils.map_utils import lat_lon_bul_fast


def show_help_section(all_data):
    st.header("🙋 Yardım Etmek İstiyorum")

    user_city = st.text_input("📍 Bulunduğunuz şehri girin (örneğin: Adana, Ankara...)")

    if user_city:
        user_city = user_city.strip().title()
        user_lat, user_lon = lat_lon_bul_fast(user_city)

        if user_lat and user_lon:
            st.map(pd.DataFrame([[user_lat, user_lon]], columns=["lat", "lon"]))

            def get_distance(row):
                return geodesic((user_lat, user_lon), (row["lat"], row["lon"])).km

            all_data["distance_km"] = all_data.apply(get_distance, axis=1)
            nearest = all_data.sort_values("distance_km").head(5)

            st.subheader("🚨 Size En Yakın Afet Noktaları")
            for _, row in nearest.iterrows():
                st.markdown(f"""
                **📍 Şehir:** {row['city']}  
                **🔥 Etiket:** {row['label']}  
                **📡 Kaynak:** {row['source']}  
                **📄 İçerik:** {row['content'][:100]}  
                **📏 Mesafe:** {row['distance_km']:.2f} km  
                [📌 Google Harita’da Gör](https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']})
                ---
                """)
        else:
            st.error("❌ Şehir konumu bulunamadı.")
