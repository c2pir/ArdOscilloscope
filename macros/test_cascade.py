"""

base montage:
S -> D1-D2 -> R1-R2
R2 -> C1-C2 -> M
R2 -> T1-T2-T3 -> M

"""

import core.macro as cmd
import time

current_state_A1 = 0

def callback_A1_high(cls):
    global current_state_A1
    if current_state_A1==0:
        cmd.set_pin(cls, ["D3","D2"], [1,0])
        current_state_A1 = 1

def callback_A1_low(cls):
    global current_state_A1
    if current_state_A1==1:
        cmd.set_pin(cls, ["D3","D2"], [0,1])
        current_state_A1 = 0

def run(cls):
    if cmd.connect(cls, "COM4"):
        # configure pins
        cmd.configure_pin(cls, "D2", mode=2) # source
        cmd.configure_pin(cls, "D3", mode=2) # command
        
        cmd.configure_pin(cls, "A0", mode=1) # read charge 00
        cmd.configure_pin(cls, "A1", mode=1) # read charge 01
        cmd.configure_pin(cls, "A2", mode=1) # read charge 20
        cmd.configure_pin(cls, "A3", mode=1) # read charge 21
        
        # link event to callback
        cmd.add_trigger(cls, "A1", lambda x: x>580, callback_A1_high)
        cmd.add_trigger(cls, "A1", lambda x: x<560, callback_A1_low)
        
        # set the source
        cmd.set_pin(cls, ["D2"], [1])
        cmd.set_pin(cls, ["D3"], [0])
        
        # time loop
        t0 = time.time()
        cmd.start_recording(cls, nb_points=2000)
        
        while time.time()-t0<10:
            time.sleep(0.01)        
        
        cmd.stop_recording(cls)
        cmd.show_data(cls)
        cmd.remove_triggers(cls)
        
        
        # TODO mesure & show tensions
        # A0-A1
        # A2-A3