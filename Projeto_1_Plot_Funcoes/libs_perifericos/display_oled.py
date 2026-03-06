from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


# Fonte 3x5 pixels para dígitos 0-9 e sinal de menos
# Cada caractere é uma lista de 5 linhas (top→bottom), cada linha é 3 bits (MSB=esquerda)
FONTE_3X5 = {
    '0': [0b111, 0b101, 0b101, 0b101, 0b111],
    '1': [0b010, 0b110, 0b010, 0b010, 0b111],
    '2': [0b111, 0b001, 0b111, 0b100, 0b111],
    '3': [0b111, 0b001, 0b111, 0b001, 0b111],
    '4': [0b101, 0b101, 0b111, 0b001, 0b001],
    '5': [0b111, 0b100, 0b111, 0b001, 0b111],
    '6': [0b111, 0b100, 0b111, 0b101, 0b111],
    '7': [0b111, 0b001, 0b001, 0b001, 0b001],
    '8': [0b111, 0b101, 0b111, 0b101, 0b111],
    '9': [0b111, 0b101, 0b111, 0b001, 0b111],
    '-': [0b000, 0b000, 0b111, 0b000, 0b000],
    '.': [0b000, 0b000, 0b000, 0b000, 0b010],
    ':': [0b000, 0b010, 0b000, 0b010, 0b000],
    'x': [0b000, 0b101, 0b010, 0b101, 0b000],
    'Z': [0b111, 0b001, 0b010, 0b100, 0b111],
    'o': [0b000, 0b010, 0b101, 0b101, 0b010],
    'm': [0b000, 0b111, 0b111, 0b101, 0b101],
}


class DisplayOLED:
    """Wrapper para o display OLED SSD1306 128x64 via I2C."""
    #tamanho do displayy
    LARGURA = 128 
    ALTURA = 64
    def __init__(self, sda_pin, scl_pin, i2c_id=1, addr=0x3C): #configs de inciação do display
        self.i2c = I2C(i2c_id, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.display = SSD1306_I2C(self.LARGURA, self.ALTURA, self.i2c, addr=addr)

    def limpar(self): #limpa o displayy
        self.display.fill(0)

    def atualizar(self): #atualiza display
        self.display.show()

    def pixel(self, x, y, cor=1): #desenha pixel no display, verificando se coordenadas estão dentro dos limites
        if 0 <= x < self.LARGURA and 0 <= y < self.ALTURA:
            self.display.pixel(x, y, cor)

    def texto(self, string, x, y, cor=1): #para por texto no dispaly
        self.display.text(string, x, y, cor)

    def texto_mini(self, string, x, y, cor=1):
        """Desenha texto com fonte 3x5 pixels (só números e '-'). Cada caractere ocupa 4px de largura (3+1 espaço)."""
        for char in str(string):
            glifo = FONTE_3X5.get(char)
            if glifo:
                for linha_idx in range(5):
                    bits = glifo[linha_idx]
                    for col in range(3):
                        if bits & (0b100 >> col):
                            self.pixel(x + col, y + linha_idx, cor)
            x += 4  # avança 3px do caractere + 1px de espaço

    def linha_h(self, x0, x1, y, cor=1): #desenha linha horizontal, verificando se coordenadas estão dentro dos limites
        for x in range(x0, x1 + 1):
            self.pixel(x, y, cor)

    def linha_v(self, x, y0, y1, cor=1):    #desenha linha vertical, verificando se coordenadas estão dentro dos limites
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


