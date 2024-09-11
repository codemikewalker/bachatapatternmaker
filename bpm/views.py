from django.shortcuts import render
from . import views
from bpm.form import InputForm
from django.http import HttpResponse
import random
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

##current_hh_state = random.choice(list(HANDHOLDS.items()))[0]
current_hh_state = 4

def nextmove(handhold=4, current_cnt=0):
    print("handhold: " + str(handhold))
    next_move_id = random.choice(MOVES_BY_HANDHOLDS[handhold])
    next_move = MOVES[next_move_id]
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
        n = int(basic_length)*8
        ##moves_len = len(MOVES)
        i = 0
        pattern = []
        while(i < n):
            ##rand_num = random.randint(0, moves_len-1)
            if(i == 0):
                move = nextmove()
                print(move)
                pattern.append(move)
            else:
                print(move)
                ##Check to see if have enough counts left to add next move
                check = True
                while(check):
                    nxt_move = nextmove(handhold=move['e_handhold'],current_cnt=i)
                    if(nxt_move['length']+ i <= n):
                        move = nxt_move
                        check = False

                ##add new move to pattern
                pattern.append(move)
            i+= move['length']
        context = {'form' : form, 'pattern' : pattern }
    else:
        context = {'form' : form}
    return render(request, 'index.html', context)


def home_view(request): 
    form = InputForm()
    if(request.GET.get('num_basic_length', None)):
        basic_length = request.GET.get('num_basic_length')
        n = int(basic_length)
        ##moves_len = len(MOVES)
        i = 0
        pattern = []
        while(i < n):
            rand_num = random.randint(0, moves_len-1)
            items = list(MOVES.items())
            move = random.choice(items)
            pattern.append(move[1])
            i+=1
        context = {'form' : form, 'pattern' : pattern }
    else:
        context = {'form' : form}
    return render(request, 'index.html', context)

