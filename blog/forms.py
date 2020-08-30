from django import forms
from .models import Post, comment

class postForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
         

class commentForm(forms.ModelForm):
    
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = comment
        fields = (('content'),)
        