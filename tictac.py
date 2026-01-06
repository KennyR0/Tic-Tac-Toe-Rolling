# Interfaz gráfica para Tic Tac Toe Rolling
# Cada jugador solo puede tener 3 fichas - la más antigua desaparece
import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.tablero = [' ' for _ in range(9)]
        self.ganador = None

class Interfaz:
    def __init__(self, window):
        self.window = window
        self.window.title("Tres en Raya Infinito")
        self.window.resizable(True, True)
        
        # Inicializar juego
        self.juego = TicTacToe()
        self.jugador_actual = 'X'
        self.numero_maximo_de_mov = 3  # Máximo de fichas por jugador
        
        # Historial de movimientos por jugador
        self.x_moves = []  # Lista de posiciones de X (en orden)
        self.o_moves = []  # Lista de posiciones de O (en orden)
        
        # Colores
        self.bg_color = "#1a1a2e"
        self.btn_color = "#16213e"
        self.x_color = "#e94560"
        self.o_color = "#4fc3f7"
        self.text_color = "#eaeaea"
        self.fade_color = "#555555"  # Color para fichas que van a desaparecer
        
        self.window.configure(bg=self.bg_color)
        
        # Título
        self.label = tk.Label(
            window, 
            text="Turno de X", 
            font=('Arial', 18, 'bold'),
            bg=self.bg_color,
            fg=self.x_color
        )
        self.label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Info del modo rolling
        self.info_label = tk.Label(
            window, 
            text="Máximo 3 fichas por jugador", 
            font=('Arial', 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.info_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))
        
        # Crear botones del tablero
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                window,
                text="",
                font=('Arial', 32, 'bold'),
                width=4,
                height=2,
                bg=self.btn_color,
                fg=self.text_color,
                activebackground="#2a2a4e",
                command=lambda idx=i: self.hacer_mov(idx)
            )
            btn.grid(row=(i // 3) + 2, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)
        
        # Contador de fichas
        self.counter_label = tk.Label(
            window, 
            text="X: 0/3  |  O: 0/3", 
            font=('Arial', 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.counter_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Botón de reinicio
        self.reset_btn = tk.Button(
            window,
            text="Nuevo Juego",
            font=('Arial', 12),
            bg="#4a4a6a",
            fg=self.text_color,
            activebackground="#5a5a7a",
            command=self.reiniciar_juego
        )
        self.reset_btn.grid(row=6, column=0, columnspan=3, pady=10)
    
    def hacer_mov(self, casilla):
        # Verificar si la casilla está disponible
        if self.juego.tablero[casilla] != ' ':
            return
        
        movimiento_actual = self.x_moves if self.jugador_actual == 'X' else self.o_moves
        color_actual = self.x_color if self.jugador_actual == 'X' else self.o_color
        
        # Si ya tiene 3 fichas, eliminar la más antigua
        if len(movimiento_actual) >= self.numero_maximo_de_mov:
            ultima_posicion = movimiento_actual.pop(0)
            self.juego.tablero[ultima_posicion] = ' '
            self.buttons[ultima_posicion].config(text="", fg=self.text_color)
            self.juego.ganador = None  # Reset winner check
        
        # Hacer el movimiento
        self.juego.tablero[casilla] = self.jugador_actual
        movimiento_actual.append(casilla)
        self.buttons[casilla].config(text=self.jugador_actual, fg=color_actual)
        
        # Marcar la ficha más antigua con color más tenue
        self.actualizar_color_ficha()
        
        # Verificar ganador
        if self.ganador(self.jugador_actual):
            self.label.config(text=f"¡{self.jugador_actual} gana! 🎉", fg=color_actual)
            self.desabilitar_botones()
            messagebox.showinfo("Fin del juego", f"¡Jugador {self.jugador_actual} gana!")
            return
        
        # Cambiar turno
        self.jugador_actual = 'O' if self.jugador_actual == 'X' else 'X'
        next_color = self.x_color if self.jugador_actual == 'X' else self.o_color
        self.label.config(text=f"Turno de {self.jugador_actual}", fg=next_color)
        
        # Actualizar contador
        self.counter_label.config(text=f"X: {len(self.x_moves)}/3  |  O: {len(self.o_moves)}/3")
    
    def actualizar_color_ficha(self):
        # Actualizar colores - la ficha más antigua se muestra más tenue
        for moves, color in [(self.x_moves, self.x_color), (self.o_moves, self.o_color)]:
            for i, pos in enumerate(moves):
                if len(moves) >= self.numero_maximo_de_mov and i == 0:
                    # La ficha más antigua parpadea/se ve diferente
                    self.buttons[pos].config(fg=self.fade_color)
                else:
                    self.buttons[pos].config(fg=color)
    
    def ganador(self, letter):
        # Verificar todas las combinaciones ganadoras
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        for combo in win_combinations:
            if all(self.juego.tablero[i] == letter for i in combo):
                # Resaltar las fichas ganadoras
                for i in combo:
                    self.buttons[i].config(bg="#2e7d32")
                return True
        return False
    
    def desabilitar_botones(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
    
    def reiniciar_juego(self):
        self.juego = TicTacToe()
        self.jugador_actual = 'X'
        self.x_moves = []
        self.o_moves = []
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, fg=self.text_color, bg=self.btn_color)
        self.label.config(text="Turno de X", fg=self.x_color)
        self.counter_label.config(text="X: 0/3  |  O: 0/3")


if __name__ == '__main__':
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()