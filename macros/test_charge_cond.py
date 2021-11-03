import core.macro as cmd
import time

def run(cls):
	
	if cmd.connect(cls, "COM8"):
		
		cmd.configure_pin(cls, "D2", mode=2) # source
		cmd.configure_pin(cls, "D3", mode=2) # commande transistor
		cmd.configure_pin(cls, "A0", mode=1) # read source
		cmd.configure_pin(cls, "A1", mode=1) # read charge 1
		cmd.configure_pin(cls, "A2", mode=1) # read charge 2
		
		cmd.set_pin(cls, ["D2","D3"], [0,0])
		time.sleep(1.0)
		
		cmd.start_recording(cls, show = False)
		t0 = time.time()
		time.sleep(2.0)
		d = 0
		b = 0
		
		# 10s loop
		while ((time.time()-t0)<10.0):
			# read pin A1
			v = cmd.get_pin(cls, ["A1"])
			if len(v)!=0:
				if v[0] > 600:
					if b==0:
						cmd.set_pin(cls, ["D3"], [1])
						b = 1
				
				if v[0] < 520:
					if b==1:
						cmd.set_pin(cls, ["D3"], [0])
						b = 0

			# make square signal for pin D2
			if (time.time()-d)>1.1:
				d = int(time.time())
				cmd.set_pin(cls, ["D2"], [d%2])
			time.sleep(0.001)
		
		cmd.stop_recording(cls)
		cmd.save_data_as_csv(cls, "results.csv")