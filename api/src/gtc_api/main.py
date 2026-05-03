from fastapi import FastAPI
from gtc_api.routers.movimientos import router as movimientos_router, sim_router as simulador_router
from gtc_api.routers.facturacion import router as facturacion_router
from gtc_api.routers import parametrizacion

app = FastAPI(title="GTC API")

# Registrar router principal de movimientos
app.include_router(movimientos_router, prefix="/movimientos", tags=["Movimientos"])

# Registrar router del simulador
app.include_router(simulador_router, prefix="/simulador", tags=["Simulador"])

# Registrar router del módulo de facturación
app.include_router(facturacion_router, prefix="/facturacion", tags=["Facturación"])

# Registrar router del módulo de parametrización
app.include_router(parametrizacion.router)
