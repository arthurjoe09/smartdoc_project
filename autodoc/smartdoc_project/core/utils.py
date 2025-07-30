from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter

def generate_qr_code(instance):
    print("🔹 Generating QR for:", instance.title)
    data = f"Title: {instance.title}, Author: {instance.author}, Type: {instance.doc_type}"
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    file_name = f"qr_{instance.id}.png"
    instance.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
    print("✅ QR done")

def generate_barcode(instance):
    print("🔹 Generating Barcode for:", instance.title)
    data = f"{instance.title[:10]}-{instance.id}"
    barcode = Code128(data, writer=ImageWriter(), add_checksum=False)
    buffer = BytesIO()
    barcode.write(buffer)
    file_name = f"barcode_{instance.id}.png"
    instance.barcode.save(file_name, ContentFile(buffer.getvalue()), save=False)
    print("✅ Barcode done")

