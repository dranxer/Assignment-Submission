@echo off
REM Vercel Deployment Setup Script (Windows)

echo ================================
echo   Vercel Deployment Setup
echo ================================
echo.

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

REM Login to Vercel
echo.
echo Logging in to Vercel...
vercel login

REM Initialize project
echo.
echo Initializing Vercel project...
vercel link

REM Add environment variables
echo.
echo Setting up environment variables...
echo You'll be prompted to add DATABASE_URL
vercel env add DATABASE_URL

REM Deploy
echo.
echo Deploying to Vercel...
vercel --prod

echo.
echo ================================
echo   Deployment Complete!
echo ================================
echo.
echo Your app is now live on Vercel!
echo Open Vercel dashboard: vercel open
echo.
pause
