-- ============================================
-- V003 - Creación de tabla param_general
-- ============================================

-- Crear tabla en el esquema GTC
CREATE TABLE IF NOT EXISTS gtc.param_general (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor VARCHAR(500) NOT NULL,
    fecha_insercion TIMESTAMP DEFAULT now() NOT NULL,
    fecha_actualiza TIMESTAMP DEFAULT now() NOT NULL
);

-- Índices adicionales (opcional pero recomendado)
CREATE INDEX IF NOT EXISTS idx_param_general_clave
    ON gtc.param_general (clave);

-- Insertar parámetros iniciales (idempotente)
INSERT INTO gtc.param_general (clave, valor)
VALUES 
    ('fecha_proceso', '2024-01-01'),
    ('fecha_contable', '2024-01-01')
ON CONFLICT (clave) DO NOTHING;
