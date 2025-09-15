import math
from unittest import case
import numpy as np

NUMBER_OF_DOTS = 3

class Node:
    def __init__(self, board_status, row_status, col_status, player, boxes_completed=None, score_player_1=0, score_player_2=0):
        self.children = []
        self.row_status = row_status
        self.col_status = col_status
        self.player = player
        self.board_status = board_status
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2
        # Calcular cajas completadas basándose en board_status
        if boxes_completed is None:
            self.boxes_completed = np.count_nonzero(board_status == 4)
        else:
            self.boxes_completed = boxes_completed
    def __str__(self):
        return f"row: \n{self.row_status}, \ncol: \n{self.col_status}, \nboard: \n{self.board_status}\n"

def create_next_state(board_status, row_status, col_status, type, logical_position):
    """
    Actualiza el estado del juego después de hacer un movimiento.
    - board_status: matriz que cuenta las líneas alrededor de cada caja
    - row_status: matriz que marca las líneas horizontales
    - col_status: matriz que marca las líneas verticales
    - type: 'row' o 'col' según el tipo de línea
    - logical_position: (fila, columna) de la línea a dibujar
    """
    r = logical_position[0]
    c = logical_position[1]
    scored = False
    if type == 'row':
        row_status[r][c] = 1
        # Afecta la caja de arriba (si existe)
        if r >= 1:
            board_status[r-1][c] += 1
            if board_status[r-1][c] == 4:
                scored = True
        # Afecta la caja de abajo (si existe)
        if r < (NUMBER_OF_DOTS-1):
            board_status[r][c] += 1
            if board_status[r][c] == 4:
                scored = True
            
    elif type == 'col':
        col_status[r][c] = 1
        # Afecta la caja de la izquierda (si existe)
        if c >= 1:
            board_status[r][c-1] += 1
            if board_status[r][c-1] == 4:
                scored = True
        # Afecta la caja de la derecha (si existe)  
        if c < (NUMBER_OF_DOTS-1):
            board_status[r][c] += 1
            if board_status[r][c] == 4:
                scored = True
    return scored

def generate_children(node):
    children = []
    possible_moves = get_possible_moves(node)

    for move in possible_moves:
        type, position = move
        new_board_status = np.copy(node.board_status)
        new_row_status = np.copy(node.row_status)
        new_col_status = np.copy(node.col_status)
        scored = create_next_state(new_board_status, new_row_status, new_col_status, type, position)

        # Evitar estados imposibles
        if np.all(new_board_status == 5):
            continue
            
        # Crear nodo hijo con el mismo jugador inicialmente
        child = Node(new_board_status, new_row_status, new_col_status, node.player, 
                    node.boxes_completed, node.score_player_1, node.score_player_2)
        if scored:
            child.boxes_completed += 1
        boxes_scored = update_scores(child)
        
        # Si no anotó, cambia de jugador
        if boxes_scored == 0:
            child.player = 2 if node.player == 1 else 1
        # Si anotó, el jugador continúa (child.player ya es el correcto)
            
        children.append(child)
    return children, possible_moves

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

def update_scores(node):
    # print(f"Boxes completed: {node.boxes_completed}, Scores: P1={node.score_player_1}, P2={node.score_player_2}")
    if node.boxes_completed > node.score_player_1 + node.score_player_2:
        if node.player == 1:
            node.score_player_1 += 1
            return 1
        else:
            node.score_player_2 += 1
            return 2
    return 0

def evaluate(node):
    """
    Función de evaluación basada en los puntajes reales de los jugadores.
    Retorna la diferencia de puntajes: score_player_1 - score_player_2
    """
    return node.score_player_1 - node.score_player_2

def minmax(node, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    """
    Algoritmo MinMax con poda alpha-beta.
    - node: nodo actual del juego
    - depth: profundidad máxima a explorar
    - is_maximizing: True si es turno del jugador maximizador (jugador 1)
    - alpha: mejor valor para el jugador maximizador
    - beta: mejor valor para el jugador minimizador
    """
    if depth == 0 or is_terminal(node):
        return evaluate(node), None

    if is_maximizing:
        max_eval = -math.inf
        best_move = None
        children, possible_moves = generate_children(node)
        
        for i, child in enumerate(children):
            eval_value, _ = minmax(child, depth - 1, False, alpha, beta)
            if eval_value > max_eval:
                max_eval = eval_value
                best_move = possible_moves[i]
            alpha = max(alpha, eval_value)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = +math.inf
        best_move = None
        children, possible_moves = generate_children(node)
        
        for i, child in enumerate(children):
            eval_value, _ = minmax(child, depth - 1, True, alpha, beta)
            if eval_value < min_eval:
                min_eval = eval_value
                best_move = possible_moves[i]
            beta = min(beta, eval_value)
            if beta <= alpha:
                break
        return min_eval, best_move

def print_best_move(best_move):
    """Imprime el mejor movimiento de manera legible"""
    if best_move:
        move_type, position = best_move
        print(f"Mejor movimiento: {move_type} en posición {position}")
    else:
        print("No hay movimientos disponibles o se alcanzó un estado terminal")

def print_game_state(node):
    """Imprime el estado actual del juego de manera legible"""
    print("\n=== ESTADO DEL JUEGO ===")
    print(f"Jugador actual: {node.player}")
    print(f"Puntajes - Jugador 1: {node.score_player_1}, Jugador 2: {node.score_player_2}")
    print(f"Cajas completadas: {node.boxes_completed}")
    print(f"Board status:\n{node.board_status}")
    print(f"Row status:\n{node.row_status}")  
    print(f"Col status:\n{node.col_status}")

if __name__ == "__main__":
    # Ejemplo de estado de juego para pruebas
    testing_board = [[3, 3],
                     [0, 0]]
    testing_row_status = [[1, 1],
                          [0, 0],
                          [0, 0]]
    testing_col_status = [[1, 1, 1], 
                          [0, 0, 0]]

    # Crear nodo raíz
    root = Node(testing_board, testing_row_status, testing_col_status, 2)
    
    print("=== EJECUTANDO MINIMAX ===")
    print_game_state(root)
    
    # Ejecutar algoritmo MinMax
    minmax_value, best_move = minmax(root, 6, True)
    
    print("\n=== RESULTADOS ===")
    print(f"Valor MinMax: {minmax_value}")
    print_best_move(best_move)