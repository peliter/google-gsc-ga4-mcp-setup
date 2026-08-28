# Windows PowerShell Installer for GSC & GA4 MCP
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) {
    $python = (Get-Command python3 -ErrorAction SilentlyContinue).Source
}

if (-not $python) {
    Write-Error "Python 3 is required but not found in PATH. Please install Python 3 first."
    exit 1
}

& $python "$scriptDir\setup.py" $args
