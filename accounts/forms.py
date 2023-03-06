from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import FITUser,Profile

# my forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = FITUser
        fields = ('email',)
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']



class ProfileForm(forms.ModelForm):
    OFFICE_CHOICE_FIELD = (
        ('FIT KENYA','FIT KENYA'),
        ('FIT UGANDA','FIT UGANDA'),
        ('FIT TANZANIA','FIT TANZANIA'),
        ('FIT RWANDA','FIT RWANDA'),
        ('FIT ETHIOPIA','FIT ETHIOPIA'),
        ('FIT SUDAN','FIT SUDAN'),
        ('FIT DJIBOUTI','FIT DJIBOUTI'),
    )

    DESCIGNATION_CHOICE_FIELD = (
        ('SALES','SALES'),
        ('PRICING','PRICING'),
        ('MANAGEMENT','MANAGEMENT'),
    )

    office = forms.ChoiceField(choices=OFFICE_CHOICE_FIELD)
    designation = forms.ChoiceField(choices=DESCIGNATION_CHOICE_FIELD)
    
    class Meta:
        model = Profile
        fields = ('office','country','designation')

 
