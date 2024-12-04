"""
Módulo: main.py
Descrição: Interface gráfica para corrigir e visualizar malhas 2D do GMSH.
"""

import PySimpleGUI as sg
from correction_functions import process_corrigir_malha
from visualization_functions import process_gerar_imagem

def main():
    """
    Função principal para executar a interface gráfica.
    """
    layout = [
        [sg.Text("Selecione o arquivo .msh para corrigir ou gerar imagem:")],
        [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse("Procurar", file_types=(("Gmsh Files", "*.msh"),))],
        [sg.Multiline(size=(60, 15), key='-OUTPUT-', disabled=True)],
        [sg.Button("Corrigir", key='-CORRIGIR-', disabled=True), 
         sg.Button("Gerar Imagem", key='-PLOTAR-', disabled=True), 
         sg.Button("Sair")]
    ]

    window = sg.Window("Correção e Visualização de Malhas Gmsh", layout)

    while True:
        event, values = window.read(timeout=100)

        if event in (sg.WINDOW_CLOSED, 'Sair'):
            break

        if event == '-FILE-':
            file_path = values['-FILE-']
            if file_path.endswith('.msh'):
                window['-CORRIGIR-'].update(disabled=False)
                window['-PLOTAR-'].update(disabled=False)

        if event == '-CORRIGIR-':
            process_corrigir_malha(file_path, window)

        if event == '-PLOTAR-':
            file_path = values['-FILE-']
            window['-OUTPUT-'].update(f"Gerando imagem da malha com materiais do arquivo {file_path}...\n")
            try:
                process_gerar_imagem(file_path, window)
            except Exception as e:
                window['-OUTPUT-'].update(f"Erro ao processar a geração de imagem: {e}\n")

    window.close()


if __name__ == '__main__':
    main()