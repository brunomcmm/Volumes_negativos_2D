"""
Módulo: mesh_processor.py
Descrição: Processa malhas 2D do GMSH, identifica e corrige elementos com áreas negativas.
"""

import os

def load_msh(file_path):
    """Carrega nós e elementos de um arquivo .msh."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Separar seções $Nodes e $Elements
    nodes_start = content.find('$Nodes')
    nodes_end = content.find('$EndNodes')
    elements_start = content.find('$Elements')
    elements_end = content.find('$EndElements')

    # Processar nós
    nodes_section = content[nodes_start + 7 : nodes_end].strip().splitlines()
    nodes_count = int(nodes_section[0])
    nodes = {
        int(line.split()[0]): tuple(map(float, line.split()[1:]))
        for line in nodes_section[1:nodes_count + 1]
    }

    # Processar elementos
    elements_section = content[elements_start + 9 : elements_end].strip().splitlines()
    elements_count = int(elements_section[0])
    elements = [
        list(map(int, line.split()))
        for line in elements_section[1:elements_count + 1]
    ]

    return nodes, elements

def calculate_triangle_area(node_ids, nodes):
    """Calcula a área de um triângulo."""
    p1, p2, p3 = [nodes[node_id] for node_id in node_ids]
    return 0.5 * ((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1]))

def identify_and_correct_negative_elements(nodes, elements):
    """Identifica e corrige elementos com áreas negativas."""
    corrected_elements = []
    negative_count = 0

    for element in elements:
        if element[1] == 2:  # Tipo 2 = Triângulo
            node_ids = element[-3:]
            area = calculate_triangle_area(node_ids, nodes)
            if area < 0:  # Área negativa, corrigir ordem
                negative_count += 1
                element[-3:] = [node_ids[0], node_ids[2], node_ids[1]]  # Inverter nós
        corrected_elements.append(element)

    return corrected_elements, negative_count

def save_corrected_msh(nodes, elements, original_path):
    """Salva o arquivo corrigido."""
    corrected_path = original_path.replace('.msh', '_corrigido.msh')

    with open(corrected_path, 'w') as file:
        file.write('$MeshFormat\n2.2 0 8\n$EndMeshFormat\n')
        
        # Escrever nós
        file.write('$Nodes\n')
        file.write(f'{len(nodes)}\n')
        for node_id, coords in nodes.items():
            file.write(f'{node_id} {" ".join(map(str, coords))}\n')
        file.write('$EndNodes\n')

        # Escrever elementos
        file.write('$Elements\n')
        file.write(f'{len(elements)}\n')
        for element in elements:
            file.write(" ".join(map(str, element)) + '\n')
        file.write('$EndElements\n')

    return corrected_path