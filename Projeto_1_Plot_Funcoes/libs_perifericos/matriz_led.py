from machine import Pin
import neopixel


NUM_PIXELS = 25

SETA_CIMA = [
    0, 0, 1, 0, 0,
    0, 1, 1, 1, 0,
    1, 0, 1, 0, 1,
    0, 0, 1, 0, 0,
    0, 0, 1, 0, 0,
]

SETA_BAIXO = [
    0, 0, 1, 0, 0,
    0, 0, 1, 0, 0,
    1, 0, 1, 0, 1,
    0, 1, 1, 1, 0,
    0, 0, 1, 0, 0,
]


class MatrizLED:
    def __init__(self, pino=7, num_pixels=NUM_PIXELS):
        self.np = neopixel.NeoPixel(Pin(pino), num_pixels)
        self.num_pixels = num_pixels

    def mostrar_seta(self, direcao_cima):
        padrao = SETA_BAIXO if direcao_cima else SETA_CIMA
        cor = (0, 50, 0)
        for i in range(self.num_pixels):
            self.np[i] = cor if padrao[i] else (0, 0, 0)
        self.np.write()

    def desligar(self):
        for i in range(self.num_pixels):
            self.np[i] = (0, 0, 0)
        self.np.write()
