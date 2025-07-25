import pandas as pd
import sqlite3
import os

# Ruta a la base de datos
DB_PATH = os.path.join("database", "pedidos.db")
EXCEL_PATH = os.path.join("data", "productos_master.xlsx")

def cargar_insumos():
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ Archivo no encontrado: {EXCEL_PATH}")
        return

    # Leer el archivo Excel
    df = pd.read_excel(EXCEL_PATH)

    # Validación mínima
    columnas_esperadas = ['id_insumo', 'codigo_ins', 'descripcion', 'id_medida', 'id_categoria', 'status']
    if not all(col in df.columns for col in columnas_esperadas):
        print("❌ El archivo Excel no tiene todas las columnas necesarias.")
        return

    # Conexión a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    insertados = 0
    errores = 0

    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO t_insumos (
                    id_insumo, codigo_ins, descripcion,
                    id_medida, id_categoria, status
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                int(row['id_insumo']),
                str(row['codigo_ins']).strip(),
                str(row['descripcion']).strip(),
                int(row['id_medida']),
                int(row['id_categoria']),
                str(row['status']).strip().capitalize()  # Activo/Inactivo
            ))
            insertados += 1
        except sqlite3.IntegrityError as e:
            print(f"⚠️ Ya existe o error con código: {row['codigo_ins']} -> {e}")
            errores += 1
        except Exception as e:
            print(f"❌ Error con el registro {row.to_dict()} -> {e}")
            errores += 1

    conn.commit()
    conn.close()

    print(f"✅ Carga completada. {insertados} insumos insertados, {errores} errores.")

# Ejecutar directamente
if __name__ == "__main__":
    cargar_insumos()