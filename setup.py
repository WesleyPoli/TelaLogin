#!/usr/bin/env python3
"""
Script de configuração inicial do sistema de login
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro: {e.stderr}")
        return False

def create_env_file():
    """Cria arquivo .env se não existir"""
    if not os.path.exists('.env'):
        print("📝 Criando arquivo .env...")
        with open('.env', 'w') as f:
            f.write("""# Configurações do Banco de Dados
DATABASE_URL=postgresql://postgres:password@localhost:5432/login_db

# Configurações de Segurança
SECRET_KEY=your-secret-key-here-change-in-production

# Configurações da Aplicação
DEBUG=True
""")
        print("✅ Arquivo .env criado!")
    else:
        print("ℹ️  Arquivo .env já existe")

def main():
    """Função principal de setup"""
    print("🚀 Configurando Sistema de Login - Arquitetura MVC")
    print("=" * 50)
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    
    # Criar arquivo .env
    create_env_file()
    
    # Instalar dependências
    if not run_command("pip install -r requirements.txt", "Instalando dependências Python"):
        print("❌ Falha ao instalar dependências")
        sys.exit(1)
    
    print("\n🎉 Configuração concluída!")
    print("\n📋 Próximos passos:")
    print("1. Configure o PostgreSQL:")
    print("   - Crie o banco: createdb login_db")
    print("   - Ou use Docker: docker-compose up -d postgres")
    print("\n2. Execute a aplicação:")
    print("   python main.py")
    print("\n3. Acesse:")
    print("   - Frontend: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("\n4. Para usar Docker:")
    print("   docker-compose up -d")

if __name__ == "__main__":
    main()
