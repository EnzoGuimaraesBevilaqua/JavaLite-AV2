
from LL1.grammar import GRAMATICA, EPSILON
from LL1.first_follow import calcular_first, calcular_follow, first_da_sequencia


def construir_tabela():
    first = calcular_first()
    follow = calcular_follow(first)

    tabela = {}
    conflitos = []

    for nao_terminal, producoes in GRAMATICA.items():

        tabela[nao_terminal] = {}

        for producao in producoes:

            conjunto_first = first_da_sequencia(producao, first)

            # Para cada terminal do FIRST, registra a produção.
            for terminal in conjunto_first - {EPSILON}:

                if terminal in tabela[nao_terminal]:
                    conflitos.append(
                        (nao_terminal, terminal,
                         tabela[nao_terminal][terminal], producao)
                    )
                else:
                    tabela[nao_terminal][terminal] = producao

            # Se a produção pode gerar epsilon,
            # utiliza os símbolos do FOLLOW.
            if EPSILON in conjunto_first:

                for terminal in follow[nao_terminal]:

                    if terminal in tabela[nao_terminal]:
                        conflitos.append(
                            (nao_terminal, terminal,
                             tabela[nao_terminal][terminal], producao)
                        )
                    else:
                        tabela[nao_terminal][terminal] = producao

    return tabela, conflitos


def exibir_tabela():
    tabela, conflitos = construir_tabela()

    print("\n=== TABELA PREDITIVA LL(1) ===")

    for nao_terminal in sorted(tabela):

        for terminal in sorted(tabela[nao_terminal]):

            producao = tabela[nao_terminal][terminal]

            lado_direito = " ".join(producao) if producao else EPSILON

            print(
                f"M[{nao_terminal}, {terminal}] = "
                f"{nao_terminal} -> {lado_direito}"
            )

    print("\n=== VERIFICACAO DE CONFLITOS ===")

    if conflitos:
        print("Foram encontrados conflitos na tabela:")

        for conflito in conflitos:
            nao_terminal, terminal, producao1, producao2 = conflito

            print(
                f"Conflito em M[{nao_terminal}, {terminal}]: "
                f"{producao1} / {producao2}"
            )
    else:
        print("Nenhum conflito encontrado. A gramatica e LL(1)!")

    return tabela, conflitos


if __name__ == "__main__":
    exibir_tabela()
