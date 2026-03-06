from machine import Pin, ADC, PWM
import time
from libs_software.config import *
from libs_perifericos.display_oled import DisplayOLED
from libs_perifericos.matriz_led import MatrizLED
from libs_perifericos.buzzer import Buzzer
from libs_software.plot_display import PlotDisplay

#Estado global do sistema
estado_atual = ESTADO_MENU #armazena o estaod do menu
funcao_selecionada = FUNCAO_AFIM #a funcao a ser selecionado começando pela afim
parametros = [0.0, 0.0, 0.0, 0.0]
indice_parametro = 0
nivel_zoom = 1.0 #nivel de zoom incial
pos_central_x = 0.0
ultimo_botao_ms = 0 #tempo preciso para o debounce dos botoes

#Inicializacao de perifericos 
display = DisplayOLED(I2C_SDA, I2C_SCL, I2C_ID, OLED_ADDR)
matriz = MatrizLED(PINO_WS2812)
buzzer = Buzzer(PINO_BUZZER)
plot = PlotDisplay(display)
adc_y = ADC(Pin(PINO_JOYSTICK_Y)) #joystick
pwm_r = PWM(Pin(PINO_RGB_VERMELHO)) #pwm nos leds
pwm_g = PWM(Pin(PINO_RGB_VERDE))
pwm_b = PWM(Pin(PINO_RGB_AZUL))
for p in (pwm_r, pwm_g, pwm_b):
    p.freq(1000)
# Botoes com pull-up
btn_c = Pin(PINO_BOTAO_C, Pin.IN, Pin.PULL_UP)
btn_a = Pin(PINO_BOTAO_A, Pin.IN, Pin.PULL_UP)
btn_b = Pin(PINO_BOTAO_B, Pin.IN, Pin.PULL_UP)

# ---- Funcoes de controle RGB ----
def definir_rgb(r, g, b):
    pwm_r.duty_u16(r * 257)  # 0-255 -> 0-65535
    pwm_g.duty_u16(g * 257)
    pwm_b.duty_u16(b * 257)

def atualizar_cores_rgb():
    cor = CORES_FUNCAO[funcao_selecionada]
    definir_rgb(*cor)

def atualizar_brilho_zoom():
    cor = CORES_FUNCAO[funcao_selecionada]
    fator = min(nivel_zoom / 10.0, 1.0)
    definir_rgb(int(cor[0] * fator), int(cor[1] * fator), int(cor[2] * fator))

#Debounce     
def debounce_ok():
    global ultimo_botao_ms
    agora = time.ticks_ms()
    if time.ticks_diff(agora, ultimo_botao_ms) < ATRASO_DEBOUNCE_MS:
        return False
    ultimo_botao_ms = agora
    return True

#Callbacks dos botoes (IRQ)
def on_botao_c(pin):
    """Botao C (GPIO 10) - Seleciona / Confirma / Volta."""
    global estado_atual, indice_parametro, parametros, nivel_zoom, pos_central_x
    if not debounce_ok():  #ignora se pressionado muito rapido (debounce)
        return
    buzzer.bip_confirma() #feedback sonoro duplo ao pressionar
    if estado_atual == ESTADO_MENU:
        #no menu: confirma a funcao selecionada e vai para configurar parametros
        estado_atual = ESTADO_CONFIGURAR_PARAMETROS
        indice_parametro = 0 #começa pelo parametro A
        parametros = [0.0, 0.0, 0.0, 0.0] #reseta os parametros
        plot.desenhar_configuracao(indice_parametro, parametros)
    elif estado_atual == ESTADO_CONFIGURAR_PARAMETROS:
        if indice_parametro < 3:
            #ainda ha parametros para configurar: avança para o proximo (A->B->C->D)
            indice_parametro += 1
            plot.desenhar_configuracao(indice_parametro, parametros)
        else:
            #ultimo parametro confirmado: vai para exibir o grafico
            estado_atual = ESTADO_EXIBIR_GRAFICO
            nivel_zoom = 1.0
            pos_central_x = 0.0
            atualizar_brilho_zoom()
            plot.desenhar_grafico(funcao_selecionada, parametros, nivel_zoom, pos_central_x)
    elif estado_atual == ESTADO_EXIBIR_GRAFICO:
        if funcao_selecionada == FUNCAO_QUADRATICA:
            #so para quadratica: exibe xv, yv e delta antes de voltar ao menu
            estado_atual = ESTADO_EXIBIR_VALORES
            plot.desenhar_valores_quadratica(parametros)
        else:
            #demais funcoes: volta direto ao menu
            estado_atual = ESTADO_MENU
            atualizar_cores_rgb()
            plot.desenhar_menu(funcao_selecionada)
    elif estado_atual == ESTADO_EXIBIR_VALORES:
        #na tela de valores: volta ao menu
        estado_atual = ESTADO_MENU
        atualizar_cores_rgb()
        plot.desenhar_menu(funcao_selecionada)

def on_botao_a(pin):
    """Botao A - Incrementa parametro."""
    global parametros
    if not debounce_ok():  #ignora se pressionado muito rapido
        return
    if estado_atual == ESTADO_CONFIGURAR_PARAMETROS:
        buzzer.bip_parametro()  #feedback sonoro ao incrementar
        parametros[indice_parametro] += 0.5  #incrementa o parametro atual em 0.5
        plot.desenhar_configuracao(indice_parametro, parametros)

def on_botao_b(pin):
    """Botao B - Decrementa parametro."""
    global parametros
    if not debounce_ok():  #ignora se pressionado muito rapido
        return
    if estado_atual == ESTADO_CONFIGURAR_PARAMETROS:
        buzzer.bip_parametro()  #feedback sonoro ao decrementar
        parametros[indice_parametro] -= 0.5  #decrementa o parametro atual em 0.5
        plot.desenhar_configuracao(indice_parametro, parametros)

#Registrar interrupcoes
btn_c.irq(trigger=Pin.IRQ_FALLING, handler=on_botao_c)
btn_a.irq(trigger=Pin.IRQ_FALLING, handler=on_botao_a)
btn_b.irq(trigger=Pin.IRQ_FALLING, handler=on_botao_b)
# Funcoes de gerenciamento de estado
def gerenciar_menu():
    global funcao_selecionada
    leitura_y = adc_y.read_u16()
    diferenca = leitura_y - ADC_CENTRO
    if abs(diferenca) > ZONA_MORTA:
        if diferenca < 0:
            matriz.mostrar_seta(True)
        else:
            matriz.mostrar_seta(False)
        if diferenca < 0 and funcao_selecionada > 0:
            funcao_selecionada -= 1
            buzzer.bip_menu()
        elif diferenca > 0 and funcao_selecionada < TOTAL_FUNCOES - 1:
            funcao_selecionada += 1
            buzzer.bip_menu()
        plot.desenhar_menu(funcao_selecionada)
        atualizar_cores_rgb()
        time.sleep_ms(200)
    else:
        matriz.desligar()

def gerenciar_grafico():
    global nivel_zoom
    leitura_y = adc_y.read_u16()
    diferenca = leitura_y - ADC_CENTRO
    if abs(diferenca) > ZONA_MORTA:
        if diferenca < 0:
            nivel_zoom *= 1.1
        else:
            nivel_zoom /= 1.1
        nivel_zoom = max(0.1, min(10.0, nivel_zoom))
        atualizar_brilho_zoom()
        plot.desenhar_grafico(funcao_selecionada, parametros, nivel_zoom, pos_central_x)
        time.sleep_ms(200)

#Main
def main():
    atualizar_cores_rgb()
    plot.desenhar_menu(funcao_selecionada)
    while True:
        if estado_atual == ESTADO_MENU:
            gerenciar_menu()
        elif estado_atual == ESTADO_EXIBIR_GRAFICO:
            gerenciar_grafico()
        #ESTADO_CONFIGURAR_PARAMETROS e ESTADO_EXIBIR_VALORES
        #sao tratados pelas interrupcoes dos botoes
        time.sleep_ms(50)
main()
