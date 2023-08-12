from django import forms
from .models import Dog, Parent
import datetime


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner',)

    def clean_birth_day(self):
        cleaned_data = self.cleaned_data['birth_day']
        if cleaned_data is None:
            return cleaned_data
        now_year = datetime.datetime.now().year
        if now_year - cleaned_data.year > 100:
            raise forms.ValidationError('Собака должна быть моложе 100 лет')
        return cleaned_data


class ParentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
