from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Move(models.Model):
    ##
    LIST_HANDHOLDS = (('h1','H1'), ('h2,','H2'))
    LIST_POSITIONS = (('open','Open'), ('open_palm','Open Palm'), ('sensual','Sensual'), ('close','Close'))
    LIST_LEVELS = (("Beginner",1),("Beginner Advanced",2))
    ##LIST_COUNTS = ((1,1), (2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8))

    name = models.CharField(max_length=100)
    length = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(8)],default=4)
    position = models.CharField(max_length=100,choices=LIST_POSITIONS)
    s_handhold = models.CharField(max_length=100,choices=LIST_HANDHOLDS)
    e_handhold = models.CharField(max_length=100,choices=LIST_HANDHOLDS)
    s_cnt = models.IntegerField(choices=LIST_COUNTS)
    level = models.IntegerField(choices=LIST_LEVELS)
    
