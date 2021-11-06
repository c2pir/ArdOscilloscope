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

<h3>Folders organisation:</h3>
	<blockquote><ul>
		<li> conf: contains configuration files for each board.<br>
		You can create your own for another board with the corresponding board source code.</li>
		<li> core: contain python code used by the UI</li>
		<li> img: contains UI images</li>
		<li> ino: contains board source code.</li>
		<li> macros: contains sample of runnable macros from the UI.<br> 
		You can create here your own macros for your measures (see core/macro.py for alvailable commands)</li>
		<li> ui: contains UI pyqt classes.</li>
	</ul></blockquote>
