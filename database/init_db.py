import sqlite3
import os

# Crear carpeta si no existe
os.makedirs("database", exist_ok=True)

# Ruta de la base de datos
db_path = "database/pedidos.db"

# Si la base ya existe, no se vuelve a crear
if os.path.exists(db_path):
    print("⚠️ La base de datos ya existe. No se volverá a crear.")
else:
    # Conectar a la base SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear todas las tablas según las instrucciones
    cursor.executescript("""

    CREATE TABLE t_sucursales (
        id_sucursal INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        direccion TEXT,
        telefono TEXT
    );

    CREATE TABLE t_categorias (
        id_categoria INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL
    );

    CREATE TABLE t_medidas (
        id_medida INTEGER PRIMARY KEY,
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
        nombre_responsable TEXT NOT NULL,
        apellido_responsable TEXT,
        tlf_responsable TEXT,
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
        id_detalles_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER,
        id_insumo INTEGER,
        cantidad REAL NOT NULL,
        FOREIGN KEY (id_pedido) REFERENCES t_pedidos(id_pedido),
        FOREIGN KEY (id_insumo) REFERENCES t_insumos(id_insumo)
    );

    INSERT INTO t_medidas (id_medida, descripcion) VALUES
        (1, 'Gr'),
        (2, 'Ml'),
        (3, 'Unid');

    INSERT INTO t_categorias (id_categoria, descripcion) VALUES
        (1, 'Abarrotes'),
        (2, 'Aseo'),
        (3, 'Bebidas'),
        (4, 'Botanicos para Cocteleria'),
        (5, 'Carnicos'),
        (6, 'Cervezas'),
        (7, 'Desechables'),
        (8, 'Dulces y Topings'),
        (9, 'Empacados'),
        (10, 'Frutas'),
        (11, 'Gaseosas'),
        (12, 'Granos'),
        (13, 'Hierbas'),
        (14, 'Hortalizas'),
        (15, 'Lacteos'),
        (16, 'Licores'),
        (17, 'Oficina'),
        (18, 'Panaderia y Granja'),
        (19, 'Producidos'),
        (20, 'Ultraprocesados'),
        (21, 'Verduras'),
        (22, 'Hongos'),
        (23, 'Pulpas');

    INSERT INTO t_estado_pedido (descripcion) VALUES
        ('pendiente'), ('procesado'), ('enviado'), ('entregado'), ('cancelado');

    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos y tablas creadas correctamente.")
