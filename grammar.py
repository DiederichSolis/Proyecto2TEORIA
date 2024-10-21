import re
import copy
import itertools
from pprint import pprint

# Validación de expresiones usando regex
def validar_expresion(regex: str, expresion: str) -> bool:
    return re.match(regex, expresion) is not None

def identificar_terminos(gramatica: dict) -> tuple[set, set]:
    noTerminales = set(gramatica.keys())
    terminales = set()

    for producciones in gramatica.values():
        for produccion in producciones:
            for termino in produccion:  # Aquí ya no usamos split, iteramos directamente
                if termino not in noTerminales:
                    terminales.add(termino)

    return noTerminales, terminales


# Construcción de conjuntos de subconjuntos (powerset)
def construir_powerset(conjunto: set) -> list[str]:
    return list(itertools.chain.from_iterable(itertools.combinations(conjunto, i) for i in range(len(conjunto)+1)))

# Verificar si un término es terminal
def es_terminal(termino: str) -> bool:
    return re.fullmatch(r"([a-z0-9]|\s)+", termino) is not None

# Verificar si un término es no terminal
def es_no_terminal(termino: str) -> bool:
    return re.fullmatch(r"([A-Z0-9])+", termino) is not None

# Eliminación de producciones epsilon
def eliminar_producciones_epsilon(gramatica: dict) -> dict:
    anulables = {k for k, v in gramatica.items() if 'ε' in v}

    while True:
        nuevo_anulable = {k for k, v in gramatica.items() for produccion in v if any(nt in anulables for nt in produccion)}
        if nuevo_anulable.issubset(anulables):
            break
        anulables.update(nuevo_anulable)

    nueva_gramatica = {}
    for k, v in gramatica.items():
        nueva_gramatica[k] = [produccion for produccion in v if 'ε' not in produccion]
        subconjuntos = construir_powerset(anulables)
        for produccion in v:
            for subconjunto in subconjuntos:
                nueva_produccion = list(produccion)
                for simbolo in subconjunto:
                    nueva_produccion = [term for term in nueva_produccion if term != simbolo]
                nueva_produccion = ' '.join(nueva_produccion).strip()
                if nueva_produccion and nueva_produccion not in nueva_gramatica[k]:
                    nueva_gramatica[k].append(nueva_produccion.split())

    return nueva_gramatica

def eliminar_producciones_unitarias(gramatica: dict) -> dict:
    nueva_gramatica = {}
    for lhs, rhs_list in gramatica.items():
        nueva_gramatica[lhs] = []
        for produccion in rhs_list:
            nueva_gramatica[lhs].append(produccion)

    while True:
        cambiada = False
        for lhs, rhs_list in nueva_gramatica.items():
            for produccion in rhs_list:
                if len(produccion) == 1 and isinstance(produccion[0], str) and produccion[0].isupper():
                    simbolo = produccion[0]
                    if simbolo in nueva_gramatica:
                        nueva_gramatica[lhs].extend(nueva_gramatica[simbolo])
                    nueva_gramatica[lhs].remove(produccion)
                    cambiada = True
        if not cambiada:
            break

    return nueva_gramatica

# Eliminación de símbolos no derivables
def eliminar_no_derivables(gramatica: dict) -> dict:
    noTerminales, terminales = identificar_terminos(gramatica)
    derivables = set()

    # Verificar si una producción tiene terminales directamente
    for nt in gramatica:
        for produccion in gramatica[nt]:
            if any(t in terminales for t in produccion):
                derivables.add(nt)

    # Expandir derivables
    while True:
        nuevo_derivable = set()
        for nt, producciones in gramatica.items():
            for produccion in producciones:
                if all(simbolo in derivables or simbolo in terminales for simbolo in produccion):
                    nuevo_derivable.add(nt)
        if nuevo_derivable.issubset(derivables):
            break
        derivables.update(nuevo_derivable)

    # Retornar solo las reglas derivables
    return {nt: producciones for nt, producciones in gramatica.items() if nt in derivables}

# Eliminación de símbolos inalcanzables
def eliminar_inalcanzables(gramatica: dict, entrada: str) -> dict:
    alcanzables = {entrada}

    while True:
        nuevo_alcanzable = set()
        for k, producciones in gramatica.items():
            if k in alcanzables:
                for produccion in producciones:
                    for simbolo in produccion:  # Iterar directamente sobre la lista de términos
                        if simbolo.isupper():
                            nuevo_alcanzable.add(simbolo)
        if nuevo_alcanzable.issubset(alcanzables):
            break
        alcanzables.update(nuevo_alcanzable)

    # Retornar solo las reglas alcanzables
    return {nt: producciones for nt, producciones in gramatica.items() if nt in alcanzables}

# Conversión de gramática a CNF
def convertir_a_CNF(gramatica: dict, entrada: str) -> dict:
    try:
        # Paso 1: Eliminar producciones epsilon, unitarias, no derivables e inalcanzables
        gramatica = eliminar_producciones_epsilon(gramatica)
        gramatica = eliminar_producciones_unitarias(gramatica)
        gramatica = eliminar_no_derivables(gramatica)
        gramatica = eliminar_inalcanzables(gramatica, entrada)

        # Paso 2: Convertir a CNF
        gramatica_cnf = copy.deepcopy(gramatica)
        terminal_replacements = {}
        t_count = 0

        for lhs, rhs_list in gramatica.items():
            new_rhs_list = []
            for rhs in rhs_list:
                # Si la producción es un terminal (por ejemplo, 'cooks')
                if len(rhs) == 1 and isinstance(rhs[0], str) and rhs[0].islower():
                    if rhs[0] not in terminal_replacements:
                        terminal_replacements[rhs[0]] = f"T{t_count}"
                        gramatica_cnf[terminal_replacements[rhs[0]]] = [rhs]  # Modificación: Almacenar el terminal como una lista simple
                        t_count += 1
                    new_rhs_list.append([terminal_replacements[rhs[0]]])

                # Si la producción tiene más de 2 símbolos
                elif len(rhs) > 2:
                    while len(rhs) > 2:
                        new_nt = f"NT{t_count}"
                        gramatica_cnf[new_nt] = [[rhs[0], rhs[1]]]
                        rhs = [new_nt] + rhs[2:]
                        t_count += 1
                    new_rhs_list.append(rhs)

                else:
                    # Si la regla ya está en forma de 2 símbolos o 1 terminal
                    new_rhs_list.append(rhs)

            # Añadir producciones sin duplicados
            gramatica_cnf[lhs] = [list(t) for t in set(tuple(rhs) for rhs in new_rhs_list)]  # Eliminar duplicados

        return gramatica_cnf

    except Exception as e:
        raise RuntimeError(f"Error al convertir la gramática a CNF: {e}")

def cargar_gramatica_desde_archivo(nombre_archivo: str) -> dict:
    """
    Cargar la gramática desde un archivo de texto y convertirla en un diccionario.
    :param nombre_archivo: El nombre del archivo que contiene la gramática.
    :return: Diccionario que representa la gramática.
    """
    gramatica = {}
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                # Limpiar la línea de espacios en blanco y saltos de línea
                linea = linea.strip()
                
                if "->" in linea:
                    # Separar el lado izquierdo (LHS) y el lado derecho (RHS)
                    lhs, rhs = linea.split("->")
                    lhs = lhs.strip()
                    rhs = rhs.strip()
                    
                    # Separar las producciones alternativas por '|'
                    producciones = [produccion.strip() for produccion in re.split(r'\s*\|\s*', rhs)]
                    
                    # Para cada producción, la separamos en símbolos
                    producciones = [produccion.split() for produccion in producciones]
                    
                    # Agregar la regla a la gramática
                    if lhs not in gramatica:
                        gramatica[lhs] = []
                    gramatica[lhs].extend(producciones)

        return gramatica
    
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
        return {}