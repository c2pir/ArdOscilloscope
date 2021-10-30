@echo off
rem Dependency Walker
cd %~dp0

:start
if "%1" equ "-h" (
	echo OPTIONS -x[OPTIONAL]:
	echo  -h to show this help
	echo  -d to run it in debug mode
	echo  -m full screen
	goto end
)

echo %1|find "m" >nul
if errorlevel 1 (set maximazed=0) else (set maximazed=1)

set PATH=%PATH%;%~dp0dll;
rem echo %PATH%

rem call venv3/scripts/activate.bat
:run
py MainUI.py %maximazed%

if "%1" equ "-d" (
	set /p var="Restart (y/n)? "
	if "%var%" equ "y" (
		goto run
	)
)

rem call venv3/scripts/deactivate.bat
:end