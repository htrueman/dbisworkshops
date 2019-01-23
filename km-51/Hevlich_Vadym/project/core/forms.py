from django import forms
from django.core.exceptions import ValidationError

from core.models import Repo, Category


class AddRepoForm(forms.ModelForm):
    class Meta:
        model = Repo
        fields = ('deep_link',)

    def clean_deep_link(self):
        deep_link = self.cleaned_data['deep_link']
        if 'github.com' not in deep_link:
            raise ValidationError('Only github repos are allowed.')
        return deep_link


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('results',)
