import tkinter as tk
from tkinter import messagebox, filedialog

import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk

# Türkçe karakterleri Latin harflerine dönüştürme fonksiyonu
def replace_turkish_chars(text):
    replacements = {
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'I': 'I',
        'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S',
        'ü': 'u', 'Ü': 'U'
    }
    for turkish, latin in replacements.items():
        text = text.replace(turkish, latin)
    return text

# vCard formatında bir veri oluşturuluyor
def create_vcard(first_name, last_name, organization, phone, email, address):
    # Türkçe karakterleri Latin harflerine dönüştürme
    first_name = replace_turkish_chars(first_name)
    last_name = replace_turkish_chars(last_name)
    organization = replace_turkish_chars(organization)
    email = replace_turkish_chars(email)
    address = replace_turkish_chars(address)

    vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{last_name};{first_name};;;\nFN:{first_name} {last_name}"
    
    if organization:
        vcard += f"\nORG:{organization}"
    vcard += f"\nTEL:{phone}"
    if email:
        vcard += f"\nEMAIL:{email}"
    if address:
        vcard += f"\nADR:{address}"
    
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

    # Zorunlu alanların doldurulup doldurulmadığını kontrol etme
    if not (first_name and last_name and phone):
        messagebox.showwarning("Giriş Hatası", "Lütfen isim, soyisim ve telefon numarası alanlarını doldurun.")
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
    qr_image_label.configure(image="")


# Uygulama penceresini oluşturma
app = ctk.CTk()
app.title("vCard QR Kod Oluşturucu")
app.geometry("800x700")

# Bilgi giriş alanları
entry_first_name = ctk.CTkEntry(app, placeholder_text="İsim", width=250)
entry_first_name.pack(pady=5)

entry_last_name = ctk.CTkEntry(app, placeholder_text="Soyisim", width=250)
entry_last_name.pack(pady=5)

entry_organization = ctk.CTkEntry(app, placeholder_text="Şirket İsmi", width=250)
entry_organization.pack(pady=5)

entry_phone = ctk.CTkEntry(app, placeholder_text="Telefon Numarası", width=250)
entry_phone.pack(pady=5)

entry_email = ctk.CTkEntry(app, placeholder_text="Mail Adresi", width=250)
entry_email.pack(pady=5)

entry_address = ctk.CTkEntry(app, placeholder_text="Adres", width=250)
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