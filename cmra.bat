@echo off
REM cmra.bat — wrapper so you can type  `cmra <file>`  from any shell
REM that has this folder on PATH (or run it directly as .\cmra.bat).
REM Prefers the local venv's Python; falls back to system Python.

SET "SCRIPT_DIR=%~dp0"
SET "VENV_PY=%SCRIPT_DIR%venv\Scripts\python.exe"

IF EXIST "%VENV_PY%" (
    "%VENV_PY%" "%SCRIPT_DIR%src\cmra\cli.py" %*
) ELSE (
    python "%SCRIPT_DIR%src\cmra\cli.py" %*
)
