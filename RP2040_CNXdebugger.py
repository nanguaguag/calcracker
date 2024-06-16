"""
Plug step:
1. exec'plug_step1'
2. wait until reg[0x01] == 0x0480 
3. exec'plug_step2'
4. check id
"""

from machine import Pin
import rp2, time

PIN_SDA = 1
PIN_SCK = 0
plugStep1 = b'\x01\x00\x00\x00\xaa\xfe\x01\x04\xb0\x00\x00\x01\x01\x04\xa3\x00\x00\x00\x1a\x00\x08'
plugStep2 = b'\x1a\x00\x00\x9e\xff\xff\x9c\xff\xff\x9a\xff\xff\x98\xff\xff\x96\xff\xff\x94\xff\xff\x8e\xff\xff\x8c\xff\xff\x88\xff\xff\x8a\xff\xff\x01\x04\x80\x81\x90`\x83G\x11\x85\x04\xb2\x87\xcfS\xa1\x00\x04\xa3\x00\x81\xa5\x00\x00\xa7\x00\x00\x01\x04\x80\x01\x04\x80\x01\x04\x80\x91\x00\x01'

@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW, set_init=rp2.PIO.OUT_LOW, sideset_init=rp2.PIO.OUT_HIGH)
def stateMachineW():
    wrap_target()
    
    pull(block) #从TX中拉取4字节，低位1字节不用
    set(pins, 1)[3] #ACK
    
    set(x, 7) [7],label("bitLoop") #循环写8个bit
    out(pins, 1).side(0)[1] # 写bit, SCK翻转
    nop().side(1) # SCK翻转
    jmp(x_dec, "bitLoop")
    nop() [7]
    set(x, 15) [3] #for x in range(3):
    label("write8") #循环写8个bit
    
    out(pins, 1).side(0)[1] # 写bit, SCK翻转
    nop().side(1) # SCK翻转
    
    jmp(x_dec, "write8")
    
    set(pins, 0).side(1)
    push() #contiue
    wrap()
    
@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW, set_init=rp2.PIO.OUT_LOW, sideset_init=rp2.PIO.OUT_HIGH)
def stateMachineR():
    wrap_target()
    
    pull(block) #address+r/w, 00000000, 00000000, 00000000
    set(pins, 1)[3] #ACK
    
    set(x, 7) [7],label("bitLoop") #循环写8个bit
    out(pins, 1).side(0)[1] # 写bit, SCK翻转
    nop().side(1) # SCK翻转
    jmp(x_dec, "bitLoop")
    
    nop()[7]
    
    set(pindirs, 0)[7] #pinMode(SDA,INPUT)
    
    set(x, 15) [3],label("bitLoop1") #循环读8个bit
    nop().side(0)[1] # SCK翻转
    in_(pins, 1).side(1) # 读bit, SCK翻转
    jmp(x_dec, "bitLoop1")
    
    
    set(pins, 0).side(1)
    set(pindirs, 1) #pinMode(SDA,OUTPUT)
    push()
    
    wrap()

def executeProgramSequence(pgm):
    global smW, smR
    for i in range(0, len(pgm), 3):
        if pgm[i]&1:
            smR.put(pgm[i], 24)
            #print("Reg[0x"+'{:02x}'.format(pgm[i])+"] is 0x"+ '{:04x}'.format(smR.get()) + ",File=0x"+'{:04x}'.format(pgm[i+1]<<8|pgm[i+2]));
        else:
            smW.put(pgm[i]<<16 | (pgm[i+1]<<8|pgm[i+2]), 8)
            smW.get()
        time.sleep(0)#delay
def resetTarget():
    global PIN_SDA, PIN_SCK
    Pin(PIN_SDA, Pin.OUT).value(0)
    Pin(PIN_SCK, Pin.OUT).value(0)
    time.sleep(0.2)
    Pin(PIN_SDA, Pin.OUT).value(0)
    Pin(PIN_SCK, Pin.OUT).value(1)
    time.sleep(1)
    input("pause")
def IDcheck():
    executeProgramSequence(b'\x01\x04\x80')
    #todo
    
machine.freq(270000000)#270hz
resetTarget()

smW = rp2.StateMachine(0, stateMachineW, freq=6000000, out_base=Pin(PIN_SDA), set_base=Pin(PIN_SDA), sideset_base=Pin(PIN_SCK))
smR = rp2.StateMachine(1, stateMachineR, freq=6000000, out_base=Pin(PIN_SDA), in_base=Pin(PIN_SDA), set_base=Pin(PIN_SDA), sideset_base=Pin(PIN_SCK))
smW.active(1)
smR.active(1)

executeProgramSequence(plugStep1)

print("Step1 complete!")
smR.put(0x01, 24);
print("Wait until reg[0x01] == 0x0480",end='')
while smR.get() != 0x0480:
    time.sleep(0.1)
    smR.put(0x01, 24);
    print('.', end='')
print("\nOK")
executeProgramSequence(plugStep2)
print("Step2 complete!")



