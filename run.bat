@echo off
echo ===================================================================
echo  Neural Topology Mapping - Crowd Analytics System (Phase 2)
echo ===================================================================
echo Starting server...
echo Usage: run.bat [--mock] [--port 8000]
echo.
python server.py %*
pause
