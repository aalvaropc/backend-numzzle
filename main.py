from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.numzzle import numzzle

app = FastAPI(
    title="NumzzleBackend",
    description="Retorna la lista de movimientos para resolver un puzzle 3x3",
    version="1.0.0",
)

# Configurar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(numzzle)
