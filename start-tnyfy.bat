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
echo [1/4] Verification de Docker...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker n'est pas demarre. Lancement de Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe" 2>nul
    echo     Attente du demarrage de Docker...
    timeout /t 15 /nobreak >nul
)

:: Start database services
echo [2/4] Demarrage PostgreSQL + Redis...
docker-compose up -d 2>nul
if %errorlevel% neq 0 (
    echo [!] Docker Compose a echoue - verifiez que Docker est installe
    echo     Le dashboard fonctionnera en mode demo sans base de donnees
)
timeout /t 3 /nobreak >nul

:: Start Backend
echo [3/4] Demarrage du backend Tnyfy...
cd /d "D:\Famille Massini\ia tnyfy\backend"
start "Tnyfy Backend" cmd /c ".venv\Scripts\activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul

:: Start Frontend
echo [4/4] Demarrage du dashboard...
cd /d "D:\Famille Massini\ia tnyfy\frontend"
start "Tnyfy Frontend" cmd /c "set PATH=C:\Program Files\nodejs;%%PATH%% && npm run dev"
timeout /t 5 /nobreak >nul

:: Open browser
echo.
echo ══════════════════════════════════════════════
echo.
echo   Tnyfy est pret !
echo.
echo   Dashboard : http://localhost:3000
echo   API       : http://localhost:8000/docs
echo.
echo   Fermer cette fenetre n'arrete PAS Tnyfy.
echo   Pour arreter : lancez stop-tnyfy.bat
echo.
echo ══════════════════════════════════════════════

:: Open dashboard in default browser
start http://localhost:3000

pause
