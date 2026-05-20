from django import forms

from .models import ProgramReview


class ProgramReviewForm(forms.ModelForm):
    class Meta:
        model = ProgramReview
        fields = ["nickname", "text", "rating"]
        widgets = {
            "nickname": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 10,
                }
            ),
        }