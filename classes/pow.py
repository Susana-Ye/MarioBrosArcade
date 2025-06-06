import pyxel
class Pow:

    def __init__(self, w: int, h: int):
        # Constantes
        self.WIDTH = 16
        self.x = w // 2 - 8
        self.y = h // 4 * 3 - 9
        self.SPRITE_NORMAL = (0, 0, 216, 16, 16)
        self.SPRITE_DEFORMADO = (0, 16, 216, 16, 13)
        self.SPRITE_APLASTADO = (0, 32, 216, 16, 9)

        self.estado = 'normal'
        self.sprite = (0, 0, 216, 16, 16)

    # Permite saber si mario ha chocado con el pow por debajo
    def es_techo_pow(self, x: int, y: int, width_mario: int):
        return ((self.x <= x <= self.x + self.WIDTH or self.x <= x + width_mario <= self.x + self.WIDTH) and
                (self.y <= y <= self.y + self.sprite[4]))

    def deformar(self):
        if self.estado.lower() == 'normal':
            self.estado = 'deformado'
            self.sprite = self.SPRITE_DEFORMADO
        elif self.estado.lower() == 'deformado':
            self.estado = 'aplastado'
            self.sprite = self.SPRITE_APLASTADO
        elif self.estado.lower() == 'aplastado':
            self.estado = 'agotado'
            self.x = - self.WIDTH
            self.y = - self.WIDTH
    
    def draw_pow(self):
        pyxel.blt(self.x, self.y, self.sprite[0], self.sprite[1], self.sprite[2], self.sprite[3], self.sprite[4], colkey=8)