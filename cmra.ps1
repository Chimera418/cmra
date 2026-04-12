# cmra.ps1 — PowerShell wrapper for the CMRA CLI
# Usage: .\cmra.ps1 <file>   .\cmra.ps1 run <file>   .\cmra.ps1 repl

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$cliPy     = Join-Path $scriptDir "src\cmra\cli.py"
$venvPy    = Join-Path $scriptDir "venv\Scripts\python.exe"

if (Test-Path $venvPy) {
    & $venvPy $cliPy @args
} else {
    python $cliPy @args
}
