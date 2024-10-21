def cykParse(grammar: dict, word: str) -> (bool,list|None):
    """
    Implementa el algoritmo CYK (Cocke-Younger-Kasami) para analizar si una palabra dada
    puede ser generada por una gramática libre de contexto (CFG) en forma normal de Chomsky (CNF).

    Parámetros:
    -----------
    grammar : dict
        Un diccionario que representa la gramática en forma normal de Chomsky. 
        Las claves del diccionario son los símbolos no terminales (izquierda de las reglas de producción),
        y los valores son listas de producciones posibles (derecha de las reglas), las cuales pueden
        ser terminales o pares de no terminales.
        
    word : str
        La palabra que se quiere analizar. Se espera que sea una cadena de caracteres.

    Retorno:
    --------
    tuple:
        - bool: `True` si la palabra puede ser generada por la gramática, `False` en caso contrario.
        - list|None: La tabla CYK si la palabra puede ser generada, `None` si no.

    Descripción:
    ------------
    El algoritmo construye una tabla triangular `T` donde `T[i][j]` contiene el conjunto de símbolos no terminales
    que pueden generar la subcadena de la palabra que va desde la posición `i` hasta la posición `j`. 
    El proceso se realiza en dos fases:

    1. Fase inicial:
       Se analiza cada posición `j` de la palabra y se busca si existe una producción de la gramática que coincida
       con el símbolo terminal en la posición `j` de la palabra. Si es así, se añade el símbolo no terminal correspondiente
       a la celda `T[j][j]`.

    2. Fase de combinaciones:
       Para cada subsección de la palabra que va desde la posición `i` a la posición `j`, se analiza si existe una
       producción de la forma `A -> B C` en la gramática, donde `B` puede generar una parte de la palabra y `C` puede
       generar la parte restante. Si la combinación es válida, se añade el símbolo no terminal `A` a la celda `T[i][j]`.

    Al final, si el símbolo inicial de la gramática puede generar la palabra completa, la celda `T[0][n-1]` contendrá
    ese símbolo, y la función retornará `True` junto con la tabla CYK. De lo contrario, retornará `False` y `None`.
    
    Ejemplo de uso:
    ---------------
    grammar = {
        'S': [['A', 'B'], ['B', 'C']],
        'A': [['a']],
        'B': [['b']],
        'C': [['c']]
    }
    
    word = "abc"
    
    # Llamar a la función:
    result, table = cykParse(grammar, word)
    
    # Resultado:
    # True, con la tabla CYK mostrando la derivación de la palabra.
    """
    
    n = len(word)
    # Inicializar la tabla CYK
    T = [[set([]) for j in range(n)] for i in range(n)]
 
    # Llenar la tabla
    for j in range(0, n):
        # Iterar sobre las reglas de la gramática
        for lhs, rule in grammar.items():
            for rhs in rule:
                # Si se encuentra un terminal
                if len(rhs) == 1 and rhs[0] == word[j]:
                    T[j][j].add(lhs)
 
        # Iterar de forma inversa desde j hasta 0
        for i in range(j, -1, -1):   
            # Iterar sobre el rango desde i a j + 1
            for k in range(i, j):     
                # Iterar sobre las reglas de la gramática
                for lhs, rule in grammar.items():
                    for rhs in rule:
                        # Si se encuentra una producción de 2 símbolos no terminales
                        if (len(rhs) == 2) and (rhs[0] in T[i][k]) and (rhs[1] in T[k+1][j]):
                            T[i][j].add(lhs)

    # Verificar si el símbolo inicial puede generar la palabra completa
    if len(T[0][n-1]) != 0:
        return True, T
    else:
        return False, None
