# Author: aqeelanwar
# Created: 13 March,2020, 9:19 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import numpy as np
import minmax
from minmax import Node, minmax as minimax_algorithm

# Paleta de colores personalizada
COLOR_OXIDO = "#a74629"   # Fichas (puntos)
COLOR_VINO  = "#1db3f4"   # Bordes jugador 1 / Títulos
COLOR_AZUL  = "#e0e0e0"   # Fondo app
COLOR_ORO   = "#A4E4FF"   # Celdas
COLOR_TEXTO = "#333333"   # Texto principal (claro para contraste)
COLOR_TEXTO_OSCURO = "#333333" # Texto oscuro para entradas
COLOR_BORDE_J2 = "#8c2a1e" # Borde para jugador 2 (variación de óxido)
COLOR_CELDA_J2 = "#d4b77a" # Celda para jugador 2 (variación de oro)

# Ajustes visuales del tablero (lado izquierdo)
BOARD_OFFSET_X = 24  # margen izquierdo interno
BOARD_OFFSET_Y = 24  # margen superior interno
COLOR_GRID = "#777777"  # líneas guía de la cuadrícula (suave)

size_of_board = 600
NUMBER_OF_DOTS = 3  # Se actualizará con la selección del usuario
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = COLOR_OXIDO
player1_color = COLOR_VINO
player1_color_light = COLOR_ORO
player2_color = COLOR_BORDE_J2
player2_color_light = COLOR_CELDA_J2
Green_color = COLOR_ORO # Reemplazado por ORO para consistencia
dot_width = 0.22*size_of_board/NUMBER_OF_DOTS
edge_width = 0.08*size_of_board/NUMBER_OF_DOTS
distance_between_dots = size_of_board / (NUMBER_OF_DOTS)

def show_game_setup():
    """Muestra ventana de configuración inicial del juego"""
    setup_window = Tk()
    setup_window.title('Configuración del Juego - Dots and Boxes')
    setup_window.geometry('450x450')  # Aumentar altura para nueva opción
    setup_window.resizable(False, False)
    
    # Centrar la ventana
    setup_window.eval('tk::PlaceWindow . center')
    
    # Variables para almacenar la configuración
    dots_var = StringVar(value="3")
    game_mode_var = StringVar(value="minmax") # 'minmax' o 'minmax_random'
    
    setup_window.config(bg=COLOR_AZUL)
    
    # Título
    Label(setup_window, text="Dots and Boxes", 
          font=("Arial", 20, "bold"), fg=COLOR_TEXTO, bg=COLOR_AZUL).pack(pady=15)
    
    # Subtítulo
    Label(setup_window, text="Configuración inicial del tablero", 
          font=("Arial", 12), fg=COLOR_TEXTO, bg=COLOR_AZUL).pack(pady=5)
    
    # Frame para entrada de tamaño
    size_frame = Frame(setup_window, bg=COLOR_AZUL)
    size_frame.pack(pady=10)
    
    Label(size_frame, text="Introduce el número de puntos por lado:", 
          font=("Arial", 12, "bold"), fg=COLOR_TEXTO, bg=COLOR_AZUL).pack(pady=5)
    
    # Frame para el campo de entrada y validación
    input_frame = Frame(size_frame, bg=COLOR_AZUL)
    input_frame.pack(pady=5)
    
    Label(input_frame, text="Puntos:", font=("Arial", 11), fg=COLOR_TEXTO, bg=COLOR_AZUL).pack(side=LEFT, padx=5)
    
    # Campo de entrada para el número de puntos
    dots_entry = Entry(input_frame, textvariable=dots_var, width=10, 
                       font=("Arial", 12), justify='center', bg="#FFFFFF", fg=COLOR_TEXTO_OSCURO)
    dots_entry.pack(side=LEFT, padx=5)
    
    Label(input_frame, text="(mínimo: 3, máximo: 10)", 
          font=("Arial", 9), fg="lightgray", bg=COLOR_AZUL).pack(side=LEFT, padx=5)
    
    # Etiqueta para mostrar información del tablero
    info_label = Label(size_frame, text="", font=("Arial", 10), fg=COLOR_TEXTO, bg=COLOR_AZUL)
    info_label.pack(pady=5)
    
    # Etiqueta para mensajes de error
    error_label = Label(size_frame, text="", font=("Arial", 10), fg=player2_color, bg=COLOR_AZUL)
    error_label.pack(pady=5)

    # Frame para selección de modo de juego
    mode_frame = Frame(setup_window, bg=COLOR_AZUL)
    mode_frame.pack(pady=10)
    Label(mode_frame, text="Elige el oponente (Jugador 2):", font=("Arial", 12, "bold"), fg=COLOR_TEXTO, bg=COLOR_AZUL).pack(pady=5)
    
    Radiobutton(mode_frame, text="MinMax Estándar", variable=game_mode_var, value="minmax",
                font=("Arial", 11), bg=COLOR_AZUL, fg=COLOR_TEXTO, selectcolor=COLOR_AZUL, activebackground=COLOR_AZUL, activeforeground=COLOR_TEXTO).pack(anchor='w')
    Radiobutton(mode_frame, text="MinMax con Aleatoriedad", variable=game_mode_var, value="minmax_random",
                font=("Arial", 11), bg=COLOR_AZUL, fg=COLOR_TEXTO, selectcolor=COLOR_AZUL, activebackground=COLOR_AZUL, activeforeground=COLOR_TEXTO).pack(anchor='w')
    
    def update_info():
        """Actualiza la información del tablero basada en la entrada"""
        try:
            dots = int(dots_var.get())
            if 3 <= dots <= 10:
                boxes = (dots - 1) ** 2
                info_label.config(text=f"Tablero: {dots}x{dots} puntos ({dots-1}x{dots-1} cajas = {boxes} cajas)")
                error_label.config(text="")
                return True
            else:
                info_label.config(text="")
                error_label.config(text="El número debe estar entre 3 y 10")
                return False
        except ValueError:
            info_label.config(text="")
            error_label.config(text="Por favor, introduce un número válido")
            return False
    
    # Actualizar información cuando cambie el valor
    def on_entry_change(*args):
        update_info()
    
    dots_var.trace('w', on_entry_change)
    
    # Actualizar información inicial
    update_info()
    
    # Frame para botones
    button_frame = Frame(setup_window, bg=COLOR_AZUL)
    button_frame.pack(pady=20)
    
    result = {'dots': 3, 'game_mode': 'minmax', 'start': False}
    
    def start_game():
        if update_info():  # Validar antes de iniciar
            result['dots'] = int(dots_var.get())
            result['game_mode'] = game_mode_var.get()
            result['start'] = True
            setup_window.quit()
            setup_window.destroy()
    
    def exit_game():
        result['start'] = False
        setup_window.quit()
        setup_window.destroy()
    
    # Botones
    start_btn = Button(button_frame, text="Iniciar Juego", command=start_game,
                       bg=COLOR_ORO, fg=COLOR_TEXTO_OSCURO, font=("Arial", 12, "bold"),
                       width=12, height=2)
    start_btn.pack(side=LEFT, padx=10)
    
    exit_btn = Button(button_frame, text="Salir", command=exit_game,
                      bg=COLOR_VINO, fg=COLOR_TEXTO, font=("Arial", 12, "bold"),
                      width=12, height=2)
    exit_btn.pack(side=LEFT, padx=10)
    
    # Información adicional
    Label(setup_window, 
          text="Un tablero más grande significa mayor complejidad y tiempo de cálculo",
          font=("Arial", 9), fg="lightgray", bg=COLOR_AZUL).pack(pady=5)
    
    # Permitir iniciar con Enter
    def on_enter(event):
        start_game()
    
    dots_entry.bind('<Return>', on_enter)
    dots_entry.focus()  # Dar foco al campo de entrada
    
    # Manejar el cierre de la ventana
    setup_window.protocol("WM_DELETE_WINDOW", exit_game)
    
    setup_window.mainloop()
    return result

class Dots_and_Boxes():
    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self, number_of_dots=3, game_mode='minmax'):
        global NUMBER_OF_DOTS, dot_width, edge_width, distance_between_dots
        
        # Actualizar variables globales con el tamaño seleccionado
        NUMBER_OF_DOTS = number_of_dots
        dot_width = 0.22*size_of_board/NUMBER_OF_DOTS
        edge_width = 0.08*size_of_board/NUMBER_OF_DOTS
        distance_between_dots = size_of_board / (NUMBER_OF_DOTS)
        
        self.window = Tk()
        self.window.title(f'Dots and Boxes - Tablero {NUMBER_OF_DOTS}x{NUMBER_OF_DOTS} - With MinMax AI')
        self.canvas = Canvas(self.window, width=size_of_board + 300, height=size_of_board, bg=COLOR_AZUL)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.game_mode = game_mode
        
        # MinMax controls
        self.setup_minimax_controls()
        
        self.refresh_board()
        self.play_again()

    def play_again(self):
        """Reinicia el estado del juego manteniendo el mismo tamaño de tablero"""
        self.canvas.delete("all")  # Limpiar todo el canvas
        self.refresh_board()
        self.board_status = np.zeros(shape=(NUMBER_OF_DOTS - 1, NUMBER_OF_DOTS - 1))
        self.row_status = np.zeros(shape=(NUMBER_OF_DOTS, NUMBER_OF_DOTS - 1))
        self.col_status = np.zeros(shape=(NUMBER_OF_DOTS - 1, NUMBER_OF_DOTS))
        
        # Reset scores for new game
        self.player1_score = 0
        self.player2_score = 0
        
        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = self.player1_starts # Jugador 1 empieza si es su turno
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.score_text_handle = []
        
        # Reset minimax controls
        self.current_best_move = None
        self.minimax_value = None
        
        # Recrear los controles de minimax
        self.setup_minimax_controls()
        
        self.display_turn_text()
        self.display_scores()
        
        # Si el Jugador 2 (IA) comienza, ejecutar su movimiento
        if not self.player1_turn:
            self.window.after(500, self.handle_ai_turn)

    def setup_minimax_controls(self):
        """Configura los controles de minimax en la interfaz"""
        # Frame para controles de minimax
        controls_x = size_of_board + 20
        
        # Título
        self.canvas.create_text(controls_x + 75, 50, 
                               text="MINIMAX AI", 
                               font="Arial 16 bold", 
                               fill=COLOR_TEXTO)
        
        # Etiqueta y campo para profundidad
        self.canvas.create_text(controls_x, 90, 
                               text="Profundidad:", 
                               font="Arial 12", 
                               fill=COLOR_TEXTO, 
                               anchor='w')
        
        # Crear entry widget para profundidad
        self.depth_var = StringVar(value="4")
        self.depth_entry = Entry(self.window, textvariable=self.depth_var, width=5, bg="#FFFFFF", fg=COLOR_TEXTO_OSCURO)
        self.canvas.create_window(controls_x + 130, 90, window=self.depth_entry)
        
        # Botón para que el JUGADOR 1 use la IA
        self.minimax_button = Button(self.window, 
                                   text="Ayuda IA (Jugador 1)", 
                                   command=self.execute_minimax_and_move,
                                   bg=COLOR_ORO,
                                   fg=COLOR_TEXTO_OSCURO,
                                   font="Arial 10 bold")

        self.canvas.create_window(controls_x + 75, 130, window=self.minimax_button)

        # Área para mostrar información del movimiento ejecutado
        self.best_move_text = self.canvas.create_text(controls_x + 75, 220,
                                                     text="La IA del Jugador 2 se\nejecutará automáticamente.\n\nUsa 'Ayuda IA' si\nnecesitas una pista.",
                                                     font="Arial 11",
                                                     fill=COLOR_TEXTO,
                                                     width=180,
                                                     justify='center')
        
        # Variables para almacenar información del movimiento
        self.current_best_move = None
        self.minimax_value = None

    def mainloop(self):
        self.window.mainloop()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def handle_ai_turn(self):
        """Gestiona el turno de la IA (Jugador 2)"""
        if self.is_gameover() or self.player1_turn:
            return

        randomize = self.game_mode == 'minmax_random'
        
        # Mostrar que la IA está pensando
        self.canvas.itemconfig(self.best_move_text, text=f"Jugador 2 (IA) está\npensando...")
        self.window.update()

        # Ejecutar el movimiento de la IA
        self.execute_minimax_and_move(is_ai_turn=True, randomize=randomize)

        # Si la IA anotó y el juego no ha terminado, debe jugar de nuevo
        if self.is_gameover():
            return
        if not self.player1_turn:
            self.window.after(500, self.handle_ai_turn) # Llamada recursiva para el siguiente movimiento de la IA
        else:
            # El turno vuelve al jugador 1
            self.display_turn_text()

    def is_grid_occupied(self, logical_position, type):
        # Verificar que la posición lógica sea válida
        if not logical_position:
            return True  # Tratar posiciones inválidas como ocupadas
        
        r = logical_position[0]
        c = logical_position[1]
        
        # Verificar que las coordenadas estén dentro de los límites
        if r < 0 or c < 0:
            return True

        if type == 'row':
            # Verificar límites para líneas horizontales
            if c < (NUMBER_OF_DOTS-1) and r < NUMBER_OF_DOTS:
                if self.row_status[r][c] == 0:
                    return False
        elif type == 'col':
            # Verificar límites para líneas verticales
            if c < NUMBER_OF_DOTS and r < (NUMBER_OF_DOTS-1):
                if self.col_status[r][c] == 0:
                    return False
        return True

    def convert_grid_to_logical_position(self, grid_position):
        # Ajustar por márgenes para que el clic mapee correctamente al grid
        grid_position = np.array(grid_position) - np.array([BOARD_OFFSET_X, BOARD_OFFSET_Y])
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)

        type = False
        logical_position = []
        
        # Verificar que la posición esté dentro de los límites del tablero
        if position[0] < 0 or position[1] < 0:
            return [], False
            
        # Verificar si es una línea horizontal (row)
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[1]//2))
            c = int((position[0]-1)//2)

            # Validar que esté dentro de los límites para líneas horizontales
            if 0 <= r < NUMBER_OF_DOTS and 0 <= c < (NUMBER_OF_DOTS-1):
                logical_position = [r, c]
                type = 'row'
                
        # Verificar si es una línea vertical (col)
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            r = int((position[1]-1) // 2)
            c = int((position[0] // 2))
            # Validar que esté dentro de los límites para líneas verticales
            if 0 <= r < (NUMBER_OF_DOTS-1) and 0 <= c < NUMBER_OF_DOTS:
                logical_position = [r, c]
                type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes_completed = 0

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                if self.player1_turn:
                    color = player1_color_light
                else:
                    color = player2_color_light
                self.shade_box(box, color)
                boxes_completed += 1

        return boxes_completed

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]

        if c < (NUMBER_OF_DOTS-1) and r < (NUMBER_OF_DOTS-1):
            self.board_status[r][c] += 1

        if type == 'row':
            self.row_status[r][c] = 1
            if r >= 1:
                self.board_status[r-1][c] += 1
        elif type == 'col':
            self.col_status[r][c] = 1
            if c >= 1:
                self.board_status[r][c-1] += 1

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = BOARD_OFFSET_X + distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = BOARD_OFFSET_Y + distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = BOARD_OFFSET_Y + distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = BOARD_OFFSET_X + distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width, capstyle='round', joinstyle='round')

    def display_gameover(self):
        # Determinar resultado en español y color asociado
        if self.player1_score > self.player2_score:
            titulo = 'Ganador: Jugador 1'
            color = player1_color
        elif self.player2_score > self.player1_score:
            titulo = 'Ganador: Jugador 2'
            color = player2_color
        else:
            titulo = 'Empate'
            color = 'gray'

        # Limpiar pantalla
        # Eliminar el texto de turno si existe
        try:
            self.canvas.delete(self.turntext_handle)
        except Exception:
            pass
        self.canvas.delete("all")

        # Panel centrado en el área del tablero (lado izquierdo)
        panel_margin = 28
        left = panel_margin
        top = panel_margin
        right = size_of_board - panel_margin
        bottom = size_of_board - panel_margin
        self.canvas.create_rectangle(left, top, right, bottom, fill=COLOR_ORO, outline=COLOR_TEXTO, width=2)

        center_x = size_of_board / 2

        # Título del resultado
        self.canvas.create_text(
            center_x,
            top + 70,
            font=("Arial", 28, "bold"),
            fill=color,
            text=titulo,
            width=int(right - left - 40),
            anchor='n'
        )

        # Encabezado de puntajes
        self.canvas.create_text(
            center_x,
            top + 130,
            font=("Arial", 18, "bold"),
            fill=COLOR_TEXTO,
            text='Puntajes',
            anchor='n'
        )

        # Detalle de puntajes
        score_text = f"Jugador 1: {self.player1_score}\nJugador 2: {self.player2_score}"
        self.canvas.create_text(
            center_x,
            top + 170,
            font=("Arial", 16, "bold"),
            fill=COLOR_TEXTO,
            text=score_text,
            justify='center',
            anchor='n'
        )

        # Indicación para continuar
        self.reset_board = True
        self.canvas.create_text(
            center_x,
            bottom - 60,
            font=("Arial", 14, "bold"),
            fill=COLOR_TEXTO,
            text='Haz clic para jugar de nuevo',
            anchor='n'
        )

    def refresh_board(self):
        # Área útil del tablero con márgenes
        left = BOARD_OFFSET_X + distance_between_dots/2 - edge_width
        top = BOARD_OFFSET_Y + distance_between_dots/2 - edge_width
        right = BOARD_OFFSET_X + size_of_board - distance_between_dots/2 + edge_width
        bottom = BOARD_OFFSET_Y + size_of_board - distance_between_dots/2 + edge_width

        # Marco del tablero
        self.canvas.create_rectangle(left, top, right, bottom, outline=COLOR_AZUL, width=2)

        # Líneas guía del grid
        for i in range(NUMBER_OF_DOTS):
            x = BOARD_OFFSET_X + i*distance_between_dots + distance_between_dots/2
            y = BOARD_OFFSET_Y + i*distance_between_dots + distance_between_dots/2
            # Vertical
            self.canvas.create_line(x, BOARD_OFFSET_Y + distance_between_dots/2, x,
                                    BOARD_OFFSET_Y + size_of_board - distance_between_dots/2,
                                    fill=COLOR_GRID, dash=(3, 3))
            # Horizontal
            self.canvas.create_line(BOARD_OFFSET_X + distance_between_dots/2, y,
                                    BOARD_OFFSET_X + size_of_board - distance_between_dots/2, y,
                                    fill=COLOR_GRID, dash=(3, 3))

        # Puntos (nodos) del tablero
        dot_diameter = max(10, int(0.18 * distance_between_dots))
        for i in range(NUMBER_OF_DOTS):
            for j in range(NUMBER_OF_DOTS):
                cx = BOARD_OFFSET_X + i*distance_between_dots+distance_between_dots/2
                cy = BOARD_OFFSET_Y + j*distance_between_dots+distance_between_dots/2
                self.canvas.create_oval(cx-dot_diameter/2, cy-dot_diameter/2, cx+dot_diameter/2,
                                        cy+dot_diameter/2, fill=dot_color,
                                        outline=dot_color)

    def display_turn_text(self):
        text = 'Siguiente turno: '
        if self.player1_turn:
            text += 'Jugador 1'
            color = player1_color
        else:
            text += 'Jugador 2 (IA)'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board + 100,
                                                       size_of_board-distance_between_dots/4,
                                                       font="cmr 15 bold", text=text, fill=color, anchor='center')

    def display_scores(self):
        score_text = f"Puntaje: \n"
        score_text += f"Jugador 1: {self.player1_score}\n"
        score_text += f"Jugador 2: {self.player2_score}\n"

        # Clear previous score display
        self.canvas.delete(self.score_text_handle)
        
        # Display scores on the right side of the board
        self.score_text_handle = self.canvas.create_text(size_of_board + 100, 
                                                        size_of_board // 2 + 150,
                                                        font="cmr 16 bold", 
                                                        text=score_text, 
                                                        fill=COLOR_TEXTO,
                                                        justify='center',
                                                        anchor='center')

    def shade_box(self, box, color):
        start_x = BOARD_OFFSET_X + distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = BOARD_OFFSET_Y + distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def is_gameover(self):
        # Game is over when all possible boxes are completed
        return (self.player1_score + self.player2_score) == (NUMBER_OF_DOTS - 1) ** 2

    def execute_minimax_and_move(self, randomize=False, is_ai_turn=False):
        """Ejecuta el algoritmo minimax, encuentra el mejor movimiento y lo ejecuta automáticamente"""
        try:
            depth = int(self.depth_var.get())
            if depth < 1:
                depth = 1
            elif depth > 10:
                depth = 10
        except ValueError:
            depth = 4
            self.depth_var.set("4")
        
        # Actualizar NUMBER_OF_DOTS en el módulo minmax
        minmax.NUMBER_OF_DOTS = NUMBER_OF_DOTS
        
        # Crear nodo actual
        current_node = Node(
            np.copy(self.board_status),
            np.copy(self.row_status), 
            np.copy(self.col_status),
            1 if self.player1_turn else 2,
            len(self.already_marked_boxes),
            self.player1_score,
            self.player2_score
        )
        
        # Mostrar que se está calculando
        self.canvas.itemconfig(self.best_move_text, text="Calculando...\nEspera un momento")
        self.window.update()  # Actualizar la interfaz inmediatamente
        
        # Ejecutar minimax
        self.minimax_value, self.current_best_move = minimax_algorithm(current_node, depth, self.player1_turn, randomize=randomize)
        
        # Verificar si hay movimiento disponible
        if self.current_best_move and not self.reset_board:
            move_type, position = self.current_best_move
            
            # Mostrar el movimiento que se va a ejecutar
            move_text = f"Ejecutando:\n{move_type.upper()} en {position}\nValor: {self.minimax_value:.2f}"
            self.canvas.itemconfig(self.best_move_text, text=move_text)
            self.window.update()  # Actualizar la interfaz
            
            # Verificar que el movimiento sigue siendo válido
            if not self.is_grid_occupied(position, move_type):
                # Ejecutar el movimiento
                self.update_board(move_type, position)
                self.make_edge(move_type, position)
                box_completed = self.mark_box()
                self.refresh_board()
                
                # Solo switch turns if no box was completed
                if not box_completed:
                    self.player1_turn = not self.player1_turn                    
                else:
                    if self.player1_turn:
                        self.player1_score += box_completed
                    else:
                        self.player2_score += box_completed

                self.display_scores()
                
                # Mostrar resultado final
                final_text = f"Movimiento ejecutado:\n{move_type.upper()} en {position}\nValor: {self.minimax_value:.2f}"
                if is_ai_turn:
                    final_text = f"Jugador 2 (IA) movió:\n{move_type.upper()} en {position}"
                self.canvas.itemconfig(self.best_move_text, text=final_text)
                
                # Limpiar variables
                self.current_best_move = None
                self.minimax_value = None
                
                if self.is_gameover():
                    self.display_gameover()
                else:
                    self.display_turn_text()
            else:
                # El movimiento ya no es válido
                self.canvas.itemconfig(self.best_move_text, text="Movimiento inválido\nEl tablero cambió")
        else:
            # No hay movimientos disponibles
            self.canvas.itemconfig(self.best_move_text, text="No hay movimientos\ndisponibles")

    def click(self, event):
        if self.reset_board:
            self.window.destroy()
            restart_game()
            return

        if not self.player1_turn:
            return # Ignorar clics si no es el turno del jugador 1

        grid_position = [event.x, event.y]
        logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
        
        if valid_input and logical_positon and len(logical_positon) == 2:
            if not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                box_completed = self.mark_box()
                self.refresh_board()
                
                if not box_completed:
                    self.player1_turn = not self.player1_turn
                else:
                    if self.player1_turn:
                        self.player1_score += box_completed
                    else:
                        self.player2_score += box_completed

                self.display_scores()
                
                if self.is_gameover():
                    self.display_gameover()
                else:
                    self.display_turn_text()
                    # Si es el turno de la IA, llamarla
                    if not self.player1_turn:
                        self.window.after(500, self.handle_ai_turn)


def restart_game():
    """Función para reiniciar el juego volviendo a la configuración"""
    try:
        setup_result = show_game_setup()
        
        if setup_result and setup_result['start']:
            game_instance = Dots_and_Boxes(setup_result['dots'], setup_result['game_mode'])
            game_instance.mainloop()
        else:
            print("Juego cancelado por el usuario")
    except Exception as e:
        print(f"Error al reiniciar el juego: {e}")

def main():
    """Función principal del juego"""
    try:
        setup_result = show_game_setup()
        
        if setup_result and setup_result['start']:
            game_instance = Dots_and_Boxes(setup_result['dots'], setup_result['game_mode'])
            game_instance.mainloop()
    
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
        # En caso de error, iniciar con valores por defecto
        game_instance = Dots_and_Boxes(3)
        game_instance.mainloop()

# Mostrar ventana de configuración y iniciar el juego
if __name__ == "__main__":
    main()
