from django import forms
from posts.models import UserPost


class PostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('post', 'caption')


# class EditPostForm(forms.Form):
#     post = forms.ImageField()
#     caption = forms.CharField(widget=forms.Textarea)
