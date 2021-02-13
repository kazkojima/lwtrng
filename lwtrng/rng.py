#
# This file is part of LwTrng.
#
# SPDX-License-Identifier: BSD-2-Clause

# Random Number Generator

from migen import *

from litex.gen import *

from litex.soc.interconnect.csr import *

class LwTrngGenerator32(Module, AutoCSR):
    def __init__(self, phy):

        bitout = phy.out
        self.o = sr = Signal(32, reset=1)
        self.pseudo = pseudo = CSRStorage(1)

        # 32-bit Galois LFSR with tap 32 31 29 1
        self.sync += sr.eq((sr >> 1) ^ ((-(sr & 1)) & 0xd0000001) ^ bitout)
        self.comb += phy.disable.eq(pseudo.storage)
        # Use the result itself to perturb ring oscillators
        if hasattr(phy, "perturb"):
            self.comb += phy.perturb.eq(sr)
