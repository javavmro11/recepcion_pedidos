import sqlite3
import os

# Crear la carpeta si no existe
os.makedirs("database", exist_ok=True)

# Ruta a la base de datos
db_path = "database/pedidos.db"

# Verificar si la base de datos ya existe
if os.path.exists(db_path):
    print("⚠️ La base de datos ya existe. No se volverá a crear.")
else:
    # Conectar a SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tablas
    cursor.executescript("""

    CREATE TABLE t_sucursales (
        id_sucursal INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        direccion TEXT,
        telefono TEXT
    );

    CREATE TABLE t_categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL
    );

    CREATE TABLE t_medidas (
        id_medida INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL
    );

    CREATE TABLE t_insumos (
        id_insumo INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_ins TEXT UNIQUE NOT NULL,
        descripcion TEXT NOT NULL,
        id_medida INTEGER NOT NULL,
        id_categoria INTEGER,
        status TEXT DEFAULT 'activo',
        FOREIGN KEY (id_medida) REFERENCES t_medidas(id_medida),
        FOREIGN KEY (id_categoria) REFERENCES t_categorias(id_categoria)
    );

    CREATE TABLE t_insumo_sucursal (
        id_insumo INTEGER,
        id_sucursal INTEGER,
        PRIMARY KEY (id_insumo, id_sucursal),
        FOREIGN KEY (id_insumo) REFERENCES t_insumos(id_insumo),
        FOREIGN KEY (id_sucursal) REFERENCES t_sucursales(id_sucursal)
    );

    CREATE TABLE t_responsables (
        id_responsable INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT,
        telefono TEXT,
        id_sucursal INTEGER,
        activo TEXT DEFAULT 'Si',
        FOREIGN KEY (id_sucursal) REFERENCES t_sucursales(id_sucursal)
    );

    CREATE TABLE t_estado_pedido (
        id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL
    );

    CREATE TABLE t_pedidos (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_pedido TEXT UNIQUE NOT NULL,
        fecha_pedido TEXT NOT NULL,
        id_sucursal INTEGER,
        id_responsable INTEGER,
        observaciones TEXT,
        prioridad TEXT CHECK(prioridad IN ('Alta', 'Media', 'Baja')),
        id_estado INTEGER DEFAULT 1,
        FOREIGN KEY (id_sucursal) REFERENCES t_sucursales(id_sucursal),
        FOREIGN KEY (id_responsable) REFERENCES t_responsables(id_responsable),
        FOREIGN KEY (id_estado) REFERENCES t_estado_pedido(id_estado)
    );

    CREATE TABLE t_detalles_pedido (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER,
        id_insumo INTEGER,
        cantidad REAL NOT NULL,
        unidad TEXT,
        FOREIGN KEY (id_pedido) REFERENCES t_pedidos(id_pedido),
        FOREIGN KEY (id_insumo) REFERENCES t_insumos(id_insumo)
    );

    INSERT INTO t_estado_pedido (descripcion) VALUES 
        ('pendiente'), ('procesado'), ('enviado'), ('entregado'), ('cancelado');

    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos creada exitosamente con todas las tablas.")
