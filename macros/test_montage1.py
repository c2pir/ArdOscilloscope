import core.macro as cmd
import time

def run(cls):
	
	cmd.configure_pin(cls, "D4", mode=2)
	cmd.configure_pin(cls, "A1", mode=1)
	cmd.configure_pin(cls, "A2", mode=1)
	
	cmd.start_recording(cls)
	
	for i in range(3):
		cmd.set_pin(cls, "D4", 1)
		time.sleep(2.0)
		cmd.set_pin(cls, "D4", 0)
		time.sleep(2.0)
	
	cmd.stop_recording(cls)