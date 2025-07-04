import sys
import os
import csv
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Proje dizinini sys.path'e ekle
sys.path.append('C:\\Users\\ASUS\\Documents\\afet-analiz')

# Unicode hatalarını önle
sys.stdout.reconfigure(encoding='utf-8')

# Ortam değişkenlerini yükle
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN") or "7686264523:AAFJoUJhsZ0jCzFdLw_Gryh3nK_ODBaq3Bg"

# Fonksiyonları içe aktar
from telegram_bot.utils.pipeline import process_single_tweet

# CSV dosyasına mesaj kayıt fonksiyonu
DATA_PATH = os.path.join(os.path.dirname(__file__), "../streamlit_app/data/messages.csv")

def save_to_csv(city, label, content):
    file_exists = os.path.exists(DATA_PATH)
    with open(DATA_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "city", "label", "content"])  # content ekledik!
        writer.writerow([datetime.now().isoformat(), city, label, content])

'''
def save_to_csv(city, label, text):
    file_exists = os.path.exists(DATA_PATH)
    with open(DATA_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "city", "label", "message"])
        writer.writerow([datetime.now().isoformat(), city, label, text])
'''
# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Merhaba! Afet bildirimi için şehir ve durumu yazınız.\n\n✉️ Örnek: 'Hatay'da yangın var, yardım lazım.'"
    )

# Mesajları işleme
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = process_single_tweet(text)

    city = result.get("city")
    label = result.get("label")

    if not city:
        await update.message.reply_text("⚠️ Şehir bilgisi tespit edilemedi. Lütfen tekrar deneyin.")
        return

    # CSV'ye kayıt
    save_to_csv(city, label, text)

    if label != "other":
        await update.message.reply_text(
            f"✔️ Afet Tespiti:\n\n📍 Şehir: {city}\n🔹 Tür: {label}\n\nKaydınız alındı. Yetkililere iletilmek üzere sisteme işlendi."
        )
    else:
        await update.message.reply_text("ℹ️ Herhangi bir afet türü tespit edilemedi.")

# Botu çalıştır
if __name__ == "__main__":
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN .env dosyasında tanımlı değil.")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✨ Telegram botu çalışıyor...")
    app.run_polling()


















'''


# telegram_bot/bot.py
import sys
sys.path.append('C:\\Users\\ASUS\\Documents\\afet-analiz')

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram_bot.utils.pipeline import process_single_tweet
from dotenv import load_dotenv
import os
import sys
import csv
from datetime import datetime
TOKEN = os.getenv("TELEGRAM_TOKEN") or "7686264523:AAFJoUJhsZ0jCzFdLw_Gryh3nK_ODBaq3Bg"

# CSV dosyasına kayıt yolu (streamlit_app içindeki data klasörü)
DATA_PATH = os.path.join(os.path.dirname(__file__), "../streamlit_app/data/messages.csv")

# CSV'ye mesajı kaydeden fonksiyon
def save_to_csv(city, label, text):
    file_exists = os.path.exists(DATA_PATH)

    with open(DATA_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "city", "label", "message"])
        writer.writerow([datetime.now().isoformat(), city, label, text])

# Unicode hatasını engelle
sys.stdout.reconfigure(encoding='utf-8')

# Ortam değişkenlerinden TOKEN yükle
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Merhaba! Afet bildirimi için şehir ve durumu yazınız.\n\n✉️ Örnek: 'Hatay'da yangın var, yardım lazım.'"
    )

# Mesajları işleme
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = process_single_tweet(text)

    city = result.get("city")
    label = result.get("label")

    if not city:
        await update.message.reply_text("⚠️ Şehir bilgisi tespit edilemedi. Lütfen tekrar deneyin.")
        return

    # Kayıt başarılıysa CSV'ye yaz
    save_to_csv(city, label, text)

    if label != "other":
        await update.message.reply_text(
            f"✔️ Afet Tespiti:\n\n📍 Şehir: {city}\n🔹 Tür: {label}\n\nKaydınız alındı. Yetkililere iletilmek üzere sisteme işlendi."
        )
    else:
        await update.message.reply_text("ℹ️ Herhangi bir afet türü tespit edilemedi.")

# Botu başlat
if __name__ == "__main__":
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN .env dosyasında tanımlı değil.")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✨ Telegram botu çalışıyor...")
    app.run_polling()




'''