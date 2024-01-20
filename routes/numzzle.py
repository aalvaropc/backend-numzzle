# numzzle.py

from fastapi import APIRouter
from dotenv import load_dotenv
from generator.algorithm import obtener_movimientos

load_dotenv()

numzzle = APIRouter()

@numzzle.get("/movements/")
async def process_text():
    # Estado inicial del rompecabezas
    start_matrix = [[5, 8, 6], [0, 4, 7], [2, 3, 1]]
    
    # Obtener la lista de movimientos para resolver el rompecabezas
    br = obtener_movimientos(start_matrix)

    # Calcular el total de pasos para resolver el rompecabezas
    total_steps = len(br) - 1
    movements = []

    # Convertir códigos de dirección en movimientos legibles por humanos
    for b in br:
        if b['dir'] != '':
            letter = ''
            if b['dir'] == 'U':
                letter = 'UP'
            elif b['dir'] == 'R':
                letter = 'RIGHT'
            elif b['dir'] == 'L':
                letter = 'LEFT'
            elif b['dir'] == 'D':
                letter = 'DOWN'

            movements.append(letter)

    # Preparar datos de respuesta
    response_data = {
        "movimientos": movements,
        "total_pasos": total_steps
    }

    return response_data