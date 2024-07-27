@echo off
setlocal enabledelayedexpansion

REM Set the output file name and extension
set OUTPUT_FILE=output.txt

REM Clear existing output file
type nul > %OUTPUT_FILE%

REM Loop through all .py and .json files in the current directory
for %%F in (*.py *.json) do (
    REM Echo a human-readable separator with the file name to the output file
    echo Current contents of [%%~nxF]: >> %OUTPUT_FILE%
    REM Echo the content of the file to the output file
    type "%%F" >> %OUTPUT_FILE%
    REM Add a separator between file contents (optional)
    echo. >> %OUTPUT_FILE%
)

echo All files merged into %OUTPUT_FILE%
pause
