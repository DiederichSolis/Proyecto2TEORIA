import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

def visualize_tree(table, grammar, sentence):
    class Node:
        def __init__(self, symbol):
            self.symbol = symbol
            self.children = []

        def add_child(self, child):
            self.children.append(child)

    def generate_tree(table, grammar, i, j, symbol):
        if i == j:
            return Node(symbol)

        for k in range(i, j):
            for lhs, rhs_list in grammar.items():
                for rhs in rhs_list:
                    if symbol == lhs and len(rhs) == 2:
                        left, right = rhs
                        if left in table[i][k] and right in table[k + 1][j]:
                            node = Node(symbol)
                            node.add_child(generate_tree(table, grammar, i, k, left))
                            node.add_child(generate_tree(table, grammar, k + 1, j, right))
                            return node
        return Node(symbol)

    def draw_tree(node, parent=None, G=None, pos=None):
        if G is None:
            G = nx.DiGraph()
        if pos is None:
            pos = {}

        G.add_node(node.symbol)
        if parent:
            G.add_edge(parent.symbol, node.symbol)

        for child in node.children:
            draw_tree(child, node, G, pos)

        return G

    # Verificación de la tabla CYK antes de intentar acceder a ella
    if len(table) == 0:
        print("Error: La tabla CYK está vacía.")
        return
    
    if len(table[0]) == 0 or len(table[0]) < len(sentence):
        print(f"Error: La tabla CYK no tiene suficientes columnas. Se esperaban al menos {len(sentence)} columnas.")
        return

    if len(table[0]) <= len(sentence) - 1:
        print(f"Error: Los índices no son válidos en la tabla CYK.")
        return

    if 'S' not in table[0][len(sentence) - 1]:
        print("Error: El símbolo 'S' no está en la celda esperada de la tabla CYK.")
        return

    # Generar el árbol de análisis desde la raíz 'S'
    parse_tree = generate_tree(table, grammar, 0, len(sentence) - 1, 'S')
    G = draw_tree(parse_tree)

    # Dibujar el árbol de análisis sintáctico
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10)
    plt.show()
