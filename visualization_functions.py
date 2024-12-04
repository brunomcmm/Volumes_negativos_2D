"""
Módulo: visualization_functions.py
Descrição: Funções auxiliares para visualização e geração de imagens de malhas 2D.
"""

import multiprocessing
from mesh_plotter import save_mesh_plot_by_materials

def gerar_imagem_async(file_path, output_path, queue):
    """
    Executa a geração da imagem em um processo separado.
    
    Args:
        file_path (str): Caminho para o arquivo .msh.
        output_path (str): Caminho para salvar a imagem .png.
        queue (multiprocessing.Queue): Fila para comunicação entre processos.
    """
    try:
        save_mesh_plot_by_materials(file_path, output_path)
        queue.put(f"Imagem da malha salva em: {output_path}")
    except Exception as e:
        queue.put(f"Erro ao gerar a imagem da malha: {e}")

def process_gerar_imagem(file_path, window):
    """
    Gera uma imagem da malha em um processo separado e atualiza a interface.
    
    Args:
        file_path (str): Caminho para o arquivo .msh.
        window (sg.Window): Janela da interface gráfica.
    """
    output_path = file_path.replace('.msh', '_materiais.png')  # Caminho para salvar a imagem
    queue = multiprocessing.Queue()  # Fila para comunicação entre processos

    # Criar e iniciar o processo
    process = multiprocessing.Process(target=gerar_imagem_async, args=(file_path, output_path, queue))
    process.start()

    # Atualizar a interface enquanto espera o término do processo
    while True:
        if not queue.empty():
            message = queue.get()
            window['-OUTPUT-'].update(f"{message}\n", append=True)

            if "Erro" in message or "salva em" in message:
                process.terminate()
                return

        if not process.is_alive():
            break