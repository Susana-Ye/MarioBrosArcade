import pyxel
class Tuberia:
    def __init__(self, w: int, h: int):
        """
        @Constantes
        TUBO_X: tupla que almacena la información correspondiente al sprite de cada tubería (x, y, banco, u, v, w, h, tipo de tubo)

        @atributo sprite: Lista que guarda la información de las 4 tuberías
        """
        TUBO_0 = (0, h // 4 - 36, 0, 68, 80, 64, 36, 'spawn_enemigo_izq')
        TUBO_1 = (w - 44, h // 4 - 36, 0, 64, 32, 64, 36,'spawn_enemigo_der')
        TUBO_2 = (0, h - 40, 0, 0, 88, 32, 24, 'entrada_izq')
        TUBO_3 = (w - 32, h - 40, 0, 0, 64, 32, 24, 'entrada_der')
        TUBO_0_CACHO = (0, h // 4 - 36, 0, 68, 80, 64, 20)
        TUBO_1_CACHO = (w - 44, h // 4 - 36, 0, 64, 32, 64, 20)

        self.sprite_fondo = [TUBO_0, TUBO_1]
        self.sprite = [TUBO_0_CACHO, TUBO_1_CACHO, TUBO_2, TUBO_3]

    # Función que mira si hay colisión entre el personaje y el tubo
    def es_tubo_entrada(self, x_ene: int, y_ene: int, w_ene: int, dir_ene: bool):
        es_tubo_entrada = False
        x_tubo = 0
        y_tubo = 0
        tubo = 'none'
        # Si el enemigo está moviéndose hacia la derecha
        if dir_ene and ((self.sprite[3][0] <= x_ene + w_ene <= self.sprite[3][0] + self.sprite[3][5]) 
                        and (self.sprite[3][1] <= y_ene <= self.sprite[3][1] + self.sprite[3][6])):
            es_tubo_entrada = True
            x_tubo = self.sprite[3][0]
            y_tubo = self.sprite[3][1]
            tubo = 'right'
        # Si el enemigo está moviéndose hacia la izquierda
        elif not dir_ene and ((self.sprite[2][0] <= x_ene <= self.sprite[2][0] + self.sprite[2][5]) 
                        and (self.sprite[2][1] <= y_ene <= self.sprite[2][1] + self.sprite[2][6])):
            es_tubo_entrada = True
            x_tubo = self.sprite[2][0] + self.sprite[2][5]
            y_tubo = self.sprite[2][1]
            tubo = 'left'

        return es_tubo_entrada, x_tubo, y_tubo, tubo

    def draw_tuberia(self):
        # Dibuja la parte del fondo de las tuberías
        for i in range(2):
            pyxel.bltm(self.sprite_fondo[i][0], self.sprite_fondo[i][1], self.sprite_fondo[i][2], self.sprite_fondo[i][3],
                       self.sprite_fondo[i][4], self.sprite_fondo[i][5], self.sprite_fondo[i][6], colkey=2)

        # Dibuja las tuberías encima, con los respectivos cachos, etc.
        for i in range(4):
            pyxel.bltm(self.sprite[i][0], self.sprite[i][1], self.sprite[i][2], self.sprite[i][3], self.sprite[i][4], 
                        self.sprite[i][5], self.sprite[i][6], colkey=2)