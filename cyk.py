def cykParse(grammar: dict, word: list[str], start_symbol: str) -> (bool, list | None):
    n = len(word)
    # Inicializar la tabla
    T = [[set() for j in range(n)] for i in range(n)]
 
    # Llenado de la tabla para los terminales
    for j in range(n):
        for lhs, rhs_list in grammar.items():
            for rhs in rhs_list:
                # Si es una producción que genera un terminal
                if len(rhs) == 1 and rhs[0] == word[j]:
                    T[j][j].add(lhs)
        # Llenado de la tabla para las combinaciones
        for i in range(j, -1, -1):
            for k in range(i, j):
                for lhs, rhs_list in grammar.items():
                    for rhs in rhs_list:
                        # Verificar producciones con dos no terminales
                        if (len(rhs) == 2 and
                            rhs[0] in T[i][k] and
                            rhs[1] in T[k+1][j]):
                            T[i][j].add(lhs)

    # Devolver si la oración es aceptada
    aceptada = start_symbol in T[0][n-1]
    return aceptada, T if aceptada else None
