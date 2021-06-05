#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import numpy as np
from Writing import read_node_quantity, read_arcs, write_sol

try:
    if len(sys.argv) != 2:
        raise Exception
    source_node = int(sys.argv[1])
except ValueError:
    sys.exit(f"Error: nodo fuente debe ser un número entero, {sys.argv[1]} rechazado")
except Exception as err:
    sys.exit("formato: Dial.py <int: nodo fuente>")

Testing = False


def initialize(node_quantity, source_node, max_cost):
    """
    node_quantity: int cantidad de nodos de la instancia
    source_node: int nodo fuente
    función que inicializa los arreglos de predecesores y distancias, y C buckets
    """
    predecessors = np.array([None for i in range(node_quantity+1)])
    distances = np.array([np.inf for i in range(node_quantity+1)])
    buckets = [ [] for i in range(max_cost+1)]

    # inicializar nodo fuente
    predecessors[source_node] = source_node
    distances[source_node] = 0
    # distancias_parciales = [(distances[n], n) for n in range(1, node_quantity+1)]
    buckets[0].append(source_node)

    return predecessors, distances, buckets



def Dial(node_quantity, source_node, arcs, V, max_cost):
    """
    node_quantity: int cantidad de nodos de la instancia
    source_node: int nodo fuente
    arcs: estructura con arcos y sus costos
    V: diccionario de nodos alcanzables desde el nodo llave
    max_cost: costo máximo de la red
    función que aplica el algoritmo de Dial
    """
    predecessors, distances, buckets = initialize(node_quantity, source_node, max_cost)
    pendientes = [i for i in range(1, node_quantity+1) if i != source_node]
    k = -1
    loop_completed = False
    while not loop_completed:  # mientras no haya verificado que todos los buckets esten vacios
        for i in range(max_cost+1):  # avanzar a lo mas max_cost+1 (C+1) pasos
            k += 1
            index_bucket = k % (max_cost + 1)  # revisar entre 0 y max_cost
            if len(buckets[index_bucket]) > 0:
                while buckets[index_bucket]:
                    nodo = buckets[index_bucket].pop()
                    for j in V[nodo]:  # arcos que salen del nodo ingresado al árbol solución
                        distancia_i_j = k + arcs[(nodo, j)]
                        if distancia_i_j < distances[j]:
                            if distances[j] != np.inf:  # nodo j ya existe en algun bucket
                                index_j_actual = int(distances[j] % (max_cost + 1))
                                buckets[index_j_actual].remove(j)  # sacar al nodo actualizado de (nodo, j) del bucket viejo
                            distances[j] = distancia_i_j  # actualizar distancia del nodo j
                            predecessors[j] = nodo  # actualizar predecesor
                            index_j_nuevo = int(distances[j] % (max_cost + 1))
                            buckets[index_j_nuevo].append(j)  # agregar al nodo actualizado de (nodo, j) al bucket nuevo
                            if j in pendientes:  # si ya entro a algun bucket es alcanzable
                                pendientes.remove(j)  # ya no esta pendiente
                break
            elif i == max_cost:  # ya dio la vuelta entera, terminar
                loop_completed = True
    while pendientes:  # finalizar los no alcanzables
        nodo = pendientes.pop()
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
    predecessors, distances = Dial(node_quantity, source_node, arcs, V, max_cost)
    solve_time = time.time()
    print("Writing solution...")
    if Testing:
        write_sol(source_node, node_quantity, predecessors, distances, f"salida_{source_node}_Dial.txt")
    else:
        write_sol(source_node, node_quantity, predecessors, distances)
    write_time = time.time()
    print(f"Total runtime: {write_time-start_time:.5f}. Reading: {read_time-start_time:.8f}, Solving: {solve_time-read_time:.8f}, Writing: {write_time-solve_time:.8f}")
  
    if Testing:
        with open("times_Dial.txt", "a") as file:
            file.write(f"{write_time-start_time:.8f}\n")

# ### MAXIMUM MEMORY USAGE
# os.system(f"grep VmPeak /proc/{os.getpid()}/status")    