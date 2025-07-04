import re

def clean_text(text):
    if not text:  # 1. Eğer metin boşsa
        return ""

    # 2. Linkleri kaldır
    text = re.sub(r'https?://\S+|t\.co/\S+', '', text)

    # 3. HTML sembollerini kaldır (örneğin &amp;, &gt;)
    text = re.sub(r"&[a-z]+;", "", text)

    # 4. Sadece Türkçe karakterler, sayılar ve boşluklar kalsın
    text = re.sub(r"[^a-zA-ZğüşöçıİĞÜŞÖÇ0-9\s]", "", text)

    # 5. Boşlukları sadeleştir
    text = re.sub(r"\s+", " ", text).strip()

    # 6. Hiç harf kalmadıysa boş döndür
    if not re.search(r"[a-zA-ZğüşöçıİĞÜŞÖÇ]", text):
        return ""

    return text

