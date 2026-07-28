"""Forms for creating and updating sticky notes."""

from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter note title"
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Enter note content",
                    "rows": 6,
                }
            ),
        }