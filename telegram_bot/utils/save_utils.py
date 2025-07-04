import os
import csv
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../streamlit_app/data/messages.csv")

def save_to_csv(city, label, text):
    file_exists = os.path.exists(DATA_PATH)
    with open(DATA_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "city", "label", "message"])
        writer.writerow([datetime.now().isoformat(), city, label, text])
