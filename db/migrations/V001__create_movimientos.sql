CREATE SCHEMA IF NOT EXISTS gtc;

CREATE TABLE IF NOT EXISTS gtc.movimiento_contrato (
    id_movimiento        BIGSERIAL PRIMARY KEY,
    id_contrato          VARCHAR(50) NOT NULL,           -- ahora alfanumérico
    fecha_operacion      TIMESTAMP   NOT NULL,
    fecha_contable       DATE        NOT NULL,
    importe              NUMERIC(18,2) NOT NULL,
    moneda               CHAR(3)     NOT NULL,
    signo                CHAR(1)     NOT NULL,           -- D/H
    tipo_movimiento      VARCHAR(50) NOT NULL,
    descripcion          VARCHAR(255),
    comercio             VARCHAR(255),
    categoria            VARCHAR(100),
    codigo_autorizacion  VARCHAR(50),
    estado               VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE',
    origen               VARCHAR(50),
    referencia_externa   VARCHAR(100),
    creado_en            TIMESTAMP   NOT NULL DEFAULT NOW(),
    actualizado_en       TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_mov_contrato_fecha
    ON gtc.movimiento_contrato (id_contrato, fecha_contable);

CREATE INDEX IF NOT EXISTS idx_mov_contrato_ref_ext
    ON gtc.movimiento_contrato (referencia_externa);
