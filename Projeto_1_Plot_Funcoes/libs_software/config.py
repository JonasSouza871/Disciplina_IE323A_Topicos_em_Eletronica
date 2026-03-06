from micropython import const

#PINOS DO PROJETO (SOMENTE PARA CODIGO MICROPYTHON no thony)
PINO_JOYSTICK_X = const(27) #Adc1 no joystick eixo x
PINO_JOYSTICK_Y = const(26) #Adc0 no joystick eixo y
PINO_BOTAO_JOYSTICK = const(22) #joystick select
PINO_BOTAO_A = const(5) #Botao de incrimento 
PINO_BOTAO_B = const(6) #Botao de decremento
PINO_BOTAO_C = const(10) #botao de Seleciona/confirma
PINO_BUZZER = const(21) #buzzer
#Leds RGB
PINO_RGB_VERMELHO = const(13)
PINO_RGB_VERDE = const(11)
PINO_RGB_AZUL = const(12)
#Display OLED I2C 
I2C_SDA = const(2)
I2C_SCL = const(3)
I2C_ID = const(1) #conectado no I2C1
OLED_ADDR = const(0x3C)
PINO_WS2812 = const(7) #matriz de led
ATRASO_DEBOUNCE_MS = const(300) #debounce
ZONA_MORTA = const(4800) #zona morta do joystick (ajustado para ADC 16 bits)
ADC_CENTRO = const(32768) #MicroPython ADC retorna 0-65535 (16 bits)

#Tipos de funcao
FUNCAO_AFIM = const(0)
FUNCAO_QUADRATICA = const(1)
FUNCAO_SENOIDAL = const(2)
FUNCAO_COSSENOIDAL = const(3)
TOTAL_FUNCOES = const(4)
NOMES_FUNCOES = ["1.AFIM", "2.QUADRATICA", "3.SENOIDAL", "4.COSSENO"]

#Estados do sistema
ESTADO_MENU = const(0)
ESTADO_CONFIGURAR_PARAMETROS = const(1)
ESTADO_EXIBIR_GRAFICO = const(2)
ESTADO_EXIBIR_VALORES = const(3)

#Cores para cada função matematica no led rgb e na matriz de led (ws2812)
CORES_FUNCAO = [
    (255, 0, 0),#Afim -> vermelho
    (0, 255, 0),#Quadratica -> verde
    (0, 0, 255),#Senoidal -> azul
    (255, 255, 255),  # Cossenoidal -> branco
]
