# 📘 GTC – Gestión de Transacciones y Contratos  
### Backend API (FastAPI + PostgreSQL)

Este proyecto implementa una API modular para la gestión de movimientos asociados a contratos, incluyendo un **Simulador de Movimientos** que permite probar operaciones antes de persistirlas en la base de datos.

La arquitectura está diseñada para ser limpia, escalable y fácilmente extensible, siguiendo buenas prácticas de separación por capas: *schemas*, *models*, *routers* y *db session*.

Hola Mario.

---

## 🏗️ Estructura del proyecto

```
api/
├── Dockerfile
├── pyproject.toml
├── src/
│   └── gtc_api/
│       ├── __init__.py
│       ├── config.py
│       ├── db/
│       │   └── session.py
│       ├── main.py
│       ├── models/
│       │   └── movimientos.py
│       ├── routers/
│       │   └── movimientos.py
│       └── schemas/
│           └── movimientos.py
└── tests/
```

### Componentes principales

| Carpeta | Descripción |
|--------|-------------|
| `config.py` | Configuración general y construcción del `DATABASE_URL`. |
| `db/session.py` | Conexión a PostgreSQL usando `databases`. |
| `schemas/` | Modelos Pydantic para validación de entrada. |
| `models/` | Modelos SQLAlchemy y sentencias SQL raw. |
| `routers/` | Endpoints FastAPI organizados por dominio. |
| `main.py` | Punto de entrada de la API y registro de routers. |

---

## 🗄️ Base de datos

La tabla principal gestionada por la API es:

```
gtc.movimiento_contrato
```

Incluye información de movimientos financieros asociados a contratos, como importe, fechas, tipo de operación, comercio, categoría, estado y origen.

---

## 🚀 Endpoints principales

### 🔹 Simulador de Movimientos

Permite simular y/o registrar movimientos en la tabla `gtc.movimiento_contrato`.

---

### **POST /simulador/procesar**

Simula un movimiento sin guardarlo.

- Valida los datos con `MovimientoCreate`
- Ejecuta una simulación mock (pendiente de motor real)
- Devuelve evaluación, riesgo y detalle

Ejemplo de entrada:

```json
{
  "id_contrato": "12345",
  "fecha_operacion": "2024-01-01T10:00:00",
  "fecha_contable": "2024-01-01",
  "importe": 100.50,
  "moneda": "EUR",
  "signo": "D",
  "tipo_movimiento": "COMPRA"
}
```

---

### **POST /simulador/guardar**

Inserta un movimiento en la base de datos.

- Usa SQL raw (`INSERT_MOVIMIENTO`)
- Devuelve el `id_movimiento` generado

---

## ⚙️ Arranque del proyecto

### Con Docker Compose

Desde la raíz del proyecto:

```bash
docker-compose up --build
```

Esto levanta:

- PostgreSQL  
- Flyway (migraciones)  
- API FastAPI  

---

## 📄 Documentación interactiva

Disponible en:

```
http://localhost:8000/docs
```

---

## 📌 Estado actual del proyecto

- ✔️ Conexión a PostgreSQL funcionando  
- ✔️ Migraciones iniciales aplicadas  
- ✔️ Modelo SQLAlchemy `MovimientoContrato`  
- ✔️ Schema `MovimientoCreate` con origen `"SIMULADOR"`  
- ✔️ Endpoint `/simulador/procesar`  
- ✔️ Endpoint `/simulador/guardar`  
- ⏳ Motor de reglas pendiente  
- ⏳ Pantalla frontend del simulador pendiente  

---

## 🛠️ Próximos pasos sugeridos

1. Implementar motor de reglas / scoring  
2. Añadir logs de simulación  
3. Crear pantalla del simulador (React/Vue)  
4. Añadir tests automáticos  
5. Añadir autenticación (si aplica)  

# Esta es una modificación para probar el runner
Modificando workflow CI
