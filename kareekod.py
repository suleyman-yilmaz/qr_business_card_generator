import tkinter as tk
from tkinter import messagebox, filedialog

import customtkinter as ctk

import qrcode

from PIL import Image, ImageTk


# vCard formatında bir veri oluşturuluyor
def create_vcard(first_name, last_name, organization, phone, email, address):
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{first_name} {last_name}\nORG:{organization}\nTEL:{phone}\nEMAIL:{email}\nADR:{address}"
    vcard += "\nEND:VCARD"
    return vcard


# QR kodunu oluşturma
def generate_qr():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    organization = entry_organization.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    # Girişlerin tümünün doldurulup doldurulmadığını kontrol etme
    if not (first_name and last_name and organization and phone and email and address):
        messagebox.showwarning("Giriş Hatası", "Lütfen tüm alanları doldurun.")
        return

    # vCard verisini oluştur
    vcard_data = create_vcard(first_name, last_name, organization, phone, email, address)

    # QR kodu oluşturma
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,  # Her bir kutunun boyutunu küçült
        border=2,  # Kenar boşluğunu küçült
    )

    qr.add_data(vcard_data)  # vCard verisini QR koda ekle
    qr.make(fit=True)  # QR kodunu oluştur

    global img  # Global değişken olarak tanımlıyoruz, böylece diğer fonksiyonlar tarafından erişilebilir.
    img = qr.make_image(fill_color="black", back_color="white")  # QR kodunu siyah-beyaz resim olarak oluşturma
    img_tk = ImageTk.PhotoImage(img)  # PIL imajını Tkinter uyumlu hale getirme

    qr_image_label.configure(image=img_tk)  # QR kodu görselini label'da gösterme
    qr_image_label.image = img_tk  # Referansı sakla

    messagebox.showinfo("Başarı", "QR kodu başarıyla oluşturuldu!")  # Başarı mesajı


# QR kodunu dosyaya kaydetme
def save_qr():
    if img is None:
        messagebox.showwarning("Kaydetme Hatası", "Önce bir QR kodu oluşturmalısınız.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                           filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        img.save(file_path)
        messagebox.showinfo("Başarı", f"QR kodu {file_path} olarak kaydedildi!")  # Başarı mesajı


def close_app():
    app.destroy()


def clean_entry():
    entry_first_name.delete(0, "end")
    entry_last_name.delete(0, "end")
    entry_organization.delete(0, "end")
    entry_phone.delete(0, "end")
    entry_email.delete(0, "end")
    entry_address.delete(0, "end")


# Uygulama penceresini oluşturma
app = ctk.CTk()
app.title("vCard QR Kod Oluşturucu")
app.geometry("800x700")

# Bilgi giriş alanları
entry_first_name = ctk.CTkEntry(app, placeholder_text="İsim")
entry_first_name.pack(pady=5)

entry_last_name = ctk.CTkEntry(app, placeholder_text="Soyisim")
entry_last_name.pack(pady=5)

entry_organization = ctk.CTkEntry(app, placeholder_text="Şirket İsmi")
entry_organization.pack(pady=5)

entry_phone = ctk.CTkEntry(app, placeholder_text="Telefon Numarası")
entry_phone.pack(pady=5)

entry_email = ctk.CTkEntry(app, placeholder_text="Mail Adresi")
entry_email.pack(pady=5)

entry_address = ctk.CTkEntry(app, placeholder_text="Adres")
entry_address.pack(pady=5)

# QR kodu gösterme alanını oluşturma
qr_image_label = ctk.CTkLabel(app, text="")
qr_image_label.pack(pady=20)

# Oluşturma butonu
generate_button = ctk.CTkButton(app, text="QR Kodunu Oluştur", command=generate_qr)
generate_button.pack(pady=10)

# Kaydetme butonu
save_button = ctk.CTkButton(app, text="QR Kodunu Kaydet", command=save_qr)
save_button.pack(pady=10)

# Temizleme butonu
clean_button = ctk.CTkButton(app, text="Temizle", command=clean_entry)
clean_button.pack(pady=10)

# Çıkış butonu
close_button = ctk.CTkButton(app, text="Exit", command=close_app, width=50)
close_button.pack(padx=20, pady=20, side='right', anchor='s')

img = None

app.mainloop()
