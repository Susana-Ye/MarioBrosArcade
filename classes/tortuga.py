from classes.enemigo import Enemigo
class Tortuga(Enemigo):
    def __init__(self, x: int, y: int, dir: bool, spawn_time: int):
        super().__init__(x, y, dir, spawn_time)
        self.sprite = (0, 16, 72, 16, 16)

    def mover(self, size: int):
        """ Este método mueve la tortuga en la dirección que indica self.dir y
            conociendo el tamaño del tablero """

        # Guardo el tamaño horizontal del sprite para saber cuándo
        # llega al borde
        size_tortuga = self.sprite[3]

        super().mover_ene(size, size_tortuga)
        if self.cambio_color:
            # Si va a la derecha actualizo el sprite mirando a la derecha
            if self.dir:
                self.sprite = (2, 200 - ((self.x//4) % 3)*16, 88, 16, 16)
            # Si va a la izquierda, actualizo el sprite mirando a la izquierda
            else:
                self.sprite = (0, ((self.x // 5) % 3) * 16, 88, 16, 16)
        else:
            # Si va a la derecha actualizo el sprite mirando a la derecha
            if self.dir:
                self.sprite = (2, 200 - ((self.x // 4) % 3) * 16, 72, 16, 16)
            # Si va a la izquierda, actualizo el sprite mirando a la izquierda
            else:
                self.sprite = (0, ((self.x // 5) % 3) * 16, 72, 16, 16)

    def update_y(self, es_suelo: tuple):
        """Este método actualiza la posición en el eje y del enemigo en
        función de si está en el suelo o cayendo"""
        return super().update_y_enemigo(es_suelo, self.sprite[4])

    def entrar_tubo(self, x_tubo: int, y_tubo: int, tubo: str):
        return super().respawn_enemigo(x_tubo, y_tubo, tubo)

    def voltear(self):
        if (self.volteado_contador % 20 == 0) and self.volteado_contador < 140:
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 152, 88, 16, 16)
                else:
                    self.sprite = (0, 48, 88, 16, 16)
            else:
                if self.dir:
                    self.sprite = (2, 152, 72, 16, 16)
                else:
                    self.sprite = (0, 48, 72, 16, 16)

        elif ((self.volteado_contador % 20 == 10) and self.volteado_contador <
              140):
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 136, 88, 16, 16)
                else:
                    self.sprite = (0, 64, 88, 16, 16)
            else:
                if self.dir:
                    self.sprite = (2, 136, 72, 16, 16)
                else:
                    self.sprite = (0, 64, 72, 16, 16)

        elif 140 <= self.volteado_contador < 146:
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 104, 88, 16, 16)
                else:
                    self.sprite = (0, 96, 88, 16, 16)
            else:
                if self.dir:
                    self.sprite = (2, 104, 72, 16, 16)
                else:
                    self.sprite = (0, 96, 72, 16, 16)

        elif 146 <= self.volteado_contador < 152:
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 80, 88, 24,16)
                else:
                    self.sprite = (0, 112, 88, 24, 16)
            else:
                if self.dir:
                    self.sprite = (2, 80, 72, 24, 16)
                else:
                    self.sprite = (0, 112, 72, 24, 16)

        elif 152 <= self.volteado_contador < 158:
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 16, 88, 24, 16)
                else:
                    self.sprite = (0, 176, 88, 24, 16)
            else:
                if self.dir:
                    self.sprite = (2, 16, 72, 24, 16)
                else:
                    self.sprite = (0, 176, 72, 24, 16)

        self.volteado_contador += 1

        # Se levanta más cabreado
        if self.volteado_contador >= 158:
            if self.dir:
                self.sprite = (2, 56, 88, 16, 16)
            else:
                self.sprite = (0, 144, 88, 24, 16)
            self.velocidad_x = 2
            self.cambio_color = True
            self.volteado = False
            self.volteado_contador = 0

    def muere(self, w_size: int, h_size: int, dir: bool):
        return super().muere_enemigo(w_size, h_size, dir, self.sprite)