import tkinter as tk
from tkinter import font
import requests
from bs4 import BeautifulSoup


# --- ส่วนที่ 1: "สมอง" - โค้ดดึงข่าว (ยกมาจากโปรเจกต์เก่า) ---
def get_bbc_news():
    url = 'https://www.bbc.com/thai/topics/cjgn73g98rqt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # ตรวจสอบว่ามี error (เช่น 404, 500) หรือไม่

        news_list = []
        soup = BeautifulSoup(response.text, 'html.parser')
        all_headlines_h2 = soup.find_all('h2', class_='bbc-187qc6w e47bds20')

        for h2_tag in all_headlines_h2:
            a_tag = h2_tag.find('a')
            if a_tag:
                title = a_tag.get_text(strip=True)
                link = a_tag['href']
                if not link.startswith('https://'):
                    link = 'https://www.bbc.com' + link
                news_list.append({'title': title, 'link': link})
        return news_list
    except requests.RequestException as e:
        print(f"เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
        return []  # คืนค่าเป็น list ว่างถ้าดึงข้อมูลไม่สำเร็จ


# --- ส่วนที่ 2: ฟังก์ชันตัวกลางสำหรับจัดการปุ่ม ---
def load_news_into_display():
    # 1. ล้างข้อมูลเก่าในช่องแสดงผลก่อน
    # '1.0' คือตำแหน่งเริ่มต้น (บรรทัด 1, ตัวอักษร 0)
    # tk.END คือตำแหน่งสุดท้าย
    news_display.delete('1.0', tk.END)

    # 2. แสดงข้อความว่ากำลังโหลด...
    news_display.insert(tk.END, "กำลังโหลดข่าวล่าสุด กรุณารอสักครู่...")
    root.update_idletasks()  # สั่งให้ UI อัปเดตทันที

    # 3. เรียกใช้ฟังก์ชันดึงข่าว
    news = get_bbc_news()

    # 4. ล้างข้อความ "กำลังโหลด" ออก
    news_display.delete('1.0', tk.END)

    # 5. นำข่าวที่ได้มาแสดงผลใน Text widget
    if news:
        for index, item in enumerate(news, 1):
            news_display.insert(tk.END, f"{index}. {item['title']}\n")
            news_display.insert(tk.END, f"   ลิงก์: {item['link']}\n\n")
    else:
        news_display.insert(tk.END, "ไม่สามารถโหลดข่าวได้ กรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")


# --- สร้างหน้าต่างหลัก ---
root = tk.Tk()
root.title("โปรแกรมดึงข่าว BBC")
root.geometry("700x500")

# --- สร้าง Widgets ---
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# **แก้ไขตรงนี้:** เพิ่ม command=load_news_into_display
load_button = tk.Button(top_frame, text="โหลดข่าวล่าสุด", font=("Helvetica", 12), command=load_news_into_display)
load_button.pack()

content_frame = tk.Frame(root)
content_frame.pack(pady=10, padx=10, fill="both", expand=True)

news_display = tk.Text(content_frame, wrap="word", font=("Helvetica", 14))
news_display.pack(fill="both", expand=True)

# --- สั่งให้โปรแกรมทำงาน ---
root.mainloop()