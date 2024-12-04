"""
Módulo: mesh_plotter.py
Descrição: Ferramentas para plotar e visualizar malhas 2D geradas no GMSH.
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mesh_processor import load_msh

def save_mesh_plot_by_materials(file_path, output_path):
    """
    Gera e salva a malha 2D como uma imagem .png destacando os materiais pelos seus Physical IDs.
    
    Args:
        file_path (str): Caminho para o arquivo .msh.
        output_path (str): Caminho para salvar a imagem .png.
    """
    # Carregar nós e elementos
    nodes, elements = load_msh(file_path)

    # Identificar Physical IDs de materiais (300-399)
    material_ids = set(
        element[3] for element in elements if element[1] == 2 and 300 <= element[3] <= 399
    )

    # Mapear cada ID de material a uma cor
    colormap = cm.get_cmap('tab20', len(material_ids))  # Usar um colormap com cores distintas
    material_colors = {material_id: colormap(i) for i, material_id in enumerate(sorted(material_ids))}

    # Criar uma figura
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Visualização da Malha 2D por Materiais')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Plotar os triângulos da malha com base nos IDs de materiais
    for element in elements:
        if element[1] == 2:  # Tipo 2 = Triângulo
            physical_id = element[3]  # Physical ID do elemento
            if physical_id in material_colors:
                node_ids = element[-3:]
                coords = [nodes[node_id] for node_id in node_ids]
                x, y = zip(*[(p[0], p[1]) for p in coords])  # Coordenadas x e y
                x += (x[0],)  # Fechar o triângulo
                y += (y[0],)
                color = material_colors[physical_id]  # Cor correspondente ao ID do material
                ax.fill(x, y, color=color, edgecolor='black', linewidth=0.1)

    # Ajustar os limites
    all_coords = list(nodes.values())
    x_coords, y_coords = zip(*[(p[0], p[1]) for p in all_coords])
    ax.set_xlim(min(x_coords), max(x_coords))
    ax.set_ylim(min(y_coords), max(y_coords))

    # Adicionar legenda
    legend_handles = [
        plt.Line2D([0], [0], color=material_colors[material_id], lw=4, label=f'Material {material_id - 300}')
        for material_id in sorted(material_colors.keys())
    ]
    ax.legend(handles=legend_handles, loc='upper right', title='Materiais')

    # Salvar o gráfico como imagem
    plt.savefig(output_path, dpi=300)  # Salvar com alta resolução
    plt.close(fig)  # Fechar a figura para liberar memória