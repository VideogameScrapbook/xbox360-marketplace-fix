@REM This batch script is for allowing dragging files/folders onto the file's icon to easily use them as input for the Python script.

@REM Turn on displaying of commands.
@ECHO OFF

@REM SETLOCAL


@REM WARNING: %~dp0 seems to return first parameter's folder instead of script's folder when the batch file is called by a different script.
SET "scriptDrive=%~d0"
SET "scriptFolder=%~dp0"
SET "scriptName=%~n0"

@REM %scriptDrive%
@REM CD "%scriptFolder%"

@REM https://stackoverflow.com/a/16144756
python.exe "%scriptFolder%%scriptName%.py" %*

@REM PAUSE
