"""
Módulo: main.py
Descrição: Interface gráfica para corrigir e visualizar malhas 2D do GMSH com PyQt.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QMessageBox
)
from correction_functions import process_corrigir_malha
from visualization_functions import process_gerar_imagem

class GMSHApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Correção e Visualização de Malhas GMSH")
        self.resize(600, 400)

        # Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Rótulo e entrada de arquivo
        self.label = QLabel("Selecione o arquivo .msh para corrigir ou gerar imagem:")
        self.layout.addWidget(self.label)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Nenhum arquivo selecionado")
        self.layout.addWidget(self.file_input)

        self.browse_button = QPushButton("Procurar")
        self.browse_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.browse_button)

        # Área de saída
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # Botões de ação
        self.corrigir_button = QPushButton("Corrigir")
        self.corrigir_button.setEnabled(False)
        self.corrigir_button.clicked.connect(self.corrigir_malha)
        self.layout.addWidget(self.corrigir_button)

        self.plotar_button = QPushButton("Gerar Imagem")
        self.plotar_button.setEnabled(False)
        self.plotar_button.clicked.connect(self.gerar_imagem)
        self.layout.addWidget(self.plotar_button)

        self.sair_button = QPushButton("Sair")
        self.sair_button.clicked.connect(self.close)
        self.layout.addWidget(self.sair_button)

        self.file_path = None

    def select_file(self):
        """Abre o diálogo para selecionar um arquivo .msh."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo", "", "GMSH Files (*.msh)", options=options)
        if file_path:
            self.file_input.setText(file_path)
            self.file_path = file_path
            self.corrigir_button.setEnabled(True)
            self.plotar_button.setEnabled(True)

    def log_message(self, message):
        """Adiciona mensagens na área de saída."""
        self.output_text.append(message)

    def corrigir_malha(self):
        """Executa a correção de malha."""
        if not self.file_path:
            QMessageBox.warning(self, "Erro", "Nenhum arquivo selecionado!")
            return

        self.log_message("Iniciando a correção da malha...")
        try:
            process_corrigir_malha(self.file_path, self)
            self.log_message("Correção da malha concluída!")
        except Exception as e:
            self.log_message(f"Erro ao corrigir a malha: {e}")

    def gerar_imagem(self):
        """Gera a imagem da malha."""
        if not self.file_path:
            QMessageBox.warning(self, "Erro", "Nenhum arquivo selecionado!")
            return

        try:
            process_gerar_imagem(self.file_path, self)
            self.log_message("Imagem gerada com sucesso!")
        except Exception as e:
            self.log_message(f"Erro ao gerar a imagem: {e}")

def main():
    app = QApplication(sys.argv)
    window = GMSHApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()