import pandas as pd
from telegram_bot.utils.pipeline import process_dataframe

# Örnek test verisi
veriler = {
    "content": [
        "Ankara'da elektrik kesintisi http://www.school.com var!",
        "Gaziantep'te su sıkıntısı yaşanıyor.",
        "Yangın çıktı İstanbul'da, yardım edin!",
        "İzmir çok sıcak ama afet yok :)",
        "Yemek, su ve internet yok Malatya'da!"
    ]
}

# DataFrame oluştur
df = pd.DataFrame(veriler)

# İşle
df_islenmis = process_dataframe(df)

# Sonuçları yazdır
print("\n✅ Temizlenmiş ve Etiketlenmiş Veri:\n")
print(df_islenmis[["content", "city", "label"]])
