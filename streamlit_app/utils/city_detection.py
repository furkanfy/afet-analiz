# streamlit_app/utils/city_detection.py

turk_sehirleri = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin",
    "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale",
    "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum",
    "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Isparta", "Mersin",
    "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli",
    "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş",
    "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas",
    "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak",
    "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan",
    "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
]

def normalize(text):
    """Metni normalize eder: Küçük harf yapar ve Türkçe karakterleri sadeleştirir"""
    return text.lower()\
        .replace("i̇", "i").replace("ı", "i")\
        .replace("ç", "c").replace("ğ", "g")\
        .replace("ö", "o").replace("ş", "s")\
        .replace("ü", "u")

def extract_city(text):
    """
    Tweet içindeki şehir adını tespit eder.
    Normalize ederek şehir isimleriyle eşleşmeye çalışır.
    """
    norm_text = normalize(text)

    for sehir in turk_sehirleri:
        if normalize(sehir) in norm_text:
            return sehir  # Orijinal haliyle şehir ismi döndürülür

    return None
