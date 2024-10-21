from django.test import TestCase
from .models import Pattern
# Create your tests here.
class PatternTestCase(TestCase):
        

    def test_pattern_init_val(self):
        p = Pattern()
       ##p.addMove(p.nextMove())
        assert p.getPatternLength() == 0
        assert p.getPattern() == []
        assert p.getPatternDict() == []

        

