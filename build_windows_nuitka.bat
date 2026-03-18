@echo off
setlocal EnableExtensions

if "%~1"=="" (
    echo Usage: build_windows_nuitka.bat path\to\program.af
    exit /b 1
)

set "ROOT=%~dp0"
set "SRC=%~1"
set "NAME=%~n1"
set "GEN=%ROOT%generated"

if not exist "%GEN%" mkdir "%GEN%"

py -3 "%ROOT%achillesferse_compiler.py" "%SRC%" "%GEN%\%NAME%.py" || exit /b 1
py -3 -m pip install -r "%ROOT%requirements-build.txt" || exit /b 1
py -3 -m nuitka --onefile --windows-disable-console --output-dir="%ROOT%dist_nuitka" --include-module=achillesferse_runtime --python-flag=no_site --assume-yes-for-downloads "%GEN%\%NAME%.py" || exit /b 1

echo.
echo Done. Your EXE should be in:
echo %ROOT%dist_nuitka\
