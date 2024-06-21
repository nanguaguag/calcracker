from machine import Pin
import rp2, time

PIN_SDA = 1
PIN_SCK = 0 
pgm=[0x10000,0x00000,0x104b0,0x00000,0x104a3,0x00000,0x00000,0x104a2,0x104a2,0x104a2,0x104a2,0x104a2,0x104a2,0x104a0,0x10480,0x00000,0x00000,0x00000,0x00000,0x00000,0x00000,0x00000,0x00000,0x00000,0x00000,0x00000,0x10480,0x19060,0x14711,0x104b2,0x1cf53,0x10004,0x10081,0x10000,0x10000,0x10480,0x10480,0x10480,0x10000,0x10480]
@rp2.asm_pio(out_init=rp2.PIO.IN_LOW, set_init=rp2.PIO.IN_LOW)
def stateMachine():
    wrap_target()
    set(x, 7), label("bitLoop")
    wait(0, gpio, 0)
    wait(1, gpio, 0)
    jmp(x_dec, "bitLoop")
    
    pull()
    wait(0, gpio, 1)
    out(pindirs, 1)
    set(x, 15), label("16bitLoop")
    wait(0, gpio, 0)
    out(pins, 1)
    wait(1, gpio, 0)
    jmp(x_dec, "16bitLoop")
    set(pindirs, 0)
    wrap()

Pin(PIN_SCK).init(mode=Pin.IN)
machine.freq(270000000)#270hz

sm = rp2.StateMachine(0, stateMachine, freq=60000000,
                      out_base=Pin(PIN_SDA),
                      set_base=Pin(PIN_SDA))
sm.put(pgm[0], 15)
sm.put(pgm[1], 15)
sm.put(pgm[2], 15)
sm.put(pgm[3], 15)
sm.active(1)
i = 4
while 1:
    while sm.tx_fifo() < 4:
        sm.put(pgm[i], 15)
        i+=1
 #   if(x & 1 == 0):
 #       
 #       print("Get:",hex(x))
 #   elif(x & 1 == 1):
 #       sm.put(0x04B0, 16)
