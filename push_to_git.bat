@echo off
setlocal
echo ============================================
echo   YouTube Videos Generator - Clean Sync
echo ============================================

:: 1. SET THE CORRECT PROJECT PATH
set "PROJECT_PATH=C:\VISWA\0000_PYTHON_APPS\YOUTUBE_VIDEO_PROD\00_FullyAutomatedYoutubeVideos"

:: Move to the directory
cd /d "%PROJECT_PATH%"

echo.
echo [INFO] Current directory: %CD%

:: 2. RESET LOCAL GIT TO ENSURE CLEAN START
:: This removes the old local history so we only have the new files
if exist ".git" (
    echo [INFO] Refreshing Git initialization...
    rd /s /q .git
)

git init
git branch -M main

:: 3. ADD FILES
echo.
echo [INFO] Adding files from current directory...
git add .

:: 4. COMMIT
echo.
set /p commitmsg="Enter commit message (e.g., Initial clean push): "
if "%commitmsg%"=="" set commitmsg="Clean project update"

git commit -m "%commitmsg%"

:: 5. CONNECT TO REMOTE
echo.
echo [INFO] Connecting to GitHub...
git remote add origin https://github.com/vsrepalle/FullyAutomatedYoutubeVideoProject.git

:: 6. FORCE PUSH (This deletes everything else on remote)
echo.
echo [WARNING] Force pushing will overwrite remote files with local ones.
echo [INFO] Uploading...
git push -u origin main --force

echo.
echo ============================================
echo SUCCESS: GitHub matches your local folder.
echo URL: https://github.com/vsrepalle/FullyAutomatedYoutubeVideoProject.git
echo ============================================
pause