
from LL1.grammar import (
    GRAMATICA,
    SIMBOLO_INICIAL,
    EPSILON
)


def first_da_sequencia(sequencia, first):
    """
    Calcula o FIRST de uma sequência de símbolos.
    """

    resultado = set()

    if not sequencia:
        resultado.add(EPSILON)
        return resultado

    todos_tem_epsilon = True

    for simbolo in sequencia:

        # Se for terminal, adiciona diretamente.
        if simbolo not in GRAMATICA:
            resultado.add(simbolo)
            todos_tem_epsilon = False
            break

        # Adiciona FIRST do não terminal, exceto epsilon.
        resultado.update(first[simbolo] - {EPSILON})

        # Se não possui epsilon, encerra.
        if EPSILON not in first[simbolo]:
            todos_tem_epsilon = False
            break

    if todos_tem_epsilon:
        resultado.add(EPSILON)

    return resultado


def calcular_first():
    first = {
        nao_terminal: set()
        for nao_terminal in GRAMATICA
    }

    houve_mudanca = True

    while houve_mudanca:
        houve_mudanca = False

        for nao_terminal, producoes in GRAMATICA.items():

            for producao in producoes:
                novos = first_da_sequencia(producao, first)

                tamanho_anterior = len(first[nao_terminal])
                first[nao_terminal].update(novos)

                if len(first[nao_terminal]) > tamanho_anterior:
                    houve_mudanca = True

    return first


def calcular_follow(first):
    follow = {
        nao_terminal: set()
        for nao_terminal in GRAMATICA
    }

    # O símbolo inicial sempre recebe EOF no FOLLOW.
    follow[SIMBOLO_INICIAL].add("EOF")

    houve_mudanca = True

    while houve_mudanca:
        houve_mudanca = False

        for nao_terminal, producoes in GRAMATICA.items():

            for producao in producoes:

                for i, simbolo in enumerate(producao):

                    # FOLLOW só é calculado para não terminais.
                    if simbolo not in GRAMATICA:
                        continue

                    restante = producao[i + 1:]

                    first_restante = first_da_sequencia(
                        restante, first
                    )

                    # Adiciona FIRST do restante, sem epsilon.
                    novos = first_restante - {EPSILON}

                    tamanho_anterior = len(follow[simbolo])
                    follow[simbolo].update(novos)

                    if len(follow[simbolo]) > tamanho_anterior:
                        houve_mudanca = True

                    # Se o restante pode gerar epsilon,
                    # adiciona FOLLOW do lado esquerdo.
                    if EPSILON in first_restante:
                        tamanho_anterior = len(follow[simbolo])

                        follow[simbolo].update(
                            follow[nao_terminal]
                        )

                        if len(follow[simbolo]) > tamanho_anterior:
                            houve_mudanca = True

    return follow


def exibir_conjuntos(titulo, conjuntos):
    print(f"\n=== {titulo} ===")

    for simbolo in sorted(conjuntos):
        elementos = sorted(conjuntos[simbolo])

        print(f"{simbolo:<22} = {{ {', '.join(elementos)} }}")


def calcular_e_exibir():
    first = calcular_first()
    follow = calcular_follow(first)

    exibir_conjuntos("CONJUNTOS FIRST", first)
    exibir_conjuntos("CONJUNTOS FOLLOW", follow)

    return first, follow
