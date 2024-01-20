# Matriz de direcciones
DIRECCIONES = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
# Estado objetivo del rompecabezas
OBJETIVO = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# Clase Node para almacenar el estado del rompecabezas y la información relacionada
class Nodo:
    def __init__(self, estado_actual, nodo_anterior, g, h, dir):
        self.estado_actual = estado_actual  # Estado actual del rompecabezas
        self.nodo_anterior = nodo_anterior  # Nodo anterior en el camino
        self.g = g  # Costo acumulado del camino desde el estado inicial hasta este nodo
        self.h = h  # Heurística (distancia euclidiana desde el estado actual hasta el objetivo)
        self.dir = dir  # Dirección de movimiento que lleva a este estado desde el nodo anterior

    def f(self):
        """
        Función heurística total (f) para evaluar la prioridad de un nodo en el algoritmo A*.
        Calcula la suma del costo acumulado del camino (g) y la heurística (h).

        Returns:
            float: Valor heurístico total del nodo.
        """
        return self.g + self.h

# Función para obtener la posición de un elemento en el rompecabezas
def obtener_pos(estado_actual, elemento):
    for fila in range(len(estado_actual)):
        if elemento in estado_actual[fila]:
            return (fila, estado_actual[fila].index(elemento))

# Función heurística para calcular la distancia euclidiana
def costo_euclidiano(estado_actual):
    costo = 0
    for fila in range(len(estado_actual)):
        for col in range(len(estado_actual[0])):
            pos = obtener_pos(OBJETIVO, estado_actual[fila][col])
            costo += abs(fila - pos[0]) + abs(col - pos[1])
    return costo

# Función para obtener nodos adyacentes en el rompecabezas
def obtener_nodos_adyacentes(nodo):
    lista_nodos = []
    pos_vacia = obtener_pos(nodo.estado_actual, 0)

    for dir in DIRECCIONES.keys():
        nueva_pos = (pos_vacia[0] + DIRECCIONES[dir][0], pos_vacia[1] + DIRECCIONES[dir][1])
        if 0 <= nueva_pos[0] < len(nodo.estado_actual) and 0 <= nueva_pos[1] < len(nodo.estado_actual[0]):
            nuevo_estado = [fila[:] for fila in nodo.estado_actual]
            nuevo_estado[pos_vacia[0]][pos_vacia[1]] = nodo.estado_actual[nueva_pos[0]][nueva_pos[1]]
            nuevo_estado[nueva_pos[0]][nueva_pos[1]] = 0
            lista_nodos.append(Nodo(nuevo_estado, nodo.estado_actual, nodo.g + 1, costo_euclidiano(nuevo_estado), dir))

    return lista_nodos

# Función para obtener el mejor nodo del conjunto abierto basado en la heurística
def obtener_mejor_nodo(conjunto_abierto):
    primera_iteracion = True

    for nodo in conjunto_abierto.values():
        if primera_iteracion or nodo.f() < mejor_f:
            primera_iteracion = False
            mejor_nodo = nodo
            mejor_f = mejor_nodo.f()
    return mejor_nodo

# Función para construir el camino óptimo a partir del conjunto cerrado
def construir_camino(conjunto_cerrado):
    nodo = conjunto_cerrado[str(OBJETIVO)]
    rama = list()

    while nodo.dir:
        rama.append({
            'dir': nodo.dir,
            'nodo': nodo.estado_actual
        })
        nodo = conjunto_cerrado[str(nodo.nodo_anterior)]
    rama.append({
        'dir': '',
        'nodo': nodo.estado_actual
    })
    rama.reverse()

    return rama

# Función principal para obtener la lista de movimientos para resolver el rompecabezas
def obtener_movimientos(estado_inicial):
    conjunto_abierto = {str(estado_inicial): Nodo(estado_inicial, estado_inicial, 0, costo_euclidiano(estado_inicial), "")}
    conjunto_cerrado = {}

    while True:
        nodo_prueba = obtener_mejor_nodo(conjunto_abierto)
        conjunto_cerrado[str(nodo_prueba.estado_actual)] = nodo_prueba

        if nodo_prueba.estado_actual == OBJETIVO:
            return construir_camino(conjunto_cerrado)

        nodos_adyacentes = obtener_nodos_adyacentes(nodo_prueba)
        for nodo in nodos_adyacentes:
            # Verificar si el nuevo nodo ya está en el conjunto cerrado o en el conjunto abierto y si su f() es menor
            if str(nodo.estado_actual) in conjunto_cerrado.keys() or str(nodo.estado_actual) in conjunto_abierto.keys() and conjunto_abierto[
                str(nodo.estado_actual)].f() < nodo.f():
                continue
            conjunto_abierto[str(nodo.estado_actual)] = nodo

        # Eliminar el nodo actual del conjunto abierto
        del conjunto_abierto[str(nodo_prueba.estado_actual)]