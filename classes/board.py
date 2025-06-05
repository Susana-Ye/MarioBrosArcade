from classes.mario import Mario
from classes.floor import Floor
from classes.tuberia import Tuberia
from classes.nivel import ListaNiveles
from classes.pow import Pow
import pyxel

class Board:
    """ Esta clase contiene toda la información para representar el
    tablero y realiza el proceso del juego"""

    def __init__(self, w: int, h: int):
        """
        @atributo width: guarda la anchura del tablero
        @atributo height: guarda la altura del tablero
        @atributo mario: creo un Mario en la mitad de la pantalla sobre el
            suelo de ladrillos mirando a la derecha
        @atributo floor: constituye todas las plataformas a las que puede
            saltar mario
        @atributo tuberia: constituye las tuberías desde las que entran y
            salen enemigos
        """
        self.width = w
        self.height = h
        self.game_over = False
        self.ganado = False
        self.NUM_NIVELES = 3
        self.mario = Mario(self.width // 4, self.height - 37, True)
        self.pow = Pow(self.width, self.height)
        self.floor = Floor(self.width, self.height)
        self.tuberia = Tuberia(self.width, self.height)
        self.partida = ListaNiveles(self.width, self.height, self.NUM_NIVELES)

    # Dadas las coordenadas (x, y) y medidas de ancho y alto (w, h) de
    # dos objetos 1 y 2, devuelve cierto si entran en colisión
    def colision(self, x1: int, y1: int, w1: int, h1: int, x2: int,
                 y2: int, w2: int, h2: int):
        return (((x1 <= x2 <= x1+w1) or (x1 <= x2+w2 <= x1+w1)) and ((y1 <= y2
                <= y1+h1) or (y1 <= y2+h2 <= y1+h1)))


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        else:
            # Si la partida no está terminada o en un proceso de cambio de
            # nivel, ejecuto la partida
            if not self.game_over and not self.ganado and not self.partida.cambio_nivel:
                # Facilito la sintaxis asignando a una variable el índice de la
                # partida que se está jugando
                index = self.partida.ind_nivel

                # Compruebo si es hora de spawnear algún personaje
                self.partida.niveles[index].activar_personaje()

                # Compruebo el estado de mario
                es_suelo = self.floor.es_suelo_mario(self.mario.x, self.mario.y, self.mario.width_mario,
                                             self.mario.sprite_mario[4], self.pow.x, self.pow.y, self.pow.WIDTH)
                es_techo = self.floor.es_techo(self.mario.x, self.mario.y, self.mario.width_mario)
                es_techo_pow = self.pow.es_techo_pow(self.mario.x, self.mario.y, self.mario.width_mario)

                # Control del movimiento de mario en el eje y
                self.mario.mov_eje_y(es_suelo, es_techo, es_techo_pow, self.floor, self.pow)

                # Control del movimiento de mario en el eje x
                if not self.mario.desactivado:
                    if pyxel.btn(pyxel.KEY_RIGHT):
                        self.mario.mover('right', self.width)
                    elif pyxel.btn(pyxel.KEY_LEFT):
                        self.mario.mover('left', self.width)
                    else:
                        self.mario.mover('stop', self.width)
                
                # Control de la muerte y respawn de mario
                self.mario.ejecutar_muerte(self.width, self.height)

                # Control de todos los personajes activos de ese nivel
                for i in range(self.partida.niveles[index].num_personajes):
                    if self.partida.niveles[index].personajes[i].vivo:

                        # Comprueba si el personaje está sobre suelo
                        es_suelo_personaje = self.floor.es_suelo(
                            self.partida.niveles[index].personajes[i].x,
                            self.partida.niveles[index].personajes[i].y,
                            self.partida.niveles[index].personajes[i].width,
                            self.partida.niveles[index].personajes[i].sprite[
                                4], self.pow.x, self.pow.y, self.pow.WIDTH)
                        # Comprueba si el personaje ha colisionado con un tubo de entrada
                        es_tubo_entrada = self.tuberia.es_tubo_entrada(
                            self.partida.niveles[index].personajes[i].x,
                            self.partida.niveles[index].personajes[i].y,
                            self.partida.niveles[index].personajes[i].width,
                            self.partida.niveles[index].personajes[i].dir)

                        # Comprueba si el personaje ha colisionado con otro personaje
                        for j in range(self.partida.niveles[index].num_personajes):
                            # Me aseguro de que no estoy chocando conmigo
                            # mismo y que el otro personaje en j está vivo,
                            # y que ninguno de los dos estuvieramos rotando
                            # porque entonces entro en bucle infinito rotando con el mismo personaje
                            if (i != j and not self.partida.niveles[index].personajes[i].rotando 
                                and not self.partida.niveles[index].personajes[i].volteado 
                                and not self.partida.niveles[index].personajes[j].rotando
                                and self.partida.niveles[index].personajes[j].vivo 
                                and self.colision(self.partida.niveles[index].personajes[i].x,
                                self.partida.niveles[index].personajes[i].y,
                                self.partida.niveles[index].personajes[i].width,
                                self.partida.niveles[index].personajes[i].sprite[4],
                                self.partida.niveles[index].personajes[j].x,
                                self.partida.niveles[index].personajes[j].y,
                                self.partida.niveles[index].personajes[i].width,
                                self.partida.niveles[index].personajes[i].sprite[4])):
                                self.partida.niveles[index].personajes[i].rotando = True
                                if not self.partida.niveles[index].personajes[j].volteado:
                                    self.partida.niveles[index].personajes[j].rotando = True

                        # Controla si mario ha chocado con alguno de los enemigos
                        if (not self.mario.respawnear and self.colision(
                        self.partida.niveles[
                             index].personajes[i].x, self.partida.niveles[
                             index].personajes[i].y, self.partida.niveles[
                             index].personajes[i].width, self.partida.niveles[
                             index].personajes[i].sprite[4], self.mario.x,
                             self.mario.y, self.mario.width_mario,
                             self.mario.sprite_mario[4]) and
                             self.partida.niveles[index].tipo[i] != 'moneda'
                                and not self.partida.niveles[
                             index].personajes[i].volteado):
                            self.mario.muriendo = True
                            self.mario.desactivado = True
                            self.partida.niveles[index].personajes[
                                 i].rotando = True

                        # Si el enemigo está rotando, activo la función rotar
                        if self.partida.niveles[index].personajes[
                                    i].rotando:
                            self.partida.niveles[index].personajes[
                                i].rotar()

                        # Controla una moneda
                        if self.partida.niveles[index].tipo[
                            i] == 'moneda':
                            # Si mario colisiona con la moneda o deforma el suelo justo de debajo o se activa el pow
                            # mientras la moneda está tocando el suelo, activo la animación
                            # de explotar la moneda y se actualizan los puntos
                            if ((self.colision(self.mario.x, self.mario.y, self.mario.width_mario, self.mario.sprite_mario[4],
                                              self.partida.niveles[index].personajes[i].x, self.partida.niveles[index].personajes[i].y,
                                              self.partida.niveles[index].personajes[i].width, self.partida.niveles[index].personajes[i].sprite[4])
                                 or (es_techo[0] and self.floor.esta_sobre_bloque(es_techo[1], es_techo[2], self.partida.niveles[index].personajes[i].x, self.partida.niveles[index].personajes[i].y,
                                              self.partida.niveles[index].personajes[i].width, self.partida.niveles[index].personajes[i].sprite[4])))
                                 or (es_techo_pow and self.floor.retumbando and es_suelo_personaje[0])
                                 and not self.partida.niveles[index].personajes[i].colision_mario):
                                self.partida.niveles[index].personajes[i].colision_mario = True
                                self.partida.niveles[index].num_derrotados += 1

                            # Mientras está activa la animación de explotar
                            # la moneda
                            if self.partida.niveles[index].personajes[i].colision_mario and not self.partida.niveles[index].personajes[i].derrotado:
                                self.partida.niveles[index].personajes[i].explota()
                                if self.partida.niveles[index].personajes[
                                    i].explota_contador == 1:
                                    self.mario.update_puntos()

                            # Si no ha ocurrido nada de lo anterior,
                            # la moneda sigue moviéndose
                            elif not self.partida.niveles[index].personajes[i].colision_mario:
                                self.partida.niveles[index].personajes[i].mover(self.width)
                                self.partida.niveles[index].personajes[i].update_y_moneda(es_suelo_personaje)

                            # Si la moneda entra en contacto con el tubo,
                            # llamo a entrar_tubo y le hago desaparecer
                            if es_tubo_entrada[0]:
                                self.partida.niveles[index].personajes[
                                    i].entrar_tubo(es_tubo_entrada[1],
                                                   es_tubo_entrada[2],
                                                   es_tubo_entrada[3])

                        # Controla un enemigo de tipo tortuga, cangrejo y
                        # mosca
                        elif self.partida.niveles[index].tipo[
                            i] == 'tortuga' or self.partida.niveles[index].tipo[
                            i] == 'cangrejo' or self.partida.niveles[index].tipo[
                            i] == 'mosca':

                            # Controla el choque y volteo de tortuga y mosca
                            if (self.partida.niveles[index].tipo[i] == 'tortuga'
                                    or self.partida.niveles[index].tipo[i] ==
                                    'mosca'):
                                # Si recibe un toque por el suelo deformado,
                                # o si el pow se activa y está tocando el suelo
                                if ((es_techo[0] and self.floor.esta_sobre_bloque(es_techo[1], es_techo[2],
                                        self.partida.niveles[index].personajes[i].x, self.partida.niveles[index].personajes[i].y,
                                        self.partida.niveles[index].personajes[i].width, self.partida.niveles[index].personajes[i].sprite[4]))
                                    or (es_techo_pow and self.floor.retumbando
                                    and es_suelo_personaje[0])):
                                    # Si ha sido el golpe debido al
                                    # pow, lo hago saber
                                    if (es_techo_pow and self.floor.retumbando
                                            and es_suelo_personaje[0]):
                                        self.partida.niveles[index].personajes[
                                            i].toque_pow += 1

                                    # Si el enemigo no está volteado, se voltea
                                    if not self.partida.niveles[index].personajes[i].volteado:
                                        self.partida.niveles[index].personajes[i].volteado = True

                                    # Debe ser cuando los toques sean superiores a 4 frames para que deje transcurrir
                                    # un tiempo y que el primer golpe debido a la deformación del suelo termine
                                    # antes de comprobar un segundo choque. Si ha sido por pow no hace falta
                                    elif (self.partida.niveles[index].personajes[
                                              i].contador_toques < 4 and
                                          self.partida.niveles[index].personajes[
                                            i].toque_pow < 1):
                                            self.partida.niveles[index].personajes[
                                            i].contador_toques += 1
                                    # Si estaba ya volteado y volvemos a dar un
                                    # toque, se levanta inmediatamente
                                    else:
                                        self.partida.niveles[index].personajes[
                                            i].volteado_contador = 158

                            # Controla el choque y volteo del cangrejo
                            elif self.partida.niveles[index].tipo[i] == 'cangrejo':
                                # Si mario le da al cangrejo deformando el
                                # suelo, o se activa el pow y el cangrejo
                                # está en contacto con el suelo
                                if ((es_techo[0] and self.floor.esta_sobre_bloque(es_techo[1], es_techo[2], self.partida.niveles[index].personajes[i].x,
                                        self.partida.niveles[index].personajes[i].y,self.partida.niveles[index].personajes[i].width,
                                        self.partida.niveles[ index].personajes[i].sprite[4]))
                                    or (es_techo_pow and self.floor.retumbando
                                    and es_suelo_personaje[0])):

                                    # Si ha sido el golpe debido al
                                    # pow, lo hago saber
                                    if (es_techo_pow and self.floor.retumbando
                                            and es_suelo_personaje[0]):
                                        self.partida.niveles[index].personajes[
                                            i].toque_pow += 1

                                    # Si es la primera vez que le da al cangrejo
                                    if self.partida.niveles[index].personajes[
                                        i].contador_toques < 1:
                                        self.partida.niveles[index].personajes[
                                            i].contador_toques += 1
                                        self.partida.niveles[index].personajes[
                                            i].enfadandose = True
                                        self.partida.niveles[index].personajes[
                                            i].velocidad_x = 2

                                    # Debe ser cuando los toques sean superiores a 4 frames para que deje transcurrir
                                    # un tiempo y que el primer golpe debido a la deformación del suelo termine
                                    # antes de comprobar un segundo choque. Si ha sido por pow no hace falta
                                    elif (self.partida.niveles[index].personajes[i].contador_toques < 5 and
                                          self.partida.niveles[index].personajes[i].toque_pow < 1):
                                        self.partida.niveles[index].personajes[
                                        i].contador_toques += 1

                                    # Si mario le da una segunda vez desde
                                    # el suelo o con el pow
                                    else:
                                        # Si le dan cuando ya estaba volteado
                                        if (self.partida.niveles[index].personajes[i].volteado):
                                            self.partida.niveles[index].personajes[
                                                i].volteado_contador = 158
                                        else:
                                            self.partida.niveles[index].personajes[
                                            i].volteado = True

                                # Si el cangrejo está en proceso de enfadarse
                                if self.partida.niveles[index].personajes[
                                    i].enfadandose:
                                    self.partida.niveles[index].personajes[
                                        i].enfadar()

                            # Si ya está dada la vuelta y mario colisiona con
                            # ella, pues sale volando y muere (igual para
                            # los tres enemigos)
                            if (self.colision(self.mario.x, self.mario.y,self.mario.width_mario, self.mario.sprite_mario[4],
                                        self.partida.niveles[index].personajes[i].x,self.partida.niveles[index].personajes[i].y,
                                        self.partida.niveles[index].personajes[i].width,
                                        self.partida.niveles[index].personajes[i].sprite[4])
                                    and self.partida.niveles[index].personajes[i].volteado
                                    and not self.partida.niveles[index].personajes[i].mata_enemigo):
                                self.partida.niveles[index].personajes[i].mata_enemigo = True
                                # Mando la posición desde la cual el enemigo muere
                                self.partida.niveles[index].personajes[i].posicion_muerte = (
                                    self.partida.niveles[index].personajes[i].x,
                                    self.partida.niveles[index].personajes[i].y)
                                self.mario.update_puntos()

                            # Si consigo voltear al enemigo, ejecuto la
                            # animación donde está volteando el enemigo
                            elif self.partida.niveles[index].personajes[
                                i].volteado:
                                self.partida.niveles[index].personajes[
                                    i].voltear()

                            # Controla que se levante otra vez la tortuga y
                            # su movimiento por la pantalla
                            if self.partida.niveles[index].tipo[
                                i] == 'tortuga':
                                # Si no se le ha rematado y no está volteado,
                                # le permito moverse
                                if not self.partida.niveles[index].personajes[
                                    i].mata_enemigo and not \
                                self.partida.niveles[index].personajes[i].volteado:
                                    self.partida.niveles[index].personajes[
                                        i].mover(self.width)
                                    self.partida.niveles[index].personajes[
                                        i].update_y(es_suelo_personaje)

                            # Controla que se levante otra vez el cangrejo
                            elif self.partida.niveles[index].tipo[i] == 'cangrejo':
                                # Si no está en proceso de animación enfadado, y no
                                # se le ha rematado y no está volteado,
                                # le permito moverse
                                if (not self.partida.niveles[index].personajes[
                                    i].mata_enemigo and not self.partida.niveles[
                                    index].personajes[i].volteado and not
                                    self.partida.niveles[index].personajes[i].
                                            enfadandose):
                                    self.partida.niveles[index].personajes[
                                        i].mover(self.width)
                                    self.partida.niveles[index].personajes[
                                        i].update_y(es_suelo_personaje)

                            # Controla que se levante otra vez la mosca
                            elif self.partida.niveles[index].tipo[
                                i] == 'mosca':
                                # Si no se le ha rematado y no está volteado,
                                # le permito moverse
                                if not self.partida.niveles[index].personajes[
                                    i].mata_enemigo and not \
                                        self.partida.niveles[index].personajes[
                                            i].volteado:
                                    self.partida.niveles[index].personajes[i].mover(
                                    self.width, es_suelo_personaje)
                                    # Si no está saltando, activo la función de
                                    # bajar de piso por la gravedad
                                    if not self.partida.niveles[index].personajes[
                                            i].saltando:
                                        self.partida.niveles[index].personajes[
                                            i].update_y(es_suelo_personaje)

                            # Se inicia la animación de matar al enemigo
                            if self.partida.niveles[index].personajes[
                                i].mata_enemigo:
                                self.partida.niveles[index].personajes[
                                    i].muere(self.width, self.height,
                                             self.mario.dir)

                            # Si ha llegado a un tubo de entrada, lo vuelvo a
                            # spawnear desde un tubo superior
                            if (es_tubo_entrada[0] and not self.partida.niveles[
                                index].personajes[i].derrotado and not
                                self.partida.niveles[index].personajes[
                                i].mata_enemigo):
                                self.partida.niveles[index].personajes[
                                    i].entrar_tubo(
                                    es_tubo_entrada[1],
                                    es_tubo_entrada[2],
                                    es_tubo_entrada[3])

                # Sirve para poner el sprite de la plataforma otra vez normal
                if not es_techo[0]:
                    self.floor.normalizar()

                # Sirve para retumbar las plataformas si mario choca con pow
                if self.floor.retumbando:
                    self.floor.retumbar()

            # Comprueba si he ganado. Termina la partida cuando he superado todos
            # los niveles
            if self.partida.ind_nivel + 1 > self.NUM_NIVELES:
                self.ganado = True

            # Comprueba si he perdido. Termina la partida cuando Mario pierde
            # todas sus vidas, las cuales no se recuperan una vez se pasa de nivel
            if self.mario.vidas == 0:
                self.game_over = True

            # Comprueba si he superado un nivel.
            if (not self.partida.cambio_nivel and not self.ganado and not
            self.game_over):
                self.partida.niveles[self.partida.ind_nivel].num_derrotados = 0
                for i in range(self.partida.niveles[
                                   self.partida.ind_nivel].num_personajes):
                    if self.partida.niveles[
                        self.partida.ind_nivel].personajes[
                        i].derrotado:
                        self.partida.niveles[
                            self.partida.ind_nivel].num_derrotados += 1
                # Paso al siguiente nivel cuando
                # haya superado el actual num_derrotados se añade cuando un
                # personaje muere, o cuando la moneda colisiona con mario
                if (self.partida.niveles[
                    self.partida.ind_nivel].num_derrotados >=
                        self.partida.niveles[
                            self.partida.ind_nivel].num_personajes):
                    self.partida.ind_nivel += 1
                    self.partida.cambio_nivel = True
                    self.partida.contador_cambio_nivel += 1
                    self.mario.reset(self.width, self.height)

            # Cuando termina la animación de cambio de nivel, paso al siguiente
            # nivel finalmente
            elif self.partida.cambio_nivel:
                if self.partida.contador_cambio_nivel > 70:
                    self.partida.cambio_nivel = False
                    self.partida.contador_cambio_nivel = 0
                else:
                    self.partida.contador_cambio_nivel += 1
                    # Cuando pase al nivel 3 y 4, el suelo es amarillo
                    if self.partida.ind_nivel > 0:
                        self.floor.cambio_color_floor = True

    def draw(self):

        pyxel.cls(0)
        # Dibuja el suelo de ladrillos
        pyxel.bltm(0, self.height - 16, 0, 0, 0, self.width, 16,
                   colkey=2)

        # Dibuja las plataformas azules
        for i in range(7):
            for j in range(self.floor.plataforma[i]["num_cachos"]):
                if self.floor.plataforma[i]["lista_cachos"][j][3]:
                    height = self.floor.plataforma[i]["lista_cachos"][j][1] - 6
                else:
                    height = self.floor.plataforma[i]["lista_cachos"][j][1]
                pyxel.blt(
                    self.floor.plataforma[i]["lista_cachos"][j][0], height,
                    self.floor.plataforma[i]["lista_cachos"][j][2][0],
                    self.floor.plataforma[i]["lista_cachos"][j][2][1],
                    self.floor.plataforma[i]["lista_cachos"][j][2][2],
                    self.floor.plataforma[i]["lista_cachos"][j][2][3],
                    self.floor.plataforma[i]["lista_cachos"][j][2][4],
                    colkey=2)

        # Dibuja la parte del fondo de las tuberías
        for i in range(2):
            pyxel.bltm(self.tuberia.sprite_fondo[i][0], self.tuberia.sprite_fondo[i][1],
                       self.tuberia.sprite_fondo[i][2], self.tuberia.sprite_fondo[i][3],
                       self.tuberia.sprite_fondo[i][4], self.tuberia.sprite_fondo[i][5],
                       self.tuberia.sprite_fondo[i][6], colkey=2)

        # Dibuja las tuberías encima, con los respectivos cachos, etc.
        for i in range(4):
            pyxel.bltm(self.tuberia.sprite[i][0], self.tuberia.sprite[i][1], self.tuberia.sprite[i][2], 
                       self.tuberia.sprite[i][3], self.tuberia.sprite[i][4], self.tuberia.sprite[i][5],
                       self.tuberia.sprite[i][6], colkey=2)

        # Dibuja el bloque Pow
        pyxel.blt(self.pow.x, self.pow.y, self.pow.sprite[0], self.pow.sprite[1], self.pow.sprite[2],
                  self.pow.sprite[3], self.pow.sprite[4], colkey=8)

        # Dibuja el marcador de puntos
        pyxel.text(4, 4, "I:", 11)
        pyxel.text(12, 4, self.mario.string_puntos, 7)

        # Dibuja el marcador de vidas
        for i in range(self.mario.vidas):
            pyxel.blt(46 + i * 10,4, self.mario.sprite_vidas[0], self.mario.sprite_vidas[1], 
                      self.mario.sprite_vidas[2], self.mario.sprite_vidas[3], self.mario.sprite_vidas[4],
                      colkey=8)

        # Si pierdo el juego, no dibujo a ningún personaje
        if self.game_over:
            pyxel.text(self.width//2 - 18, self.height//3+6, "GAME OVER", 7)

        # Si he ganado dibuja un mensaje de: felicidades, has ganado
        elif self.ganado:
            pyxel.text(self.width // 4- 4, self.height // 3 + 6,
                           "CONGRATULATIONS! YOU HAVE WON THE GAME!", 7)

        # Estoy cambiando de nivel
        elif self.partida.cambio_nivel:
         pyxel.text((self.width // 3) +
                   self.partida.contador_cambio_nivel, self.height
                       // 3 + 6,
                       "FASE %i" % (self.partida.ind_nivel + 1), 7)


        # Si estoy jugando (no he perdido, no he ganado, no estoy en un
        # cambio de nivel), dibujo a los personajes que estén vivos
        else:

            # Dibujo en el extremo inferior el número de la fase que estoy
            # jugando
            pyxel.text(3, self.height - 50,
                       "FASE %i" % (self.partida.ind_nivel + 1), 7)

            # Dibujo todos los personajes activos de ese nivel
            for i in range(self.partida.niveles[self.partida.ind_nivel].num_personajes):
                if self.partida.niveles[self.partida.ind_nivel].personajes[i].vivo:

                    # Gestiona toda la animación de la moneda
                    if self.partida.niveles[self.partida.ind_nivel].tipo[
                        i] == 'moneda':
                        # Dibuja la moneda
                        if self.partida.niveles[self.partida.ind_nivel].personajes[i].derrotado and self.partida.niveles[self.partida.ind_nivel].personajes[i].vivo:
                            if self.partida.niveles[self.partida.ind_nivel].personajes[i].puntos_contador*2 <= 8:
                                pyxel.text(self.partida.niveles[self.partida.ind_nivel].personajes[i].x-2,
                                           self.partida.niveles[self.partida.ind_nivel].personajes[i].y
                                       - self.partida.niveles[self.partida.ind_nivel].personajes[i].puntos_contador*2, "800", 11)
                            else:
                                pyxel.text(self.partida.niveles[self.partida.ind_nivel].personajes[i].x-2,
                                           self.partida.niveles[self.partida.ind_nivel].personajes[i].y
                                           - 8, "800", 11)
                            if self.partida.niveles[self.partida.ind_nivel].personajes[i].puntos_contador >= 12:
                                self.partida.niveles[self.partida.ind_nivel].personajes[i].vivo = False
                            self.partida.niveles[self.partida.ind_nivel].personajes[i].puntos_contador += 1
                        if self.partida.niveles[self.partida.ind_nivel].personajes[i].vivo and self.partida.niveles[self.partida.ind_nivel].personajes[i].puntos_contador < 5:
                            pyxel.blt(self.partida.niveles[self.partida.ind_nivel].personajes[i].x, self.partida.niveles[self.partida.ind_nivel].personajes[i].y, self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[0],
                                      self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[1], self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[2],
                                      self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[3], self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[4],
                                      colkey=8)

                    # Dibuja al enemigo que no sea una moneda
                    else:
                        pyxel.blt(self.partida.niveles[self.partida.ind_nivel].personajes[i].x,
                                  self.partida.niveles[self.partida.ind_nivel].personajes[i].y,
                                  self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[0],
                                  self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[1],
                                  self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[2],
                                  self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[3],
                                  self.partida.niveles[self.partida.ind_nivel].personajes[i].sprite[4], colkey=8)
                        # Gestiona la animación de la puntuación cuando un
                        # enemigo es derrotado
                        if self.partida.niveles[self.partida.ind_nivel].personajes[i].mata_enemigo:
                            # Si mario mata al enemigo, dibujo los efectos
                            # especiales de la puntuación
                            if self.partida.niveles[self.partida.ind_nivel].personajes[i].puntos_contador * 2 <= 8:
                                pyxel.text(self.partida.niveles[self.partida.ind_nivel].personajes[i].posicion_muerte[0],
                                           self.partida.niveles[self.partida.ind_nivel].personajes[i].posicion_muerte[1]
                                           - self.partida.niveles[self.partida.ind_nivel].personajes[i].puntos_contador * 2,
                                           "800", 11)
                            else:
                                pyxel.text(self.partida.niveles[self.partida.ind_nivel].personajes[i].posicion_muerte[0],
                                           self.partida.niveles[self.partida.ind_nivel].personajes[i].posicion_muerte[1]
                                           - 8, "800", 11)
                                self.partida.niveles[self.partida.ind_nivel].personajes[i].derrotado \
                                    = True
                            self.partida.niveles[self.partida.ind_nivel].personajes[i].puntos_contador += 1

            # Dibuja las tuberías encima, con los respectivos cachos para
            # que parezca que los enemigos aparecen detrás
            for i in range(4):
                pyxel.bltm(self.tuberia.sprite[i][0],
                           self.tuberia.sprite[i][1],
                           self.tuberia.sprite[i][2],
                           self.tuberia.sprite[i][3],
                           self.tuberia.sprite[i][4],
                           self.tuberia.sprite[i][5],
                           self.tuberia.sprite[i][6], colkey=2)

            # Dibuja el bloque donde mario reaparece tras morir
            if self.mario.respawnear:
                pyxel.blt(self.mario.x_bloque, self.mario.y_bloque,
                  self.mario.sprite_bloque[0], self.mario.sprite_bloque[1],
                  self.mario.sprite_bloque[2], self.mario.sprite_bloque[3],
                  self.mario.sprite_bloque[4], colkey=8)

            # Dibuja a Mario
            pyxel.blt(self.mario.x, self.mario.y, self.mario.sprite_mario[0],
                      self.mario.sprite_mario[1], self.mario.sprite_mario[2],
                      self.mario.sprite_mario[3], self.mario.sprite_mario[4],
                      colkey=8)

            self.partida.niveles[self.partida.ind_nivel].tiempo += 1

