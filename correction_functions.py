"""
Módulo: correction_functions.py
Descrição: Funções auxiliares para corrigir malhas 2D no aplicativo.
"""

from mesh_processor import load_msh, identify_and_correct_negative_elements, save_corrected_msh

def process_corrigir_malha(file_path, window):
    """
    Processa a correção de malha e atualiza a interface.
    
    Args:
        file_path (str): Caminho para o arquivo .msh.
        window (sg.Window): Janela da interface gráfica.
    """
    window['-OUTPUT-'].update("Carregando arquivo...\n")
    try:
        nodes, elements = load_msh(file_path)
        window['-OUTPUT-'].update("Arquivo carregado com sucesso.\n")

        corrected_elements, negative_count = identify_and_correct_negative_elements(nodes, elements)
        window['-OUTPUT-'].update(f"Identificados {negative_count} elementos com área negativa.\n")

        corrected_path = save_corrected_msh(nodes, corrected_elements, file_path)
        window['-OUTPUT-'].update(f"Arquivo corrigido salvo em: {corrected_path}\n")
    except Exception as e:
        window['-OUTPUT-'].update(f"Erro ao processar o arquivo: {e}\n")