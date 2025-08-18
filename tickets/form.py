from django import forms
from .models import Ticket, Comment

class TicketForm(forms.ModelForm):
    # allow multi-file uploads via a plain input in the template
    attachments = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

    class Meta:
        model = Ticket
        fields = ["title", "description", "priority", "assigned_to", "due_date"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3})
        }
