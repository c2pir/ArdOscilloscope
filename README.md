# ArdOscilloscope

A python UI (PyQt5) to use arduino card as an oscilloscope.

Installation:
	-> install python 3 (on window check "Add to path" or do a python3 virtual env and activate it)
	-> run "install.cmd" (need an internet connexion)
	-> run "run.bat"

Actual coverage:
	Arduino boards:
		- Nano 	OK
		- Uno 	KO
		- ...
		You can define your board by creating a JSON file in the conf folder
	Commands alvailables:
		- set digital pin mode 				OK
		- write on a digital pin 			OK
		- read on an analog pin 			OK
		- write on a PWM pin 				KO
		- use analog pin as INPUT_PULLUP 	KO