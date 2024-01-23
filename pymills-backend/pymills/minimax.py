import copy

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

# Prints board visually to CLI
def print_board(board):
    print("7  " + ("0" if board["A7"] is None else board["A7"][-1]) + "-----------" + ("0" if board["D7"] is None else board["D7"][-1]) + "------------" + ("0" if board["G7"] is None else board["G7"][-1]))
    print("   " + "|           |            |")
    print("6  " + "|   " + ("0" if board["B6"] is None else board["B6"][-1]) + "-------" + ("0" if board["D6"] is None else board["D6"][-1]) + "--------" + ("0" if board["F6"] is None else board["F6"][-1]) + "   |")
    print("   " + "|   |       |        |   |")
    print("5  " + "|   |   " + ("0" if board["C5"] is None else board["C5"][-1]) + "---" + ("0" if board["D5"] is None else board["D5"][-1]) + "---" + ("0" if board["E5"] is None else board["E5"][-1]) + "    |   |")
    print("   " + "|   |   |       |    |   |")
    print("4  " + ("0" if board["A4"] is None else board["A4"][-1]) + "---" + ("0" if board["B4"] is None else board["B4"][-1]) + "---" + ("0" if board["C4"] is None else board["C4"][-1]) + "       " + ("0" if board["E4"] is None else board["E4"][-1]) + "----" + ("0" if board["F4"] is None else board["F4"][-1]) + "---" + ("0" if board["G4"] is None else board["G4"][-1]))
    print("   " + "|   |   |       |    |   |")
    print("3  " + "|   |   " + ("0" if board["C3"] is None else board["C3"][-1]) + "---" + ("0" if board["D3"] is None else board["D3"][-1]) + "---" + ("0" if board["E3"] is None else board["E3"][-1]) + "    |   |")
    print("   " + "|   |       |        |   |")
    print("2  " + "|   " + ("0" if board["B2"] is None else board["B2"][-1]) + "-------" + ("0" if board["D2"] is None else board["D2"][-1]) + "--------" + ("0" if board["F2"] is None else board["F2"][-1]) + "   |")
    print("   " + "|           |            |")
    print("1  " + ("0" if board["A1"] is None else board["A1"][-1]) + "-----------" + ("0" if board["D1"] is None else board["D1"][-1]) + "------------" + ("0" if board["G1"] is None else board["G1"][-1]))
    print("   " + "A   B   C   D   E    F   G")

def evaluate_board(board, player, max_unplaced, min_unplaced, difficulty):
    if game_over(board, player, max_unplaced, min_unplaced):
        return -100000 if player else 100000
    
    score = 0
    mill_weight = 300
    piece_weight = 30
    if difficulty == "hard":
        control_weight = 10
        movement_weight = 10
        returning_mill_weight = 50
        preventing_mill_weight = 100
    else:
        control_weight = 0
        movement_weight = 0
        returning_mill_weight = 0
        preventing_mill_weight = 0
    
    max_arr = [key for key, value in board.items() if value == "Player1"]
    min_arr = [key for key, value in board.items() if value == "Player2"]
    
    max_pieces = count_pieces(board, "Player1")
    min_pieces = count_pieces(board, "Player2")
    
    future_max_mills = []
    future_min_mills = []
    
    # Max scoring
    max_mills = count_mills(board, "Player1")
    score += mill_weight * max_mills
    
    if max_mills == 3:
        return 100000
    
    # if max_pieces == 3 and max_unplaced == 0:
    #     score += mill_weight * max_mills
        
    score += piece_weight * max_pieces
    
    for point in max_arr:
        # Evaluate connections for maximizing player
        connection = connections[points.index(point)]
        can_move = False
        
        for conn in connection:
            if board[conn] is None:
                # If the piece has nighbouring possible move
                can_move = True
            
                if conn != point:
                    # Give more points for longer open connections
                    score += movement_weight
            
            # If a mill is possible in the next move for the maximizing player
            if max_unplaced == 0 and max_pieces > 3 and is_mills(board, True, conn):
                if conn not in future_max_mills and any(board[neighbour] == "Player1" and is_mills(board, True, neighbour) for neighbour in connections[points.index(conn)]):
                    future_max_mills.append(conn)   
        
        if not can_move:
            score -= 20
                
        # If a piece is preventing a mill, give additional points
        for mill in mills:
            if point in mill:
                preventing_mill = True
                player_count = 0
                none_count = 0
                possible_max_mill = None
                
                for p in mill:
                    if board[point] == "Player1":
                        player_count += 1
                    elif board[point] == None:
                        none_count += 1
                        possible_max_mill = p
                        
                    if p != point:
                        if board[p] == "Player1" or board[p] is None:
                            preventing_mill = False
                
                if player_count == 2 and none_count == 1 and ((max_unplaced == 0 and max_pieces == 3) or max_unplaced > 0):
                    future_max_mills.append(possible_max_mill)
                
                if preventing_mill:
                    score += preventing_mill_weight
        
        # To more points the piece is connected the more it is worth    
        score += control_weight * (len(connection) - 1)

    min_mills = count_mills(board, "Player2")
    
    if min_mills == 3:
        return -100000
    
    # Min scoring   
    score -= mill_weight * min_mills
    
    # if min_pieces == 3 and min_unplaced == 0:
    #     score -= mill_weight * min_mills
        
    score -= piece_weight * min_pieces
    
    for point in min_arr:
        # Evaluate connections for minimizing player
        connection = connections[points.index(point)]
        for conn in connection:
            can_move = False
            
            if board[conn] is None:
                can_move = True
                
                if conn != point:
                    # Give more points for longer open connections
                    score -= movement_weight
                
            # If a mill is possible in the next move for the minimizing player
            if min_unplaced == 0 and min_pieces > 3 and is_mills(board, False, conn):
                if conn not in future_min_mills and any(board[neighbour] == "Player2" and is_mills(board, False, neighbour) for neighbour in connections[points.index(conn)]):
                    future_min_mills.append(conn)
        
        if not can_move:
            score += 20
               
        # If a piece is preventing a mill, give additional points
        for mill in mills:
            if point in mill:
                preventing_mill = True
                player_count = 0
                none_count = 0
                possible_min_mill = None
                
                for p in mill:
                    if board[point] == "Player2":
                        player_count += 1
                    elif board[point] == None:
                        none_count += 1
                        possible_min_mill = p
                        
                    if p != point:
                        if board[p] == "Player2" or board[p] is None:
                            preventing_mill = False
                
                if player_count == 2 and none_count == 1 and ((min_unplaced == 0 and min_pieces == 3) or min_unplaced > 0):
                    future_min_mills.append(possible_min_mill)
                   
                if preventing_mill:
                    score -= preventing_mill_weight
            
        # To more points the piece is connected the more it is worth    
        score -= control_weight * (len(connection) - 1)
        
   # Add returning mill weight bonuses based on future mill possibilities
    if not future_min_mills and future_max_mills:
        for max_fmill in future_max_mills:
            if all(board[c] != "Player2" and board[c] != None for c in connections[points.index(max_fmill)]):
                score += returning_mill_weight

    if not future_max_mills and future_min_mills:
        for min_fmill in future_min_mills:
            if all(board[c] != "Player1" and board[c] != None for c in connections[points.index(min_fmill)]):
                score -= returning_mill_weight
            
    return score

# Counts the number of mills for a player on the board
def count_mills(board, player):
    count = 0
    
    for mill in mills:
        if all(board[point] == player for point in mill):
            count += 1
            
    return count

# Counts the number of pieces for a player on 
def count_pieces(board, player):
    return sum(1 for value in board.values() if value == player)

# move array format [type, piecedestination, ismax, ismills, pieceorigin, ifmillswhattoremove]
# Generates all possible moves for a player in the passed in boards condition
def generate_moves(board, player, max_unplaced, min_unplaced):
    placeable = False
    moves = []
    
    # Generates moves if a player can place a piece
    if (player and max_unplaced > 0) or (not player and min_unplaced > 0):
        placeable = True
    
    if placeable:
            for point, value in board.items():
                if value is None:
                    move = [
                        "PLACE",
                        point, 
                        player, 
                        is_mills(board, player, point),
                        None,
                        None
                    ]
                    moves.append(move)
                    
            return moves

    # Number of points a player has on the board
    points_with_player = [key for key, value in board.items() if value == ("Player1" if player else "Player2")]
    
    # If there is more then 3 pieces on the board, generate the possible moves
    if len(points_with_player) > 3:
        for point in points_with_player:
            possible_moves = connections[points.index(point)]
            
            for dest in possible_moves:
                if board[dest] == None:
                    board[point] = None
                    move = [
                        "MOVE",
                        dest,
                        player,
                        is_mills(board, player, dest),
                        point,
                        None
                    ]
                    moves.append(move)
                    board[point] = ("Player1" if player else "Player2")
                    
        return moves
    
    # If there is less than or 3 pieces on the board, the piece can be moved anywhere
    elif len(points_with_player) <= 3:
        for point in points_with_player:
            possible_moves = [key for key, value in board.items() if value is None]
            
            for dest in possible_moves:
                # t_board = copy.deepcopy(board)
                # t_board[point] = None
                # t_board[dest] = player
                board[point] = None
                move = [
                    "MOVE",
                    dest,
                    player,
                    is_mills(board, player, dest),
                    point,
                    None
                ]
                moves.append(move)
                board[point] = ("Player1" if player else "Player2")
                
        return moves   
    
    # connections[points.index(point)] - all possible moves from that point
    return moves

# Checks if a piece placed by the player on the specific_point makes a mill on the current board
def is_mills(board, player, specific_point):
    piece = ("Player1" if player else "Player2")
    
    for mill in mills:
        if specific_point in mill and board[specific_point] == None:
            if all(board[p] == piece for p in mill if p != specific_point):
                return True
            
    return False

# Checks if the board has any possible moves
def game_over(board, player, max_unplaced, min_unplaced):
    piece = ("Player1" if player else "Player2")
    count_player1 = sum(1 for value in board.values() if value == piece)
    count_player2 = sum(1 for value in board.values() if value == piece)

    if count_player1 <= 2 and max_unplaced == 0:
        #print("Player1 has been reduced to two pieces. Player2 wins!")
        return True
    elif count_player2 <= 2 and min_unplaced == 0:
        #print("Player2 has been reduced to two pieces. Player1 wins!")
        return True

    player1_moves = generate_moves(board, player, max_unplaced, min_unplaced)
    player2_moves = generate_moves(board, player, max_unplaced, min_unplaced)

    if player and not player1_moves:
        #print("Player1 is blocked. Player2 wins!")
        return True
    elif not player and not player2_moves:
        #print("Player2 is blocked. Player1 wins!")
        return True

    return False

# move array format [type, piecedestination, ismax, ismills, pieceorigin, ifmillswhattoremove]
# Applies the passed in move to the board
def make_move(board, move, max_unplaced, min_unplaced):
    piece = ("Player1" if move[2] else "Player2")
    if move[0] == "PLACE":
        if move[2]:
            max_unplaced = max_unplaced - 1
        else:
            min_unplaced = min_unplaced - 1
            
        board[move[1]] = piece
    elif move[0] == "MOVE":
        board[move[1]] = piece
        board[move[4]] = None
        
    if move[5] != None:
        board[move[5]] = None
        
    return

# Reverses the passed in move
def undo_move(board, move, max_unplaced, min_unplaced):
    piece = ("Player1" if move[2] else "Player2")
    
    if move[0] == "PLACE":
        if move[2]:
            max_unplaced = max_unplaced + 1
        else:
            min_unplaced = min_unplaced + 1
        
        board[move[1]] = None
    elif move[0] == "MOVE":
        board[move[1]] = None
        board[move[4]] = piece
        
    return

# Checks if the specific point is a part of a mill
def in_mill(board, point):
    piece = board[point]
    m = [all(board[point] == piece for point in mill) for mill in [mill for mill in mills if point in mill]]
    if any(m):
        return True
    
    return False    

# Returns array of enemy pieces points
def return_enemies(board, player):
    enemy_piece = ("Player2" if player else "Player1")
    return [key for key, value in board.items() if value == enemy_piece]

# The Minimax alpha-beta pruning algorithm function 
def minimax(board, depth, alpha, beta, maximizing_player, unplaced_of_maximizing_player, unplaced_of_minimizing_player, difficulty):
    if depth == 0 or game_over(board, maximizing_player, unplaced_of_maximizing_player, unplaced_of_minimizing_player):
        return evaluate_board(board, maximizing_player, unplaced_of_maximizing_player, unplaced_of_minimizing_player, difficulty), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        moves = generate_moves(board, maximizing_player, unplaced_of_maximizing_player, unplaced_of_minimizing_player)
        moves = sorted(moves, key=lambda move: move[3], reverse=True)
        
        for move in moves:
            make_move(board, move, unplaced_of_maximizing_player, unplaced_of_minimizing_player)

            if move[3]:
                flag_removed = False
                enemies = return_enemies(board, maximizing_player)
                
                min_mills = count_mills(board, "Player2")
                min_pieces = count_pieces(board, "Player2")
                
                all_in_mill = False
                
                if unplaced_of_minimizing_player == 0:
                    if (min_pieces <= 6 and min_mills == 2) or (min_pieces <= 9 and min_mills == 3) or (min_pieces == 3 and min_mills == 1):
                        all_in_mill = True 
                
                for enemy in enemies:
                    if all_in_mill or not in_mill(board, enemy):
                        flag_removed = True
                        board[enemy] = None
                        eval, _ = minimax(board, depth - 1, alpha, beta, False, unplaced_of_maximizing_player, unplaced_of_minimizing_player, difficulty)
                        board[enemy] = "Player2"
                        
                        if eval > max_eval:
                            move[5] = enemy
                            max_eval = eval
                            best_move = move

                if not flag_removed:
                    eval, _ = minimax(board, depth - 1, alpha, beta, False, unplaced_of_maximizing_player, unplaced_of_minimizing_player, difficulty)
            else:
                eval, _ = minimax(board, depth - 1, alpha, beta, False, unplaced_of_maximizing_player, unplaced_of_minimizing_player, difficulty)

            undo_move(board, move, unplaced_of_maximizing_player, unplaced_of_minimizing_player)
           
            if eval > max_eval:
                max_eval = eval
                best_move = move
                
            alpha = max(alpha, eval)
            
            if alpha >= beta:
                break

        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        moves = generate_moves(board, maximizing_player, unplaced_of_maximizing_player, unplaced_of_minimizing_player)
        moves = sorted(moves, key=lambda move: move[3], reverse=True)

        for move in moves:
            make_move(board, move, unplaced_of_maximizing_player, unplaced_of_minimizing_player)

            if move[3]:
                flag_removed = False
                enemies = return_enemies(board, maximizing_player)
                
                max_mills = count_mills(board, "Player1")
                max_pieces = count_pieces(board, "Player1")
                
                all_in_mill = False
                
                if unplaced_of_maximizing_player == 0:
                    if (max_pieces <= 6 and max_mills == 2) or (max_pieces <= 9 and max_mills == 3) or (max_pieces == 3 and max_mills == 1):
                        all_in_mill = True 
                
                for enemy in enemies:
                    if all_in_mill or not in_mill(board, enemy):
                        flag_removed = True
                        board[enemy] = None
                        eval, _ = minimax(board, depth - 1, alpha, beta, True, unplaced_of_maximizing_player, unplaced_of_minimizing_player, difficulty)
                        board[enemy] = "Player1"
                        
                        if eval < min_eval:
                            move[5] = enemy
                            min_eval = eval
                            best_move = move

                if not flag_removed:
                    eval, _ = minimax(board, depth - 1, alpha, beta, True, unplaced_of_maximizing_player, unplaced_of_minimizing_player, difficulty)
            else:
                eval, _ = minimax(board, depth - 1, alpha, beta, True, unplaced_of_maximizing_player, unplaced_of_minimizing_player, difficulty)

            undo_move(board, move, unplaced_of_maximizing_player, unplaced_of_minimizing_player)

            if eval < min_eval:
                min_eval = eval
                best_move = move
                
            beta = min(beta, eval)
            
            if alpha >= beta:
                break
           
        return min_eval, best_move

#  a7----------d7-----------g7
#  |           |            |
#  |   b6------d6-------f6  |
#  |   |       |        |   |
#  |   |   c5--d5---e5  |   |
#  |   |   |        |   |   |
#  a4--b4--c4       e4--f4--g4
#  |   |   |        |   |   |
#  |   |   c3--d3--e3   |   |
#  |   |       |        |   |
#  |   b2------d2-------f2  |
#  |           |            |
#  a1----------d1----------g1