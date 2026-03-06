from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import math


class DisplayOLED:
    """Wrapper para o display OLED SSD1306 128x64 via I2C."""

    LARGURA = 128
    ALTURA = 64

    def __init__(self, sda_pin, scl_pin, i2c_id=1, addr=0x3C):
        self.i2c = I2C(i2c_id, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.display = SSD1306_I2C(self.LARGURA, self.ALTURA, self.i2c, addr=addr)

    def limpar(self):
        self.display.fill(0)

    def atualizar(self):
        self.display.show()

    def pixel(self, x, y, cor=1):
        if 0 <= x < self.LARGURA and 0 <= y < self.ALTURA:
            self.display.pixel(x, y, cor)

    def texto(self, string, x, y, cor=1):
        self.display.text(string, x, y, cor)

    def linha_h(self, x0, x1, y, cor=1):
        for x in range(x0, x1 + 1):
            self.pixel(x, y, cor)

    def linha_v(self, x, y0, y1, cor=1):
        for y in range(y0, y1 + 1):
            self.pixel(x, y, cor)

    def linha(self, x0, y0, x1, y1, cor=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.pixel(x0, y0, cor)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def retangulo(self, x, y, w, h, cor=1, preencher=False):
        if preencher:
            for j in range(y, y + h):
                self.linha_h(x, x + w - 1, j, cor)
        else:
            self.linha_h(x, x + w - 1, y, cor)
            self.linha_h(x, x + w - 1, y + h - 1, cor)
            self.linha_v(x, y, y + h - 1, cor)
            self.linha_v(x + w - 1, y, y + h - 1, cor)
