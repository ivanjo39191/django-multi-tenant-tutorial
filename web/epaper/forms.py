from django import forms
from epaper.models import EPaperEmail

class EPaperForm(forms.ModelForm):
    class Meta:
        model = EPaperEmail
        fields = ('email',)