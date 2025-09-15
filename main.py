# Author: aqeelanwar
# Created: 13 March,2020, 9:19 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import numpy as np
import minmax
from minmax import Node, minmax as minimax_algorithm, get_possible_moves

size_of_board = 600
NUMBER_OF_DOTS = 3  # Se actualizará con la selección del usuario
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25*size_of_board/NUMBER_OF_DOTS
edge_width = 0.1*size_of_board/NUMBER_OF_DOTS
distance_between_dots = size_of_board / (NUMBER_OF_DOTS)

def show_game_setup():
    """Muestra ventana de configuración inicial del juego"""
    setup_window = Tk()
    setup_window.title('Configuración del Juego - Dots and Boxes')
    setup_window.geometry('450x350')
    setup_window.resizable(False, False)
    
    # Centrar la ventana
    setup_window.eval('tk::PlaceWindow . center')
    
    # Variable para almacenar el número de puntos
    dots_var = StringVar(value="3")
    
    # Título
    Label(setup_window, text="Dots and Boxes", 
          font=("Arial", 20, "bold"), fg="#2E86C1").pack(pady=20)
    
    # Subtítulo
    Label(setup_window, text="Configuración inicial del tablero", 
          font=("Arial", 12)).pack(pady=10)
    
    # Frame para entrada de tamaño
    size_frame = Frame(setup_window)
    size_frame.pack(pady=20)
    
    Label(size_frame, text="Introduce el número de puntos por lado:", 
          font=("Arial", 12, "bold")).pack(pady=10)
    
    # Frame para el campo de entrada y validación
    input_frame = Frame(size_frame)
    input_frame.pack(pady=10)
    
    Label(input_frame, text="Puntos:", font=("Arial", 11)).pack(side=LEFT, padx=5)
    
    # Campo de entrada para el número de puntos
    dots_entry = Entry(input_frame, textvariable=dots_var, width=10, 
                       font=("Arial", 12), justify='center')
    dots_entry.pack(side=LEFT, padx=5)
    
    Label(input_frame, text="(mínimo: 3, máximo: 10)", 
          font=("Arial", 9), fg="gray").pack(side=LEFT, padx=5)
    
    # Etiqueta para mostrar información del tablero
    info_label = Label(size_frame, text="", font=("Arial", 10), fg="#2E86C1")
    info_label.pack(pady=10)
    
    # Etiqueta para mensajes de error
    error_label = Label(size_frame, text="", font=("Arial", 10), fg="#E74C3C")
    error_label.pack(pady=5)
    
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
    button_frame = Frame(setup_window)
    button_frame.pack(pady=30)
    
    result = {'dots': 3, 'start': False}
    
    def start_game():
        if update_info():  # Validar antes de iniciar
            result['dots'] = int(dots_var.get())
            result['start'] = True
            setup_window.quit()  # Cambiar destroy() por quit()
            setup_window.destroy()
    
    def exit_game():
        result['start'] = False
        setup_window.quit()  # Cambiar destroy() por quit()
        setup_window.destroy()
    
    # Botones
    start_btn = Button(button_frame, text="Iniciar Juego", command=start_game,
                       bg="#27AE60", fg="white", font=("Arial", 12, "bold"),
                       width=12, height=2)
    start_btn.pack(side=LEFT, padx=10)
    
    exit_btn = Button(button_frame, text="Salir", command=exit_game,
                      bg="#E74C3C", fg="white", font=("Arial", 12, "bold"),
                      width=12, height=2)
    exit_btn.pack(side=LEFT, padx=10)
    
    # Información adicional
    Label(setup_window, 
          text="Un tablero más grande significa mayor complejidad y tiempo de cálculo",
          font=("Arial", 9), fg="gray").pack(pady=10)
    
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
    def __init__(self, number_of_dots=3):
        global NUMBER_OF_DOTS, dot_width, edge_width, distance_between_dots
        
        # Actualizar variables globales con el tamaño seleccionado
        NUMBER_OF_DOTS = number_of_dots
        dot_width = 0.25*size_of_board/NUMBER_OF_DOTS
        edge_width = 0.1*size_of_board/NUMBER_OF_DOTS
        distance_between_dots = size_of_board / (NUMBER_OF_DOTS)
        
        self.window = Tk()
        self.window.title(f'Dots and Boxes - Tablero {NUMBER_OF_DOTS}x{NUMBER_OF_DOTS} - With MinMax AI')
        self.canvas = Canvas(self.window, width=size_of_board + 300, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        
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
        self.player1_turn = not self.player1_starts
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

    def setup_minimax_controls(self):
        """Configura los controles de minimax en la interfaz"""
        # Frame para controles de minimax
        controls_x = size_of_board + 20
        
        # Título
        self.canvas.create_text(controls_x + 100, 50, 
                               text="MINIMAX AI", 
                               font="Arial 16 bold", 
                               fill="#2E86C1")
        
        # Etiqueta y campo para profundidad
        self.canvas.create_text(controls_x + 50, 90, 
                               text="Profundidad:", 
                               font="Arial 12", 
                               fill="black", 
                               anchor='w')
        
        # Crear entry widget para profundidad
        self.depth_var = StringVar(value="4")
        self.depth_entry = Entry(self.window, textvariable=self.depth_var, width=5)
        self.canvas.create_window(controls_x + 130, 90, window=self.depth_entry)
        
        # Botón para ejecutar minimax (ahora ejecuta directamente)
        self.minimax_button = Button(self.window, 
                                   text="Ejecutar MinMax", 
                                   command=self.execute_minimax_and_move,
                                   bg="#27AE60",
                                   fg="white",
                                   font="Arial 10 bold")
        self.canvas.create_window(controls_x + 100, 130, window=self.minimax_button)
        
        # Área para mostrar información del movimiento ejecutado
        self.best_move_text = self.canvas.create_text(controls_x + 100, 200,
                                                     text="Presiona 'Ejecutar MinMax'\npara calcular y ejecutar\nel mejor movimiento",
                                                     font="Arial 11",
                                                     fill="#E74C3C",
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
        grid_position = np.array(grid_position)
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
                print("row", r, c)
                logical_position = [r, c]
                type = 'row'
                
        # Verificar si es una línea vertical (col)
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            r = int((position[1]-1) // 2)
            c = int((position[0] // 2))
            # Validar que esté dentro de los límites para líneas verticales
            if 0 <= r < (NUMBER_OF_DOTS-1) and 0 <= c < NUMBER_OF_DOTS:
                print("har", r, c)
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

        print(logical_position)


        if c < (NUMBER_OF_DOTS-1) and r < (NUMBER_OF_DOTS-1):
            self.board_status[r][c] += 1

        if type == 'row':
            self.row_status[r][c] = 1
            if r >= 1:
                self.board_status[r-1][c] += 1
            print('\nrow after:\n', self.row_status)
        elif type == 'col':
            self.col_status[r][c] = 1
            if c >= 1:
                self.board_status[r][c-1] += 1
            print('\ncol after:\n', self.col_status)

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)

    def display_gameover(self):
        if self.player1_score > self.player2_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = player1_color
        elif self.player2_score > self.player1_score:
            text = 'Winner: Player 2 '
            color = player2_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(self.player1_score) + '\n'
        score_text += 'Player 2 : ' + str(self.player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(NUMBER_OF_DOTS):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(NUMBER_OF_DOTS):
            for j in range(NUMBER_OF_DOTS):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                        end_x+dot_width/2, fill=dot_color,
                                        outline=dot_color)

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)

    def display_scores(self):
        score_text = f"SCORES\n"
        score_text += f"Player 1: {self.player1_score}\n"
        score_text += f"Player 2: {self.player2_score}\n"

        # Clear previous score display
        self.canvas.delete(self.score_text_handle)
        
        # Display scores on the right side of the board
        self.score_text_handle = self.canvas.create_text(size_of_board + 100, 
                                                        size_of_board // 2 + 100,
                                                        font="cmr 16 bold", 
                                                        text=score_text, 
                                                        fill=Green_color,
                                                        anchor='w')

    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def is_gameover(self):
        # Game is over when all possible boxes are completed
        return (self.player1_score + self.player2_score) == (NUMBER_OF_DOTS - 1) ** 2

    def execute_minimax_and_move(self):
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
        print(f"Current Node:\n{current_node}")
        
        # Mostrar que se está calculando
        self.canvas.itemconfig(self.best_move_text, text="Calculando...\nEspera un momento")
        self.window.update()  # Actualizar la interfaz inmediatamente
        
        # Ejecutar minimax
        self.minimax_value, self.current_best_move = minimax_algorithm(current_node, depth, self.player1_turn)
        
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

    def execute_minimax(self):
        """Función legacy - redirige a la nueva función combinada"""
        self.execute_minimax_and_move()
    
    def execute_best_move(self):
        """Función legacy - ya no se usa pero se mantiene para compatibilidad"""
        pass

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            
            # Validar que el clic sea en una posición válida y que sea una línea válida
            if valid_input and logical_positon and len(logical_positon) == 2:
                # Solo procesar si la posición es válida y no está ocupada
                if not self.is_grid_occupied(logical_positon, valid_input):
                    self.update_board(valid_input, logical_positon)
                    self.make_edge(valid_input, logical_positon)
                    box_completed = self.mark_box()  # Check if any boxes were completed
                    self.refresh_board()
                    
                    # Only switch turns if no box was completed
                    if not box_completed:
                        self.player1_turn = not self.player1_turn                    
                    else:
                        if self.player1_turn:
                            self.player1_score += box_completed
                        else:
                            self.player2_score += box_completed

                    self.display_scores()  # Update scores after each move
                    if self.is_gameover():
                        # self.canvas.delete("all")
                        self.display_gameover()
                    else:
                        self.display_turn_text()
                # Si el clic no es válido, simplemente no hacer nada (ignorar el clic)
        else:
            # En lugar de reiniciar en la misma ventana, cerrar y volver a configuración
            self.window.destroy()
            restart_game()


def restart_game():
    """Función para reiniciar el juego volviendo a la configuración"""
    try:
        setup_result = show_game_setup()
        
        if setup_result and setup_result['start']:
            print(f"Reiniciando juego con tablero de {setup_result['dots']} puntos")
            game_instance = Dots_and_Boxes(setup_result['dots'])
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
            game_instance = Dots_and_Boxes(setup_result['dots'])
            game_instance.mainloop()
    
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
        # En caso de error, iniciar con valores por defecto
        game_instance = Dots_and_Boxes(3)
        game_instance.mainloop()

# Mostrar ventana de configuración y iniciar el juego
if __name__ == "__main__":
    main()
