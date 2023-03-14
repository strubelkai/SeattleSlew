from django import forms
from .models import *

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['patient_name', 'sample_Img']
