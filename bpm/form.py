from django import forms
from .models import Move
class InputForm(forms.Form):
    num_basic_length = forms.IntegerField() ##Limit to 1-10\
    moves = Move.objects.all()
    contains = forms.ModelChoiceField(moves, blank=True )

    