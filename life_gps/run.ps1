# Life-GPS Flutter Developer Scripts
# Usage: .\run.ps1 <command>

param([string]$Command = "help")

$FlutterPath = "C:\src\flutter\bin\flutter.bat"
$ProjectDir = $PSScriptRoot

function Invoke-Flutter {
  param([string[]]$Args)
  & $FlutterPath @Args
}

switch ($Command) {
  "run" {
    Write-Host "Starting Life-GPS in development mode..." -ForegroundColor Cyan
    Set-Location $ProjectDir
    Invoke-Flutter "run" "--dart-define=APP_ENV=development"
  }
  "test" {
    Write-Host "Running Flutter tests..." -ForegroundColor Cyan
    Set-Location $ProjectDir
    Invoke-Flutter "test" "--coverage"
  }
  "analyze" {
    Write-Host "Running Flutter analyze..." -ForegroundColor Cyan
    Set-Location $ProjectDir
    Invoke-Flutter "analyze"
  }
  "build" {
    Write-Host "Building release APK..." -ForegroundColor Cyan
    Set-Location $ProjectDir
    Invoke-Flutter "build" "apk" "--release" "--dart-define=APP_ENV=production"
  }
  "web" {
    Write-Host "Building web release..." -ForegroundColor Cyan
    Set-Location $ProjectDir
    Invoke-Flutter "build" "web" "--dart-define=APP_ENV=production"
  }
  "clean" {
    Write-Host "Cleaning Flutter build artifacts..." -ForegroundColor Yellow
    Set-Location $ProjectDir
    Invoke-Flutter "clean"
    Invoke-Flutter "pub" "get"
  }
  "gen" {
    Write-Host "Running code generation (build_runner)..." -ForegroundColor Cyan
    Set-Location $ProjectDir
    Invoke-Flutter "pub" "run" "build_runner" "build" "--delete-conflicting-outputs"
  }
  "deps" {
    Write-Host "Fetching Flutter dependencies..." -ForegroundColor Cyan
    Set-Location $ProjectDir
    Invoke-Flutter "pub" "get"
  }
  "doctor" {
    Write-Host "Running Flutter doctor..." -ForegroundColor Cyan
    Invoke-Flutter "doctor" "-v"
  }
  default {
    Write-Host @"

Life-GPS Flutter Developer Scripts
====================================
  .\run.ps1 run       Start dev server
  .\run.ps1 test      Run all tests with coverage
  .\run.ps1 analyze   Run flutter analyze
  .\run.ps1 build     Build release APK
  .\run.ps1 web       Build web release
  .\run.ps1 clean     Clean + pub get
  .\run.ps1 gen       Run code generation
  .\run.ps1 deps      Fetch dependencies
  .\run.ps1 doctor    Run flutter doctor

"@ -ForegroundColor White
  }
}
