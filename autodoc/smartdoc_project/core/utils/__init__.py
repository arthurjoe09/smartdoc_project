from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
import imgkit
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.core.files import File
from io import BytesIO
from core.models import ImportedDocument

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
    barcode = Code128(data, writer=ImageWriter() )
    buffer = BytesIO()
    barcode.write(buffer)
    file_name = f"barcode_{instance.id}.png"
    instance.barcode.save(file_name, ContentFile(buffer.getvalue()), save=False)
    print("✅ Barcode done")


def generate_html_image(instance):
    print("🔹 Generating html_image for:", instance.title)

    html = render_to_string('core/html_template.html', {'doc': instance})

    output_dir = os.path.join(settings.MEDIA_ROOT, 'html_images')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f'{instance.id}_html_image.jpg')

    config = imgkit.config(wkhtmltoimage=settings.WKHTMLTOIMAGE_CMD)
    imgkit.from_string(html, output_path, config=config)

    # Save relative path to model field
    instance.html_image.name = os.path.relpath(output_path, settings.MEDIA_ROOT)
    instance.save()

    print("✅ html_image done")
