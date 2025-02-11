import os
import random
import logging
from datetime import datetime
import time
import json
from instabot import Bot
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Log dosyasının yapılandırılması
logging.basicConfig(filename='instagram_automation.log', level=logging.INFO)

# Instagram giriş bilgilerini .env dosyasından al
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Media klasör yolu
media_folder = r"C:\Users\Abdullah Soylu\Desktop\botfather\pro\otomasyon\randomfolder\cat"

# Daha önce kullanılan dosyaların kontrolü
used_files = set()

if os.path.exists('used_files.txt'):
    with open('used_files.txt', 'r') as file:
        used_files = set(file.read().splitlines())

# Medya dosyalarını filtrele (jpg, png, mp4, mpv)
media_files = [f for f in os.listdir(media_folder) if f.endswith(('jpg', 'png', 'mp4', 'mpv'))]

# Daha önce kullanılmamış dosyaları filtrele
available_files = [f for f in media_files if f not in used_files]

# Eğer yeterli dosya yoksa (3 dosya), uyarı ver ve çık
if len(available_files) < 3:
    logging.warning(f"{datetime.now()} - Yeterli kullanılabilir dosya yok!")
    print("Yeterli kullanılabilir dosya yok.")
    exit()

# Rastgele 3 dosya seç
selected_files = random.sample(available_files, 3)

# Seçilen dosyaların tam yolu
selected_paths = [os.path.join(media_folder, file) for file in selected_files]

# Seçilen dosyaları log dosyasına yaz
logging.info(f"{datetime.now()} - Seçilen dosyalar: {selected_files}")

# comment.json dosyasından caption verisini oku
with open('comment.json', 'r') as comment_file:
    comment_data = json.load(comment_file)
    caption = random.choice(comment_data['comments'])

# hashtag.json dosyasından hashtag verisini oku
with open('hashtag.json', 'r') as hashtag_file:
    hashtag_data = json.load(hashtag_file)
    hashtags = " ".join(random.sample(hashtag_data['hashtags'], 5))  # 5 rastgele hashtag

# Instagram Botu başlat
bot = Bot()

# Instagram giriş bilgileri ile giriş yap
bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)

# Karusel paylaşımı yap
try:
    post_caption = f"{caption}\n\n{hashtags}"  # Başlık ve hashtagler birleşiyor
    bot.upload_album(selected_paths, caption=post_caption)
    logging.info(f"{datetime.now()} - Karusel paylaşımı başarıyla yapıldı: {selected_files}")
except Exception as e:
    logging.error(f"{datetime.now()} - Hata oluştu: {str(e)}")

# Dosyaları 'used_files.txt' dosyasına ekle
with open('used_files.txt', 'a') as file:
    for selected_file in selected_files:
        file.write(f"{selected_file}\n")

# Paylaşım sonrası dosyaları sil
for file in selected_paths:
    os.remove(file)
    logging.info(f"{datetime.now()} - Silindi: {file}")

# Log kaydını güncelle
logging.info(f"{datetime.now()} - Paylaşım yapıldı ve dosyalar silindi.")

# 5 dakika (300 saniye) bekleme süresi
time.sleep(300)
