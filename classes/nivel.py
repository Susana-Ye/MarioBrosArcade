from classes.tortuga import Tortuga
from classes.cangrejo import Cangrejo
from classes.mosca import Mosca
from classes.moneda import Moneda
from classes.pow import Pow
from classes.floor import Floor
from classes.tuberia import Tuberia
from classes.mario import Mario
import pyxel

class ListaNiveles:
    def __init__(self, w: int, h: int, num_niveles: int):
        # Índice del nivel que estamos jugando
        self.ind_nivel = 0
        self.contador_cambio_nivel = 0
        self.cambio_nivel = False
        self.niveles = []
        for i in range(num_niveles):
            nivel = Nivel(w, h, i)
            self.niveles.append(nivel)
    
    def control_cambio_nivel(self, ganado: bool, game_over: bool, mario: Mario, floor: Floor, width: int, height: int):   
        # Comprueba si he superado un nivel
        if (not self.cambio_nivel and not ganado and not game_over):
            self.niveles[self.ind_nivel].num_derrotados = 0
            for i in range(self.niveles[self.ind_nivel].num_personajes):
                if self.niveles[self.ind_nivel].personajes[i].derrotado:
                    self.niveles[self.ind_nivel].num_derrotados += 1
            
            # Paso al siguiente nivel cuando haya superado el actual num_derrotados, se añade cuando un
            # personaje muere, o cuando la moneda colisiona con mario
            if (self.niveles[self.ind_nivel].num_derrotados >= self.niveles[self.ind_nivel].num_personajes):
                self.ind_nivel += 1
                self.cambio_nivel = True
                self.contador_cambio_nivel += 1
                mario.reset(width, height)

        # Cuando termina la animación de cambio de nivel, paso al siguiente nivel finalmente
        elif self.cambio_nivel:
            if self.contador_cambio_nivel > 70:
                self.cambio_nivel = False
                self.contador_cambio_nivel = 0
            else:
                self.contador_cambio_nivel += 1
                # Cuando pase al nivel 1, el suelo es amarillo
                if self.ind_nivel > 0:
                    floor.cambio_color_floor = True
    
class Nivel:
    def __init__(self, w: int, h: int, ind_nivel: int):
        """
        @atributo personajes: lista de los personajes que van a salir en el nivel
        """
        LISTA_NUM_PERSONAJES = [10, 10, 10, 10]
        TUBO_IZQ = (38, True)
        TUBO_DER = (248, False)

        # Indica el número de personajes que hay en ese nivel
        self.num_personajes = LISTA_NUM_PERSONAJES[ind_nivel]
        self.num_derrotados = 0
        # Sirve para controlar el tiempo del nivel, saber cuánto tiempo lleva desde que ha empezado el nivel
        self.tiempo = 0
        if ind_nivel == 0:
            self.personajes = [Mosca(TUBO_DER[0], 20, TUBO_DER[1], 0),
                               Tortuga(TUBO_IZQ[0], 20, TUBO_IZQ[1], 100),
                               Moneda(TUBO_IZQ[0], 20, TUBO_IZQ[1], 200),
                               Tortuga(TUBO_DER[0], 20, TUBO_DER[1], 300),
                               Moneda(TUBO_DER[0], 20, TUBO_DER[1], 400),
                               Cangrejo(TUBO_IZQ[0], 20, TUBO_IZQ[1], 500),
                               Tortuga(TUBO_IZQ[0], 20, TUBO_IZQ[1], 600),
                               Mosca(TUBO_DER[0], 20, TUBO_DER[1], 700),
                               Moneda(TUBO_IZQ[0], 20, TUBO_IZQ[1], 800),
                               Cangrejo(TUBO_DER[0], 20, TUBO_DER[1], 900), ]
            self.tipo = ['mosca', 'tortuga', 'moneda', 'tortuga', 'moneda',
                         'cangrejo', 'tortuga', 'mosca', 'moneda', 'cangrejo']

        elif ind_nivel == 1:
            self.personajes = [Cangrejo(TUBO_DER[0], 20, TUBO_DER[1], 0),
                               Tortuga(TUBO_IZQ[0], 20, TUBO_IZQ[1], 100),
                               Cangrejo(TUBO_IZQ[0], 20, TUBO_IZQ[1], 200),
                               Tortuga(TUBO_DER[0], 20, TUBO_DER[1], 300),
                               Moneda(TUBO_DER[0], 20, TUBO_DER[1], 400),
                               Cangrejo(TUBO_IZQ[0], 20, TUBO_IZQ[1], 500),
                               Mosca(TUBO_IZQ[0], 20, TUBO_IZQ[1], 600),
                               Mosca(TUBO_DER[0], 20, TUBO_DER[1], 700),
                               Moneda(TUBO_IZQ[0], 20, TUBO_IZQ[1], 800),
                               Tortuga(TUBO_DER[0], 20, TUBO_DER[1], 900)]
            self.tipo = ['cangrejo', 'tortuga', 'cangrejo', 'tortuga',
                         'moneda','cangrejo', 'mosca', 'mosca', 'moneda','tortuga']

        elif ind_nivel == 2:
            self.personajes = [Mosca(TUBO_DER[0], 20, TUBO_DER[1], 0),
                               Mosca(TUBO_IZQ[0], 20, TUBO_IZQ[1], 100),
                               Moneda(TUBO_IZQ[0], 20, TUBO_IZQ[1], 200),
                               Cangrejo(TUBO_DER[0], 20, TUBO_DER[1], 300),
                               Moneda(TUBO_DER[0], 20, TUBO_DER[1], 400),
                               Cangrejo(TUBO_IZQ[0], 20, TUBO_IZQ[1], 500),
                               Mosca(TUBO_DER[0], 20, TUBO_DER[1], 600),
                               Tortuga(TUBO_DER[0], 20, TUBO_DER[1], 700),
                               Cangrejo(TUBO_IZQ[0], 20, TUBO_IZQ[1], 800),
                               Moneda(TUBO_DER[0], 20, TUBO_DER[1], 900)]
            self.tipo = ['mosca', 'mosca', 'moneda', 'cangrejo', 'moneda',
                         'cangrejo', 'mosca', 'tortuga', 'cangrejo', 'moneda']

        elif ind_nivel == 3:
            self.personajes = [Mosca(TUBO_DER[0], 20, TUBO_DER[1], 0),
                               Cangrejo(TUBO_IZQ[0], 20, TUBO_IZQ[1], 100),
                               Cangrejo(TUBO_IZQ[0], 20, TUBO_IZQ[1], 200),
                               Tortuga(TUBO_DER[0], 20, TUBO_DER[1], 300),
                               Cangrejo(TUBO_DER[0], 20, TUBO_DER[1], 400),
                               Cangrejo(TUBO_IZQ[0], 20, TUBO_IZQ[1], 500),
                               Mosca(TUBO_IZQ[0], 20, TUBO_IZQ[1], 600),
                               Mosca(TUBO_DER[0], 20, TUBO_DER[1], 700),
                               Mosca(TUBO_IZQ[0], 20, TUBO_IZQ[1], 800),
                               Cangrejo(TUBO_DER[0], 20, TUBO_DER[1], 900)]
            self.tipo = ['mosca', 'cangrejo', 'cangrejo', 'tortuga',
                         'cangrejo','cangrejo', 'mosca', 'mosca', 'mosca', 'cangrejo']

    # Recorre la lista de personajes y según el tiempo que llevamos jugando el
    # nivel, si le toca a un personaje aparecer y lo activa
    def activar_personaje(self):
        for i in range(self.num_personajes):
            if (self.tiempo >= self.personajes[i].spawn_time and not
            self.personajes[i].derrotado):
                self.personajes[i].vivo = True

    # Dadas las coordenadas (x, y) y medidas de ancho y alto (w, h) de
    # dos objetos 1 y 2, devuelve cierto si entran en colisión
    def colision(self, x1: int, y1: int, w1: int, h1: int, x2: int,
                 y2: int, w2: int, h2: int):
        return (((x1 <= x2 <= x1+w1) or (x1 <= x2+w2 <= x1+w1)) and ((y1 <= y2
                <= y1+h1) or (y1 <= y2+h2 <= y1+h1)))

    # Recorre la lista de personajes y comprueba para cada uno las funcionalidades correspondientes
    def ejecucion_personajes(self, mario: Mario, floor: Floor, tuberia: Tuberia, pow: Pow, es_techo: list, es_techo_pow: bool, width: int, height: int):
        
        for i in range(self.num_personajes):
            if self.personajes[i].vivo:

                # Comprueba si el personaje está sobre suelo
                es_suelo_personaje = floor.es_suelo(self.personajes[i].x, self.personajes[i].y,
                    self.personajes[i].width, self.personajes[i].sprite[4], pow.x, pow.y, pow.WIDTH)
                
                # Comprueba si el personaje ha colisionado con un tubo de entrada
                es_tubo_entrada = tuberia.es_tubo_entrada(self.personajes[i].x, self.personajes[i].y,
                    self.personajes[i].width, self.personajes[i].dir)

                # Comprueba si el personaje ha colisionado con otro personaje
                for j in range(self.num_personajes):
                    # Me aseguro de que no estoy chocando conmigo mismo y que el otro personaje en j está vivo,
                    # y que ninguno de los dos estuvieramos rotando porque entonces entro en bucle infinito 
                    # rotando con el mismo personaje
                    if (i != j and not self.personajes[i].rotando and not self.personajes[i].volteado 
                        and not self.personajes[j].rotando and self.personajes[j].vivo 
                        and self.colision(self.personajes[i].x, self.personajes[i].y, self.personajes[i].width,
                        self.personajes[i].sprite[4], self.personajes[j].x, self.personajes[j].y, 
                        self.personajes[i].width, self.personajes[i].sprite[4])):

                        self.personajes[i].rotando = True
                        if not self.personajes[j].volteado:
                            self.personajes[j].rotando = True

                # Controla si mario ha chocado con alguno de los enemigos
                if (not mario.respawnear and self.colision(self.personajes[i].x, self.personajes[i].y, self.personajes[i].width, 
                        self.personajes[i].sprite[4], mario.x, mario.y, mario.width_mario, mario.sprite_mario[4]) and
                        self.tipo[i] != 'moneda' and not self.personajes[i].volteado):
                    
                    mario.muriendo = True
                    mario.desactivado = True
                    self.personajes[i].rotando = True

                # Si el enemigo está rotando, activo la función rotar
                if self.personajes[i].rotando:
                    self.personajes[i].rotar()

                # Controla una moneda
                if self.tipo[i] == 'moneda':
                    self.personajes[i].ejecucion_moneda(self.num_derrotados, mario, floor, es_techo, es_techo_pow, es_suelo_personaje, es_tubo_entrada, width)
    
                #Iría aquí el """""" de arriba de controla una moneda

                # Controla un enemigo de tipo tortuga, cangrejo y mosca
                elif self.tipo[i] == 'tortuga' or self.tipo[i] == 'cangrejo' or self.tipo[i] == 'mosca':

                    # Controla el choque y volteo de tortuga y mosca
                    if (self.tipo[i] == 'tortuga' or self.tipo[i] == 'mosca'):
                        # Si recibe un toque por el suelo deformado, o si el pow se activa y está tocando el suelo
                        if ((es_techo[0] and floor.esta_sobre_bloque(es_techo[1], es_techo[2], self.personajes[i].x, self.personajes[i].y, self.personajes[i].width, self.personajes[i].sprite[4]))
                            or (es_techo_pow and floor.retumbando and es_suelo_personaje[0])):
                            # Si ha sido el golpe debido al pow, lo hago saber
                            if (es_techo_pow and floor.retumbando and es_suelo_personaje[0]):
                                self.personajes[i].toque_pow += 1

                            # Si el enemigo no está volteado, se voltea
                            if not self.personajes[i].volteado:
                                self.personajes[i].volteado = True

                            # Debe ser cuando los toques sean superiores a 4 frames para que deje transcurrir
                            # un tiempo y que el primer golpe debido a la deformación del suelo termine
                            # antes de comprobar un segundo choque. Si ha sido por pow no hace falta
                            elif (self.personajes[i].contador_toques < 4 and self.personajes[i].toque_pow < 1):
                                    self.personajes[i].contador_toques += 1
                            
                            # Si estaba ya volteado y volvemos a dar un toque, se levanta inmediatamente
                            else:
                                self.personajes[i].volteado_contador = 158

                    # Controla el choque y volteo del cangrejo
                    elif self.tipo[i] == 'cangrejo':
                        self.personajes[i].choque_cangrejo(es_techo, es_techo_pow, es_suelo_personaje, floor)

                    # Si ya está dada la vuelta y mario colisiona con ella, pues sale volando y muere (igual para los tres enemigos)
                    if (self.colision(mario.x, mario.y, mario.width_mario, mario.sprite_mario[4], self.personajes[i].x, self.personajes[i].y, self.personajes[i].width, self.personajes[i].sprite[4])
                            and self.personajes[i].volteado and not self.personajes[i].mata_enemigo):
                        self.personajes[i].mata_enemigo = True
                        # Mando la posición desde la cual el enemigo muere
                        self.personajes[i].posicion_muerte = (self.personajes[i].x, self.personajes[i].y)
                        mario.update_puntos()

                    # Si consigo voltear al enemigo, ejecuto la animación donde está volteando el enemigo
                    elif self.personajes[i].volteado:
                        self.personajes[i].voltear()

                    # Controla que se levante otra vez la tortuga y su movimiento por la pantalla
                    if self.tipo[i] == 'tortuga':
                        # Si no se le ha rematado y no está volteado, le permito moverse
                        if not self.personajes[i].mata_enemigo and not self.personajes[i].volteado:
                            self.personajes[i].mover(width)
                            self.personajes[i].update_y(es_suelo_personaje)

                    # Controla que se levante otra vez el cangrejo
                    elif self.tipo[i] == 'cangrejo':
                        # Si no está en proceso de animación enfadado, y no se le ha rematado y no está volteado, le permito moverse
                        if (not self.personajes[i].mata_enemigo and not self.personajes[i].volteado 
                            and not self.personajes[i].enfadandose):
                            self.personajes[i].mover(width)
                            self.personajes[i].update_y(es_suelo_personaje)

                    # Controla que se levante otra vez la mosca
                    elif self.tipo[i] == 'mosca':
                        # Si no se le ha rematado y no está volteado, le permito moverse
                        if not self.personajes[i].mata_enemigo and not self.personajes[i].volteado:
                            self.personajes[i].mover(width, es_suelo_personaje)
                            # Si no está saltando, activo la función de bajar de piso por la gravedad
                            if not self.personajes[i].saltando:
                                self.personajes[i].update_y(es_suelo_personaje)

                    # Se inicia la animación de matar al enemigo
                    if self.personajes[i].mata_enemigo:
                        self.personajes[i].muere(width, height, mario.dir)

                    # Si ha llegado a un tubo de entrada, lo vuelvo a spawnear desde un tubo superior
                    if (es_tubo_entrada[0] and not self.personajes[i].derrotado 
                        and not self.personajes[i].mata_enemigo):
                        self.personajes[i].entrar_tubo(es_tubo_entrada[1], es_tubo_entrada[2], es_tubo_entrada[3])
    
    # Dibujo los personajes activos del nivel
    def draw_lvlchars(self):
        for i in range(self.num_personajes):
            if self.personajes[i].vivo:

                # Gestiona toda la animación de la moneda
                if self.tipo[i] == 'moneda':
                    # Dibuja la moneda
                    self.personajes[i].draw_coin()

                # Dibuja al enemigo que no sea una moneda
                else:
                    pyxel.blt(self.personajes[i].x, self.personajes[i].y, self.personajes[i].sprite[0], self.personajes[i].sprite[1], 
                                self.personajes[i].sprite[2], self.personajes[i].sprite[3], self.personajes[i].sprite[4], colkey=8)
                    # Gestiona la animación de la puntuación cuando un enemigo es derrotado
                    if self.personajes[i].mata_enemigo:
                        # Si mario mata al enemigo, dibujo los efectos especiales de la puntuación
                        if self.personajes[i].puntos_contador * 2 <= 8:
                            pyxel.text(self.personajes[i].posicion_muerte[0], self.personajes[i].posicion_muerte[1]
                                        - self.personajes[i].puntos_contador * 2, "800", 11)
                        else:
                            pyxel.text(self.personajes[i].posicion_muerte[0], self.personajes[i].posicion_muerte[1] - 8, "800", 11)
                            self.personajes[i].derrotado = True
                        self.personajes[i].puntos_contador += 1