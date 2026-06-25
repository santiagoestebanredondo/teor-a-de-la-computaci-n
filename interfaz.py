import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from maquina_turing import (
    MaquinaTuring,
    transiciones_anbn,
    transiciones_palindromo
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SimuladorMT(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Simulador de Máquinas de Turing")

        self.geometry("1500x900")

        self.mt = None
        self.velocidad = 500

        self.crear_layout()

    # =====================
    # LAYOUT PRINCIPAL
    # =====================

    def crear_layout(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_sidebar()
        self.crear_panel_principal()

    # =====================
    # SIDEBAR
    # =====================

    def crear_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=350,
            corner_radius=10
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=10,
            pady=10
        )

        titulo = ctk.CTkLabel(
            self.sidebar,
            text="1. Seleccionar Máquina",
            font=("Arial", 20, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.combo = ctk.CTkComboBox(
            self.sidebar,
            values=[
                "L = {aⁿbⁿ}",
                "Palíndromo"
            ]
        )

        self.combo.pack(
            fill="x",
            padx=15
        )

        entrada_lbl = ctk.CTkLabel(
            self.sidebar,
            text="2. Entrada",
            font=("Arial", 20, "bold")
        )

        entrada_lbl.pack(
            anchor="w",
            padx=15,
            pady=(25, 5)
        )

        self.entrada = ctk.CTkEntry(
            self.sidebar,
            height=40
        )

        self.entrada.pack(
            fill="x",
            padx=15
        )

        botones = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        botones.pack(
            fill="x",
            padx=15,
            pady=20
        )

        self.btn_inicio = ctk.CTkButton(
            botones,
            text="Iniciar",
            fg_color="green",
            command=self.iniciar
        )

        self.btn_inicio.pack(
            side="left",
            expand=True,
            padx=5
        )

        self.btn_reset = ctk.CTkButton(
            botones,
            text="Reiniciar",
            command=self.reiniciar
        )

        self.btn_reset.pack(
            side="left",
            expand=True,
            padx=5
        )

        controles = ctk.CTkLabel(
            self.sidebar,
            text="3. Controles",
            font=("Arial", 20, "bold")
        )

        controles.pack(
            anchor="w",
            padx=15,
            pady=(20, 5)
        )

        self.btn_paso = ctk.CTkButton(
            self.sidebar,
            text="▶ Paso",
            command=self.ejecutar_paso
        )

        self.btn_paso.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.btn_auto = ctk.CTkButton(
            self.sidebar,
            text="▶ Auto",
            command=self.ejecucion_automatica
        )

        self.btn_auto.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.slider = ctk.CTkSlider(
            self.sidebar,
            from_=100,
            to=2000
        )

        self.slider.pack(
            fill="x",
            padx=15,
            pady=15
        )

    # =====================
    # PANEL DERECHO
    # =====================

    def crear_panel_principal(self):

        self.main = ctk.CTkFrame(
            self
        )

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        titulo = ctk.CTkLabel(
            self.main,
            text="Ejecución Paso a Paso",
            font=("Arial", 24, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        self.estado_frame = ctk.CTkFrame(
            self.main,
            height=80
        )

        self.estado_frame.pack(
            fill="x",
            padx=20
        )

        self.lbl_estado = ctk.CTkLabel(
            self.estado_frame,
            text="Estado Actual: q0",
            font=("Arial", 24)
        )

        self.lbl_estado.pack(
            side="left",
            padx=20,
            pady=15
        )

        # ===================
        # CINTA
        # ===================

        self.canvas = tk.Canvas(
            self.main,
            bg="white",
            height=220,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # ===================
        # TRANSICIÓN
        # ===================

        self.transicion_frame = ctk.CTkFrame(
            self.main
        )

        self.transicion_frame.pack(
            fill="x",
            padx=20
        )

        self.lbl_transicion = ctk.CTkLabel(
            self.transicion_frame,
            text="δ(q0,a) = (q1,X,R)",
            font=("Consolas", 24)
        )

        self.lbl_transicion.pack(
            pady=15
        )

        # ===================
        # HISTORIAL
        # ===================

        historial_lbl = ctk.CTkLabel(
            self.main,
            text="Historial de Configuraciones",
            font=("Arial", 20, "bold")
        )

        historial_lbl.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        columnas = (
            "Paso",
            "Estado",
            "Cabezal",
            "Acción"
        )

        self.tree = ttk.Treeview(
            self.main,
            columns=columnas,
            show="headings",
            height=12
        )

        for c in columnas:
            self.tree.heading(c, text=c)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # ===================
        # RESULTADO
        # ===================

        self.resultado = ctk.CTkLabel(
            self.main,
            text="Resultado:",
            height=60,
            font=("Arial", 22, "bold")
        )

        self.resultado.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.metricas_frame = ctk.CTkFrame(self.main)
        self.metricas_frame.pack(fill="x", padx=20, pady=(0, 10))

        metricas_lbl = ctk.CTkLabel(
            self.metricas_frame,
            text="Métricas",
            font=("Arial", 18, "bold")
        )
        metricas_lbl.pack(anchor="w", padx=15, pady=(10, 5))

        self.metricas_grid = ctk.CTkFrame(self.metricas_frame, fg_color="transparent")
        self.metricas_grid.pack(fill="x", padx=15, pady=(0, 10))

        self.metricas_labels = {}
        metricas_items = [
            ("Pasos ejecutados", "0"),
            ("Celdas visitadas", "0"),
            ("Celdas no blancas", "0"),
            ("Movimientos a izquierda", "0"),
            ("Movimientos a derecha", "0"),
            ("Resultado final", "-"),
            ("Longitud de entrada", "0"),
        ]

        for i, (nombre, valor) in enumerate(metricas_items):
            lbl_nombre = ctk.CTkLabel(
                self.metricas_grid,
                text=f"{nombre}:",
                font=("Arial", 14),
                anchor="w"
            )
            lbl_nombre.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=2)

            lbl_valor = ctk.CTkLabel(
                self.metricas_grid,
                text=valor,
                font=("Consolas", 14, "bold"),
                anchor="e"
            )
            lbl_valor.grid(row=i, column=1, sticky="e", pady=2)
            self.metricas_labels[nombre] = lbl_valor

    # =====================
    # DIBUJAR CINTA
    # =====================

    def dibujar_cinta(self,
                      cinta,
                      cabezal):

        self.canvas.delete("all")

        ancho = 65
        inicio = 50

        inicio_visible = max(0, cabezal - 7)
        fin_visible = inicio_visible + 15

        for i, simbolo in enumerate(cinta[inicio_visible:fin_visible]):

            posicion_real = inicio_visible + i

            x = inicio + i * ancho

            color = "#ffffff"

            if simbolo == "X":
                color = "#d8ffd8"

            elif simbolo == "Y":
                color = "#fff1c9"

            if posicion_real == cabezal:

                self.canvas.create_rectangle(
                    x,
                    60,
                    x + ancho,
                    120,
                    width=3,
                    outline="#2563eb",
                    fill=color
                )

                self.canvas.create_text(
                    x + ancho/2,
                    150,
                    text="▲",
                    font=("Arial", 20),
                    fill="#2563eb"
                )

                self.canvas.create_text(
                    x + ancho/2,
                    175,
                    text="Cabezal",
                    font=("Arial", 12),
                    fill="#2563eb"
                )

            else:

                self.canvas.create_rectangle(
                    x,
                    60,
                    x + ancho,
                    120,
                    fill=color
                )

            self.canvas.create_text(
                x + ancho/2,
                90,
                text=simbolo,
                font=("Arial", 20)
            )
    def iniciar(self):

        entrada = self.entrada.get().strip()

        if not entrada:
            return

        if self.combo.get() == "L = {aⁿbⁿ}":

            self.mt = MaquinaTuring(
                entrada,
                transiciones_anbn,
                "q0",
                "qa",
                "qr"
            )

        else:

            self.mt = MaquinaTuring(
                entrada,
                transiciones_palindromo,
                "q0",
                "qa",
                "qr"
            )

        self.lbl_estado.configure(
            text=f"Estado Actual: {self.mt.estado}"
        )

        self.lbl_transicion.configure(
            text="Máquina iniciada"
        )

        self.resultado.configure(
            text="Resultado: En ejecución"
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.dibujar_cinta(
            self.mt.cinta,
            self.mt.cabezal
        )

        for lbl in self.metricas_labels.values():
            lbl.configure(text="0")
        self.metricas_labels["Resultado final"].configure(text="En ejecución")
        self.metricas_labels["Longitud de entrada"].configure(text=str(len(self.entrada.get().strip())))
    def ejecutar_paso(self):

        if self.mt is None:
            return

        if self.mt.terminado():
            return

        self.mt.paso()

        self.lbl_estado.configure(
            text=f"Estado Actual: {self.mt.estado}"
        )

        self.dibujar_cinta(
            self.mt.cinta,
            self.mt.cabezal
        )

        if self.mt.ultima_transicion:

            estado, simbolo, nuevo_estado, escribir, mover = (
                self.mt.ultima_transicion
            )

            self.lbl_transicion.configure(
                text=f"δ({estado},{simbolo}) = ({nuevo_estado},{escribir},{mover})"
            )
        if len(self.mt.historial) > 0:

            ultimo = self.mt.historial[-1]

            self.tree.insert(
                "",
                "end",
                values=(
                    ultimo["paso"],
                    ultimo["estado"],
                    ultimo["cabezal"],
                    ultimo["accion"]
                )
            )

        if self.mt.estado == "qa":

            self.resultado.configure(
                text="✅ Resultado: CADENA ACEPTADA"
            )

        elif self.mt.estado == "qr":

            self.resultado.configure(
                text="❌ Resultado: CADENA RECHAZADA"
            )

        self._actualizar_metricas()
    def _actualizar_metricas(self):

        if self.mt is None:
            return

        metricas = self.mt.obtener_metricas()

        for nombre, valor in metricas.items():
            if nombre in self.metricas_labels:
                self.metricas_labels[nombre].configure(text=str(valor))
    def ejecucion_automatica(self):

        if self.mt is None:
            return

        if self.mt.terminado():
            return

        self.ejecutar_paso()

        velocidad = int(self.slider.get())

        self.after(
            velocidad,
            self.ejecucion_automatica
        )
    def reiniciar(self):

        self.mt = None

        self.entrada.delete(0, "end")

        self.lbl_estado.configure(
            text="Estado Actual: q0"
        )

        self.lbl_transicion.configure(
            text="δ(q0,a) = (q1,X,R)"
        )

        self.resultado.configure(
            text="Resultado:"
        )

        self.canvas.delete("all")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for lbl in self.metricas_labels.values():
            lbl.configure(text="0")
        self.metricas_labels["Resultado final"].configure(text="-")
        self.metricas_labels["Longitud de entrada"].configure(text="0")
