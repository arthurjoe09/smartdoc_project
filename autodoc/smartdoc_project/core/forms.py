from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document # Assigning a class (not a string or instance).
        fields = ['title', 'author', 'doc_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'doc_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



    # This is field-level validation —
    # Django automatically runs clean_<fieldname>() methods when
    # validating the form
    def clean_title(self):
        title = self.cleaned_data['title'] #cleaned data is a dictinory of values that already is validated
        if "test" in title.lower():
            raise forms.ValidationError("Title cannot contain the word 'test'")
        return title

    # Form-level validation
    def clean(self):
        cleaned_data = super().clean() #the inbuit clean() method returns the dictionary
        title = cleaned_data.get("title")
        author = cleaned_data.get("author")

        if title and author and title.lower() == author.lower():
            raise forms.ValidationError("Title and Author cannot be the same")
        return cleaned_data

    # Override init (for dynamic UI later)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = True
