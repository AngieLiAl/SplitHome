-- ============================================================
-- SCRIPT DDL + DML - SplitHome: Gestor de Gastos Compartidos
-- Motor: PostgreSQL 15+
-- ============================================================

-- Eliminar la BD si ya existe (en PostgreSQL se hace desde fuera)
-- Ejecuta esto primero en la BD "postgres" si necesitas recrearla:
-- DROP DATABASE IF EXISTS splithome_db;
-- CREATE DATABASE splithome_db;

-- ============================================================
-- TABLA: persona
-- ============================================================
CREATE TABLE persona (
    id_persona      SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    email           VARCHAR(150) UNIQUE,
    fecha_registro  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- TABLA: categoria
-- ============================================================
CREATE TABLE categoria (
    id_categoria INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre       VARCHAR(80) NOT NULL UNIQUE,
    icono        VARCHAR(10) NULL,
    descripcion  TEXT NULL
);

-- ============================================================
-- TABLA: gasto
-- ============================================================
CREATE TABLE gasto (
    id_gasto      SERIAL PRIMARY KEY,
    descripcion   VARCHAR(200) NOT NULL,
    monto         DECIMAL(10,2) NOT NULL
                  CHECK (monto >= 0),
    fecha         DATE NOT NULL
                  DEFAULT CURRENT_DATE,
    es_compartido BOOLEAN NOT NULL DEFAULT FALSE,
    id_persona    INT NOT NULL,
    id_categoria  INT NOT NULL,

    CONSTRAINT FK_Gasto_Persona
        FOREIGN KEY (id_persona)
        REFERENCES persona(id_persona)
        ON DELETE NO ACTION,

    CONSTRAINT FK_Gasto_Categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categoria(id_categoria)
        ON DELETE NO ACTION
);

-- ============================================================
-- TABLA INTERMEDIA: participacion (N:M gasto-persona)
-- ============================================================
CREATE TABLE participacion (
    id_gasto        INT NOT NULL,
    id_persona      INT NOT NULL,

    proporcion      DECIMAL(5,2) NOT NULL
                    DEFAULT 50.00
                    CHECK (proporcion > 0 AND proporcion <= 100),

    monto_asignado  DECIMAL(10,2) NOT NULL,

    CONSTRAINT PK_Participacion
        PRIMARY KEY (id_gasto, id_persona),

    CONSTRAINT FK_Participacion_Gasto
        FOREIGN KEY (id_gasto)
        REFERENCES gasto(id_gasto)
        ON DELETE CASCADE,

    CONSTRAINT FK_Participacion_Persona
        FOREIGN KEY (id_persona)
        REFERENCES persona(id_persona)
        ON DELETE NO ACTION
);

-- ============================================================
-- ÍNDICES
-- ============================================================
CREATE INDEX idx_gasto_persona
ON gasto(id_persona);

CREATE INDEX idx_gasto_categoria
ON gasto(id_categoria);

CREATE INDEX idx_gasto_fecha
ON gasto(fecha);

CREATE INDEX idx_part_persona
ON participacion(id_persona);

-- ============================================================
-- DATOS DE PRUEBA
-- ============================================================

INSERT INTO persona (nombre, email)
VALUES
    ('Angie Lizarsaburu', 'angie@splithome.pe'),
    ('Angela Escobedo',   'angela@splithome.pe');

INSERT INTO categoria (nombre, icono)
VALUES
    ('Alquiler',  '🏠'),
    ('Luz',       '💡'),
    ('Agua',      '💧'),
    ('Internet',  '📶'),
    ('Comida',    '🍛'),
    ('Limpieza',  '🧹'),
    ('Otros',     '📦');

INSERT INTO gasto
(descripcion, monto, fecha, id_persona, id_categoria)
VALUES
    ('Alquiler Enero',  1200.00, '2025-01-01', 1, 1),
    ('Recibo de Luz',     85.00, '2025-01-10', 2, 2),
    ('Recibo de Agua',    60.00, '2025-01-12', 2, 3),
    ('Internet mensual',  99.00, '2025-01-15', 1, 4),
    ('Mercado semanal',  180.00, '2025-01-05', 2, 5);

-- ============================================================
-- PARTICIPACIONES DE EJEMPLO
-- ============================================================

INSERT INTO participacion
(id_gasto, id_persona, proporcion, monto_asignado)
VALUES
(1, 1, 50.00, 600.00),
(1, 2, 50.00, 600.00),

(2, 1, 50.00, 42.50),
(2, 2, 50.00, 42.50),

(3, 1, 50.00, 30.00),
(3, 2, 50.00, 30.00),

(4, 1, 50.00, 49.50),
(4, 2, 50.00, 49.50),

(5, 1, 50.00, 90.00),
(5, 2, 50.00, 90.00);

-- ============================================================
-- CONSULTA DE VERIFICACIÓN
-- ============================================================

SELECT
    g.id_gasto,
    g.descripcion,
    g.monto,
    p.nombre AS responsable,
    c.nombre AS categoria
FROM gasto g
INNER JOIN persona p
    ON g.id_persona = p.id_persona
INNER JOIN categoria c
    ON g.id_categoria = c.id_categoria;