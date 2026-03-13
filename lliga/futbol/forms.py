from django import forms

from .models import Lliga


class LligaChoiceForm(forms.Form):
    lliga = forms.ModelChoiceField(
        queryset=Lliga.objects.all(),
        empty_label="Tria una lliga",
        label="Lliga",
    )
