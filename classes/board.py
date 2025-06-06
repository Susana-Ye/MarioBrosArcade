from classes.mario import Mario
from classes.floor import Floor
from classes.tuberia import Tuberia
from classes.nivel import ListaNiveles
from classes.pow import Pow
import pyxel

class Board:
    """ Esta clase contiene toda la información para representar el tablero y realiza el proceso del juego"""

    def __init__(self, w: int, h: int):
        """
        @atributo width: guarda la anchura del tablero
        @atributo height: guarda la altura del tablero
        @atributo mario: creo un Mario en la mitad de la pantalla sobre el suelo de ladrillos mirando a la derecha
        @atributo floor: constituye todas las plataformas a las que puede saltar mario
        @atributo tuberia: constituye las tuberías desde las que entran y salen enemigos
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

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        else:
            # Si la partida no está terminada o en un proceso de cambio de nivel, ejecuto la partida
            if not self.game_over and not self.ganado and not self.partida.cambio_nivel:
                # Facilito la sintaxis asignando a una variable el índice de la partida que se está jugando
                index = self.partida.ind_nivel

                # Compruebo si es hora de spawnear algún personaje
                self.partida.niveles[index].activar_personaje()

                # Compruebo el estado de mario
                es_suelo = self.floor.es_suelo_mario(self.mario.x, self.mario.y, self.mario.width_mario,
                                            self.mario.sprite_mario[4], self.pow.x, self.pow.y, self.pow.WIDTH)
                es_techo = self.floor.es_techo(self.mario.x, self.mario.y, self.mario.width_mario)
                es_techo_pow = self.pow.es_techo_pow(self.mario.x, self.mario.y, self.mario.width_mario)

                # Control de ejecución de mario
                self.mario.ejecucion_mario(es_suelo, es_techo, es_techo_pow, self.floor, self.pow, self.width, self.height)
                
                # Control de todos los personajes activos de ese nivel
                self.partida.niveles[index].ejecucion_personajes(self.mario, self.floor, self.tuberia, self.pow, es_techo, es_techo_pow, self.width, self.height)

                # Sirve para poner el sprite de la plataforma otra vez normal
                if not es_techo[0]:
                    self.floor.normalizar()

                # Sirve para retumbar las plataformas si mario choca con pow
                if self.floor.retumbando:
                    self.floor.retumbar()

            # Comprueba si he ganado. Termina la partida cuando he superado todos los niveles
            if self.partida.ind_nivel + 1 > self.NUM_NIVELES:
                self.ganado = True

            # Comprueba si he perdido. Termina la partida cuando Mario pierde
            # todas sus vidas, las cuales no se recuperan una vez se pasa de nivel
            if self.mario.vidas == 0:
                self.game_over = True

            # Control cambio de nivel
            self.partida.control_cambio_nivel(self.ganado, self.game_over, self.mario, self.floor, self.width, self.height)
            
    def draw(self):

        pyxel.cls(0)

        # Dibuja el suelo de ladrillos
        pyxel.bltm(0, self.height - 16, 0, 0, 0, self.width, 16, colkey=2)

        # Dibuja las plataformas
        self.floor.draw_floor()

        # Dibuja las tuberías
        self.tuberia.draw_tuberia()

        # Dibuja el bloque Pow
        self.pow.draw_pow()

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
            pyxel.text(self.width // 4- 4, self.height // 3 + 6, "CONGRATULATIONS! YOU HAVE WON THE GAME!", 7)

        # Estoy cambiando de nivel
        elif self.partida.cambio_nivel:
            pyxel.text((self.width // 3) + self.partida.contador_cambio_nivel, self.height // 3 + 6, "FASE %i" % (self.partida.ind_nivel + 1), 7)

        # Si estoy jugando (no he perdido, no he ganado, no estoy en un cambio de nivel), dibujo a los personajes que estén vivos
        else:

            # Dibujo en el extremo inferior el número de la fase que estoy jugando
            pyxel.text(3, self.height - 50, "FASE %i" % (self.partida.ind_nivel + 1), 7)

            # Dibujo todos los personajes activos de ese nivel
            self.partida.niveles[self.partida.ind_nivel].draw_lvlchars()

            # Dibuja las tuberías encima, con los respectivos cachos para que parezca que los enemigos aparecen detrás
            for i in range(4):
                pyxel.bltm(self.tuberia.sprite[i][0], self.tuberia.sprite[i][1], self.tuberia.sprite[i][2],
                           self.tuberia.sprite[i][3], self.tuberia.sprite[i][4], self.tuberia.sprite[i][5],
                           self.tuberia.sprite[i][6], colkey=2)

            # Dibuja el bloque donde mario reaparece tras morir
            if self.mario.respawnear:
                pyxel.blt(self.mario.x_bloque, self.mario.y_bloque, self.mario.sprite_bloque[0], self.mario.sprite_bloque[1],
                  self.mario.sprite_bloque[2], self.mario.sprite_bloque[3], self.mario.sprite_bloque[4], colkey=8)

            # Dibuja a Mario
            pyxel.blt(self.mario.x, self.mario.y, self.mario.sprite_mario[0], self.mario.sprite_mario[1], self.mario.sprite_mario[2],
                      self.mario.sprite_mario[3], self.mario.sprite_mario[4], colkey=8)

            self.partida.niveles[self.partida.ind_nivel].tiempo += 1