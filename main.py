"""
Módulo: main.py
Descrição: Interface gráfica para corrigir malhas 2D do GMSH com áreas negativas.
"""

import PySimpleGUI as sg
from mesh_processor import load_msh, identify_and_correct_negative_elements, save_corrected_msh

def main():
    layout = [
        [sg.Text("Selecione o arquivo .msh para corrigir:")],
        [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse("Procurar", file_types=(("Gmsh Files", "*.msh"),))],
        [sg.Multiline(size=(60, 15), key='-OUTPUT-', disabled=True)],
        [sg.Button("Corrigir", key='-CORRIGIR-', disabled=True), sg.Button("Sair")]
    ]

    window = sg.Window("Correção de Malha Gmsh", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Sair'):
            break

        if event == '-FILE-':
            file_path = values['-FILE-']
            if file_path.endswith('.msh'):
                window['-CORRIGIR-'].update(disabled=False)

        if event == '-CORRIGIR-':
            file_path = values['-FILE-']
            window['-OUTPUT-'].update("Carregando arquivo...\n")
            
            # Processar arquivo
            try:
                nodes, elements = load_msh(file_path)
                window['-OUTPUT-'].update("Arquivo carregado com sucesso.\n")

                corrected_elements, negative_count = identify_and_correct_negative_elements(nodes, elements)
                window['-OUTPUT-'].update(f"Identificados {negative_count} elementos com área negativa.\n")

                corrected_path = save_corrected_msh(nodes, corrected_elements, file_path)
                window['-OUTPUT-'].update(f"Arquivo corrigido salvo em: {corrected_path}\n")
            except Exception as e:
                window['-OUTPUT-'].update(f"Erro ao processar o arquivo: {e}\n")

    window.close()

if __name__ == '__main__':
    main()