from django import forms
from .models import Move

class InputForm(forms.Form):
    length = forms.IntegerField(min_value=1, max_value=8) ##Limit to 1-10\
    moves = Move.objects.all()
    contains = forms.ModelChoiceField(moves, required=False,blank=True)
    startsWith = forms.ModelChoiceField(moves, required=False, blank=True, initial=Move.objects.filter(name='basic').first())
    