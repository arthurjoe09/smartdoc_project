from django.shortcuts import render, redirect
from .forms import DocumentForm
import pandas as pd
from django.contrib import messages
from .models import ImportedDocument
from .forms import FileUploadForm
import xml.etree.ElementTree as ET #xml.etree.ElementTree is a module for parsing and creating XML documents.
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from .models import ImportedDocument


def upload_document(request): #request contains everything from the user's HTTP request, such as:form data (request.POST)
                                                                                        #Uploaded files (request.FILES) ,Metadata (headers, user, method, cookies...)
    if  request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_success')
    else:
        form = DocumentForm()
    return render(request, 'core/upload.html', {'form': form})





def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)#This creates a bound form using the user’s input:
        if form.is_valid(): #This runs the form's built-in validation, which:Calls .clean() methods,Verifies required fields,
                            # Populates form.cleaned_data.
            file = request.FILES['file'] #Access the uploaded file by key 'file' from the MultiValueDict.
            file_name = file.name.lower()

            try:
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file)#pd.read_csv() → from pandas (not built-in), reads the file-like object into a DataFrame.
                    for _, row in df.iterrows():# df.iterrows() yields each row as a tuple of (index, row).
                        ImportedDocument.objects.create(
                            title=row['title'],
                            author=row['author'],
                            doc_type=row['doc_type']
                        )

                elif file_name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                    for _, row in df.iterrows():
                        ImportedDocument.objects.create(
                            title=row['title'],
                            author=row['author'],
                            doc_type=row['doc_type']
                        )

                #ET.parse(file): parses uploaded file into an ElementTree.

                # getroot(): gets the root XML tag.
                # findall() returns all <document> nodes.
                # .find().text: gets the text inside child tags.
                elif file_name.endswith('.xml'):
                    tree = ET.parse(file)
                    root = tree.getroot()

                    for doc in root.findall('document'):
                        title = doc.find('title').text
                        author = doc.find('author').text
                        doc_type = doc.find('doc_type').text

                        ImportedDocument.objects.create(
                            title=title,
                            author=author,
                            doc_type=doc_type
                        )

                else:
                    messages.error(request, "Unsupported file format.")
                    return redirect('upload_file')



                    messages.success(request, "Data imported successfully.")
                return redirect('upload_file')

            except Exception as e:
                messages.error(request, f"Error during import: {str(e)}")
                return redirect('upload_file')
    else:
        form = FileUploadForm()#Creates an unbound form (empty) if it’s a GET request (first time loading the page).

    return render(request, 'core/file_upload.html', {'form': form})



def document_pdf(request, doc_id):#doc_id comes from the URL (e.g., /document/pdf/5/).
    doc = ImportedDocument.objects.get(id=doc_id)#fetch the id from database using id
    html_string = render_to_string('core/pdf_template.html', {'doc': doc})#Loads the HTML file pdf_template.html
                                                                                              # and fills it with data from doc.
    #Creates a PDF from the rendered HTML string.
    pdf_file = HTML(string=html_string).write_pdf()#HTML(string=...) → parses HTML.
                                                    # #.write_pdf() → renders it into a PDF file in memory.

    # Creates an HTTP response with the PDF data and tells the browser it's a PDF.
    response = HttpResponse(pdf_file, content_type='application/pdf')#content_type='application/pdf' tells the browser how to handle it.
    response['Content-Disposition'] = f'filename="{doc.title}.pdf"'  #Sets the Content-Disposition header to suggest a filename when saving the PDF.
    return response