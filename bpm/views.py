from django.shortcuts import render
from . import views
from bpm.form import InputForm
from django.http import HttpResponse
import random
from .models import Move, MoveMatrix
# Create your views here.
MOVES = {
    0 : {"name" : 'basic',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : 4,
     "level" : 1},
     1 : {"name" : 'double hand follower turn',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : "H1"},
     2 : {"name" : 'L hand follower turn',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : 4},
     3 : {"name" : 'R hand follower turn',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : 4},
    4 : {"name" : 'double hand follower hammerlock',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : 8},
     5 : {"name" : 'switch side turn',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : 4},
     6 : {"name" : 'wrap',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : "H1"},
     7 : {"name" : 'unwrap',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : 4},
     8 : {"name" : 'unwrap',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : "",
     "e_handhold" : 4},
     9 : {"name" : 'basic',
     "position" : 'close',
     "length" : 4,
     "s_handhold" : 9,
     "e_handhold" : 9},
     10 : {"name" : 'box step',
     "position" : 'close',
     "length" : 8   ,
     "s_handhold" : 9,
     "e_handhold" : 9},
     11 : {"name" : 'transition to open',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : 9,
     "e_handhold" : 4},
     12 : {"name" : 'transition to close',
     "position" : 'close',
     "length" : 4,
     "s_handhold" : 4,
     "e_handhold" : 9},
     13 : {"name" : 'hip roll',
     "position" : 'open',
     "length" : 4,
     "s_handhold" : 8,
     "e_handhold" : 8},
     14 : {"name" : 'turn into cuddle',
     "position" : 'cuddle',
     "length" : 4,
     "s_handhold" : 4,
     "e_handhold" : 4,
     "s_count" : 4},
     15 : {"name" : 'body roll',
     "position" : 'cuddle',
     "length" : 4,
     "s_handhold" : 8,
     "e_handhold" : 8},
}

POSITIONS = [
    'open', 'close', 'close sensual', 'cuddle','sweetheart', 'shadow-fl',
    'shadow-lf'
]

HANDHOLDS = {
    ##0 : 'left to left',
    ##1 : 'left to right',
    ##2 : 'right to left',
    ##3 : 'right to right',
    4 : 'left to right, right to left',
    ##5 : 'right to right, left to left',
    ##6 : 'left to right, right to left',
    ##7 : 'arm lock',
    8 : 'left to right, right to left hammerlock',
    9 : 'close position'
}


MOVES_BY_HANDHOLDS = {
    4 : [0,2,3,4,5,12,13],
    8 : [5,7],
    9 : [9,10,11]
}


def nextmove(move=''):
    if move == '':
        current_move = Move.objects.all().order_by("?").first()
        current_handhold = current_move.end_handhold
        ##move = current_move
        return current_move
    else:
        current_move = move
        current_handhold = current_move.end_handhold
        current_position = current_move.new_position
        print(current_move.end_handhold)
        move_matrix = MoveMatrix.objects.filter(handHold=current_handhold,position=current_position) ##Filter to moves with specified handhold and position
        print(move_matrix)
        next_move_id = move_matrix.order_by("?").first().moveKey_id ##randomly sort and pick first (one) and get the move primary id
        next_move = Move.objects.filter(id=next_move_id).first()
        print("Next move:" + next_move.__str__())
        return next_move

def checkValidMove(move,cnt):
    if move['s_count'] == cnt % 8:
        return True 
    else:
        return False


def home(request): 
    form = InputForm()
    if(request.GET.get('num_basic_length', None)):
        basic_length = request.GET.get('num_basic_length')
        contains = request.GET.get('contains')
        n = int(basic_length)*8
        ##moves_len = len(MOVES)
        i = 0
        pattern = []
        pattern1 = []
        loop = True
        while(loop):
            print("I: " + str(i))
            ##At the end of the loop, if contains has been set and the pattern has what is in contains then loop = false
            if(i ==n):
                if contains != '':
                    contains_move = Move.objects.get(id=contains)
                    print(contains_move)
                    contains_bool = False
                    for m in pattern:
                        if m == contains_move:
                            contains_bool = True
                    print(contains_bool)
                    if contains_bool == False:
                        ##reset all variables
                        i = 0
                        pattern = []
                        pattern1 = []
                    else:
                        loop = False
                    contains_bool
                else:
                    loop = False
            ##rand_num = random.randint(0, moves_len-1)
            elif(i == 0):
                ##problem here
                move = nextmove()
                print(move.__str__())
                pattern.append(move)
                ##need to change handhold id in Move model to string description
                ##how to connect this elif with else statement so changes in one affect the other. if i change move.position to move.new_position here, I also have to do it in the else statement
                move1 = { 'length' : move.length, 'position' : move.new_position, 'name' : move.name, 'start_handhold' : move.get_start_handhold_desc(), 'end_handhold' : move.end_handhold.description}
                pattern1.append(move1)
                i+= move.length

            else:
                current_move = pattern[len(pattern)-1]
                ##Check to see if have enough counts left to add next move
                check = True
                while(check):
                    nxt_move = nextmove(current_move)
                    if(nxt_move.length + i <= n):
                        move = nxt_move
                        check = False

                ##add new move to pattern
                move1 = { 'length' : move.length, 'position' : move.new_position, 'name' : move.name, 'start_handhold' : move.get_start_handhold_desc(), 'end_handhold' : move.end_handhold.description}
                pattern.append(move)
                pattern1.append(move1)
                print(pattern)
                i+= move.length
        context = {'form' : form, 'pattern' : pattern1 }
    else:
        context = {'form' : form}
    return render(request, 'index.html', context)

