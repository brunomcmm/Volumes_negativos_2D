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

def process_gerar_imagem(file_path, app):
    """
    Gera uma imagem da malha em um processo separado e atualiza a interface.

    Args:
        file_path (str): Caminho para o arquivo .msh.
        app (GMSHApp): Instância da interface gráfica para exibir mensagens.
    """
    output_path = file_path.replace('.msh', '_materiais.png')  # Caminho para salvar a imagem
    queue = multiprocessing.Queue()  # Fila para comunicação entre processos

    # Informar início do processo
    app.log_message("Gerando imagem da malha...\n")
    app.log_message(f"Arquivo de entrada: {file_path}\n")

    # Criar e iniciar o processo
    process = multiprocessing.Process(target=gerar_imagem_async, args=(file_path, output_path, queue))
    process.start()

    # Atualizar a interface enquanto espera o término do processo
    while True:
        if not queue.empty():
            message = queue.get()
            app.log_message(f"{message}\n")

            # Encerrar o processo se a mensagem for de conclusão ou erro
            if "Erro" in message or "salva em" in message:
                process.terminate()
                break

        if not process.is_alive():
            break
