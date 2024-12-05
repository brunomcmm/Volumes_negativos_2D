# Correção de Malhas 2D do GMSH

Este programa identifica e corrige elementos com áreas negativas em malhas 2D geradas no GMSH. Ele usa uma interface gráfica para facilitar o uso e gera um arquivo corrigido automaticamente.

## Funcionalidades

- **Identificação de problemas:** Detecta elementos com áreas negativas.
- **Correção automática:** Reordena os nós dos elementos para corrigir áreas negativas.
- **Interface amigável:** Utiliza **PySimpleGUI** ou o **PyQt** para permitir interação com o usuário.

## Requisitos

Certifique-se de ter o Python 3 instalado e os seguintes pacotes:
- `PySimpleGUI`
- `matplotlib`
- `PyQt5`

Para instalar as dependências, execute:
```bash (terminal)
pip install PySimpleGUI
pip install matplotlib
pip install PyQt5
