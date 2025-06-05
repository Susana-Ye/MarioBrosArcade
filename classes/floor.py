class Floor:
    """ Esta clase controla el suelo, se conforma de 7
    plataformas empezando a contar de izquierda a derecha y arriba para abajo
    desde 0 a 6; y un suelo de ladrillos"""

    def __init__(self, w: int, h: int):
        """
        @Constantes
        NUM_CACHOS_FLOOR: tupla que guarda el número de cachos que tiene
            cada plataforma, ej. la plataforma 0 tiene 5 cachos
        X_FLOOR: tupla que guarda la posición x de cada plataforma,
            ej. la plataforma 0 está en la posición x=0
        Y_FLOOR: tupla que guarda la posición y de cada plataforma,
            ej. la plataforma 0 comienza a la altura y = h//4

        (Se diferencia además entre el azul y el amarillo
        @atributo SPRITE_CACHO_NORMAL:(banco 1, posición y tamaño 24x8)
        @atributo SPRITE_CACHO_DEFORMADO: (banco 1, posición y tamaño 24x15)
        @atributo plataforma: lista que contiene un diccionario con la
        información correspondiente a cada plataforma, esta es:
            x: la posición x donde comienza la plataforma
            y: la posición y donde comienza la plataforma
            num_cacho: entero que indica el número de cachos de suelo
                que conforma esa plataforma
            lista_cachos: lista que guarda la info del sprite de cada cacho de
                la plataforma, se asignan las posiciones de izquierda a derecha.
                La info guardada es: las posiciones x, y del cacho; tupla con el
                sprite del cacho y un booleano de si está deformado o no
        """
        NUM_CACHOS_FLOOR = (5, 5, 5, 2, 2, 5, 5)
        X_FLOOR = (0, w - 120, w // 2 - 60, 0, w - 48, -8, w - 112)
        self.Y_FLOOR = (h // 4+1, h // 4+1, h // 2 - 6, h // 2+2, h // 2+2,
                   h // 4 * 3 - 9, h // 4 * 3 - 9)
        self.Y_FLOOR_LADRILLOS = h - 16
        self.WIDTH_CACHO = 24
        self.HEIGHT_CACHO_NORMAL = 8
        self.SPRITE_CACHO_DEFORMADO_AZUL = (1, 28, 0, 24, 15)
        self.SPRITE_CACHO_NORMAL_AZUL = (1, 0, 0, 24, 8)
        self.SPRITE_CACHO_DEFORMADO_AMARILLO = (1, 28, 16, 24, 15)
        self.SPRITE_CACHO_NORMAL_AMARILLO = (1, 0, 16, 24, 8)
        self.cambio_color_floor = False
        self.retumbar_contador = 0
        self.retumbando = False
        self.plataforma = []


        for i in range(7):
            plataforma = {"x": X_FLOOR[i], "y": self.Y_FLOOR[i],
                          "num_cachos": NUM_CACHOS_FLOOR[i]}
            lista_cachos = []
            for j in range(NUM_CACHOS_FLOOR[i]):
                cacho = [X_FLOOR[i] + j * 24, self.Y_FLOOR[i],
                         self.SPRITE_CACHO_NORMAL_AZUL,
                         False]
                lista_cachos.append(cacho)
            plataforma["lista_cachos"] = lista_cachos
            self.plataforma.append(plataforma)

    # Comprueba para los demás personajes (sin mario) si están sobre el
    # suelo o no
    def es_suelo(self, x: int, y: int, width, height, x_pow: int, y_pow: int, width_pow:
                        int):
        es_suelo = False
        i = 0
        while i < 7 and not es_suelo:
            if ((self.plataforma[i]["x"] <= x <= self.plataforma[i][
                "x"] + (self.plataforma[i][
                            "num_cachos"] * self.WIDTH_CACHO) or
                 (self.plataforma[i]["x"] <= x + width <=
                  self.plataforma[i]["x"] + (
                          self.plataforma[i]["num_cachos"]
                          * self.WIDTH_CACHO))) and (
                    self.plataforma[i]["y"] <= y <=
                    self.plataforma[i]["y"] + self.HEIGHT_CACHO_NORMAL or
                    self.plataforma[i]["y"] <= y + height <=
                    self.plataforma[i]["y"] + self.HEIGHT_CACHO_NORMAL)):
                es_suelo = True
            i += 1
        y_suelo = self.plataforma[i - 1]["y"]

        if y + height >= self.Y_FLOOR_LADRILLOS:
            es_suelo = True
            y_suelo = self.Y_FLOOR_LADRILLOS

        # Permite saber si mario se ha subido al bloque pow
        if (((x_pow < x < x_pow + width_pow) or (x_pow < x +
            width < x_pow + width_pow)) and y_pow - 2 < y + height < y_pow +
                2):
            es_suelo = True
            y_suelo = y_pow

        return es_suelo, y_suelo

    # Dada la posición y tamaño de Mario, me dice si ha colisionado
    # con el suelo o no.
    def es_suelo_mario(self, x_mario: int, y_mario: int, width_mario: int,
                       height_mario: int, x_pow: int, y_pow: int, width_pow:
                        int):
        es_suelo = False
        i = 0
        while i < 7 and not es_suelo:
            if ((self.plataforma[i]["x"] < x_mario < self.plataforma[i][
                "x"] + (self.plataforma[i][
                            "num_cachos"] * self.WIDTH_CACHO) or
                 (self.plataforma[i]["x"] < x_mario + width_mario <
                  self.plataforma[i]["x"] + (
                          self.plataforma[i]["num_cachos"]
                          * self.WIDTH_CACHO))) and
                    self.plataforma[i]["y"] - 2 < y_mario + height_mario <
                    self.plataforma[i]["y"] + 2):
                es_suelo = True
            i += 1

        if y_mario + 21 >= self.Y_FLOOR_LADRILLOS:
            es_suelo = True

        # Permite saber si mario se ha subido al bloque pow
        if  (((x_pow < x_mario < x_pow + width_pow) or (x_pow < x_mario +
            width_mario < x_pow + width_pow)) and y_pow - 2 < y_mario +
                height_mario < y_pow + 2):
            es_suelo = True

        return es_suelo

    # Dada la posición x e y de Mario, si coincide con la parte baja de
    # alguna plataforma, devuelve: true; el índice de la plataforma y el cacho
    # correspondiente; y la altura a la que debe dejar de saltar mario
    def es_techo(self, x: int, y: int, width_mario: int):
        es_techo = False
        i = 0
        j = 0
        while i < 7 and not es_techo:
            j = 0
            while j < self.plataforma[i]["num_cachos"] and not es_techo:
                if ((self.plataforma[i]["lista_cachos"][j][0] <= x + 2 <
                     self.plataforma[i]["lista_cachos"][j][0] +
                     self.plataforma[i]["lista_cachos"][j][2][3] or
                     self.plataforma[i]["lista_cachos"][j][0] <= x +
                     width_mario - 2 < self.plataforma[i]["lista_cachos"][
                         j][0] + self.plataforma[i]["lista_cachos"][j][2][3])
                        and (y <= self.plataforma[i]["y"] + self.plataforma[
                            i]["lista_cachos"][j][2][4]
                             and not (y <= self.plataforma[i]["y"]))):
                    es_techo = True
                j += 1
            i += 1

        return es_techo, i - 1, j - 1

    # Según el x, y recibidos, el índice de la plataforma y el índice del
    # cacho, lo deforma
    def deformar(self, ind_plat: int, ind_cacho: int):
        self.plataforma[ind_plat]["lista_cachos"][ind_cacho][3] = True
        if self.cambio_color_floor:
            self.plataforma[ind_plat]["lista_cachos"][ind_cacho][2] = (
                self.SPRITE_CACHO_DEFORMADO_AMARILLO)
        else:
            self.plataforma[ind_plat]["lista_cachos"][ind_cacho][2] = (
            self.SPRITE_CACHO_DEFORMADO_AZUL)

    # Actualiza los sprites de las plataformas a la versión donde no están
    # deformadas
    def normalizar(self):
        for i in range(7):
            for j in range(self.plataforma[i]["num_cachos"]):
                # Actualizo el sprite de la plataforma la normal
                if self.cambio_color_floor:
                    self.plataforma[i]["lista_cachos"][j][
                        2] = self.SPRITE_CACHO_NORMAL_AMARILLO
                else:
                    self.plataforma[i]["lista_cachos"][j][2] = (
                        self.SPRITE_CACHO_NORMAL_AZUL)
                self.plataforma[i]["lista_cachos"][j][3] = False

    # Hago una animación donde todas las plataformas se elevan unos píxeles
    # y vuelven después a su estado original
    def retumbar(self):
        if self.retumbar_contador < 3:
            for i in range(7):
                for j in range(self.plataforma[i]["num_cachos"]):
                    self.plataforma[i]["lista_cachos"][j][1] -= 2
            self.retumbar_contador += 1
        else:
            for i in range(7):
                for j in range(self.plataforma[i]["num_cachos"]):
                    self.plataforma[i]["lista_cachos"][j][1] += 6
            self.retumbar_contador = 0
            self.retumbando = False
