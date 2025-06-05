from classes.tortuga import Tortuga
from classes.cangrejo import Cangrejo
from classes.mosca import Mosca
from classes.moneda import Moneda

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
class Nivel:

    def __init__(self, w: int, h: int, ind_nivel: int):
        """
        @atributo personajes: lista de los personajes que van a salir en el 
        nivel
        """
        LISTA_NUM_PERSONAJES = [10, 10, 10, 10]
        TUBO_IZQ = (38, True)
        TUBO_DER = (248, False)

        # Indica el número de personajes que hay en ese nivel
        self.num_personajes = LISTA_NUM_PERSONAJES[ind_nivel]
        self.num_derrotados = 0
        # Sirve para controlar el tiempo del nivel, saber cuánto tiempo
        # lleva desde que ha empezado el nivel
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
                               Tortuga(TUBO_DER[0], 20, TUBO_DER[1], 900), ]
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
                               Moneda(TUBO_DER[0], 20, TUBO_DER[1], 900), ]
            self.tipo = ['mosca', 'mosca', 'moneda', 'cangrejo', 'moneda',
                         'cangrejo', 'mosca', 'tortuga', 'cangrejo',
                         'moneda']

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
                               Cangrejo(TUBO_DER[0], 20, TUBO_DER[1], 900), ]
            self.tipo = ['mosca', 'cangrejo', 'cangrejo', 'tortuga',
                         'cangrejo','cangrejo', 'mosca', 'mosca', 'mosca',
                         'cangrejo']

    # Recorre la lista de personajes y según el tiempo que llevamos jugando el
    # nivel, si le toca a un personaje aparecer y lo activa
    def activar_personaje(self):
        for i in range(self.num_personajes):
            if (self.tiempo >= self.personajes[i].spawn_time and not
            self.personajes[i].derrotado):
                self.personajes[i].vivo = True
