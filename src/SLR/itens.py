
from SLR.grammar import (
    GRAMATICA_AUMENTADA,
    SIMBOLO_INICIAL_AUMENTADO,
    NAO_TERMINAIS
)


# Transforma a gramatica em uma lista de producoes.
# Cada producao possui um lado esquerdo e um lado direito.
PRODUCOES = []

for nao_terminal, alternativas in GRAMATICA_AUMENTADA.items():
    for alternativa in alternativas:
        PRODUCOES.append((nao_terminal, tuple(alternativa)))


# Organiza os indices das producoes por nao terminal.
PRODUCOES_POR_NAO_TERMINAL = {}

for indice, (nao_terminal, _) in enumerate(PRODUCOES):
    if nao_terminal not in PRODUCOES_POR_NAO_TERMINAL:
        PRODUCOES_POR_NAO_TERMINAL[nao_terminal] = []

    PRODUCOES_POR_NAO_TERMINAL[nao_terminal].append(indice)


def exibir_item(item):
    indice_producao, posicao_ponto = item

    nao_terminal, producao = PRODUCOES[indice_producao]

    elementos = list(producao)
    elementos.insert(posicao_ponto, ".")

    direita = " ".join(elementos)

    if not direita:
        direita = "."

    return f"{nao_terminal} -> {direita}"


def closure(itens_iniciais):
    itens = set(itens_iniciais)

    mudou = True

    while mudou:
        mudou = False

        for indice, posicao in list(itens):
            nao_terminal, producao = PRODUCOES[indice]

            # Verifica se existe simbolo depois do ponto.
            if posicao >= len(producao):
                continue

            simbolo = producao[posicao]

            # Se for um nao terminal, adiciona suas producoes.
            if simbolo in NAO_TERMINAIS:
                for novo_indice in PRODUCOES_POR_NAO_TERMINAL.get(
                    simbolo, []
                ):
                    novo_item = (novo_indice, 0)

                    if novo_item not in itens:
                        itens.add(novo_item)
                        mudou = True

    return itens


def goto(itens, simbolo):
    novos_itens = set()

    for indice, posicao in itens:
        nao_terminal, producao = PRODUCOES[indice]

        # Verifica se o ponto esta antes do simbolo desejado.
        if posicao < len(producao) and producao[posicao] == simbolo:

            # Avanca o ponto uma posicao.
            novos_itens.add((indice, posicao + 1))

    # Calcula o fechamento dos novos itens.
    if novos_itens:
        return closure(novos_itens)

    return set()

def construir_estados():

    # Cria o estado inicial.
    indice_inicial = PRODUCOES_POR_NAO_TERMINAL[
        SIMBOLO_INICIAL_AUMENTADO
    ][0]

    estado_inicial = frozenset(
        closure({(indice_inicial, 0)})
    )

    estados = [estado_inicial]

    # Guarda as transicoes entre os estados.
    transicoes = {}

    indice = 0

    # Percorre os estados enquanto houver novos para analisar.
    while indice < len(estados):

        estado_atual = estados[indice]

        # Descobre quais simbolos aparecem depois dos pontos.
        simbolos = set()

        for numero_producao, posicao in estado_atual:
            _, producao = PRODUCOES[numero_producao]

            if posicao < len(producao):
                simbolos.add(producao[posicao])

        # Calcula o GOTO para cada simbolo encontrado.
        for simbolo in sorted(simbolos):

            novo_estado = frozenset(
                goto(estado_atual, simbolo)
            )

            if not novo_estado:
                continue

            # Verifica se o estado ja existe.
            if novo_estado not in estados:
                estados.append(novo_estado)

            destino = estados.index(novo_estado)

            transicoes[(indice, simbolo)] = destino

        indice += 1

    return estados, transicoes

def exibir_itens(itens):
    for item in sorted(itens):
        print(exibir_item(item))




if __name__ == "__main__":

    estados, transicoes = construir_estados()

    print("=== AUTOMATO LR(0) ===")

    print("\nQuantidade de estados:", len(estados))

    for numero, estado in enumerate(estados):

        print(f"\n=== ESTADO {numero} ===")
        exibir_itens(estado)

    print("\n=== TRANSICOES ===")

    for (origem, simbolo), destino in sorted(transicoes.items()):
        print(f"Estado {origem} -- {simbolo} --> Estado {destino}")

