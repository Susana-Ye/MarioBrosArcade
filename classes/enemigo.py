# Hacer la clase general de enemigo
class Enemigo:
    def __init__(self, x: int, y: int, dir: bool, spawn_time: int):
        self.x = x
        self.y = y
        self.dir = dir
        self.width = 16

        # Atributos para controlar el movimiento del enemigo
        self.tiempo = 0
        self.velocidad_x = 1
        self.velocidad_y = 4
        self.gravedad = 2

        # Atributos para controlar la aparición del enemigo en el nivel
        self.vivo = False
        self.spawn_time = spawn_time

        # Se vuelve True cuando un personaje ya ha aparecido y mario lo mata
        self.derrotado = False

        # Contador del proceso en que el personaje rota al colisionar con otro
        # para que no entre en bucle infinito
        self.rotar_contador = 0
        self.rotando = False

        # Atributos para controlar interacción del enemigo con mario
        # Para mantener constancia del tiempo que está volteado
        self.volteado_contador = 0
        # Para dibujar la puntuación ganada tras matarlo
        self.puntos_contador = 0
        # Para saber si se le ha volteado
        self.volteado = False
        # Para que reconozca si el toque que está recibiendo ha terminado o
        # es uno nuevo (Puesto que cuando mario salta y deforma un bloque,
        # se queda durante 4 frames siendo es_techo = True)
        self.contador_toques = 0
        # Para saber si el primer toque fue con el pow y anulamos el
        # contador_toques
        self.toque_pow = 0
        # Para dibujar el sprite mientras muere
        self.contador_muerte = 0
        # Para saber si mario le ha matado una vez volteado y que comience
        # la animación de morir
        self.mata_enemigo = False
        # Para saber en qué posición le mató mario y poder hacerle caer por
        # la pantalla
        self.posicion_muerte = (0, 0)
        # Para saber si hay está cambiado el color del enemigo porque está
        # enfadado
        self.cambio_color = False


    def mover_ene(self, size: int, size_ene: int):

        if self.dir and self.x < size - size_ene:
            self.x += self.velocidad_x
        # Cuando ha llegado al borde de la pantalla y sigue yendo a la
        # derecha, lo mando al otro lado izquierdo de la pantalla
        elif self.dir:
            self.x = 0
        elif not self.dir and self.x > 0:
            self.x -= self.velocidad_x
        # Cuando llega al borde de la pantalla y sigue yendo a la
        # izquierda, lo mando al otro lado derecho de la pantalla
        elif not self.dir:
            self.x = size - size_ene

    def update_y_enemigo(self, es_suelo: tuple, height: int):
        """Este método actualiza la posición en el eje y del enemigo en
        función de si está en el suelo o cayendo"""

        if es_suelo[0]:
            self.y = es_suelo[1] - height
        else:
            self.y += self.velocidad_y

    def respawn_enemigo(self, x_tubo: int, y_tubo: int, tubo: str):
        """Dado un tubo (True es derecho, False es izquierdo), actualiza la
        información de la posición y dirección del enemigo para que salga
        por el tubo correspondiente"""
        self.y = y_tubo + 3
        # Sale por el tubo derecho
        if tubo.lower() == 'right' and x_tubo <= self.x:
            self.x = 248
            self.y = 20
            self.dir = False
        # Sale por el tubo izquierdo
        elif (tubo.lower() == 'left' and self.x + self.width <=
              x_tubo):
            self.x = 38
            self.y = 20
            self.dir = True

    def colision(self, x1: int, y1: int, w1: int, h1: int, x2: int,
                         y2: int, w2: int, h2: int):
                return (((x1 <= x2 <= x1+w1) or (x1 <= x2+w2 <= x1+w1)) and ((y1 <= y2
                        <= y1+h1) or (y1 <= y2+h2 <= y1+h1)))

    def muere_enemigo(self, w_size: int, h_size: int, dir: bool, sprite:
    tuple):

        if (self.x >= w_size or self.x + self.width < 0 or self.y >=
                h_size or self.y + sprite[4] < 0):
            self.vivo = False
            self.mata_enemigo = False
        elif self.contador_muerte < 6 and dir:
            self.x += 3
        elif self.contador_muerte < 6:
            self.x -= 3
        elif dir:
            self.y += 6
            self.x += 1
        else:
            self.y += 6
            self.x -= 1

        self.contador_muerte += 1

    def rotar(self):
        if self.rotar_contador < 1:
            if self.dir:
                self.dir = False
            else:
                self.dir = True
            self.rotar_contador += 1
        elif self.rotar_contador > 20:
            self.rotando = False
            self.rotar_contador = 0
        else:
            self.rotar_contador += 1