@echo off
title Arret de Tnyfy
color 0C

echo.
echo Arret de Tnyfy...
echo.

:: Kill backend and frontend
taskkill /FI "WINDOWTITLE eq Tnyfy Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Tnyfy Frontend*" /F >nul 2>&1

:: Kill uvicorn and node processes started by Tnyfy
taskkill /IM "uvicorn.exe" /F >nul 2>&1
taskkill /IM "node.exe" /FI "WINDOWTITLE eq Tnyfy*" /F >nul 2>&1

:: Stop Docker containers
cd /d "D:\Famille Massini\ia tnyfy"
docker-compose down >nul 2>&1

echo.
echo Tnyfy arrete avec succes.
echo.
pause
