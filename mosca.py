from enemigo import Enemigo

class Mosca(Enemigo):
    def __init__(self, x: int, y: int, dir: bool, spawn_time: int):
        super().__init__(x, y, dir, spawn_time)
        self.sprite = (0, 16, 104, 16, 16)
        self.velocidad_y_salto = 1
        self.saltando = False
        self.salta_abajo = False
        self.y_salto = 0
        self.ALTURA_SALTO = 18
        # Lo hago para permitir a la mosca estar unos frames más pegado al
        # suelo y que sea más fácil derribarle
        self.contador_en_suelo = 0

    def mover(self, size: int, es_suelo: tuple):
        """ Este método mueve la mosca en la dirección que indica self.dir y
            conociendo el tamaño del tablero, lo mueve dando saltos,
            modificando tanto en el eje y como el eje x """
        size_mosca = self.sprite[3]
        height_mosca = self.sprite[4]
        # Control del movimiento en el eje x
        super().mover_ene(size, size_mosca)

        # Control del movimiento de la mosca en el eje y dando saltos
        if (es_suelo[0] and not self.saltando):
            self.saltando = True
            # Registro la altura desde la que empieza a saltar
            self.y_salto = es_suelo[1] - 1

        if self.saltando:
            # Si estoy subiendo en mi salto y aun no he llegado a la altura
            # máxima de salto
            if (self.y + height_mosca > self.y_salto - self.ALTURA_SALTO and
                 self.y > 0 and not self.salta_abajo):
                self.y -= self.velocidad_y_salto
            # Si he alcanzado la altura máxima de salto, empiezo a bajar
            elif (self.y + height_mosca <= self.y_salto - self.ALTURA_SALTO
                  and not self.salta_abajo):
                self.salta_abajo = True
                self.y += self.velocidad_y_salto
            # Mientras que no haya tocado el suelo y esté saltando para abajo
            elif self.y + height_mosca <= es_suelo[1] and self.salta_abajo:
                self.y += self.velocidad_y_salto
            # Excepción: caso especial para cuando esté en el último piso de
            # ladrillos
            elif 168 + height_mosca <= self.y + height_mosca <= 220 - 16 and \
                    self.salta_abajo:
                self.y += self.velocidad_y_salto
            elif self.contador_en_suelo > 2:
                self.saltando = False
                self.salta_abajo = False
                self.contador_en_suelo = 0
            else:
                self.contador_en_suelo += 1

        if self.cambio_color:
            # Si va a la derecha actualizo el sprite mirando a la derecha
            if self.dir:
                self.sprite = (2, 200 - ((self.x // 4) % 3) * 16, 120, 16, 16)
            # Si va a la izquierda, actualizo el sprite mirando a la izquierda
            else:
                self.sprite = (0, ((self.x // 2) % 3) * 16, 120, 16, 16)

        else:
            # Si va a la derecha actualizo el sprite mirando a la derecha
            if self.dir:
                self.sprite = (2, 200 - ((self.x//4) % 3)*16, 104, 16, 16)
            # Si va a la izquierda, actualizo el sprite mirando a la izquierda
            else:
                self.sprite = (0, ((self.x // 2) % 3) * 16, 104, 16, 16)

    # Permite a la mosca caer de un piso a otro
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
                    self.sprite = (2, 152, 120, 16, 16)
                else:
                    self.sprite = (0, 48, 120, 16, 16)
            else:
                if self.dir:
                    self.sprite = (2, 152, 104, 16, 16)
                else:
                    self.sprite = (0, 48, 104, 16, 16)
        elif ((self.volteado_contador % 20 == 10) and self.volteado_contador <
              140):
            if self.cambio_color:
                if self.dir:
                    self.sprite = (2, 136, 120, 16, 16)
                else:
                    self.sprite = (0, 64, 120, 16, 16)
            else:
                if self.dir:
                    self.sprite = (2, 136, 104, 16, 16)
                else:
                    self.sprite = (0, 64, 104, 16, 16)

        self.volteado_contador += 1

        if self.volteado_contador >= 158:
            if self.dir:
                self.sprite = (2, 200, 120, 16, 16)
            else:
                self.sprite = (0, 0, 120, 16, 16)
            # Se levanta más enfadada
            self.velocidad_x = 2
            self.velocidad_y_salto = 2
            self.cambio_color = True
            self.volteado = False
            # Termina la animación de la mosca volteada
            self.volteado_contador = 0

    def muere(self, w_size: int, h_size: int, dir: bool):
        return super().muere_enemigo(w_size, h_size, dir, self.sprite)
