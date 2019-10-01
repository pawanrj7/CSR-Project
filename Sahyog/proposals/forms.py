from django import forms
from .models import blog_posts
class PostsForm(forms.ModelForm):
    name = forms.CharField(disabled=True)

    class Meta:
        model = blog_posts
        fields = ['id', 'InitiativeTitle','requirements','name','location', 'budget','details']