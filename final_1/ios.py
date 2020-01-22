from migen import *

from litex.soc.interconnect.csr import *
from litex.soc.cores import gpio


from pwm import PWM

# see:
# https://github.com/enjoy-digital/litex/blob/master/litex/soc/cores/gpio.py

class Led(gpio.GPIOOut):
    pass

class RGBLed(Module, AutoCSR):
    def __init__(self, pads):
        self.submodules.r = PWM(pads.r)
        self.submodules.g = PWM(pads.g)
        self.submodules.b = PWM(pads.b)

class Button(gpio.GPIOIn):
    pass

class Buttoninter(gpio.GPIOIn):
    def __init__(self, signal):
        self._in = CSRStatus(len(signal))
        self.specials += MultiReg(signal, self._in.status)

        self.submodules.ev = EventManager()
        self.ev.zero = EventSourceProcess()
        self.ev.finalize()

        self.comb += self.ev.zero.trigger.eq(self._in != 1)
    pass

class Switch(gpio.GPIOIn):

    pass
