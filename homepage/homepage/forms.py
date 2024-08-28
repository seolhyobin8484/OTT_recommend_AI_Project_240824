from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model= ()

from django import forms

class ReviewForm(forms.Form):
    rating = forms.IntegerField(widget=forms.HiddenInput())
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '리뷰 내용을 작성해주세요.'}))
