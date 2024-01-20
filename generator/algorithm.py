# Matriz de direcciones
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
# Estado objetivo del rompecabezas
END = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# Clase Node para almacenar el estado del rompecabezas y la información relacionada
class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node # Estado actual del rompecabezas
        self.previous_node = previous_node # Nodo anterior en el camino
        self.g = g # Costo acumulado del camino desde el estado inicial hasta este nodo
        self.h = h # Heurística (distancia euclidiana desde el estado actual hasta el objetivo)
        self.dir = dir # Dirección de movimiento que lleva a este estado desde el nodo anterior

    def f(self):
        """
        Función heurística total (f) para evaluar la prioridad de un nodo en el algoritmo A*.
        Calcula la suma del costo acumulado del camino (g) y la heurística (h).

        Returns:
            float: Valor heurístico total del nodo.
        """
        return self.g + self.h

# Función para obtener la posición de un elemento en el rompecabezas
def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))

# Función heurística para calcular la distancia euclidiana
def euclidianCost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

# Función para obtener nodos adyacentes en el rompecabezas
def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = [row[:] for row in node.current_node]  # Copy the matrix without using deepcopy
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode.append(Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir))

    return listNode

# Función para obtener el mejor nodo del conjunto abierto basado en la heurística
def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

# Función para construir el camino óptimo a partir del conjunto cerrado
def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

# Función principal para obtener la lista de movimientos para resolver el rompecabezas
def get_movements(start_matrix):
    open_set = {str(start_matrix): Node(start_matrix, start_matrix, 0, euclidianCost(start_matrix), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            # Verificar si el nuevo nodo ya está en el conjunto cerrado o en el conjunto abierto y si su f() es menor
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        # Eliminar el nodo actual del conjunto abierto
        del open_set[str(test_node.current_node)]
