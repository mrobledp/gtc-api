-- ============================================
-- V002 - Tablas para facturación y saldos GTC
-- ============================================

CREATE SCHEMA IF NOT EXISTS gtc;

-- ============================================
-- 1. Tabla paramétrica: tipo_trx_saldo
-- ============================================
CREATE TABLE IF NOT EXISTS gtc.tipo_trx_saldo (
    tipo_movimiento        VARCHAR(50) PRIMARY KEY,
    tipo_saldo             VARCHAR(50) NOT NULL,
    descripcion            VARCHAR(255),
    activo                 BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en              TIMESTAMP NOT NULL DEFAULT NOW(),
    actualizado_en         TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================
-- 2. Tabla paramétrica: param_saldo
-- ============================================
CREATE TABLE IF NOT EXISTS gtc.param_saldo (
    tipo_saldo             VARCHAR(50) PRIMARY KEY,
    descripcion            VARCHAR(255),
    interes_anual          NUMERIC(5,2) NOT NULL,
    forma_calculo          VARCHAR(50) NOT NULL,   -- 360, 365, simple, compuesto...
    pct_pago_minimo        NUMERIC(5,2) NOT NULL,
    comisiones             JSONB,
    gastos                 JSONB,
    activo                 BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en              TIMESTAMP NOT NULL DEFAULT NOW(),
    actualizado_en         TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================
-- 3. Tabla de acumulación de saldos: saldos_factura
-- ============================================
CREATE TABLE IF NOT EXISTS gtc.saldos_factura (
    id_contrato            VARCHAR(50) NOT NULL,
    num_extracto           INTEGER NOT NULL,
    tipo_saldo             VARCHAR(50) NOT NULL,
    saldo_acumulado        NUMERIC(18,2) NOT NULL DEFAULT 0,
    saldo_amortizado       NUMERIC(18,2) NOT NULL DEFAULT 0,
    saldo_diario           JSONB,
    aplicacion_pagos       JSONB,
    creado_en              TIMESTAMP NOT NULL DEFAULT NOW(),
    actualizado_en         TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id_contrato, num_extracto, tipo_saldo)
);

-- ============================================
-- 4. Tabla de pagos: pagos_contrato
-- ============================================
CREATE TABLE IF NOT EXISTS gtc.pagos_contrato (
    id_pago                BIGSERIAL PRIMARY KEY,
    id_contrato            VARCHAR(50) NOT NULL,
    num_extracto           INTEGER NOT NULL,
    fecha_pago             DATE NOT NULL,
    importe_pago           NUMERIC(18,2) NOT NULL,
    metodo_pago            VARCHAR(50),
    referencia_externa     VARCHAR(100),
    detalle_aplicacion     JSONB,
    creado_en              TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pagos_contrato_extracto
    ON gtc.pagos_contrato (id_contrato, num_extracto);

-- ============================================
-- 5. Tabla de extractos: extractos
-- ============================================
CREATE TABLE IF NOT EXISTS gtc.extractos (
    id_contrato            VARCHAR(50) NOT NULL,
    num_extracto           INTEGER NOT NULL,
    fecha_apertura         DATE NOT NULL,
    fecha_cierre           DATE,
    estado                 VARCHAR(30) NOT NULL DEFAULT 'ABIERTO',
    creado_en              TIMESTAMP NOT NULL DEFAULT NOW(),
    actualizado_en         TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id_contrato, num_extracto)
);

-- ============================================
-- 6. Tabla de contratos: contratos
-- ============================================
CREATE TABLE IF NOT EXISTS gtc.contratos (
    id_contrato            VARCHAR(50) PRIMARY KEY,
    extracto_abierto       INTEGER NOT NULL DEFAULT 1,
    limite_credito         NUMERIC(18,2),
    saldo_disponible       NUMERIC(18,2),
    estado                 VARCHAR(30) NOT NULL DEFAULT 'ACTIVO',
    creado_en              TIMESTAMP NOT NULL DEFAULT NOW(),
    actualizado_en         TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================
-- Índices adicionales recomendados
-- ============================================

CREATE INDEX IF NOT EXISTS idx_saldos_factura_extracto
    ON gtc.saldos_factura (id_contrato, num_extracto);

CREATE INDEX IF NOT EXISTS idx_extractos_estado
    ON gtc.extractos (estado);

CREATE INDEX IF NOT EXISTS idx_contratos_estado
    ON gtc.contratos (estado);
