import core.macro as cmd
import time

def run(cls):
    
    if cmd.connect(cls, "COM8"):
        
        cmd.configure_pin(cls, "D3", mode=2)
        cmd.configure_pin(cls, "A1", mode=1)
        cmd.configure_pin(cls, "A2", mode=1)
        
        cmd.start_recording(cls)
        
        for i in range(3):
            cmd.set_pin(cls, ["D3"], [1])
            time.sleep(2.0)
            cmd.set_pin(cls, ["D3"], [0])
            time.sleep(2.0)
        
        time.sleep(3.0)
        cmd.stop_recording(cls)
        cmd.show_data(cls)
        cmd.save_data_as_csv(cls, "results.csv")