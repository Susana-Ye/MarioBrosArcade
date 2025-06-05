from classes.enemigo import Enemigo

class Cangrejo(Enemigo):
    def __init__(self, x: int, y: int, dir: bool, spawn_time: int):
        super().__init__(x, y, dir, spawn_time)
        self.enfadandose = False
        self.enfadado = False
        self.enfadado_contador = 0
        self.sprite = (0, 0, 136, 16, 16)

    def mover(self, size: int):
        """ Este método mueve el cangrejo en la dirección que indica self.dir y
            conociendo el tamaño del tablero """

        # Guardo el tamaño horizontal del sprite para saber cuándo
        # llega al borde
        size_cangrejo = self.sprite[3]
        super().mover_ene(size, size_cangrejo)
        # Actualizo el sprite dependiendo de si está enfadado
        if self.cambio_color:
            # Si va a la derecha actualizo el sprite mirando a la derecha
            if self.dir:
                self.sprite = (2, 136 -((self.x // 2) % 3) * 16, 168, 16,
             16)
            # Si va a la izquierda, actualizo el sprite mirando a la izquierda
            else:
                self.sprite = (0, ((self.x // 2) % 3) * 16 + 64, 168, 16, 16)
        elif not self.enfadado:
            # Si va a la derecha actualizo el sprite mirando a la derecha
            if self.dir:
                self.sprite = (2, 200-((self.x // 2) % 3) * 16, 136, 16, 16)
            # Si va a la izquierda, actualizo el sprite mirando a la izquierda
            else:
                self.sprite = (0, ((self.x // 2) % 3) * 16, 136, 16, 16)
        # Si está enfadado
        else:
            if self.dir:
                self.sprite = (2, 136 - ((self.x//2) % 3)*16, 136, 16, 16)
            else:
                self.sprite = (0, 64 + ((self.x // 2) % 3) * 16, 136, 16, 16)

    def update_y(self, es_suelo: tuple):
        """Este método actualiza la posición en el eje y del enemigo en
        función de si está en el suelo o cayendo"""
        return super().update_y_enemigo(es_suelo, self.sprite[4])

    def entrar_tubo(self, x_tubo: int, y_tubo: int, tubo: str):
        return super().respawn_enemigo(x_tubo, y_tubo, tubo)

    def enfadar(self):
        if self.enfadado_contador < 4:
            if self.dir:
                self.sprite = (2, 152, 136, 16, 16)
            else:
                self.sprite = (0, 48, 136, 16, 16)
        elif 4 <= self.enfadado_contador < 8:
            if self.dir:
                self.sprite = (2, 136, 136, 16, 16)
            else:
                self.sprite = (0, 64, 136, 16, 16)
        elif 8 <= self.enfadado_contador < 12:
            if self.dir:
                self.sprite = (2, 120, 136, 16, 16)
            else:
                self.sprite = (0, 80, 136, 16, 16)
        elif 12 <= self.enfadado_contador < 16:
            if self.dir:
                self.sprite = (2, 104, 136, 16, 16)
            else:
                self.sprite = (0, 96, 136, 16, 16)

        self.enfadado_contador += 1

        if self.enfadado_contador >= 16:
            self.enfadandose = False
            self.enfadado = True

    def voltear(self):
        if (self.volteado_contador % 20 == 0) and self.volteado_contador < 140:
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 88, 168, 16, 16)
                else:
                    self.sprite = (0, 112, 168, 16, 16)
            else:
                if self.dir:
                    self.sprite = (2, 88, 136, 16, 16)
                else:
                    self.sprite = (0, 112, 136, 16, 16)

        elif ((self.volteado_contador % 20 == 10) and self.volteado_contador <
              140):
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 72, 168, 16, 16)
                else:
                    self.sprite = (0, 128, 168, 16, 16)
            else:
                if self.dir:
                    self.sprite = (2, 72, 136, 16, 16)
                else:
                    self.sprite = (0, 128, 136, 16, 16)

        self.volteado_contador += 1

        if self.volteado_contador >= 158:
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 136, 168, 16, 16)
                else:
                    self.sprite = (0, 64, 168, 16, 16)
            else:
                if self.dir:
                    self.sprite = (2, 136, 136, 16, 16)
                else:
                    self.sprite = (0, 64, 136, 16, 16)
            # Termina la animación del cangrejo volteado
            self.volteado = False
            self.volteado_contador = 0
            # Cuando se levanta otra vez cambia de color
            if self.enfadado:
                self.cambio_color = True

    def muere(self, w_size: int, h_size: int, dir: bool):
        return super().muere_enemigo(w_size, h_size, dir, self.sprite)

