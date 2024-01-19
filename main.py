from fastapi import FastAPI
from routes.numzzle import numzzle
app = FastAPI(
    title="NumzzleBackend",
    description="retorna la lista de movimientos para resolver un puzzle 3x3",
    version="1.0.0",
)

app.include_router(numzzle)