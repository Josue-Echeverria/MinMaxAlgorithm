import math
from unittest import case
import numpy as np

NUMBER_OF_DOTS = 3

class Node:
    def __init__(self, board_status, row_status, col_status, player):
        self.children = []
        self.row_status = row_status
        self.col_status = col_status
        self.player = player
        self.board_status = board_status
    def __str__(self):
        return f"row: \n{self.row_status}, \ncol: \n{self.col_status}, \nboard: \n{self.board_status}\n"

def create_next_state(board_status, row_status, col_status, type, logical_position):
    r = logical_position[0]
    c = logical_position[1]

    if c < (NUMBER_OF_DOTS-1) and r < (NUMBER_OF_DOTS-1):
        board_status[r][c] += 1

    if type == 'row':
        row_status[r][c] = 1
        if r >= 1:
            board_status[r-1][c] += 1
            
    elif type == 'col':
        col_status[r][c] = 1
        if c >= 1:
            board_status[r][c-1] += 1


def generate_children(node):
    children = []
    possible_moves = get_possible_moves(node)

    for move in possible_moves:
        # print("Generating child for move:", move)
        type, position = move
        new_board_status = np.copy(node.board_status)
        new_row_status = np.copy(node.row_status)
        new_col_status = np.copy(node.col_status)
        create_next_state(new_board_status, new_row_status, new_col_status, type, position)
        if np.all(new_board_status == 5):
            continue
        child = Node(new_board_status, new_row_status, new_col_status, 2 if node.player == 1 else 1)
        children.append(child)
    return children

def get_possible_moves(node):
    """Retorna una lista de movimientos posibles para el nodo actual"""
    possible_moves = []
    for i in range(NUMBER_OF_DOTS):
        for j in range(NUMBER_OF_DOTS - 1):
            if node.row_status[i][j] == 0:
                possible_moves.append(('row', (i, j)))
            if node.col_status[j][i] == 0:
                possible_moves.append(('col', (j, i)))
    return possible_moves

def is_terminal(node):
    return np.all(node.board_status == 4)

def get_score(board_status, player):
    score = 0
    base = 10
    if player == 2:
        base = -10
    match board_status:
        case 4:
            score += base
        case 3:
            score += 0
        case 2:
            score += base / 2
        case 1:
            score += base / 3
    return score

def evaluate(node):
    value = 0
    for i in range(NUMBER_OF_DOTS - 1):
        for j in range(NUMBER_OF_DOTS - 1):
            value += get_score(node.board_status[i][j], node.player)
    return value

def minmax(node, depth, is_maximizing):
    if depth == 0 or is_terminal(node):
        return evaluate(node), None

    if is_maximizing:
        # -Infinito
        max_eval = -math.inf
        best_move = None
        children = generate_children(node)
        possible_moves = get_possible_moves(node)
        
        for i, child in enumerate(children):
            eval_value, _ = minmax(child, depth - 1, False)
            if eval_value > max_eval:
                max_eval = eval_value
                best_move = possible_moves[i]
        return max_eval, best_move
    else:
        # Infinito
        min_eval = +math.inf
        best_move = None
        children = generate_children(node)
        possible_moves = get_possible_moves(node)
        
        for i, child in enumerate(children):
            eval_value, _ = minmax(child, depth - 1, True)
            if eval_value < min_eval:
                min_eval = eval_value
                best_move = possible_moves[i]
        return min_eval, best_move

def print_best_move(best_move):
    """Imprime el mejor movimiento de manera legible"""
    if best_move:
        move_type, position = best_move
        print(f"  {move_type} at {position}")
    else:
        print(" No hay movimientos disponibles o se alcanzó un estado terminal")

if __name__ == "__main__":
    # testing_board = [[2]]
    # testing_row_status = [[0], [1]]
    # testing_col_status = [[0, 1]]

    # testing_board = [[3]]
    # testing_row_status = [[0], [1]]
    # testing_col_status = [[1, 1]]

    # testing_board = [[4]]
    # testing_row_status = [[1], [1]]
    # testing_col_status = [[1, 1]]

    # testing_board = [[3, 4],
    #                  [3, 4]]
    # testing_row_status = [[1, 1], 
    #                       [0, 1], 
    #                       [1, 1]]
    # testing_col_status = [[1, 1, 1], 
    #                       [1, 1, 1]]

    # testing_board = [[3, 4],
    #                  [3, 2]]
    # testing_row_status = [[1, 1], 
    #                       [0, 1], 
    #                       [1, 0]]
    # testing_col_status = [[1, 1, 1], 
    #                       [1, 1, 0]]

    testing_board = [[3, 3],
                     [0, 0]]
    testing_row_status = [[1, 1],
                          [0, 0],
                          [0, 0]]
    testing_col_status = [[1, 1, 1], 
                          [0, 0, 0]]

    root = Node(testing_board, testing_row_status, testing_col_status, 2)
    print("=== EJECUTANDO MINIMAX ===")
    minmax_value, best_move = minmax(root, 6, True)
    
    print("\n=== RESULTADOS ===")
    print(f"Valor MinMax: {minmax_value}")
    print_best_move(best_move)