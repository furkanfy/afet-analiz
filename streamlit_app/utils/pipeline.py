import sys
sys.path.append('C:\\Users\\ASUS\\Documents\\afet-analiz')

from utils.text_cleaning import clean_text
from utils.city_detection import extract_city
from utils.label_detection import detect_label

def process_dataframe(df):
    df['content'] = df['content'].apply(clean_text)
    df['city'] = df['content'].apply(extract_city)
    df['label'] = df['content'].apply(detect_label)
    return df
def process_single_tweet(text):
    cleaned = clean_text(text)
    city = extract_city(cleaned)
    label = detect_label(cleaned)
    return {
        "cleaned": cleaned,
        "city": city,
        "label": label
    }
