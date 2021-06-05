#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

nodes_filename = "nodos.txt"
arcs_filename = "arcos.txt"
output_filename = "salida.txt"


def read_node_quantity(filename=nodes_filename):
    """
    filename: str con el nombre del archivo que contiene la cantidad de nodos de la instancia
    función que lee el archivo de texto y retorna la cantidad de nodos de la instancia
    """
    if not ".txt" in filename:
        filename += ".txt"

    with open(filename, "r") as file:
        return int(file.readline().strip())


def read_arcs(filename=arcs_filename):
    """
    filename: str con el nombre del archivo que contiene los arcos de la instancia
    función que lee el archivo de texto y retorna un arreglo de arcos con sus costos, diccionario de vecinos y costo máximo
    """
    if not ".txt" in filename:
        filename += ".txt"

    arcs = {}
    V = {}  
    max_costo = 0
    with open(filename, "r") as file:
        for line in file:
            if "EOF" in line:
                break
            else:
                splitted = line.strip().split(" ")
                costo = int(splitted[2])
                if costo < 0:
                    print(f"### Arco con costo negativo: {line}, tomando el valor absoluto ###")
                    costo = costo*-1
                if costo > max_costo:
                    max_costo = costo
                i = int(splitted[0])
                j =int(splitted[1])
                if i not in V.keys():
                    V[i] = []
                if j not in V.keys():
                    V[j] = []
                V[i].append(j)
                arcs[(i, j)] = costo
    return arcs, V, max_costo


def write_sol(source_node, node_quantity, predecessors, distances, filename=output_filename):
    """
    source_node: int nodo fuente del árbol de rutas generado
    tree: arbol de rutas mínimas: arreglo en que la posicion n contiene la info del nodo n+1: nodo predecesor y costo
    tree[n] = (predecesor del nodo n, costo de ruta hasta nodo)
    filename: str con el nombre del archivo que contiene los arcos de la instancia
    función que lee escribe el árbol de la solcución en un archivo de texto
    """
    if not ".txt" in filename:
        filename += ".txt"

    with open(filename, "w") as file:
        file.write(f"{source_node}\n")
        for n in range(1, node_quantity+1):
            file.write(f"{n} {predecessors[n]} {int(distances[n])}\n")




if __name__ == "__main__":
    print("Modulo con funciones para lectura y escritura de archivos.")
