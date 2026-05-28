#!/usr/bin/env python3
"""
Script para gerenciar Cloudflare Tunnel da aplicação
"""

import subprocess
import os
import sys
import platform

def check_cloudflared():
    """Verifica se cloudflared está instalado"""
    try:
        result = subprocess.run(['cloudflared', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_cloudflared():
    """Guia de instalação do cloudflared"""
    print("\n" + "="*50)
    print("❌ Cloudflared não encontrado!")
    print("="*50)
    
    system = platform.system()
    
    if system == "Windows":
        print("\n📦 Para instalar no Windows, escolha uma opção:\n")
        print("1️⃣  Usando Chocolatey (recomendado):")
        print("   choco install cloudflare-warp -y\n")
        print("2️⃣  Usando winget (Windows 11+):")
        print("   winget install Cloudflare.Cloudflared -e\n")
        print("3️⃣  Ou execute o script em batch:")
        print("   install_cloudflared.bat\n")
        
        print("4️⃣  Download manual:")
        print("   https://github.com/cloudflare/cloudflared/releases\n")
        
    elif system == "Darwin":  # macOS
        print("\n📦 Para instalar no macOS:")
        print("   brew install cloudflare/cloudflare/cloudflared\n")
        
    elif system == "Linux":
        print("\n📦 Para instalar no Linux:")
        print("   Ubuntu/Debian: sudo apt-get install cloudflared")
        print("   RHEL/CentOS: sudo yum install cloudflared\n")
    
    input("Pressione Enter quando terminar a instalação e reiniciar o terminal...")
    
    if check_cloudflared():
        print("✅ Cloudflared detectado com sucesso!\n")
        return True
    else:
        print("❌ Cloudflared ainda não foi encontrado.\n")
        return False

def main():
    print("\n" + "="*50)
    print("🔧 Gerenciador Cloudflare Tunnel")
    print("="*50)
    
    # Verifica cloudflared
    if not check_cloudflared():
        print("\n⚠️  Cloudflared não está instalado.")
        if not install_cloudflared():
            print("Saindo...")
            sys.exit(1)
    else:
        result = subprocess.run(['cloudflared', '--version'], capture_output=True, text=True)
        print(f"\n✅ {result.stdout.strip()}")
    
    print("\n📋 Opções:")
    print("  1. Iniciar aplicação com Cloudflare Tunnel")
    print("  2. Testar tunnel com URL pública")
    print("  3. Ver informações de instalação")
    print("  4. Sair")
    
    choice = input("\nEscolha uma opção (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Iniciando aplicação com Cloudflare Tunnel...")
        print("   Pressione Ctrl+C para parar.\n")
        os.system("python app.py")
        
    elif choice == "2":
        print("\n🧪 Testando tunnel...")
        result = subprocess.run(['cloudflared', 'tunnel', '--hello-world'], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        input("\nPressione Enter para sair...")
        
    elif choice == "3":
        print("\n📖 Veja CLOUDFLARE_SETUP.md para mais detalhes.")
        input("\nPressione Enter para sair...")
        
    elif choice == "4":
        print("\nSaindo...")
        sys.exit(0)
    else:
        print("❌ Opção inválida!")
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEncerrando...")
        sys.exit(0)
