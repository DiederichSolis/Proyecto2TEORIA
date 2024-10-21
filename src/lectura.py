import os
from datetime import datetime
from manejo import Output

def readFile(fileName: str) -> list[str]:
    """
    Función que lee el contenido de un archivo de texto y lo devuelve como una lista de cadenas.

    Parámetros:
    fileName (str): La ruta del archivo que se desea leer.

    Retorno:
    list[str]: Una lista donde cada elemento es una línea del archivo.

    Excepciones:
    FileNotFoundError: Si el archivo no existe en la ruta especificada.
    ValueError: Si el archivo está vacío.
    IOError: Si ocurre algún error durante la lectura del archivo.

    Proceso:
    - Se verifica si el archivo existe. Si no, se lanza un FileNotFoundError.
    - Se abre el archivo en modo de lectura ('r') y con codificación 'utf-8'.
    - Se lee el archivo línea por línea, separando el contenido por saltos de línea ('\n').
    - Si el archivo está vacío, se lanza un ValueError.
    - Si ocurre cualquier otro error, se lanza un IOError con el mensaje del error capturado.
    """
    if not os.path.exists(fileName):
        raise FileNotFoundError(f"El archivo {fileName} no existe.")
    
    try:
        with open(fileName, 'r', encoding='utf-8') as file:
            data = file.read().split('\n')
            if not data:
                raise ValueError(f"El archivo {fileName} está vacío.")
            return data
    except Exception as e:
        raise IOError(f"Error al leer el archivo {fileName}: {e}")


def log_result(accepted: bool, sentence: str, Output: str):
    """
    Función que guarda los resultados de una prueba en un archivo de log.

    Parámetros:
    accepted (bool): Indica si la prueba de la frase fue aceptada (True) o no (False).
    sentence (str): La frase que fue evaluada.
    output_dir (str): El directorio donde se guardará el archivo de log.

    Proceso:
    - Se genera o actualiza un archivo llamado 'resultado.txt' en el directorio especificado.
    - Se obtiene la fecha y hora actual con el formato 'YYYY-MM-DD HH:MM:SS'.
    - Se construye un mensaje de log, que indica si la frase fue aceptada o no.
    - Se intenta abrir el archivo en modo de 'añadir' (append) y escribir el mensaje de log.
    - Si ocurre un error al escribir en el archivo, se captura un IOError y se muestra un mensaje de error.
    """
    print("Guardando resultados en el archivo de log...")
    print("Testeando la frase: ", sentence)
    log_file = os.path.join(Output, 'resultado.txt')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Construir mensaje de log
    if accepted:
        message = f"[{timestamp}] La frase '{' '.join(sentence)}' fue aceptada.\n"
    else:
        message = f"[{timestamp}] La frase '{' '.join(sentence)}' NO fue aceptada.\n"
    
    # Guardar en el archivo de logs
    try:
        with open(log_file, 'a', encoding='utf-8') as file:
            file.write(message)
    except IOError as e:
        print(f"Error al escribir en el archivo de log: {e}")
