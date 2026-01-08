# Lógica del juego Tic Tac Toe Rolling
# Cada jugador solo puede tener 3 fichas - la más antigua desaparece
import random

class TicTacToe:
    def __init__(self):
        self.tablero = [' ' for _ in range(9)]
        self.ganador_actual = None
        self.jugador_actual = 'X'
        self.numero_maximo_de_mov = 3
        
        # Historial de movimientos por jugador
        self.x_moves = []
        self.o_moves = []
        
        # Combinaciones ganadoras
        self.win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
    
    def casilla_disponible(self, casilla):
        """Verifica si una casilla está disponible"""
        return self.tablero[casilla] == ' '
    
    def obtener_movimientos_actuales(self):
        """Retorna la lista de movimientos del jugador actual"""
        return self.x_moves if self.jugador_actual == 'X' else self.o_moves
    
    def hacer_movimiento(self, casilla):
        """
        Realiza un movimiento en la casilla indicada.
        Retorna una tupla (exito, casilla_eliminada) donde:
        - exito: True si el movimiento fue válido
        - casilla_eliminada: índice de la casilla eliminada o None
        """
        if not self.casilla_disponible(casilla):
            return False, None
        
        movimientos = self.obtener_movimientos_actuales()
        casilla_eliminada = None
        
        # Si ya tiene 3 fichas, eliminar la más antigua
        if len(movimientos) >= self.numero_maximo_de_mov:
            casilla_eliminada = movimientos.pop(0)
            self.tablero[casilla_eliminada] = ' '
            self.ganador_actual = None
        
        # Hacer el movimiento
        self.tablero[casilla] = self.jugador_actual
        movimientos.append(casilla)
        
        return True, casilla_eliminada
    
    def verificar_ganador(self, jugador):
        """
        Verifica si el jugador indicado ha ganado.
        Retorna la combinación ganadora o None.
        """
        for combo in self.win_combinations:
            if all(self.tablero[i] == jugador for i in combo):
                self.ganador_actual = jugador
                return combo
        return None
    
    def cambiar_turno(self):
        """Cambia el turno al siguiente jugador"""
        self.jugador_actual = 'O' if self.jugador_actual == 'X' else 'X'
    
    def obtener_fichas_a_desvanecer(self):
        """
        Retorna las posiciones de las fichas que están por desaparecer.
        Una ficha está por desaparecer si el jugador ya tiene el máximo de fichas.
        """
        fichas_desvanecidas = []
        
        if len(self.x_moves) >= self.numero_maximo_de_mov:
            fichas_desvanecidas.append(('X', self.x_moves[0]))
        
        if len(self.o_moves) >= self.numero_maximo_de_mov:
            fichas_desvanecidas.append(('O', self.o_moves[0]))
        
        return fichas_desvanecidas
    
    def reiniciar(self):
        """Reinicia el juego a su estado inicial"""
        self.tablero = [' ' for _ in range(9)]
        self.ganador_actual = None
        self.jugador_actual = 'X'
        self.x_moves = []
        self.o_moves = []
    
    def obtener_conteo_fichas(self):
        """Retorna el conteo de fichas de cada jugador"""
        return len(self.x_moves), len(self.o_moves)
    
    def obtener_casillas_disponibles(self):
        """Retorna lista de casillas vacías"""
        return [i for i, c in enumerate(self.tablero) if c == ' ']
    
    def simular_movimiento(self, casilla, jugador):
        """Simula un movimiento sin modificar el estado real. Retorna copia del estado."""
        moves = self.x_moves[:] if jugador == 'X' else self.o_moves[:]
        tablero = self.tablero[:]
        
        # Simular eliminación de ficha antigua
        if len(moves) >= self.numero_maximo_de_mov:
            tablero[moves[0]] = ' '
            moves = moves[1:]
        
        tablero[casilla] = jugador
        moves.append(casilla)
        return tablero, moves


class IA:
    """Inteligencia Artificial para el juego Tic Tac Toe Rolling"""
    
    def __init__(self, juego, simbolo='O', dificultad='medio'):
        self.juego = juego
        self.simbolo = simbolo
        self.oponente = 'X' if simbolo == 'O' else 'O'
        self.dificultad = dificultad
    
    def obtener_movimiento(self):
        """Retorna la mejor casilla para jugar según la dificultad"""
        disponibles = self.juego.obtener_casillas_disponibles()
        
        if not disponibles:
            return None
        
        if self.dificultad == 'facil':
            return self._movimiento_aleatorio(disponibles)
        elif self.dificultad == 'medio':
            return self._movimiento_medio(disponibles)
        else:  # dificil
            return self._movimiento_dificil(disponibles)
    
    def _movimiento_aleatorio(self, disponibles):
        """Elige una casilla al azar"""
        return random.choice(disponibles)
    
    def _movimiento_medio(self, disponibles):
        """Intenta ganar o bloquear, sino elige estratégicamente"""
        # 1. Intentar ganar
        for casilla in disponibles:
            tablero, _ = self.juego.simular_movimiento(casilla, self.simbolo)
            if self._hay_ganador(tablero, self.simbolo):
                return casilla
        
        # 2. Bloquear al oponente
        for casilla in disponibles:
            tablero, _ = self.juego.simular_movimiento(casilla, self.oponente)
            if self._hay_ganador(tablero, self.oponente):
                return casilla
        
        # 3. Preferir centro, luego esquinas
        preferencias = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        for casilla in preferencias:
            if casilla in disponibles:
                return casilla
        
        return disponibles[0]
    
    def _movimiento_dificil(self, disponibles):
        """Usa minimax simplificado para el modo rolling"""
        mejor_puntaje = -float('inf')
        mejor_casilla = disponibles[0]
        
        for casilla in disponibles:
            puntaje = self._minimax(casilla, self.simbolo, 0, False)
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_casilla = casilla
        
        return mejor_casilla
    
    def _minimax(self, casilla, jugador, profundidad, es_maximizando):
        """Minimax adaptado para rolling (profundidad limitada)"""
        tablero, _ = self.juego.simular_movimiento(casilla, jugador)
        
        # Verificar estados terminales
        if self._hay_ganador(tablero, self.simbolo):
            return 10 - profundidad
        if self._hay_ganador(tablero, self.oponente):
            return profundidad - 10
        
        # Limitar profundidad para el modo rolling
        if profundidad >= 3:
            return self._evaluar_tablero(tablero)
        
        disponibles = [i for i, c in enumerate(tablero) if c == ' ']
        if not disponibles:
            return 0
        
        if es_maximizando:
            mejor = -float('inf')
            for c in disponibles:
                puntaje = self._minimax(c, self.simbolo, profundidad + 1, False)
                mejor = max(mejor, puntaje)
            return mejor
        else:
            mejor = float('inf')
            for c in disponibles:
                puntaje = self._minimax(c, self.oponente, profundidad + 1, True)
                mejor = min(mejor, puntaje)
            return mejor
    
    def _hay_ganador(self, tablero, jugador):
        """Verifica si hay ganador en un tablero dado"""
        for combo in self.juego.win_combinations:
            if all(tablero[i] == jugador for i in combo):
                return True
        return False
    
    def _evaluar_tablero(self, tablero):
        """Evalúa posición del tablero (heurística simple)"""
        puntaje = 0
        for combo in self.juego.win_combinations:
            mis_fichas = sum(1 for i in combo if tablero[i] == self.simbolo)
            fichas_oponente = sum(1 for i in combo if tablero[i] == self.oponente)
            
            if fichas_oponente == 0:
                puntaje += mis_fichas
            if mis_fichas == 0:
                puntaje -= fichas_oponente
        
        # Bonus por centro
        if tablero[4] == self.simbolo:
            puntaje += 2
        
        return puntaje
