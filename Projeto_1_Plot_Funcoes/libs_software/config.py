from micropython import const

# --- Pinos do Joystick e Botoes ---
PINO_JOYSTICK_Y = const(26)       # ADC0
PINO_BOTAO_JOYSTICK = const(22)   # Botao C (seleciona/confirma)
PINO_BOTAO_A = const(5)           # Incremento
PINO_BOTAO_B = const(6)           # Decremento

# --- LED RGB (PWM) ---
PINO_RGB_VERMELHO = const(13)
PINO_RGB_VERDE = const(11)
PINO_RGB_AZUL = const(12)

# --- Display OLED I2C ---
I2C_SDA = const(14)
I2C_SCL = const(15)
I2C_ID = const(1)
OLED_ADDR = const(0x3C)

# --- Matriz LED WS2812 ---
PINO_WS2812 = const(7)

# --- Constantes do sistema ---
ATRASO_DEBOUNCE_MS = const(300)
ZONA_MORTA = const(300)
ADC_CENTRO = const(32768)  # MicroPython ADC retorna 0-65535 (16 bits)

# --- Tipos de funcao ---
FUNCAO_AFIM = const(0)
FUNCAO_QUADRATICA = const(1)
FUNCAO_SENOIDAL = const(2)
FUNCAO_COSSENOIDAL = const(3)
TOTAL_FUNCOES = const(4)

NOMES_FUNCOES = ["1.AFIM", "2.QUADRATICA", "3.SENOIDAL", "4.COSSENO"]

# --- Estados do sistema ---
ESTADO_MENU = const(0)
ESTADO_CONFIGURAR_PARAMETROS = const(1)
ESTADO_EXIBIR_GRAFICO = const(2)
ESTADO_EXIBIR_VALORES = const(3)

# --- Cores RGB por funcao (r, g, b) ---
CORES_FUNCAO = [
    (255, 0, 0),      # Afim -> vermelho
    (0, 255, 0),      # Quadratica -> verde
    (0, 0, 255),      # Senoidal -> azul
    (255, 255, 255),  # Cossenoidal -> branco
]
