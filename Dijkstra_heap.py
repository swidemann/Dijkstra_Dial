#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import numpy as np
import heapq
from Writing import read_node_quantity, read_arcs, write_sol

try:
    if len(sys.argv) != 2:
        raise Exception
    source_node = int(sys.argv[1])
except ValueError:
    sys.exit(f"Error: nodo fuente debe ser un número entero, {sys.argv[1]} rechazado")
except Exception as err:
    sys.exit("formato: Dijkstra_heap.py <int: nodo fuente>")

Testing = False


def initialize(node_quantity, source_node):
    """
    node_quantity: int cantidad de nodos de la instancia
    source_node: int nodo fuente
    función que inicializa los arreglos de predecesores y distancias
    """
    predecessors = np.array([None for i in range(node_quantity+1)])
    distances = np.array([np.inf for i in range(node_quantity+1)])

    # inicializar nodo fuente
    predecessors[source_node] = source_node
    distances[source_node] = 0
    distancias_parciales = [(distances[n], n) for n in range(1, node_quantity+1)]
    heapq.heapify(distancias_parciales)

    return predecessors, distances, distancias_parciales



def Dijkstra(node_quantity, source_node, arcs, V):
    """
    node_quantity: int cantidad de nodos de la instancia
    source_node: int nodo fuente
    arcs: estructura con arcos y sus costos
    V: diccionario de nodos alcanzables desde el nodo llave
    función que aplica el algoritmo de Dijkstra original
    """
    predecessors, distances, distancias_parciales = initialize(node_quantity, source_node)
    no_alcanzables = []
    while distancias_parciales:  # mientras queden nodos sin agregar
        dist_nodo, nodo = heapq.heappop(distancias_parciales)
        if dist_nodo == np.inf:  # nodo no alcanzable desde el nodo fuente
            # print(f"nodo INALCANZABLE: {nodo}")
            no_alcanzables.append(nodo)
        else:
            # print(f"nodo agregado: {nodo}, distancia: {distances[nodo]}")
            for j in V[nodo]:  # arcos que salen del nodo ingresado al árbol solución
                distancia_i_j = dist_nodo + arcs[(nodo, j)]
                if distances[j] > distancia_i_j:  # es mejor llegar a j a traves de i
                    distancias_parciales.remove( (distances[j], j) )  # cambiar el valor de la etiqueta sacando el item del heap
                    heapq.heapify(distancias_parciales)
                    heapq.heappush(distancias_parciales, (distancia_i_j, j))  # y agregandolo al heap en orden
                    distances[j] = distancia_i_j  # actualizar las distancias_parciales
                    predecessors[j] = nodo
    while no_alcanzables:  # finalizar los no alcanzables
        nodo = no_alcanzables.pop()
        predecessors[nodo] = 0
        distances[nodo] = -1

    return predecessors, distances

if __name__ == "__main__":
    print(f"Reading instance source node {source_node}...")
    start_time = time.time()
    node_quantity = read_node_quantity()
    arcs, V, max_cost = read_arcs()
    print(f"Size of arcs array: {round(sys.getsizeof(arcs)/1024)} kilobytes")
    read_time = time.time()
    print("Solving...")
    predecessors, distances = Dijkstra(node_quantity, source_node, arcs, V)
    solve_time = time.time()
    print("Writing solution...")
    if Testing:
        write_sol(source_node, node_quantity, predecessors, distances, f"salida_{source_node}_Dijkstra_heap.txt")
    else:
        write_sol(source_node, node_quantity, predecessors, distances)
    write_time = time.time()
    print(f"Total runtime: {write_time-start_time:.8f}. Reading: {read_time-start_time:.8f}, Solving: {solve_time-read_time:.8f}, Writing: {write_time-solve_time:.8f}")
    
    if Testing:
        with open("times_Dijkstra_heap.txt", "a") as file:
            file.write(f"{write_time-start_time:.8f}\n")

# ### MAXIMUM MEMORY USAGE
# os.system(f"grep VmPeak /proc/{os.getpid()}/status")    