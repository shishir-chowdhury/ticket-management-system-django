from django import forms
from .models import Ticket, Comment

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class TicketForm(forms.ModelForm):
    attachments = forms.FileField(
        required=False,
        widget=MultiFileInput(attrs={"multiple": True, "class": "form-control"})
    )

    class Meta:
        model = Ticket
        fields = ["title", "description", "priority", "assigned_to", "due_date"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "class": "form-control"})
        }
