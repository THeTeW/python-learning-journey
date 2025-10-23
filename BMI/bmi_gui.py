import tkinter as tk
from tkinter import font
from tkinter import messagebox  # เพิ่ม messagebox สำหรับแจ้งเตือน


# --- สร้างฟังก์ชันสำหรับคำนวณ (นี่คือสมองของโปรแกรม) ---
def calculate_bmi():
    try:
        # 1. ดึงค่าจากช่องกรอก (จะได้เป็น string)
        weight_str = weight_entry.get()
        height_str = height_entry.get()

        # 2. แปลง string เป็น float (ตัวเลขทศนิยม)
        weight_kg = float(weight_str)
        height_cm = float(height_str)

        # 3. คำนวณ BMI (ต้องแปลง cm เป็น m ก่อน)
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        # 4. อัปเดตป้ายแสดงผล
        result_label.config(text=f"ค่า BMI ของคุณคือ: {bmi:.2f}")

    except ValueError:
        # 5. ดักจับ Error ถ้าผู้ใช้กรอกข้อมูลที่ไม่ใช่ตัวเลข
        messagebox.showerror("ข้อมูลผิดพลาด", "กรุณาป้อนเฉพาะตัวเลขเท่านั้น")


# --- สร้างหน้าต่างหลัก ---
root = tk.Tk()
root.title("โปรแกรมคำนวณ BMI")
root.geometry("300x250")

# --- สร้าง Widgets ---
weight_label = tk.Label(root, text="น้ำหนัก (kg):")
weight_entry = tk.Entry(root)
height_label = tk.Label(root, text="ส่วนสูง (cm):")
height_entry = tk.Entry(root)

# **แก้ไขตรงนี้:** เพิ่ม command=calculate_bmi เข้าไปในปุ่ม
calculate_button = tk.Button(root, text="คำนวณ BMI", command=calculate_bmi)

result_label = tk.Label(root, text="ผลลัพธ์ BMI จะแสดงที่นี่", font=("Helvetica", 12))

# --- จัดวาง Widgets ---
weight_label.pack(pady=5)
weight_entry.pack(pady=5)
height_label.pack(pady=5)
height_entry.pack(pady=5)
calculate_button.pack(pady=10)
result_label.pack(pady=20)

# --- สั่งให้โปรแกรมทำงาน ---
root.mainloop()