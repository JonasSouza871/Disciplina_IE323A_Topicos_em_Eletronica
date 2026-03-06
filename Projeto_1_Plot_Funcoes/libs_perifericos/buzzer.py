from machine import Pin, PWM
import time


class Buzzer:
    def __init__(self, pino):
        self.pwm = PWM(Pin(pino))
        self.pwm.duty_u16(0)

    def _beep(self, freq, duracao_ms):
        self.pwm.freq(freq)
        self.pwm.duty_u16(32768)  # 50% duty cycle
        time.sleep_ms(duracao_ms)
        self.pwm.duty_u16(0)

    def bip_menu(self):
        """Joystick navega entre opcoes - bip curto e agudo."""
        self._beep(1000, 50)

    def bip_parametro(self):
        """Botao A/B incrementa/decrementa - bip medio e grave."""
        self._beep(700, 80)

    def bip_confirma(self):
        """Botao C confirma/avanca tela - bip duplo rapido."""
        self._beep(1200, 40)
        time.sleep_ms(30)
        self._beep(1200, 40)
