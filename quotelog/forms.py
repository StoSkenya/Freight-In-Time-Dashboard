import imp
from django import forms
from django.forms import ModelForm

from .models import QuoteLogdb

class DateInput(forms.DateInput):
    input_type = 'date'



class CreateQuoteLogForm(ModelForm):
    class Meta:
        model = QuoteLogdb
        fields = '__all__'
        widgets = {
            'date_of_reciept_of_request': DateInput(),
            'date_of_reply_to_client': DateInput(),
        }
