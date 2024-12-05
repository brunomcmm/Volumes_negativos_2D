"""
Módulo: correction_functions.py
Descrição: Funções auxiliares para corrigir malhas 2D no aplicativo.
"""

from mesh_processor import load_msh, identify_and_correct_negative_elements, save_corrected_msh

def process_corrigir_malha(file_path, app):
    """
    Processa a correção de malha e atualiza a interface.

    Args:
        file_path (str): Caminho para o arquivo .msh.
        app (GMSHApp): Instância da interface gráfica para exibir mensagens.
    """
    app.log_message("Carregando arquivo...\n")
    try:
        # Carregar nós e elementos do arquivo
        nodes, elements = load_msh(file_path)
        app.log_message("Arquivo carregado com sucesso.\n")

        # Identificar e corrigir elementos com área negativa
        corrected_elements, negative_count = identify_and_correct_negative_elements(nodes, elements)
        app.log_message(f"Identificados {negative_count} elementos com área negativa.\n")

        # Salvar arquivo corrigido
        corrected_path = save_corrected_msh(nodes, corrected_elements, file_path)
        app.log_message(f"Arquivo corrigido salvo em: {corrected_path}\n")
    except Exception as e:
        app.log_message(f"Erro ao processar o arquivo: {e}\n")