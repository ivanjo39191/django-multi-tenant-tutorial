
from django import forms
from django.db import models
from customers.models import Client, Domain

class CustomersForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(CustomersForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "租戶名稱"
        self.fields['from_schema_name'].label = "要複製的 schema 名稱"
        self.fields['to_schema_name'].label = "新增的 schema 名稱"
        self.fields['description'].label = "說明"
        self.fields['domain'].label = "網域"
    
    name = forms.CharField(required=True)
    from_schema_name = forms.CharField(required=True)
    to_schema_name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    domain = forms.CharField(required=True)

    def clean_name(self):
        data = self.cleaned_data['name']
        if Client.objects.filter(name=data).exists():
            raise forms.ValidationError(f'租戶名稱 "{data}" 已存在。')
        return data

    def clean_from_schema_name(self):
        data = self.cleaned_data['from_schema_name']
        if not Client.objects.filter(schema_name=data).exists():
            raise forms.ValidationError(f'要複製的 schema 名稱 "{data}" 不存在。')
        return data
        
    def clean_to_schema_name(self):
        data = self.cleaned_data['to_schema_name']
        if '.' in data:
            raise forms.ValidationError(f'新建的 schema 名稱 "{data}" 不可包含 "." 字元。')
        if not data.isalnum() or data.isdigit():
            raise forms.ValidationError(f'新建的 schema 名稱 "{data}" 需英數字混和。')
        if Client.objects.filter(schema_name=data).exists():
            raise forms.ValidationError(f'新建的 schema 名稱 "{data}" 已存在。')
        return data
        
    def clean_domain(self):
        data = self.cleaned_data['domain']
        if Domain.objects.filter(domain=data).exists():
            raise forms.ValidationError(f'網域"{data}" 已存在。')
        return data