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

    def __str__(self):
        return f"{self.title} by {self.author}"
