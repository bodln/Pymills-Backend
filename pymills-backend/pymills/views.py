from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import os
from pymills.minimax import minimax, make_move, generate_moves

# All possible points on a board
points = ["A1", "A4", "A7", 
          "B2", "B4", "B6", 
          "C3", "C4", "C5", 
          "D1", "D2", "D3", "D5", "D6", "D7", 
          "E3", "E4", "E5", 
          "F2", "F4", "F6", 
          "G1", "G4", "G7"]

# All possible mills on board
mills = [
    ["A1", "A4", "A7"],
    ["B2", "B4", "B6"],
    ["C3", "C4", "C5"],
    ["D1", "D2", "D3"],
    ["D5", "D6", "D7"],
    ["E3", "E4", "E5"],
    ["F2", "F4", "F6"],
    ["G1", "G4", "G7"],
    ["A1", "D1", "G1"],
    ["B2", "D2", "F2"],
    ["C3", "D3", "E3"],
    ["A4", "B4", "C4"],
    ["E4", "F4", "G4"],
    ["C5", "D5", "E5"],
    ["B6", "D6", "F6"],
    ["A7", "D7", "G7"]
]

# All possible connections for each point, at connections[0] being the connections for points[0] and so on
connections = [
    ["A1", "A4", "D1"],
    ["A4", "A1", "A7", "B4"],
    ["A7", "A4", "D7"],
    ["B2", "B4", "D2"],
    ["B4", "B2", "B6", "A4", "C4"],
    ["B6", "B4", "D6"],
    ["C3", "C4", "D3"],
    ["C4", "C5", "C3", "B4"],
    ["C5", "C4", "D5"],
    ["D1", "A1", "G1", "D2"],
    ["D2", "D1", "D3", "B2", "F2"],
    ["D3", "D2", "C3", "E3"],
    ["D5", "D6", "C5", "E5"],
    ["D6", "D5", "D7", "B6", "F6"],
    ["D7", "A7", "G7", "D6"],
    ["E3", "E4", "D3"],
    ["E4", "E5", "E3", "F4"],
    ["E5", "E4", "D5"],
    ["F2", "F4", "D2"],
    ["F4", "F2", "F6", "G4", "E4"],
    ["F6", "F4", "D6"],
    ["G1", "G4", "D1"],
    ["G4", "G1", "G7", "F4"],
    ["G7", "G4", "D7"]
]

# The board represented by a dictionary 
board = {point: None for point in points}

@require_http_methods(["GET", "POST"])
@csrf_exempt
def OK(request):
    return HttpResponse("OK")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def maps_list(request):
    current_dir = os.path.dirname(__file__)
    maps_dir = os.path.join(current_dir, 'maps')

    maps = []

    for file in os.listdir(maps_dir):
        if file.endswith('.json'):
            maps.append({
                'map_name': file[:-5],
                'map_data': json.load(open(os.path.join(maps_dir, file)))
            })

    return HttpResponse(json.dumps(maps))


@require_http_methods(["GET", "POST"])
@csrf_exempt
def get_move(request):
    body = request.body
    
    for point, player in board.items():
        board[point] = None

    map_name = json.loads(body)['mapName']
    timeout = json.loads(body)['timeout']
    depth = json.loads(body)['depth']
    difficulty = json.loads(body)['difficulty']
    current_game_state = json.loads(body)['gameState']
    
    turn = current_game_state['player'] == "white"
    white_unplaced = current_game_state['unplacedPieces']['white']
    black_unplaced = current_game_state['unplacedPieces']['black']
    occupied_points = current_game_state['occupiedPoints']
    
    print(turn)
    
    print(white_unplaced)
    print(black_unplaced)
    
    for point_info in occupied_points:
        point = point_info['point']
        player = point_info['player']
        
        if player == "white":
            piece = "Player1"
        else:
            piece = "Player2"
            
        board[point] = piece
        
    if difficulty == "easy":
        depth = 1
    else:
        depth = 4
    
    eval, best_move = minimax(board, depth, float('-inf'), float('inf'), turn, white_unplaced, black_unplaced, difficulty)

    print(difficulty)
    
    if turn:
        next_player = "black"
        if white_unplaced > 0:
            white_unplaced -= 1
    else: 
        next_player = "white"
        if black_unplaced > 0:
            black_unplaced -= 1
    
    #print(board)
    #print(best_move)
    make_move(board, best_move, white_unplaced, black_unplaced)
    #print(board)
    
    game_state_dict = {
    'gameState': {
        'player': next_player,
        'unplacedPieces': {
            'black': black_unplaced,
            'white': white_unplaced
        },
        'occupiedPoints': [{'point': point, 'player': 'white' if player == 'Player1' else 'black' if player == 'Player2' else None} for point, player in board.items() if player is not None]
        },
    'eval': eval,
    'move': best_move
    }
    #print(game_state_dict)

    #new_game_state = get_best_move(current_game_state, depth, map_name, difficulty, timeout)
    
    #print(new_game_state)
    
    return HttpResponse(json.dumps(game_state_dict))

# Game map example:
#  0-----------1-----------2
#  |           |           |
#  |   3-------4-------5   |
#  |   |       |       |   |
#  |   |   6---7---8   |   |
#  |   |   |       |   |   |
#  9--10--11       12--13--14
#  |   |   |       |   |   |
#  |   |   15-16--17   |   |
#  |   |       |       |   |
#  |   18------19-----20   |
#  |           |           |
#  21---------22----------23
