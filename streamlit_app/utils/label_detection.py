
def detect_label(text):
    text = text.lower()  # küçük harfe çevir

    if any(k in text for k in ["yiyecek", "yemek", "gıda"]):
        return "yemek"
    elif any(k in text for k in ["elektrik", "enerji", "internet"]):
        return "utilities"
    elif any(k in text for k in ["yangın", "ateş"]):
        return "yangın"
    elif any(k in text for k in ["yardım", "kurtar"]):
        return "kurtarma"
    elif any(k in text for k in ["su", "içme suyu"]):
        return "su"
    else:
        return "other"



