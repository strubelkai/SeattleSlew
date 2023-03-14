from django import forms

class SampleForm(forms.Form):
    patient_name = forms.CharField(label='Patient Name', max_length=100)