from django.db import models

from django.db import models

DOCUMENT_TYPES = [
    ('pdf', 'PDF Document'),
    ('excel', 'Excel Spreadsheet'),
    ('csv', 'CSV File'),
    ('image', 'Image File'),
    ('xml', 'XML File'),
]

#document model for uploading
class Document(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    doc_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"{self.title} ({self.doc_type})"

#new model to store imported documents from files.
class ImportedDocument(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    doc_type = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    barcode = models.ImageField(upload_to='barcodes/', null=True, blank=True)
    document_image = models.ImageField(upload_to='doc_images/', null=True, blank=True)
    html_image = models.ImageField(upload_to='html_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first to get instance.id
        from core.utils import generate_qr_code, generate_barcode
        generate_qr_code(self)
        generate_barcode(self)
        super().save(update_fields=['qr_code', 'barcode'])  # Save again to store images

    def __str__(self):
        return f"{self.title} by {self.author}"


