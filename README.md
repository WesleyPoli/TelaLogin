# Sistema de Login 

Equipe:
Daniel Henrique Braga da Silva - 14565431


Wesley Oliveira Cunha - 14612367

## Execução

```bash
# Navegar para o projeto
cd caminho_projeto

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate
```

### **Instalar Dependências**
```bash
pip install -r requirements.txt

pip install python-dotenv

pip install pydantic email-validator

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart pydantic[email] alembic
```

### **Passo 3: Configurar Banco de Dados**
```bash
# O banco de dados que usamos foi o disponibilizado no site da disciplina. Conectamos com .env. Pode ser configurado diretamente em config/settings.py
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME")

### **Passo 4: Executar Aplicação**
```bash
python main.py
```
### **Passo 5: Acessar Sistema**
- **Frontend**: http://localhost:8000

# Desativar ambiente virtual
```bash
deactivate
```

