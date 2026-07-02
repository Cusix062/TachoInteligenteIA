@echo off
cd /d "%~dp0"
set STREAMLIT_EMAIL=
set STREAMLIT_SERVER_HEADLESS=false
set TF_CPP_MIN_LOG_LEVEL=3
cls
echo ============================================
echo      Tacho Inteligente con IA
echo ============================================
echo.
echo  NO CIERRE ESTA VENTANA mientras usa la app
echo.
"C:\Users\jaire\Downloads\TachoInteligenteIA\venv\Scripts\streamlit" run app.py --server.port 8510
echo.
echo  Servidor detenido.
pause
