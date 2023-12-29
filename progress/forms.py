from django import forms 
from progress.models import TaskNote, ProjectNote

class NoteForm(forms.Form):
    note = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "w-full mb-2 p-2 rounded-lg border-solid border-2 border-b-gray-200",
            "placeholder":"Add a Note",
            "rows":"3"
            })
        )
