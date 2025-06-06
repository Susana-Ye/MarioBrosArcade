from classes.enemigo import Enemigo
from classes.floor import Floor

class Cangrejo(Enemigo):
    def __init__(self, x: int, y: int, dir: bool, spawn_time: int):
        super().__init__(x, y, dir, spawn_time)
        self.enfadandose = False
        self.enfadado = False
        self.enfadado_contador = 0
        self.sprite = (0, 0, 136, 16, 16)

    def choque_cangrejo(self, es_techo: list, es_techo_pow: bool, es_suelo_personaje: list, floor: Floor):
        # Si mario le da al cangrejo deformando el suelo, o se activa el pow y el cangrejo
        # está en contacto con el suelo
        if ((es_techo[0] and floor.esta_sobre_bloque(es_techo[1], es_techo[2], self.x, self.y, self.width, self.sprite[4]))
            or (es_techo_pow and floor.retumbando and es_suelo_personaje[0])):

            # Si ha sido el golpe debido al pow, lo hago saber
            if (es_techo_pow and floor.retumbando and es_suelo_personaje[0]):
                self.toque_pow += 1

            # Si es la primera vez que le da al cangrejo
            if self.contador_toques < 1:
                self.contador_toques += 1
                self.enfadandose = True
                self.velocidad_x = 2

            # Debe ser cuando los toques sean superiores a 4 frames para que deje transcurrir
            # un tiempo y que el primer golpe debido a la deformación del suelo termine
            # antes de comprobar un segundo choque. Si ha sido por pow no hace falta
            elif (self.contador_toques < 5 and self.toque_pow < 1):
                self.contador_toques += 1

            # Si mario le da una segunda vez desde el suelo o con el pow
            else:
                # Si le dan cuando ya estaba volteado
                if (self.volteado):
                    self.volteado_contador = 158
                else:
                    self.volteado = True

        # Si el cangrejo está en proceso de enfadarse
        if self.enfadandose:
            self.enfadar()
    
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

