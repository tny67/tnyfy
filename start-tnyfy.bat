@echo off
title Tnyfy - AI E-Commerce Platform
color 0A

echo.
echo  ████████╗███╗   ██╗██╗   ██╗███████╗██╗   ██╗
echo  ╚══██╔══╝████╗  ██║╚██╗ ██╔╝██╔════╝╚██╗ ██╔╝
echo     ██║   ██╔██╗ ██║ ╚████╔╝ █████╗   ╚████╔╝
echo     ██║   ██║╚██╗██║  ╚██╔╝  ██╔══╝    ╚██╔╝
echo     ██║   ██║ ╚████║   ██║   ██║        ██║
echo     ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝        ╚═╝
echo.
echo     AI-Powered E-Commerce Automation
echo.
echo ══════════════════════════════════════════════
echo.

cd /d "D:\Famille Massini\ia tnyfy"

:: Check Docker
echo [1/2] Verification de Docker...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker n'est pas demarre. Lancement de Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe" 2>nul
    echo     Attente du demarrage de Docker...
    timeout /t 15 /nobreak >nul
)

:: Start database services
echo [2/2] Demarrage PostgreSQL + Redis...
docker-compose up -d 2>nul
if %errorlevel% neq 0 (
    echo [!] Docker Compose a echoue - verifiez que Docker est installe
    echo     Le logiciel fonctionnera en mode demo sans base de donnees
)
timeout /t 3 /nobreak >nul

:: Launch Tnyfy Electron app
echo.
echo ══════════════════════════════════════════════
echo.
echo   Lancement de Tnyfy...
echo.
echo ══════════════════════════════════════════════

cd /d "D:\Famille Massini\ia tnyfy\desktop"
set PATH=C:\Program Files\nodejs;%PATH%
npx electron . --dev
