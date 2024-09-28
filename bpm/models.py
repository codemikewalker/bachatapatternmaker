from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import random

# Create your models here.

class HandHold(models.Model):        
    LIST_HANDHOLDS = (('h1','H1'), ('h2','H2'))

    ##handhold = models.CharField(max_length=25,choices=LIST_HANDHOLDS)
    handhold = models.CharField(max_length=25)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.description

class Position(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    

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
    ##position = models.CharField(max_length=100,choices=LIST_POSITIONS)
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
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(8)],default=0)
    def __str__(self) -> str:
        return self.position.__str__() + ' , ' + self.moveKey.__str__() 
    

class Pattern():
    pattern = []
    pattern_length = 0
    pattern_dict = []
    i = 0
    def __init__(self):
        self.pattern = []   
        self.pattern_length = 0
        self.i = 0
        return 
    
    def __str__(self):
        return self.pattern
    
    def addMove(self, Move):
        self.pattern.append(Move)
        self.pattern_length += 1

        move_dict = { 'length' : Move.length, 'position' : Move.new_position, 'name' : Move.name, 'start_handhold' : Move.get_start_handhold_desc(), 'end_handhold' : Move.end_handhold.description}
        self.pattern_dict.append(move_dict)
        self.i+= Move.length

        return

    def reset(self):
        self.pattern = []
        self.pattern_dict = []
        self.i = 0
        return 
    
    def getPattern(self):
        return self.pattern
    
    def getPatternDict(self):
        return self.pattern_dict
    
    def getLastMove(self):
        if len(self.pattern) > 0:
            return self.pattern[len(self.pattern) - 1]
        else:
            return None
        
    def nextMove(self):
        move = ''
        if len(self.pattern) > 0:
            move = self.getLastMove() ##get the last move in the pattern

        if move == '':
            current_move = Move.objects.all().order_by("?").first()
            current_handhold = current_move.end_handhold
            ##move = current_move
            return current_move
        else:
            current_move = move
            current_handhold = current_move.end_handhold
            current_position = current_move.new_position
            ##print(current_move.end_handhold)    
            move_matrix = MoveMatrix.objects.filter(handHold=current_handhold,position=current_position) ##Filter to moves with specified handhold and position
            ##print(move_matrix)
            next_move_id = move_matrix.order_by("?").first().moveKey_id ##randomly sort and pick first (one) and get the move primary id
            next_move = Move.objects.filter(id=next_move_id).first()
            return next_move


    def createPattern(self, basic_length, contains='', startsWith=''):
        n = int(basic_length)*8
        ##moves_len = len(MOVES)
        ##i = 0
        loop = True
        while(loop):
            ##print("I: " + str(i))
            ##At the end of the loop, if contains has been set and the pattern has what is in contains then loop = false
            if(self.i ==n):
                if contains != '':
                    contains_move = Move.objects.get(id=contains)
                    ##print(contains_move)
                    contains_bool = False
                    for m in self.pattern:
                        if m == contains_move:
                            contains_bool = True
                    ##print(contains_bool)
                    if contains_bool == False:
                        ##reset all variables
                        self.reset()
                    else:
                        loop = False
                    contains_bool
                else:
                    loop = False
            ##rand_num = random.randint(0, moves_len-1)
            elif(self.i == 0):
                ##problem here
                move = self.nextMove()
                ##print(move.__str__())
                if startsWith != '':
                    if move == Move.objects.get(id=startsWith):
                        ## B 
                        self.addMove(move)                                       

                else:
                    ## B
                    self.addMove(move)

            else:
                current_move = self.getLastMove()
                ##Check to see if have enough counts left to add next move
                check = True
                while(check):
                    nxt_move = self.nextMove()
                    if(nxt_move.length + self.i <= n):
                        move = nxt_move
                        check = False

                    self.addMove(nxt_move)
                    