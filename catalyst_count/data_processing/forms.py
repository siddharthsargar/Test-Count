# forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

# class QueryForm(forms.Form):
#     industry = forms.CharField(required=False)
#     min_revenue = forms.FloatField(required=False)
#     max_revenue = forms.FloatField(required=False)


class QueryForm(forms.Form):
    name = forms.CharField(required=False)
    industry = forms.CharField(required=False)
    year_founded = forms.IntegerField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    country = forms.CharField(required=False)
    employees_from = forms.IntegerField(required=False)
    employees_to = forms.IntegerField(required=False)
