from django import forms
from .models import *

class BasePostForm(forms.ModelForm):
    title = forms.CharField(label="Заголовок", widget=forms.TextInput(attrs={"style": "width:100%"}))
    text = forms.CharField(label="Текст", widget=forms.Textarea(attrs={"style": "width:100%"}))

    class Meta:
        model = Post
        fields = ['title', 'text']


class CreatePostForm(BasePostForm):
    category = forms.ModelMultipleChoiceField(label="Категория", queryset=Category.objects.all(), widget=forms.SelectMultiple(attrs={"style": "width:100%"}))

    class Meta:
        model = Post
        fields = ['title', 'text', 'category' ]
