@echo off
REM Script para instalar Cloudflared no Windows

echo ===================================
echo Instalando Cloudflare Tunnel...
echo ===================================
echo.

REM Verifica se Chocolatey está instalado
where choco >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Chocolatey encontrado. Instalando cloudflared...
    choco install cloudflare-warp -y
    goto verificar
) else (
    echo Chocolatey não encontrado.
    echo.
    echo Tentando com winget...
    where winget >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo Instalando cloudflared via winget...
        winget install Cloudflare.Cloudflared -e
        goto verificar
    ) else (
        echo.
        echo Erro: Nenhum gerenciador de pacotes encontrado.
        echo.
        echo Opções de instalação manual:
        echo.
        echo 1. Instale Chocolatey:
        echo    https://chocolatey.org/install
        echo.
        echo 2. Ou instale via winget (pré-instalado no Windows 11)
        echo.
        echo 3. Ou baixe diretamente:
        echo    https://github.com/cloudflare/cloudflared/releases
        echo.
        pause
        exit /b 1
    )
)

:verificar
echo.
echo Verificando instalação...
cloudflared --version
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===================================
    echo Instalação concluída com sucesso!
    echo ===================================
    echo.
    echo Agora você pode executar: python app.py
    pause
) else (
    echo.
    echo Erro: cloudflared ainda não foi encontrado.
    echo Tente reiniciar o terminal.
    pause
    exit /b 1
)
