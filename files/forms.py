from django import forms
from .models import UploadedFile


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = ["file"]

    def clean_file(self):

        file = self.cleaned_data["file"]

        allowed_extensions = [
            ".pdf",
            ".doc",
            ".docx",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".zip",
            ".txt",
        ]

        filename = file.name.lower()

        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError(
                "Only PDF, DOC, DOCX, Images, ZIP and TXT files are allowed."
            )

        max_size = 10 * 1024 * 1024

        if file.size > max_size:
            raise forms.ValidationError(
                "File size must not exceed 10 MB."
            )

        return file