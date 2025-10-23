# เพิ่ม import ที่จำเป็น
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta # <-- 1. import เครื่องมือจัดการเวลา


# --- ส่วนของโค้ดดึงข่าว BBC (เราจะยกมาไว้ในฟังก์ชัน) ---
def get_bbc_news():
    url = 'https://www.bbc.com/thai/topics/cjgn73g98rqt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)

    news_list = []  # เตรียม list ว่างสำหรับเก็บข่าว

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        all_headlines_h2 = soup.find_all('h2', class_='bbc-187qc6w e47bds20')

        for h2_tag in all_headlines_h2:
            a_tag = h2_tag.find('a')
            if a_tag:
                title = a_tag.get_text(strip=True)
                link = a_tag['href']

                if not link.startswith('https://'):
                    link = 'https://www.bbc.com' + link

                # เก็บข้อมูลเป็น dictionary แล้วเพิ่มลงใน list
                news_list.append({'title': title, 'link': link})

    return news_list


# --- ส่วนของ Flask App ---
app = Flask(__name__)
#สร้าง "ที่พักข้อมูล" นอกฟังก์ชัน
cached_news = []
last_scraped_time = None


@app.route("/")
def index():
    # 3. ทำให้ตัวแปรเป็น global เพื่อให้เราแก้ไขค่ามันได้
    global cached_news, last_scraped_time

    # กำหนดว่าข้อมูลจะหมดอายุในกี่นาที
    cache_duration = timedelta(minutes=1)

    # 4. ตรวจสอบเงื่อนไขของ Cache
    # ถ้ายังไม่เคยดึงข้อมูลเลย หรือ ข้อมูลเก่าเกิน 10 นาทีแล้ว
    if not last_scraped_time or (datetime.now() - last_scraped_time > cache_duration):
        print("ข้อมูลเก่าแล้ว กำลังดึงข้อมูลใหม่จาก BBC...")
        cached_news = get_bbc_news()  # ดึงข้อมูลใหม่
        last_scraped_time = datetime.now()  # บันทึกเวลาที่ดึงล่าสุด
    else:
        print("ข้อมูลยังใหม่อยู่ ใช้ข้อมูลจาก Cache...")

    # ส่งข้อมูลที่อยู่ใน Cache ไปแสดงผล
    return render_template('index.html', news_list=cached_news)


if __name__ == "__main__":
    app.run(debug=True)