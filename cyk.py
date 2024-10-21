def cykParse(grammar: dict, word: list[str]) -> (bool, list | None):
    n = len(word)
    # Inicializar la tabla
    T = [[set() for j in range(n)] for i in range(n)]
 
    # Llenado de la tabla para los terminales
    for j in range(0, n):
        for lhs, rhs_list in grammar.items():
            for rhs in rhs_list:
                # Si es una producción que genera un terminal
                if len(rhs) == 1 and rhs[0] == word[j]:
                    T[j][j].add(lhs)
 
        for i in range(j, -1, -1):
            for k in range(i, j):
                for lhs, rhs_list in grammar.items():
                    for rhs in rhs_list:
                        # Verificar producciones con dos no terminales
                        if len(rhs) == 2 and rhs[0] in T[i][k] and rhs[1] in T[k+1][j]:
                            T[i][j].add(lhs)

    # Devolver si la oración es aceptada
    return 'S' in T[0][n-1], T if 'S' in T[0][n-1] else None
