from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.guardar_pedidos import procesar_pedido, obtener_insumos, obtener_responsables

app = FastAPI()

# Archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "titulo": "Recepción de Pedidos - Artisan"})

@app.get("/crear-pedido", response_class=HTMLResponse)
async def formulario_pedido(request: Request):
    insumos = obtener_insumos()
    responsables = obtener_responsables()
    return templates.TemplateResponse("crear_pedido.html", {
        "request": request,
        "insumos": insumos,
        "responsables": responsables,
        "mensaje": None
    })

@app.post("/crear-pedido", response_class=HTMLResponse)
async def guardar_pedido(
    request: Request,
    sucursal: str = Form(...),
    responsable: str = Form(...),
    insumo: str = Form(...),
    cantidad: int = Form(...),
    prioridad: str = Form(...),
    fecha: str = Form(...),
    observaciones: str = Form("")
):
    mensaje = procesar_pedido(sucursal, responsable, insumo, cantidad, prioridad, fecha, observaciones)
    insumos = obtener_insumos()
    responsables = obtener_responsables()
    return templates.TemplateResponse("crear_pedido.html", {
        "request": request,
        "mensaje": mensaje,
        "insumos": insumos,
        "responsables": responsables
    })
