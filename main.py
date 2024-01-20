from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.numzzle import numzzle

app = FastAPI(
    title="NumzzleBackend",
    description="Retorna la lista de movimientos para resolver un puzzle 3x3",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(numzzle)