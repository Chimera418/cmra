@echo off
REM Build a standalone cmra.exe with PyInstaller
echo Building CMRA executable...
pyinstaller --onefile --name cmra src\cmra\cli.py
echo.
echo Done. Executable is at dist\cmra.exe
