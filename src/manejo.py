import os

# definicion de la rutas
direccion = os.path.dirname(os.path.abspath(__file__))
Input = os.path.join(direccion, '../input')
Output = os.path.join(direccion, '../output')
ruta = '/Users/diederichsolis/Documents/carpeta sin título/Teoria-Computacion-Gabriel-Paz/Proyecto2/input/gramatica.txt'
os.makedirs(Input, exist_ok=True)
os.makedirs(Output, exist_ok=True)
