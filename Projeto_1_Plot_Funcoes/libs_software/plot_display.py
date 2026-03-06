from libs_software.config import *
from libs_software.funcoes_matematicas import FUNCOES, calcular_vertice_delta


class PlotDisplay:
    """Gerencia todas as telas do display OLED."""

    def __init__(self, display):
        self.display = display

    #TELA 1: MENU 
    def desenhar_menu(self, funcao_selecionada):
        self.display.limpar()
        self.display.texto("SELECIONE:", 0, 0)
        for i in range(TOTAL_FUNCOES): #para todas as funçoes
            y = 16 + i * 12
            if i == funcao_selecionada:
                self.display.texto(">", 4, y)
                self.display.texto(NOMES_FUNCOES[i], 16, y)
            else:
                self.display.texto(NOMES_FUNCOES[i], 12, y)
        self.display.atualizar() #atualiza display

    #TELA 2: CONFIGURAR PARAMETROS
    def desenhar_configuracao(self, indice_param, parametros):
        self.display.limpar()
        nomes = ["A", "B", "C", "D"]

        self.display.texto("CONFIGURAR {}:".format(nomes[indice_param]), 0, 0)
        self.display.texto("Valor: {:.1f}".format(parametros[indice_param]), 0, 16)
        self.display.texto("A:{:.1f} B:{:.1f}".format(parametros[0], parametros[1]), 0, 30)
        self.display.texto("C:{:.1f} D:{:.1f}".format(parametros[2], parametros[3]), 0, 40)
        self.display.texto("BTN: Confirmar", 0, 54)
        self.display.atualizar()

    # TELA 3: PLOT GRAFICO 
    def desenhar_grafico(self, funcao_tipo, parametros, nivel_zoom, pos_central_x):
        self.display.limpar()
        centro_x = 64
        centro_y = 32
        escala_x = nivel_zoom
        escala_y = 0.5 * nivel_zoom
        # Eixos
        self.display.linha_v(centro_x, 0, 63)
        self.display.linha_h(0, 127, centro_y)
        # Marcadores nos eixos
        esp = 5
        for i in range(-30, 31, esp):
            # Eixo X
            x_pos = centro_x + int((i - pos_central_x) * escala_x)
            if 0 <= x_pos < 128:
                self.display.linha_v(x_pos, centro_y - 2, centro_y + 2)
                if i != 0 and ((abs(i) <= 10 and i % 5 == 0) or (abs(i) > 10 and i % 10 == 0)):
                    self.display.texto(str(i), x_pos - 4, centro_y + 4)
            # Eixo Y
            y_pos = centro_y - int(i * escala_y)
            if 0 <= y_pos < 64:
                self.display.linha_h(centro_x - 2, centro_x + 2, y_pos)
                if i != 0 and ((abs(i) <= 10 and i % 5 == 0) or (abs(i) > 10 and i % 10 == 0)):
                    self.display.texto(str(i), centro_x + 4, y_pos - 2)
        # Plotar a funcao
        func = FUNCOES[funcao_tipo]
        ultimo_y = -1

        for px in range(128):
            x_val = (px - centro_x) / escala_x + pos_central_x
            try:
                y_val = func(x_val, parametros)
            except (ValueError, ZeroDivisionError):
                ultimo_y = -1
                continue

            y_pos = centro_y - int(y_val * escala_y)

            if 0 <= y_pos < 64:
                self.display.pixel(px, y_pos)
                # Conectar pontos para curva suave
                if ultimo_y != -1 and abs(y_pos - ultimo_y) > 1:
                    inicio = min(ultimo_y, y_pos)
                    fim = max(ultimo_y, y_pos)
                    for y in range(inicio, fim + 1):
                        if 0 <= y < 64:
                            self.display.pixel(px - 1, y)
                ultimo_y = y_pos
            else:
                ultimo_y = -1
        # Info zoom
        self.display.texto("Zoom:{:.1f}x".format(nivel_zoom), 0, 55)
        self.display.atualizar()

    # TELA 4: VALORES QUADRATICA 
    def desenhar_valores_quadratica(self, parametros):
        self.display.limpar()
        xv, yv, delta = calcular_vertice_delta(parametros) #calcula vlaores vertice
        self.display.texto("VALORES QUADRATICA", 0, 0)
        self.display.texto("Xv: {:.2f}".format(xv), 0, 16)
        self.display.texto("Yv: {:.2f}".format(yv), 0, 28)
        self.display.texto("Delta: {:.2f}".format(delta), 0, 40)
        self.display.texto("BTN C: Voltar", 0, 54)
        self.display.atualizar()
