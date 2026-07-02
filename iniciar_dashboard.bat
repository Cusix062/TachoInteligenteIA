@echo off
cd /d "%~dp0"
set STREAMLIT_EMAIL=
set TF_CPP_MIN_LOG_LEVEL=3
cls
echo ============================================
echo      Tacho Inteligente con IA
echo ============================================
echo.
echo  Iniciando servidor, espera unos segundos...
echo.
echo  CUANDO VEA ESTO EN LA PANTALLA:
echo.
echo     Local URL: http://localhost:8510
echo.
echo  COPIE ESA DIRECCION Y PEGUELA EN SU NAVEGADOR
echo.
echo  Si no funciona, pruebe: http://127.0.0.1:8510
echo.
echo  Presione Ctrl+C para detener
echo ============================================
echo.
"venv\Scripts\streamlit" run app.py --server.port 8510
pause
