from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from mysocial.models import UserProfile


GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    user_image = forms.ImageField()
    phone_number = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=GENDER_CHOICES,
                               widget=forms.RadioSelect)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ('username', 'email', 'user_image', 'phone_number',
                  'gender', 'dob', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        # Get the 'exclude' parameter from the kwargs
        exclude_fields = kwargs.pop('exclude', [])
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Exclude fields dynamically
        for field_name in exclude_fields:
            if field_name in self.fields:
                del self.fields[field_name]


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

