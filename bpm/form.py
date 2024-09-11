from django import forms

class InputForm(forms.Form):
    num_basic_length = forms.IntegerField() ##Limit to 1-10

    