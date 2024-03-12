import qrcode

def create_vcard(first_name, last_name, organization, phone, email, address):
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{first_name} {last_name}\nORG:{organization}\nTEL:{phone}\nEMAIL:{email}\nADR:{address}"
    vcard += "\nEND:VCARD"
    return vcard

# Kartvizit bilgileri
first_name = "İsim Giriniz"
last_name = "Soy İsim Giriniz"
organization = " Şirket İsmi Giriniz"
phone = " Telefon Numarasi Giriniz"
email = "Mail Adresi Giriniz"
address = "Adres Giriniz"

# vCard oluştur
vcard_data = create_vcard(first_name, last_name, organization, phone, email, address,)

# vCard verilerini içeren bir QR kod oluştur
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(vcard_data)
qr.make(fit=True)

# QR kodu görüntüle
img = qr.make_image(fill_color="black", back_color="white")
img.save("elektronik_kartvizit_qr2.png") # Bilgisayarda gözükücek olan QR kod ismi

print("Elektronik kartvizit QR kodu oluşturuldu.")

## Programı yazan : Süleyman YILMAZ.