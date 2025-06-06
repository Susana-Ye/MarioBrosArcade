from classes.mario import Mario
from classes.floor import Floor
import pyxel

class Moneda:

    def __init__(self, x: int, y: int, dir: bool, spawn_time: int):
        self.x = x
        self.y = y
        self.dir = dir
        self.width = 8
        self.velocidad_x = 2
        self.velocidad_y = 4
        self.spawn_time = spawn_time
        self.sprite = (0, 0, 184, 8, 11)
        self.volteado = False
        # Indica que el personaje está activo y aparece por pantalla
        self.vivo = False
        # Contador del proceso en que la moneda explota
        self.explota_contador = 0
        # Indica que la moneda ha comenzado a existir y terminado su
        # interacción
        self.derrotado = False
        # Booleano que se vuelve True cuando la moneda entra en contacto con
        # Mario y comienza el proceso de explotar
        self.colision_mario = False
        self.puntos_contador = 0
        # Contador del proceso en que la moneda rota para que no entre en
        # bucle de rotar infinitamente
        self.rotar_contador = 0
        self.rotando = False

    # Dadas las coordenadas (x, y) y medidas de ancho y alto (w, h) de
    # dos objetos 1 y 2, devuelve cierto si entran en colisión
    def colision(self, x1: int, y1: int, w1: int, h1: int, x2: int,
                 y2: int, w2: int, h2: int):
        return (((x1 <= x2 <= x1+w1) or (x1 <= x2+w2 <= x1+w1)) and ((y1 <= y2
                <= y1+h1) or (y1 <= y2+h2 <= y1+h1)))

    
    def ejecucion_moneda(self, num_derrotados: int, mario: Mario, floor: Floor, es_techo: list, es_techo_pow: bool, es_suelo_personaje: list, es_tubo_entrada: list, width: int):
        
        # Si mario colisiona con la moneda o deforma el suelo justo de debajo o se activa el pow mientras 
        # la moneda está tocando el suelo, activo la animación de explotar la moneda y se actualizan los puntos
        if ((self.colision(mario.x, mario.y, mario.width_mario, mario.sprite_mario[4],
                            self.x, self.y, self.width, self.sprite[4])
                or (es_techo[0] and floor.esta_sobre_bloque(es_techo[1], es_techo[2], self.x, self.y,
                            self.width, self.sprite[4])))
                or (es_techo_pow and floor.retumbando and es_suelo_personaje[0])
                and not self.colision_mario):
            self.colision_mario = True
            num_derrotados += 1

        # Mientras está activa la animación de explotar la moneda
        if self.colision_mario and not self.derrotado:
            self.explota()
            if self.explota_contador == 1:
                mario.update_puntos()

        # Si no ha ocurrido nada de lo anterior, la moneda sigue moviéndose
        elif not self.colision_mario:
            self.mover(width)
            self.update_y_moneda(es_suelo_personaje)

        # Si la moneda entra en contacto con el tubo, llamo a entrar_tubo y le hago desaparecer
        if es_tubo_entrada[0]:
            self.entrar_tubo(es_tubo_entrada[1], es_tubo_entrada[2], es_tubo_entrada[3])
    

    def mover(self, size: int):
        """ Este método mueve la moneda en la dirección que indica self.dir y
        conociendo el tamaño del tablero """

        # Guardo el tamaño horizontal del sprite para saber cuándo
        # llega al borde
        moneda_x_size = self.sprite[3]

        if self.dir and self.x < size - moneda_x_size:
            self.x += self.velocidad_x
        # Cuando ha llegado al borde de la pantalla y sigue yendo a la
        # derecha, lo mando al otro lado izquierdo de la pantalla
        elif self.dir:
            self.x = 0
        elif not self.dir and self.x > 0:
            self.x -= self.velocidad_x
        # Cuando Mario ha llegado al borde de la pantalla y sigue yendo a la
        # izquierda, lo mando al otro lado derecho de la pantalla
        elif not self.dir:
            self.x = size - moneda_x_size

        self.sprite = (0, ((self.x//4) % 4) * 8, 184, 8, 11)

    def update_y_moneda(self, es_suelo: tuple):
        """Este método actualiza la posición en el eje y de la moneda en
        función de si está en el suelo o cayendo"""
        if es_suelo[0]:
            self.y = es_suelo[1] - self.sprite[4]
        else:
            self.y += self.velocidad_y

    def entrar_tubo(self, x_tubo: int, y_tubo: int, tubo: str):
        self.y = y_tubo + 5
        if tubo.lower() == 'right' and x_tubo <= self.x:
            self.vivo = False
            self.derrotado = True
        if (tubo.lower() == 'left' and self.x + self.width <=
              x_tubo):
            self.vivo = False
            self.derrotado = True

    def explota(self):
        if self.explota_contador < 4:
            self.y -= self.explota_contador * 3
            self.sprite = (0, 32 + ((self.explota_contador-1) * 16),
                                  186, 16, 11)
            self.explota_contador += 1
        elif self.explota_contador == 4:
            self.x += 4
            self.explota_contador += 1
            self.sprite = (0, 128, 0, 16, 11)
        else:
            self.derrotado = True

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

    def draw_coin(self):
        if self.derrotado and self.vivo:
            if self.puntos_contador*2 <= 8:
                pyxel.text(self.x-2, self.y - self.puntos_contador*2, "800", 11)
            else:
                pyxel.text(self.x-2, self.y - 8, "800", 11)
            if self.puntos_contador >= 12:
                self.vivo = False
            self.puntos_contador += 1
        if self.vivo and self.puntos_contador < 5:
            pyxel.blt(self.x, self.y, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], self.sprite[4], colkey=8)
