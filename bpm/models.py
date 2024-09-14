from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import random

# Create your models here.

class HandHold(models.Model):        
    LIST_HANDHOLDS = (('h1','H1'), ('h2','H2'))

    handhold = models.CharField(max_length=25,choices=LIST_HANDHOLDS)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.description

class Position(models.Model):
    name = models.CharField(max_length=25)


    

class Move(models.Model):
    ##
    MOVES_BY_HANDHOLDS = {
    4 : [0,2,3,4,5,12,13],
    8 : [5,7],
    9 : [9,10,11]
}

    ##LIST_HANDHOLDS = (('h1','H1'), ('h2,','H2'))
    LIST_POSITIONS = (('open','Open'), ('open_palm','Open Palm'), ('sensual','Sensual'), ('close','Close'))
    LIST_LEVELS = (('Beginner',"Beginner"),('Beginner Advanced',"Beginner Advanced"))
    ##LIST_COUNTS = ((1,1), (2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8))

    name = models.CharField(max_length=100)
    length = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(8)],default=4)
    position = models.CharField(max_length=100,choices=LIST_POSITIONS)
    new_position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    ##Note -> reverse accessor error for s_handhold and e_handhold. adding related_name field fixed problem
    ##Since I added these after the model was created,..
    start_handhold = models.ForeignKey(HandHold,related_name='s_handhold', on_delete=models.CASCADE, null=True)
    end_handhold = models.ForeignKey(HandHold,related_name='e_handhold', on_delete=models.CASCADE, null=True)

    ##s_handhold = models.CharField(max_length=100,choices=LIST_HANDHOLDS)
    ##e_handhold = models.CharField(max_length=100,choices=LIST_HANDHOLDS)

    ##s_cnt = models.IntegerField(choices=LIST_COUNTS)
    level = models.CharField(max_length=25,choices=LIST_LEVELS)

    def __str__(self):
        return self.name
    
    def get_length(self):
        return self.length

    def get_start_handhold_desc(self):
        return self.start_handhold.description
        
"""   
    def nextmove(self, handhold='', current_cnt=0):
        print("handhold: " + str(handhold))
        self.end_handhold
        if handhold == '':
            handhold = HandHold.objects.filter(handhold='h1')

        move_matrix = MoveMatrix.objects.filter(handhold=handhold) ##Filter to moves with specified handhold 
        next_move_id = move_matrix.order_by("?").first().moveKey ##randomly sort and pick first (one) and get the move primary id
        next_move = Move.objects.filter(id=next_move_id)
        return next_move """


class MoveMatrix(models.Model):
    handHold = models.ForeignKey(HandHold, on_delete=models.CASCADE)
    moveKey = models.ForeignKey(Move, on_delete=models.CASCADE)

    

