from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import os
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

DB_PATH = os.path.join("database", "pedidos.db")

@router.get("/crear-pedido")
def mostrar_formulario(request: Request):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id_sucursal, descripcion FROM t_sucursales")
    sucursales = cursor.fetchall()

    cursor.execute("SELECT id_responsable, nombre_responsable || ' ' || apellido_responsable FROM t_responsable WHERE activo = 'Si'")
    responsables = cursor.fetchall()

    cursor.execute("SELECT id_insumo, descripcion FROM t_insumos")
    insumos = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse("crear_pedido.html", {
        "request": request,
        "sucursales": sucursales,
        "responsables": responsables,
        "insumos": insumos
    })


@router.post("/crear-pedido")
def procesar_pedido(
    request: Request,
    sucursal: int = Form(...),
    responsable: int = Form(...),
    insumo: int = Form(...),
    cantidad: int = Form(...),
    prioridad: str = Form(...),
    observaciones: str = Form("")
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fecha_actual = datetime.now().strftime("%d/%m/%y")
    
    cursor.execute("""
        INSERT INTO t_pedido (codigo_pedido, fecha_pedido, id_sucursal, id_responsable, cantidad, observaciones, prioridad)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "pendiente_codigo", fecha_actual, sucursal, responsable, cantidad, observaciones, prioridad
    ))

    pedido_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO t_detalles_pedido (id_pedido, id_insumo, cantidad)
        VALUES (?, ?, ?)
    """, (
        pedido_id, insumo, cantidad
    ))

    conn.commit()
    conn.close()

    return RedirectResponse(url="/crear-pedido", status_code=303)