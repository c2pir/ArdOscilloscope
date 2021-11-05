import core.macro as cmd
import time

def run(cls):
    
    if cmd.connect(cls, "COM8"):
        
        cmd.configure_pin(cls, "D3", mode=2)
        cmd.configure_pin(cls, "D4", mode=2)
        cmd.configure_pin(cls, "A2", mode=1)
        
        cmd.start_recording(cls)
        
        time.sleep(0.5)
        cmd.set_pin(cls, ["D3","D4"], [1,1])
        time.sleep(1.0)
        cmd.set_pin(cls, ["D3","D4"], [1,0])
        time.sleep(1.0)
        cmd.set_pin(cls, ["D3","D4"], [1,1])
        time.sleep(1.0)
        cmd.set_pin(cls, ["D3","D4"], [1,0])
        time.sleep(1.0)
        
        cmd.stop_recording(cls)
        cmd.show_data(cls)
        cmd.save_data_as_csv(cls, "results.csv")