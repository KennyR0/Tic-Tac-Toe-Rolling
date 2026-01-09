# Interfaz gráfica para Tic Tac Toe Rolling
import tkinter as tk
from tkinter import messagebox
from backend import TicTacToe, IA

# Colores compartidos
COLORES = {
    'bg': "#1a1a2e", 'btn': "#16213e", 'x': "#e94560",
    'o': "#4fc3f7", 'texto': "#eaeaea", 'acento': "#4a4a6a",
    'fade': "#555555", 'win': "#2e7d32"
}

class MenuPrincipal:
    def __init__(self, window):
        self.window = window
        self.window.title(" Menú Principal ")
        self.window.resizable(True, True)
        self.window.configure(bg=COLORES['bg'])
        
        self.modo_seleccionado = None
        self.pantalla_actual = 'principal'  # 'principal' o 'nombres'
        self.en_transicion = False  # Bandera para evitar problemas durante transiciones
        self.base_size = (400, 500)
        self.last_size = (0, 0)

        self.menu_frame = tk.Frame(window, bg=COLORES['bg'])
        self.menu_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.crear_pantalla_principal()
        self.window.bind('<Configure>', self.on_resize)

    def _calcular_escala(self):
        """Calcula factor de escala basado en tamaño de ventana"""
        w = max(self.window.winfo_width(), self.base_size[0])
        h = max(self.window.winfo_height(), self.base_size[1])
        raw = min(w / self.base_size[0], h / self.base_size[1])
        return min(1 + (raw - 1) * 0.4 if raw > 1 else raw, 2)

    def _crear_label(self, texto, size, bold=False, color='texto'):
        """Crea y empaqueta un label"""
        font = ('Arial', size, 'bold') if bold else ('Arial', size)
        lbl = tk.Label(self.menu_frame, text=texto, font=font, 
                       bg=COLORES['bg'], fg=COLORES[color])
        return lbl

    def _crear_boton(self, texto, size, width, color, hover, comando):
        """Crea y empaqueta un botón"""
        return tk.Button(self.menu_frame, text=texto, font=('Arial', size, 'bold'),
                        width=width, height=2, bg=COLORES[color], fg="white",
                        activebackground=hover, command=comando)

    def crear_pantalla_principal(self):
        self._limpiar_frame()
        self.pantalla_actual = 'principal'
        s = self._calcular_escala()
        pad = int(15 * s)
        
        self._crear_label(" Tres en Raya Rolling ", int(28*s), True, 'x').pack(pady=pad)
        self._crear_label("¡Solo puedes tener 3 fichas a la vez!", int(12*s)).pack(pady=(0, int(20*s)))
        self._crear_label("Selecciona el modo de juego:", int(14*s), True).pack(pady=pad)
        
        btn_w = int(20 * s)
        self._crear_boton(" 1 vs 1 ", int(16*s), btn_w, 'x', "#c73850",
                         lambda: self.mostrar_pantalla_nombres("1vs1")).pack(pady=int(8*s))
        self._crear_boton("Un Jugador", int(16*s), btn_w, 'o', "#3a9fc4",
                         lambda: self.mostrar_pantalla_nombres("vs_ia")).pack(pady=int(8*s))
        
        tk.Button(self.menu_frame, text="Salir", font=('Arial', int(12*s)),
                 width=int(10*s), bg=COLORES['acento'], fg=COLORES['texto'],
                 activebackground="#5a5a7a", command=self.window.quit).pack(pady=int(20*s))

    def mostrar_pantalla_nombres(self, modo):
        self.en_transicion = True
        self._limpiar_frame()
        self.pantalla_actual = 'nombres'
        self.modo_seleccionado = modo
        
        # Aumentar tamaño de ventana para pantalla de nombres
        self.window.geometry("500x450")
        
        s = self._calcular_escala()
        
        self._crear_label(" Ingresa los nombres ", int(28*s), True, 'x').pack(pady=int(20*s))
        
        jugadores = ['Jugador 1 (X)', 'Jugador 2 (O)'] if modo == "1vs1" else ['Jugador (X)']
        self.entries = {}
        
        for jugador in jugadores:
            self._crear_label(jugador, int(16*s)).pack()
            entry = tk.Entry(self.menu_frame, font=('Arial', int(14*s)), width=25)
            entry.pack(pady=int(12*s))
            self.entries[jugador] = entry
        
        # Selector de dificultad para modo vs IA
        if modo == "vs_ia":
            self._crear_label("Dificultad de la IA:", int(16*s), True).pack(pady=(int(20*s), int(8*s)))
            
            self.dificultad_var = tk.StringVar(value='medio')
            frame_dif = tk.Frame(self.menu_frame, bg=COLORES['bg'])
            frame_dif.pack(pady=int(8*s))
            
            dificultades = [('Fácil', 'facil'), ('Medio', 'medio'), ('Difícil', 'dificil')]
            for texto, valor in dificultades:
                rb = tk.Radiobutton(
                    frame_dif, text=texto, variable=self.dificultad_var, value=valor,
                    font=('Arial', int(14*s)), bg=COLORES['bg'], fg=COLORES['texto'],
                    selectcolor=COLORES['btn'], activebackground=COLORES['bg'],
                    activeforeground=COLORES['texto']
                )
                rb.pack(side='left', padx=int(12*s))
        
        color = 'x' if modo == "1vs1" else 'o'
        hover = "#c73850" if modo == "1vs1" else "#3a9fc4"
        self._crear_boton("Iniciar Juego", int(18*s), 22, color, hover, 
                         self.iniciar_juego).pack(pady=int(20*s))
        
        self.en_transicion = False
    
    def _limpiar_frame(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
    
    def on_resize(self, event):
        # Evitar recrear durante transiciones
        if self.en_transicion:
            return
        
        current = (self.window.winfo_width(), self.window.winfo_height())
        if abs(current[0] - self.last_size[0]) > 50 or abs(current[1] - self.last_size[1]) > 50:
            self.last_size = current
            # Solo recrear si estamos en la pantalla principal
            if self.pantalla_actual == 'principal':
                self.crear_pantalla_principal()
            # No recrear pantalla de nombres para evitar problemas

    def iniciar_juego(self):
        dificultad = getattr(self, 'dificultad_var', None)
        dificultad = dificultad.get() if dificultad else 'medio'
        
        # Obtener nombres de los jugadores
        if self.modo_seleccionado == "1vs1":
            nombre_x = self.entries['Jugador 1 (X)'].get() or "Jugador 1"
            nombre_o = self.entries['Jugador 2 (O)'].get() or "Jugador 2"
        else:
            nombre_x = self.entries['Jugador (X)'].get() or "Jugador"
            nombre_o = "IA"
        
        self.window.destroy()
        InterfazJuego(tk.Tk(), self.modo_seleccionado, dificultad, nombre_x, nombre_o).window.mainloop()

class InterfazJuego:
    def __init__(self, window, modo="1vs1", dificultad='medio', nombre_x="Jugador 1", nombre_o="Jugador 2"):
        self.window = window
        self.window.title("Tres en Raya Infinito")
        self.window.resizable(True, True)
        self.window.state('zoomed')  # Pantalla completa en Windows
        self.modo = modo
        
        # Nombres de los jugadores
        self.nombre_x = nombre_x
        self.nombre_o = nombre_o
        
        # Inicializar juego
        self.juego = TicTacToe()
        
        # Inicializar IA si es modo vs_ia
        self.ia = IA(self.juego, 'O', dificultad) if modo == "vs_ia" else None
        
        # Colores
        self.bg_color = "#1a1a2e"
        self.btn_color = "#16213e"
        self.x_color = "#e94560"
        self.o_color = "#4fc3f7"
        self.text_color = "#eaeaea"
        self.fade_color = "#555555"  # Color para fichas que van a desaparecer
        
        self.window.configure(bg=self.bg_color)
        
        # Frame contenedor para centrar todo
        self.main_frame = tk.Frame(window, bg=self.bg_color)
        self.main_frame.pack(expand=True)
        
        # Título
        self.label = tk.Label(
            self.main_frame, 
            text=f"Turno de {self.nombre_x} (X)", 
            font=('Arial', 24, 'bold'),
            bg=self.bg_color,
            fg=self.x_color
        )
        self.label.grid(row=0, column=0, columnspan=3, pady=12)
        
        # Info del modo rolling
        max_fichas = self.juego.numero_maximo_de_mov
        self.info_label = tk.Label(
            self.main_frame, 
            text=f"Máximo {max_fichas} fichas por jugador", 
            font=('Arial', 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.info_label.grid(row=1, column=0, columnspan=3, pady=(0, 8))
        
        # Crear botones del tablero
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.main_frame,
                text="",
                font=('Arial', 40, 'bold'),
                width=4,
                height=2,
                bg=self.btn_color,
                fg=self.text_color,
                activebackground="#2a2a4e",
                command=lambda idx=i: self.hacer_mov(idx)
            )
            btn.grid(row=(i // 3) + 2, column=i % 3, padx=4, pady=4)
            self.buttons.append(btn)
        
        # Contador de fichas
        max_f = self.juego.numero_maximo_de_mov
        self.counter_label = tk.Label(
            self.main_frame, 
            text=f"{self.nombre_x}: 0/{max_f}  |  {self.nombre_o}: 0/{max_f}", 
            font=('Arial', 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.counter_label.grid(row=5, column=0, columnspan=3, pady=8)
        
        # Botón de reinicio
        self.reset_btn = tk.Button(
            self.main_frame,
            text="Nuevo Juego",
            font=('Arial', 12),
            bg="#4a4a6a",
            fg=self.text_color,
            activebackground="#5a5a7a",
            command=self.reiniciar_juego
        )
        self.reset_btn.grid(row=6, column=0, columnspan=3, pady=12)
        
        # Botón para volver al menú
        texto_menu = "Cambiar Dificultad" if self.modo == "vs_ia" else "Volver al Menú"
        self.menu_btn = tk.Button(
            self.main_frame,
            text=texto_menu,
            font=('Arial', 12),
            bg="#4a4a6a",
            fg=self.text_color,
            activebackground="#5a5a7a",
            command=self.volver_al_menu
        )
        self.menu_btn.grid(row=7, column=0, columnspan=3, pady=5)
    
    def hacer_mov(self, casilla):
        # Usar la lógica del backend para hacer el movimiento
        color_actual = self.x_color if self.juego.jugador_actual == 'X' else self.o_color
        
        exito, casilla_eliminada = self.juego.hacer_movimiento(casilla)
        
        if not exito:
            return
        
        # Si se eliminó una ficha, actualizar la interfaz
        if casilla_eliminada is not None:
            self.buttons[casilla_eliminada].config(text="", fg=self.text_color)
        
        # Actualizar el botón con el movimiento
        self.buttons[casilla].config(text=self.juego.jugador_actual, fg=color_actual)
        
        # Marcar la ficha más antigua con color más tenue
        self.actualizar_color_ficha()
        
        # Verificar ganador
        combo_ganador = self.juego.verificar_ganador(self.juego.jugador_actual)
        nombre_ganador = self.nombre_x if self.juego.jugador_actual == 'X' else self.nombre_o
        if combo_ganador:
            self.label.config(text=f"¡{nombre_ganador} gana! 🎉", fg=color_actual)
            # Resaltar las fichas ganadoras
            for i in combo_ganador:
                self.buttons[i].config(bg="#2e7d32")
            self.desabilitar_botones()
            messagebox.showinfo("Fin del juego", f"¡{nombre_ganador} gana!")
            return
        
        # Cambiar turno
        self.juego.cambiar_turno()
        next_color = self.x_color if self.juego.jugador_actual == 'X' else self.o_color
        nombre_turno = self.nombre_x if self.juego.jugador_actual == 'X' else self.nombre_o
        simbolo = self.juego.jugador_actual
        self.label.config(text=f"Turno de {nombre_turno} ({simbolo})", fg=next_color)
        
        # Actualizar contador
        x_count, o_count = self.juego.obtener_conteo_fichas()
        max_f = self.juego.numero_maximo_de_mov
        self.counter_label.config(text=f"{self.nombre_x}: {x_count}/{max_f}  |  {self.nombre_o}: {o_count}/{max_f}")
        
        # Si es modo vs IA y es turno de la IA, hacer movimiento
        if self.ia and self.juego.jugador_actual == 'O':
            self.window.after(500, self._movimiento_ia)
    
    def _movimiento_ia(self):
        """Ejecuta el movimiento de la IA"""
        casilla = self.ia.obtener_movimiento()
        if casilla is not None:
            self.hacer_mov(casilla)
    
    def actualizar_color_ficha(self):
        # Actualizar colores - la ficha más antigua se muestra más tenue
        for moves, color in [(self.juego.x_moves, self.x_color), (self.juego.o_moves, self.o_color)]:
            for i, pos in enumerate(moves):
                if len(moves) >= self.juego.numero_maximo_de_mov and i == 0:
                    # La ficha más antigua parpadea/se ve diferente
                    self.buttons[pos].config(fg=self.fade_color)
                else:
                    self.buttons[pos].config(fg=color)
    
    def desabilitar_botones(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
    
    def reiniciar_juego(self):
        self.juego.reiniciar()
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, fg=self.text_color, bg=self.btn_color)
        self.label.config(text=f"Turno de {self.nombre_x} (X)", fg=self.x_color)
        max_f = self.juego.numero_maximo_de_mov
        self.counter_label.config(text=f"{self.nombre_x}: 0/{max_f}  |  {self.nombre_o}: 0/{max_f}")
    
    def volver_al_menu(self):
        """Cierra el juego actual y abre el menú principal"""
        self.window.destroy()
        root = tk.Tk()
        MenuPrincipal(root)
        root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()