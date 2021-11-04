# ArdOscilloscope

A python UI (PyQt5) to use arduino card as an oscilloscope.

<h3>Installation:</h3>
<ol>
	<li> install python 3 (on window check "Add to path" or do a python3 virtual env and activate it)</li>
	<li> run "install.cmd" (need an internet connexion)</li>
	<li> Upload the corresponding ino to your Arduino board (don't forget to close the Serial Monitor if you have it open)</li>
	<li> run "run.bat"</li>
</ol>

<h3>Actual coverage:</h3>
	Arduino boards:<br>
	<blockquote><ul>
		<li> Nano 	OK</li>
		<li> Uno 	OK</li>
		<li> ...</li>
		You can define your board by creating a JSON file in the conf folder
	</ul></blockquote>
	Commands alvailables:
	<blockquote><ul>
		<li> set digital pin mode 			OK</li>
		<li> write on a digital pin 			OK</li>
		<li> read on an analog pin 			OK</li>
		<li> write on a PWM pin 			OK</li>
		<li> use analog pin as INPUT_PULLUP 		KO</li>
	</ul></blockquote>
		
TODO:<br>
	- macro callbacks on condition (as an editable list of functions)
