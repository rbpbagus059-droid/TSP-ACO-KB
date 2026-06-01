import random
import numpy as np

graph = {
    'A': {'#': 3, 'C': 6},
    '#': {'A': 3, 'C': 2, 'G': 5},
    'C': {'A': 6, '#': 2, 'F': 4, 'B': 9},
    'F': {'C': 4, 'E': 2},
    'E': {'F': 2, 'G': 1, 'H': 1, 'D': 7},
    'G': {'#': 5, 'E': 1, 'H': 3},
    'H': {'G': 3, 'E': 1, 'D': 9},
    'D': {'H': 9, 'E': 7, 'B': 8},
    'B': {'C': 9, 'D': 8}
}

nodes = list(graph.keys())

num_ants = 20
num_iterations = 100

alpha = 1
beta = 2

evaporation = 0.5
Q = 100

pheromone = {}

for node in graph:
    pheromone[node] = {}
    for neighbor in graph[node]:
        pheromone[node][neighbor] = 1.0

def route_length(route):

    total = 0

    for i in range(len(route)-1):
        total += graph[route[i]][route[i+1]]

    return total


def choose_next(current, visited):

    candidates = []

    for neighbor in graph[current]:

        if neighbor not in visited:

            tau = pheromone[current][neighbor] ** alpha
            eta = (1 / graph[current][neighbor]) ** beta

            candidates.append((neighbor, tau * eta))

    if len(candidates) == 0:
        return None

    total = sum(prob for _, prob in candidates)

    r = random.random() * total

    cumulative = 0

    for node, prob in candidates:
        cumulative += prob

        if cumulative >= r:
            return node

    return candidates[-1][0]


def construct_solution():

    start = 'H'
    target = 'D'
    must_visit = '#'

    current = start

    route = [start]
    visited = {start}

    found_hash = False

    while True:

        if current == must_visit:
            found_hash = True

        if current == target and found_hash:
            break

        nxt = choose_next(current, visited)

        if nxt is None:
            return None

        route.append(nxt)
        visited.add(nxt)

        current = nxt

    return route

best_route = None
best_distance = float('inf')

for iteration in range(num_iterations):

    all_routes = []

    for ant in range(num_ants):

        route = construct_solution()

        if route is not None:

            distance = route_length(route)

            all_routes.append((route, distance))

            if distance < best_distance:

                best_distance = distance
                best_route = route

    for i in pheromone:
        for j in pheromone[i]:
            pheromone[i][j] *= (1 - evaporation)

    for route, distance in all_routes:

        deposit = Q / distance

        for i in range(len(route)-1):

            a = route[i]
            b = route[i+1]

            pheromone[a][b] += deposit
            pheromone[b][a] += deposit

print("=== HASIL TERBAIK ===")
print("Rute :", " -> ".join(best_route))
print("Total Jarak :", best_distance)