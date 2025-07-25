from django.shortcuts import render, redirect
from .forms import DocumentForm
import pandas as pd
from django.contrib import messages
from .models import ImportedDocument
from .forms import FileUploadForm

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = DocumentForm()
    return render(request, 'core/upload.html', {'form': form})





def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = file.name.lower()

            try:
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file)

                elif file_name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    messages.error(request, "Unsupported file format.")
                    return redirect('upload_file')

                # Expected columns: title, author, doc_type
                print(df.head())
                print(df.columns)
                for _, row in df.iterrows():

                    ImportedDocument.objects.create(
                        title=row['title'],
                        author=row['author'],
                        doc_type=row['doc_type']
                    )

                messages.success(request, "Data imported successfully.")
                return redirect('upload_file')

            except Exception as e:
                messages.error(request, f"Error during import: {str(e)}")
                return redirect('upload_file')
    else:
        form = FileUploadForm()

    return render(request, 'core/file_upload.html', {'form': form})
