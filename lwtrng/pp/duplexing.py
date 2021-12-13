from amaranth import *
from amaranth.cli import main
from amaranth.sim import Simulator, Delay, Settle
#from amaranth.test.tools import *

# Duplexing with Keccak-f200
class Duplexing(Elaboratable):
    def __init__(self):
        self.fin = Signal(200)
        self.fout = Signal(200)
        self.rc = Signal(8)

    def elaborate(self, platform):
        m = Module()

        bc = [ Signal(8) for _ in range(5) ]
        t = [ Signal(8) for _ in range(5) ]
        stt = [ Signal(8) for _ in range(25) ]
        stp = [ Signal(8) for _ in range(25) ]
        stc = [ Signal(8) for _ in range(25) ]

        st = [ self.fin.word_select(i,8) for i in range(25) ]
        # Theta
        for i in range(5):
            m.d.comb += bc[i].eq(st[i]^st[i+5]^st[i+10]^st[i+15]^st[i+20])

        for i in range(5):
            m.d.comb += t[i].eq(bc[(i+4)%5]^(bc[(i+1)%5].rotate_left(1)))
            for j in range(5):
                m.d.comb += stt[5*j+i].eq(st[5*j+i]^t[i])

        # Rho Pi
        li = lambda a, b: 5*b+a
        (x, y) = (1, 0)
        m.d.comb += stp[0].eq(stt[0])
        for i in range(24):
            m.d.comb += stp[li(y,(2*x+3*y)%5)].eq(stt[li(x,y)].rotate_left((i+1)*(i+2)//2))
            (x, y) = (y, (2*x+3*y)%5)
            
        # Chi
        for y in range(5):
            for x in range(5):
                m.d.comb += stc[li(x,y)].eq(stp[li(x,y)]^((~stp[li((x+1)%5,y)])&stp[li((x+2)%5,y)]))

        for i in range(1,25):
            m.d.comb += self.fout.word_select(i,8).eq(stc[i])

        # Iota
        m.d.comb += self.fout.word_select(0,8).eq(stc[0]^self.rc)

        return m

# Post processor with duplexing stages.
# sig: raw random data of sig_width
# sig_width: width of raw random data which is 1, 2, 4 or 8
# z: processed 32-bit data
# z_valid: 1 when z is valid, 0 otherwise
# z_ack: Assert when the processed data is read by user
class DuplexingPP(Elaboratable):
    def __init__(self, sig_width):
        self.sig = Signal(sig_width)
        self.sig_width = sig_width
        self.z = Signal(32)
        self.z_valid = Signal()
        self.z_ack = Signal()

    def elaborate(self, platform):
        m = Module()
        m.submodules.dup = dup = Duplexing()

        rn = Signal(5)
        bits = Signal(4)
        sig_width = self.sig_width
        sigma = Signal(8)
        zc = Signal(36)
        state = Signal(200)
        roundc = Signal(144)
        for i, b in enumerate([
                0x01, 0x82, 0x8a, 0x00, 0x8b, 0x01, 0x81, 0x09,
                0x8a, 0x88, 0x09, 0x0a, 0x8b, 0x8b, 0x89, 0x03,
                0x02, 0x80
        ]):
            m.d.comb += roundc.word_select(i,8).eq(b)

        m.d.comb += self.z.eq(zc >> 4)
        with m.FSM() as fsm:
            with m.State("START"):
                m.next = "COLLECT"
                m.d.sync += [
                    rn.eq(0),
                    sigma.eq(0),
                    bits.eq(0),
                    state.eq(0),
                ]
            with m.State("COLLECT"):
                with m.If(bits == 8):
                    m.next = "DUPLEX"
                    m.d.sync += bits.eq(0)
                with m.Else():
                    m.d.sync += [
                        sigma.eq((sigma << sig_width)|self.sig),
                        bits.eq(bits + sig_width),
                    ]
            with m.State("DUPLEX"):
                with m.If(rn == 18):
                    m.next = "STOP"
                    m.d.sync += self.z_valid.eq(1)
                with m.Else():
                    m.next = "COLLECT"
                    m.d.comb += [
                        dup.fin.eq(state^sigma^0x201),
                        dup.rc.eq(roundc.word_select(rn,8))
                    ]
                    m.d.sync += [
                        state.eq(dup.fout),
                        zc.word_select(rn,2).eq(dup.fout&0x3),
                        rn.eq(rn+1)
                    ]
            with m.State("STOP"):
                with m.If(self.z_ack):
                    m.next = "DONE"
                    m.d.sync += self.z_valid.eq(0)
            with m.State("DONE"):
                with m.If(~self.z_ack):
                    m.next = "START"

        return m

if __name__ == "__main__":

    pp = DuplexingPP(1)

    ports = [ pp.sig, pp.z, pp.z_valid, pp.z_ack ]
    main(pp, name="DuplexingPP", ports=ports)

    """
    sim = Simulator(pp)
    sim.add_clock(1e-6)
    def process():
        sigbits = 0xf7bacd14b04ad308e76524071e44e31c92da9ffa0227a965b2c6dce8
        for cycle in range(512):
            yield pp.sig.eq((sigbits >> (cycle%256))&1)
            valid = yield pp.z_valid
            yield pp.z_ack.eq(valid)
            yield
            return process
    
    sim.add_sync_process(process)
    with sim.write_vcd("dup.vcd", "dup.gtkw"):
        sim.run()
    """
