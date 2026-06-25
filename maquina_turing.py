class MaquinaTuring:

    def __init__(
        self,
        cinta,
        transiciones,
        estado_inicial,
        estado_aceptacion,
        estado_rechazo,
        limite_pasos=None
    ):

        self.input_length = len(cinta)

        # Agregamos blancos a ambos lados
        self.cinta = ['B'] * 10 + list(cinta) + ['B'] * 20

        self.cabezal = 10

        self.estado = estado_inicial

        self.q_accept = estado_aceptacion
        self.q_reject = estado_rechazo

        self.transiciones = transiciones

        self.paso_actual = 0

        self.historial = []

        self.ultima_transicion = None

        self.celdas_visitadas = set()
        self.celdas_visitadas.add(self.cabezal)

        self.movimientos_L = 0
        self.movimientos_R = 0

        self.limite_pasos = limite_pasos

    def terminado(self):

        return self.estado in (
            self.q_accept,
            self.q_reject
        )

    def obtener_cinta_visible(self):

        return self.cinta

    def paso(self):

        if self.terminado():
            return

        if self.limite_pasos is not None and self.paso_actual >= self.limite_pasos:
            self.ultima_transicion = (
                self.estado,
                self.cinta[self.cabezal],
                self.q_reject,
                self.cinta[self.cabezal],
                "S"
            )
            self.estado = self.q_reject
            return

        simbolo = self.cinta[self.cabezal]

        clave = (
            self.estado,
            simbolo
        )

        if clave not in self.transiciones:

            self.ultima_transicion = (
                self.estado,
                simbolo,
                self.q_reject,
                simbolo,
                "S"
            )

            self.estado = self.q_reject
            return

        nuevo_estado, escribir, mover = self.transiciones[clave]

        estado_anterior = self.estado

        self.cinta[self.cabezal] = escribir

        if mover == "R":
            self.cabezal += 1
            self.movimientos_R += 1

        elif mover == "L":
            self.cabezal -= 1
            self.movimientos_L += 1

        self.celdas_visitadas.add(self.cabezal)

        self.estado = nuevo_estado

        self.ultima_transicion = (
            estado_anterior,
            simbolo,
            nuevo_estado,
            escribir,
            mover
        )

        self.historial.append({

            "paso": self.paso_actual,

            "estado": estado_anterior,

            "cabezal": self.cabezal,

            "accion":
            f"δ({estado_anterior},{simbolo})"
            f"→({nuevo_estado},{escribir},{mover})"

        })

        self.paso_actual += 1

    def ejecutar_completo(self):

        while not self.terminado():
            self.paso()

        return self.estado == self.q_accept

    def resultado(self):

        if self.estado == self.q_accept:
            return "ACEPTADA"

        if self.estado == self.q_reject:
            return "RECHAZADA"

        return "EN EJECUCIÓN"
    
    def obtener_metricas(self):
        celdas_no_blancas = sum(1 for s in self.cinta if s != 'B')

        if self.estado == self.q_accept:
            resultado = "Accept"
        elif self.estado == self.q_reject:
            resultado = "Reject"
        else:
            resultado = "Sin conclusión"

        return {
            "Pasos ejecutados": self.paso_actual,
            "Celdas visitadas": len(self.celdas_visitadas),
            "Celdas no blancas": celdas_no_blancas,
            "Movimientos a izquierda": self.movimientos_L,
            "Movimientos a derecha": self.movimientos_R,
            "Resultado final": resultado,
            "Longitud de entrada": self.input_length,
        }
    

transiciones_anbn = {

    ('q0', 'X'): ('q0', 'X', 'R'),
    ('q0', 'a'): ('q1', 'X', 'R'),
    ('q0', 'Y'): ('q3', 'Y', 'R'),

    ('q1', 'a'): ('q1', 'a', 'R'),
    ('q1', 'X'): ('q1', 'X', 'R'),
    ('q1', 'Y'): ('q1', 'Y', 'R'),
    ('q1', 'b'): ('q2', 'Y', 'L'),

    ('q2', 'a'): ('q2', 'a', 'L'),
    ('q2', 'b'): ('q2', 'b', 'L'),
    ('q2', 'X'): ('q2', 'X', 'L'),
    ('q2', 'Y'): ('q2', 'Y', 'L'),
    ('q2', 'B'): ('q0', 'B', 'R'),

    ('q3', 'Y'): ('q3', 'Y', 'R'),
    ('q3', 'B'): ('qa', 'B', 'R'),
}

transiciones_palindromo = {

    ('q0', 'X'): ('q0', 'X', 'R'),
    ('q0', 'Y'): ('q0', 'Y', 'R'),

    ('q0', 'a'): ('qA', 'X', 'R'),
    ('q0', 'b'): ('qB', 'Y', 'R'),

    ('q0', 'B'): ('qa', 'B', 'R'),

    # Buscar extremo derecho para a

    ('qA', 'a'): ('qA', 'a', 'R'),
    ('qA', 'b'): ('qA', 'b', 'R'),
    ('qA', 'X'): ('qA', 'X', 'R'),
    ('qA', 'Y'): ('qA', 'Y', 'R'),
    ('qA', 'B'): ('qA2', 'B', 'L'),

    ('qA2', 'X'): ('qA2', 'X', 'L'),
    ('qA2', 'Y'): ('qA2', 'Y', 'L'),
    ('qA2', 'a'): ('qR', 'X', 'L'),

    # Buscar extremo derecho para b

    ('qB', 'a'): ('qB', 'a', 'R'),
    ('qB', 'b'): ('qB', 'b', 'R'),
    ('qB', 'X'): ('qB', 'X', 'R'),
    ('qB', 'Y'): ('qB', 'Y', 'R'),
    ('qB', 'B'): ('qB2', 'B', 'L'),

    ('qB2', 'X'): ('qB2', 'X', 'L'),
    ('qB2', 'Y'): ('qB2', 'Y', 'L'),
    ('qB2', 'b'): ('qR', 'Y', 'L'),

    # Regresar al inicio

    ('qR', 'a'): ('qR', 'a', 'L'),
    ('qR', 'b'): ('qR', 'b', 'L'),
    ('qR', 'X'): ('qR', 'X', 'L'),
    ('qR', 'Y'): ('qR', 'Y', 'L'),
    ('qR', 'B'): ('q0', 'B', 'R')
}