from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Montar carpeta 'static' para estilos, logos, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Usar carpeta 'templates' para HTML con Jinja2
templates = Jinja2Templates(directory="templates")

# Ruta base - homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "titulo": "Recepción de Pedidos - Artisan"})