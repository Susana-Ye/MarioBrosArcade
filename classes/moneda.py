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


