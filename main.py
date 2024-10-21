import time
from cyk import cykParse
from grammar import  cargar_gramatica_desde_archivo, convertir_a_CNF
from parsetree import visualize_tree

if __name__ == "__main__":
   

    grammar_file = "grammar.txt"
    reglas_gramatica = cargar_gramatica_desde_archivo(grammar_file)
    

    simbolo_inicial = list(reglas_gramatica.keys())[0]  # Usar el primer símbolo como entrada

    if reglas_gramatica:
        reglas_cnf = convertir_a_CNF(reglas_gramatica, simbolo_inicial)
        print("Gramática convertida a CNF:")
        for lhs, rhs_list in reglas_cnf.items():
            print(f"{lhs} -> {rhs_list}")


    oracion_usuario = input("Ingrese una oración en inglés: ").split()


    sentence = [word.strip() for word in oracion_usuario]

    tiempo_inicio = time.time()

    aceptada, tabla_cyk = cykParse(reglas_gramatica, sentence, simbolo_inicial)


    print(tabla_cyk)

    if aceptada:
        print("La oración es aceptada.")
        visualize_tree(tabla_cyk, reglas_cnf, sentence)
    else:
        print("La oración NO es aceptada.")

    tiempo_final = time.time()
    print(f"Tiempo de ejecución: {tiempo_final - tiempo_inicio:.4f} segundos")
