from django import forms

class FilterForm(forms.Form):
    city = forms.ChoiceField(choices=[('SF', 'San Francisco'), ('Montreal', 'Montreal')], required=False)
    fruit = forms.ChoiceField(choices=[('Apples', 'Apples'), ('Oranges', 'Oranges'), ('Bananas', 'Bananas')], required=False)