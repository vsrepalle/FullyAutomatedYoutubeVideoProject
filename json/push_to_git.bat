@echo off
echo ============================================
echo   YouTube Videos Generator - Git Upload
echo ============================================

REM Move to project directory
cd /d C:\VISWA\0000_PYTHON_APPS\Youtube_VIDEOS_GENERATION

echo.
echo 📂 Current directory:
cd

REM Initialize git if not already
if not exist ".git" (
    echo 🔧 Initializing Git repository...
    git init
)

REM Ensure .gitignore exists
if not exist ".gitignore" (
    echo ❌ ERROR: .gitignore not found!
    echo Please create .gitignore before continuing.
    pause
    exit /b
)

echo.
echo 🔍 Checking ignored files...
git status --ignored

echo.
echo ➕ Adding allowed files to Git...
git add .

echo.
echo 📌 Git status (review before commit):
git status

echo.
set /p commitmsg="📝 Enter commit message: "

if "%commitmsg%"=="" (
    echo ❌ Commit message cannot be empty!
    pause
    exit /b
)

git commit -m "%commitmsg%"

REM Ensure branch is main
git branch -M main

REM Remove old remote if exists
git remote remove origin 2>nul

echo 🔗 Adding correct GitHub remote...
git remote add origin https://github.com/vsrepalle/FullyAutomatedYoutubeVideoProject.git

echo.
echo 🚀 Pushing to GitHub...
git push -u origin main

echo.
echo ✅ Upload complete!
echo Check: https://github.com/vsrepalle/Youtube_video_prod_apps
echo ============================================
pause
