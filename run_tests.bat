@echo off
title Siddarth Swiggy Support Desk AI - Test Suite Runner
cd /d "%~dp0"
echo ========================================================
echo Running Siddarth Swiggy AI Unit Tests and Benchmark...
echo ========================================================
python -m unittest discover tests -v
pause
