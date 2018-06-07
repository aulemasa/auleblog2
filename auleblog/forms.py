#coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function
from django import forms
from .models import Comment, Article

forms.DateInput.input_type = "date"
forms.DateInput.input_formats = "'%Y-%m-%d'"


class CommentForm(forms.ModelForm):
    post = forms.ModelChoiceField(label="", queryset=Article.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = '__all__'  #('tworca','tresc_komentarza')
        widgets = {
            'comment_author': forms.TextInput(attrs={'placeholder': 'Autor'}),
            'comment_content': forms.Textarea(attrs={'placeholder': 'Treść'}),
        }
