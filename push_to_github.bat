@echo off
title Push to GitHub
cd /d "%~dp0"
echo ========================================================
echo Pushing Siddarth Swiggy Support Desk to GitHub...
echo ========================================================
git push -u origin main
echo ========================================================
echo Done!
echo ========================================================
pause
