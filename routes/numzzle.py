from fastapi import APIRouter
from dotenv import load_dotenv
from generator.algorithm import get_movements

load_dotenv()

numzzle = APIRouter()

@numzzle.get("/movements/")
async def process_text():
    start_matrix = [[5, 8, 6], [0, 4, 7], [2, 3, 1]]
    br = get_movements(start_matrix)

    total_steps = len(br) - 1
    movements = []

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

    response_data = {
        "list_move": movements,
        "total_steps": total_steps
    }

    return response_data