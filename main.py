from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from config.database import create_tables
from config.settings import settings
from views.auth_views import auth_router
from views.user_views import user_router

# Criar instância do FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Montar arquivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(auth_router)
app.include_router(user_router)

# Criar tabelas do banco de dados
create_tables()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve a página de login"""
    with open("static/login.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {"status": "healthy", "message": "API funcionando corretamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
