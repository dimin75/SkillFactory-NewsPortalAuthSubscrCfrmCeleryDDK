import django_filters
from django import forms
from django_filters import FilterSet
from .models import Post, Author

class PostFilter(FilterSet):
    author = django_filters.ModelChoiceFilter(label="Автор", queryset=Author.objects.all())
    created_at = django_filters.DateFilter(label="Дата публикации", lookup_expr='contains', widget=forms.DateInput(attrs={'type': 'date'}))
    title = django_filters.CharFilter(label="Название", lookup_expr='icontains')
    text = django_filters.CharFilter(label="Текст", lookup_expr='icontains')


    class Meta:
        model = Post
        fields = ['author', 'created_at', 'title', 'text']
