import pyxel
from classes.floor import Floor
from classes.pow import Pow

class Mario:
    def __init__(self, x: int, y: int, dir: bool):
        """
            @atributo x: la coordenada x inicial de Mario
            @atributo y: la coordenada y inicial Mario
            @atributo dir: un booleano que guarda la dirección inicial de Mario.
                True si está mirando a la derecha, False si mira a la izquierda
            @atributo width_mario: guarda el ancho de Mario
            @atributo jumping: un booleano que dice si Mario está saltando o no,
                tanto hacia arriba como abajo
            @atributo tiempo: un contador que aumenta cuando Mario inicia un
                salto o cae por la gravedad (permite controlar cuando Mario esté
                moviéndose sobre el eje y)
            @atributo velocidad: un entero que indica el número de frames
                durante los cuales Mario debe subir de altura (en cada frame sube
                4 píxeles)
            @atributo gravedad: un entero que permite hacer que Mario caiga
                cuando no haya suelo debajo
            @atributo sprite: tupla que guarda la información correspondiente al
                sprite de mario (banco 0, posición 0 0, tamaño 16x21)
            @atributo vidas: guarda el número de vidas que le quedan a mario,
                siempre empieza con 3 vidas
            @atributo sprite_vidas: tupla que guarda la información
                correspondiente al sprite de una vida de mario
            @atributo puntos: entero que guarda los puntos del jugador Mario
            @atributo string_puntos: string que rellena los puntos de Mario con
                0s para mostrarlo en el marcador de puntos
        """
        self.x = x
        self.y = y
        self.dir = dir
        self.width_mario = 16
        self.jumping = False
        self.tiempo = 0
        self.velocidad = 0
        self.gravedad = 2
        self.sprite_mario = (0, 0, 0, 16, 21)
        self.vidas = 3
        self.sprite_vidas = (0, 112, 2, 8, 6)
        self.puntos = 0
        self.string_puntos = "000000"

        # Atributos para controlar la muerte de mario y las animaciones
        # correspondientes
        self.y_bloque = -6
        self.x_bloque = 122
        self.sprite_bloque = (0, 176, 2, 15, 6)
        self.contador_muerte = 0
        self.muriendo = False
        self.respawn_contador = 0
        self.respawnear = False

        # Bool que me dice si puedo controlar el movimiento de mario o no
        # con las teclas
        self.desactivado = False

    def ejecucion_mario(self, es_suelo: bool, es_techo: list, es_techo_pow: bool, floor: Floor, pow: Pow, width: int, height: int):

        # Control del movimiento de mario en el eje y
        self.mov_eje_y(es_suelo, es_techo, es_techo_pow, floor, pow)

        # Control del movimiento de mario en el eje x
        if not self.desactivado:
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.mover('right', width)
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.mover('left', width)
            else:
                self.mover('stop', width)
        
        # Control de la muerte y respawn de mario
        self.ejecutar_muerte(width, height)
         
    def mov_eje_y(self, es_suelo: bool, es_techo: list, es_techo_pow: bool, floor: Floor, pow: Pow):
        """ Este método controla el movimiento de Mario en el eje y """
        if not self.respawnear:
            # Si mario no está saltando
            if not self.jumping:
                # Si no hay suelo, cae por la gravedad
                if not es_suelo:
                    self.velocidad = 0
                # Si está sobre suelo e inicia un salto
                elif pyxel.btn(pyxel.KEY_UP):
                    self.tiempo += 1
                    self.jumping = True
                    self.velocidad = -45
                # Si no está saltando y está sobre el suelo (puede que
                # estuviera cayendo o que esté moviéndose horizontalmente)
                else:
                    # Mantengo la altura constante cancelando cualquier
                    # movimiento vertical que tuviera poniendo tiempo a 0
                    self.velocidad = 0
                    self.tiempo = 0
            # Si mario está saltando
            else:
                # Si está saltando y colisiona con el suelo
                if es_suelo:
                    # Paro el salto
                    self.velocidad = 0
                    self.tiempo = 0
                    self.jumping = False
                # Si está saltando y colisiona con el techo
                elif es_techo[0]:
                    # Cancelo la velocidad inicial y que caiga por la gravedad
                    self.velocidad = 0
                    # Mando el índice de la plataforma y el cacho cuyo sprite
                    # quiero deformar
                    floor.deformar(es_techo[1], es_techo[2])
                # Si está saltando y colisiona con el bloque pow
                elif es_techo_pow:
                    # Cancelo la velocidad inicial y que caiga por la gravedad
                    self.velocidad = 0
                    if pow.estado.lower() != 'agotado':
                        # Actualizo el sprite y estado de pow
                        pow.deformar()
                        # Hago retumbar floor
                        floor.retumbando = True
        if not self.muriendo and not self.respawnear:
            self.update_y_mario(es_suelo)    
    
    def mover(self, direction: str, size: int):
        """ Este método mueve a Mario en la dirección que nos indican y
        conociendo el tamaño del tablero """

        # Guardo el tamaño horizontal del sprite de Mario para saber cuándo
        # llega al borde
        mario_x_size = self.sprite_mario[3]

        if direction.lower() == 'right' and self.x < size - mario_x_size:
            # Actualiza los sprites y mueve a Mario según si está saltando o no
            if self.jumping:
                self.sprite_mario = (0, 64, 0, 16, 21)
            else:
                self.sprite_mario = (0, (self.x%3+1)*16, 0, 16, 21)
            self.x += 2
            self.dir = True
        # Cuando Mario ha llegado al borde de la pantalla y sigue yendo a la
        # derecha, lo mando al otro lado izquierdo de la pantalla
        elif direction.lower() == 'right':
            self.x = 0
        elif direction.lower() == 'left' and self.x > 0:
            if self.jumping:
                self.sprite_mario = (2, 136, 0, 16, 21)
            else:
                self.sprite_mario = (2, (self.x%3+1)*16+ 152, 0, 16, 21)
            self.x -= 2
            self.dir = False
        # Cuando Mario ha llegado al borde de la pantalla y sigue yendo a la
        # izquierda, lo mando al otro lado derecho de la pantalla
        elif direction.lower() == 'left':
            self.x = size - mario_x_size
        # Si Mario no se mueve, hago que el sprite sea el correspondiente a
        # la dirección en el que se quedó
        elif direction.lower() == 'stop':
            # Mira a la derecha
            if self.dir:
                if self.jumping:
                    self.sprite_mario = (0, 64, 0, 16, 21)
                else:
                    self.sprite_mario = (0, 0, 0, 16, 21)
            # Mira a la izquierda
            else:
                if self.jumping:
                    self.sprite_mario = (2, 136, 0, 16, 21)
                else:
                    self.sprite_mario = (2, 200, 0, 16, 21)

    def ejecutar_muerte(self, width: int, height: int):
        """ Este método comprueba si mario ha muerto o está respawneando y ejecuta las funciones correspondientes """
        # Si mario muere controla la animación
        if self.muriendo:
            self.morir(width, height)

        # Si finaliza la animación de mario muriendo y debe
        # respawnear por encima de la panalla
        if self.respawnear:
            self.respawn()

        # Control de activar a mario después del respawn
        if (self.respawnear and self.y_bloque +
            self.sprite_bloque[4] >= 38):
            if ((pyxel.btn(pyxel.KEY_RIGHT) or
                pyxel.btn(pyxel.KEY_LEFT) or
            pyxel.btn(pyxel.KEY_UP))):
                self.respawn_contador = 400
 
    def update_y_mario(self, es_suelo: bool):
        """Este método actualiza la posición en el eje y de mario en función
        de si está en el suelo, o saltando..."""

        update_y = 0
        if self.velocidad*self.tiempo + self.gravedad*(self.tiempo**2) < 0:
            update_y = -4
        elif self.velocidad*self.tiempo + self.gravedad*(self.tiempo**2) > 0:
            update_y = 4
        if self.jumping or not es_suelo:
            self.velocidad += 1
            self.tiempo += 1

        self.y += update_y

    def update_puntos(self):
        # Tanto para coger una moneda como al matar a cualquier enemigo,
        # suma 800 puntos
        self.puntos += 800
        self.string_puntos = '{0:06d}'.format(self.puntos)

    # Reseteamos la información de mario cuando empieza un nivel nuevo
    def reset(self, w: int, h: int):
        self.x = w // 4
        self.y = h - 37
        self.dir = True
        self.jumping = False
        self.tiempo = 0
        self.velocidad = 0

    # Gestiona la animación de mario tras morir y le hace caer por la pantalla
    def morir(self, w_size: int, h_size: int):
        self.contador_muerte += 1

        # Si se sale por debajo de la pantalla le hago reaparecer
        if (self.y >= h_size):
            self.sprite_mario = (0, 0, 0, 16, 21)
            self.dir = True
            self.respawnear = True
            self.y = -27
            self.x = 122
            self.vidas -= 1
            self.contador_muerte = 0
            self.muriendo = False

        elif self.contador_muerte < 35 and self.dir:
            self.sprite_mario = (0, 0, 48, 16, 24)

        elif self.contador_muerte < 35:
            self.sprite_mario = (2, 200, 48, 16, 24)

        else:
            self.sprite_mario = (0, 16, 48, 16, 24)
            self.y += 6

    # Hacemos que mario vuelva a aparecer por arriba tras morir y se
    # gestiona la animación del bloque y mario esperando a moverse otra vez
    def respawn(self):

        if (self.respawn_contador < 100 and (self.respawn_contador % 2 == 0)
                and self.y_bloque + self.sprite_bloque[4] < 38 and self.y +
                self.sprite_mario[
                    4] < 38):
            self.y_bloque += 1
            self.y += 1

        elif 150 <= self.respawn_contador < 275:
            self.sprite_bloque = (0, 176, 9, 15, 4)

        elif 275 <= self.respawn_contador < 400:
            self.sprite_bloque = (0, 176, 14, 15, 2)

        self.respawn_contador += 1

        if self.respawn_contador >= 400:
            # Vuelvo a colocar el bloque como antes
            self.sprite_bloque = (0, 176, 2, 15, 6)
            self.y_bloque = -6
            self.respawnear = False
            self.desactivado = False
            self.respawn_contador = 0

