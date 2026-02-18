@echo off
setlocal

REM Builds originplanet_c_hub.exe with MinGW GCC if available.
REM Run this from a Developer Command Prompt or terminal with gcc in PATH.

gcc -std=c11 -Wall -Wextra -O2 -o originplanet_c_hub.exe originplanet_c_hub.c
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo Build succeeded: %CD%\originplanet_c_hub.exe
endlocal
