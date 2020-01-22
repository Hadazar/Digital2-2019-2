from migen import *

from migen.genlib.io import CRG

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.spi import SPIMaster


from ios import Led, RGBLed, Button, Switch
from btn_itrupt import*


#salidas para nexys 4 ddr
_io = [


    """
    ("boton",  0, Pins("G16"), IOStandard("LVCMOS33")),
    ("boton",  1, Pins("F16"), IOStandard("LVCMOS33")),
    ("boton",  2, Pins("D14"), IOStandard("LVCMOS33")),
    ("boton",  3, Pins("H14"), IOStandard("LVCMOS33")),
    ("boton",  4, Pins("G13"), IOStandard("LVCMOS33")),  #direcciones
    ("boton",  5, Pins("F13"), IOStandard("LVCMOS33")),
    ("boton",  6, Pins("E16"), IOStandard("LVCMOS33")),
    ("boton",  7, Pins("H16"), IOStandard("LVCMOS33")),
    """

    ("boton",  0, Pins("J15"), IOStandard("LVCMOS33")),
    ("boton",  1, Pins("L16"), IOStandard("LVCMOS33")),
    ("boton",  2, Pins("M13"), IOStandard("LVCMOS33")),
    ("boton",  3, Pins("R15"), IOStandard("LVCMOS33")),
    ("boton",  4, Pins("R17"), IOStandard("LVCMOS33")),  #direcciones
    ("boton",  5, Pins("T18"), IOStandard("LVCMOS33")),
    ("boton",  6, Pins("U18"), IOStandard("LVCMOS33")),
    ("boton",  7, Pins("R13"), IOStandard("LVCMOS33")),


    ("lcd_spi", 0,
        Subsignal("cs_n", Pins("C17")),
        Subsignal("mosi", Pins("G17")),
        Subsignal("miso", Pins("E17")),
        Subsignal("clk", Pins("D17")),
        IOStandard("LVCMOS33")
    ),
    ("rst_lcd",  0, Pins("D18"), IOStandard("LVCMOS33")),#rst
    ("rs_lcd",  0, Pins("E18"), IOStandard("LVCMOS33")),

    ("clk100", 0, Pins("E3"), IOStandard("LVCMOS33")),

    ("cpu_reset", 0, Pins("C12"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("D4")),
        Subsignal("rx", Pins("C4")),
        IOStandard("LVCMOS33"),
    ),

    ("sd_spi", 0,
        Subsignal("cs_n", Pins("K1")),
        Subsignal("mosi", Pins("F6")),
        Subsignal("miso", Pins("J2")),
        Subsignal("clk", Pins("G6")),
        IOStandard("LVCMOS33")
    ),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk100"
    default_clk_period = 10.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7a100t-CSG324-1", _io, toolchain="ise")

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)


def csr_map_update(csr_map, csr_peripherals):
    csr_map.update(dict((n, v)
        for v, n in enumerate(csr_peripherals, start=max(csr_map.values()) + 1)))


# create our platform (fpga interface)
platform = Platform()

# create our soc (fpga description)
class BaseSoC(SoCCore):
    # Peripherals CSR declaration
    csr_peripherals = [


        "botones",
        "lcd",
        "rs",
        "rst",
        "SD"
    ]
    csr_map_update(SoCCore.csr_map, csr_peripherals)

    def __init__(self, platform):
        sys_clk_freq = int(100e6)
        # SoC with CPU
        interrupt_map = {
            "botones" : 4,
        }
        SoCCore.interrupt_map.update(interrupt_map)

        SoCCore.__init__(self, platform,
            cpu_type="lm32",
            clk_freq=100e6,
            ident="CPU Test SoC", ident_version=True,
            integrated_rom_size=0x8000,
            integrated_main_ram_size=16*1024)

        # Clock Reset Generation
        self.submodules.crg = CRG(platform.request("clk100"), ~platform.request("cpu_reset"))


        #botones con interrupcion
        bot = Cat(*[platform.request("boton", i) for i in range(8)])
        self.submodules.botones = btnintrupt(bot)
        # lcd
        self.submodules.lcd = SPIMaster(platform.request("lcd_spi"))
        self.submodules.rs = Led(platform.request("rs_lcd"))
        self.submodules.rst = Led(platform.request("rst_lcd"))
        #Memoria SD
        self.submodules.SD = SPIMaster(platform.request("sd_spi"))

soc = BaseSoC(platform)

#
# build
#
builder = Builder(soc, output_dir="build", csr_csv="test/csr.csv")
builder.build()
