#
# This file is part of LwTrng.
#
# SPDX-License-Identifier: BSD-2-Clause

# Random Number Generator

from migen import *

from litex.gen import *

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

from lwtrng.pp import data_file

class LwTrngGenerator32(Module, AutoCSR):
    def __init__(self, platform, phy):

        platform.add_source(data_file("DuplexingPP.v"), "verilog")

        sig = phy.out
        self.submodules.fifo = fifo = stream.SyncFIFO([("data", 32)], 512)

        # CPU side
        self.ready = CSRStatus(1)
        self.data = CSRStatus(32)
        self.comb += [
            fifo.source.ready.eq(self.data.we),
            self.data.status.eq(fifo.source.data),
            self.ready.status.eq(fifo.source.valid)
        ]

        # RNG side
        z = Signal(32)
        z_valid = Signal()
        z_ack = Signal()
        self.comb += [
            fifo.sink.data.eq(z),
            fifo.sink.valid.eq(z_ack)
        ]
        self.sync += [
            If(z_valid & fifo.sink.ready, z_ack.eq(1)),
            If(z_ack, z_ack.eq(0))
        ]
        if hasattr(phy, "perturb"):
            self.sync += If(z_valid, phy.perturb.eq(z))

        self.specials += Instance("DuplexingPP",
                                  i_clk = ClockSignal(),
                                  i_rst = ResetSignal(),
                                  i_sig = sig,
                                  o_z = z,
                                  o_z_valid = z_valid,
                                  i_z_ack = z_ack)
