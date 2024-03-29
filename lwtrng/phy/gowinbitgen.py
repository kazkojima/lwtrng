#
# This file is part of LwTrng.
#
# Copyright (c) 2021 Kazumoto Kojima <kkojima@rr.iij4u.or.jp>
# SPDX-License-Identifier: BSD-2-Clause

# Raw random bit generator PHY for Gowin FPGA

from migen import *

class _PHYRingOscillator(Module):
    def __init__(self, disable, delay):

        # Ring oscillator ~120MHz with one inverter LUT + delay line LUT x 7
        # 'delay' changes the signal path which modifies delay.
        # Looks ECP5 LUT BCD=010 has ~20ps more delay compared to BCD=101.

        chain = Signal(8)
        self.out = chain[1]
        for i in range(8):
            self.specials += [
                Instance("LUT4",
                         p_INIT = (1 if i == 0 else 0xaaaa),
                         o_F = (chain[0] if i==7 else chain[i+1]),
                         i_I0 = chain[i],
		         i_I1 = (disable if i==0 else ~delay),
		         i_I2 = (0 if i==0 else delay),
                         i_I3 = (0 if i==0 else ~delay))
            ]
        
class LwTrngPHYBitGen(Module):
    def __init__(self):

        self.disable = disable = Signal()
        self.perturb = perturb = Signal(32)
        self.out = Signal()
        outer_out = Signal()
        inner_out = Signal(4)

        # Expect metastable bits on self.out
        self.sync += self.out.eq(outer_out)

        ro_list = [ _PHYRingOscillator(disable, perturb[i]) for i in range(16) ]
        self.submodules.ro_list = ro_list

        for i in range(4):
            self.specials += [
                Instance("LUT4",
                         p_INIT = 0xace1,
                         o_F = inner_out[i],
                         i_I0 = ro_list[4*i].out,
		         i_I1 = ro_list[4*i+1].out,
		         i_I2 = ro_list[4*i+2].out,
                         i_I3 = ro_list[4*i+3].out)
            ]

        self.specials += [
            Instance("LUT4",
                     p_INIT = 0xace1,
                     o_F = outer_out,
                     i_I0 = inner_out[0],
                     i_I1 = inner_out[1],
                     i_I2 = inner_out[2],
                     i_I3 = inner_out[3])
        ]
