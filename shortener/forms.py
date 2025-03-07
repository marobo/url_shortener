from django import forms
from .models import ShortURL
import re


class URLShortenerForm(forms.ModelForm):
    custom_short_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Custom short code (optional)'
            }
        ),
        help_text='Leave blank for auto-generated code. Use only letters and numbers.'
    )

    class Meta:
        model = ShortURL
        fields = ['original_url']
        widgets = {
            'original_url': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your URL here'
                }
            )
        }

    def clean_custom_short_code(self):
        code = self.cleaned_data.get('custom_short_code')
        if code:
            # Check if code contains only letters and numbers
            if not re.match(r'^[a-zA-Z0-9]+$', code):
                raise forms.ValidationError(
                    'Short code can only contain letters and numbers.'
                )
            # Check if code is already taken
            if ShortURL.objects.filter(short_code=code).exists():
                raise forms.ValidationError(
                    'This short code is already taken.'
                )
        return code

    def save(self, commit=True):
        instance = super().save(commit=False)
        custom_code = self.cleaned_data.get('custom_short_code')
        if custom_code:
            instance.short_code = custom_code
        if commit:
            instance.save()
        return instance 