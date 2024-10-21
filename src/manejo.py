import os

# definicion de la rutas
direccion = os.path.dirname(os.path.abspath(__file__))
Input = os.path.join(direccion, '../input')
Output = os.path.join(direccion, '../output')

# Ingreso de la ruta
ruta = 'input\gr.txt'

# Manejo de creacion por si no existen
os.makedirs(Input, exist_ok=True)
os.makedirs(Output, exist_ok=True)
