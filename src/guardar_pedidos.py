import sqlite3
from datetime import datetime

DB_PATH = "database/pedidos.db"

def obtener_insumos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id_insumo, descripcion FROM t_insumos WHERE status = 'activo'")
    insumos = cursor.fetchall()
    conn.close()
    return insumos

def obtener_responsables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id_responsable, nombre_responsable FROM t_responsable")
    responsables = cursor.fetchall()
    conn.close()
    return responsables

def generar_codigo_pedido(sucursal):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM t_pedido WHERE id_sucursal = ?", (sucursal,))
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"{sucursal}_{str(count).zfill(4)}"

def procesar_pedido(sucursal, responsable, insumo, cantidad, prioridad, fecha, observaciones):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        codigo = generar_codigo_pedido(sucursal)

        cursor.execute("""
            INSERT INTO t_pedido (
                codigo_pedido, fecha_pedido, id_sucursal, id_responsable, cantidad, observaciones, prioridad
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (codigo, fecha, sucursal, responsable, cantidad, observaciones, prioridad))

        id_pedido = cursor.lastrowid

        cursor.execute("""
            INSERT INTO t_detalle_pedido (id_pedido, id_insumo, cantidad)
            VALUES (?, ?, ?)
        """, (id_pedido, insumo, cantidad))

        conn.commit()
        conn.close()
        return f"✅ Pedido guardado correctamente con código: {codigo}"
    except Exception as e:
        return f"❌ Error al guardar el pedido: {e}"
