# Changelog
Todos los cambios relevantes de este proyecto se documentarán en este archivo.

El formato sigue las recomendaciones de **Keep a Changelog**  
https://keepachangelog.com/es-ES/1.0.0/

Y el versionado sigue **Semantic Versioning (SemVer)**  
https://semver.org/lang/es/

---

## [0.0.1] - 2026-05-03
### Added
- Estructura inicial del proyecto GTC.
- API base desarrollada con FastAPI.
- Modelos iniciales para contratos, extractos, movimientos y pagos.
- Servicios de facturación y movimientos.
- Endpoints principales:
  - `/movimientos/crear`
  - `/facturacion/saldos/{id_contrato}/{num_extracto}`
  - `/facturacion/pagos`
  - `/health`
- Sistema de migraciones con Flyway (carpeta `db/migrations`).
- Configuración de base de datos PostgreSQL.
- Tests automatizados con Pytest:
  - Facturación
  - Movimientos
  - Healthcheck
- Integración continua con GitHub Actions:
  - Instalación de dependencias
  - Arranque de PostgreSQL
  - Ejecución de migraciones Flyway
  - Ejecución de tests
- Estructura modular del proyecto:
  - `routers/`
  - `services/`
  - `models/`
  - `schemas/`
  - `config.py`

### Changed
- Reset completo del historial Git para iniciar un repositorio limpio.
- Reorganización del proyecto para alinearlo con buenas prácticas de FastAPI.

### Fixed
- Corrección de rutas relativas en tests.
- Creación del endpoint `/health` para evitar errores 404 en CI.
- Ajustes en CI para ejecutar migraciones antes de los tests.

---

## [Unreleased]
- Nuevas funcionalidades de facturación.
- Integración de reglas de negocio avanzadas.
- Generación automática de extractos.
- Motor de simulación de movimientos.
