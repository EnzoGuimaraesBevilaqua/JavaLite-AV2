
from SLR.grammar import (
    GRAMATICA_AUMENTADA,
    SIMBOLO_INICIAL_AUMENTADO,
    NAO_TERMINAIS,
    TERMINAIS
)

from SLR.itens import (
    PRODUCOES,
    construir_estados
)


EPSILON = "ε"
FIM_ENTRADA = "EOF"


# ==================================================
# CALCULO DOS CONJUNTOS FIRST
# ==================================================

def calcular_first():

    first = {
        nao_terminal: set()
        for nao_terminal in NAO_TERMINAIS
    }

    mudou = True

    while mudou:
        mudou = False

        for nao_terminal, producoes in GRAMATICA_AUMENTADA.items():

            for producao in producoes:

                conjunto = first_da_sequencia(producao, first)

                tamanho_anterior = len(first[nao_terminal])

                first[nao_terminal].update(conjunto)

                if len(first[nao_terminal]) != tamanho_anterior:
                    mudou = True

    return first


def first_da_sequencia(sequencia, first):

    if not sequencia:
        return {EPSILON}

    resultado = set()

    for simbolo in sequencia:

        if simbolo in TERMINAIS:
            resultado.add(simbolo)
            return resultado

        resultado.update(first[simbolo] - {EPSILON})

        if EPSILON not in first[simbolo]:
            return resultado

    resultado.add(EPSILON)

    return resultado


# ==================================================
# CALCULO DOS CONJUNTOS FOLLOW
# ==================================================

def calcular_follow(first):

    follow = {
        nao_terminal: set()
        for nao_terminal in NAO_TERMINAIS
    }

    # O fim da entrada acompanha o simbolo inicial aumentado.
    follow[SIMBOLO_INICIAL_AUMENTADO].add(FIM_ENTRADA)

    mudou = True

    while mudou:
        mudou = False

        for esquerda, producoes in GRAMATICA_AUMENTADA.items():

            for producao in producoes:

                for i, simbolo in enumerate(producao):

                    if simbolo not in NAO_TERMINAIS:
                        continue

                    restante = producao[i + 1:]

                    first_restante = first_da_sequencia(
                        restante,
                        first
                    )

                    novos = first_restante - {EPSILON}

                    tamanho_anterior = len(follow[simbolo])

                    follow[simbolo].update(novos)

                    if EPSILON in first_restante:
                        follow[simbolo].update(follow[esquerda])

                    if len(follow[simbolo]) != tamanho_anterior:
                        mudou = True

    return follow


# ==================================================
# CONSTRUCAO DA TABELA ACTION E GOTO
# ==================================================

def construir_tabela():

    estados, transicoes = construir_estados()

    first = calcular_first()
    follow = calcular_follow(first)

    action = [
        {}
        for _ in estados
    ]

    goto = [
        {}
        for _ in estados
    ]

    conflitos = []

    def adicionar_acao(estado, simbolo, acao):

        existente = action[estado].get(simbolo)

        if existente is None:
            action[estado][simbolo] = acao

        elif existente != acao:
            conflitos.append({
                "estado": estado,
                "simbolo": simbolo,
                "acao_existente": existente,
                "nova_acao": acao
            })

    # 1. Processa as transicoes entre estados.
    for (origem, simbolo), destino in transicoes.items():

        if simbolo in TERMINAIS:

            adicionar_acao(
                origem,
                simbolo,
                ("SHIFT", destino)
            )

        elif simbolo in NAO_TERMINAIS:

            goto[origem][simbolo] = destino

    # 2. Processa os itens completos para gerar reducoes.
    for numero_estado, estado in enumerate(estados):

        for indice_producao, posicao_ponto in estado:

            esquerda, direita = PRODUCOES[indice_producao]

            # Verifica se o ponto chegou ao final da producao.
            if posicao_ponto != len(direita):
                continue

            # 3. Verifica a producao inicial aumentada.
            if esquerda == SIMBOLO_INICIAL_AUMENTADO:

                adicionar_acao(
                    numero_estado,
                    FIM_ENTRADA,
                    ("ACCEPT",)
                )

            else:

                # 4. Adiciona reducoes nos simbolos de FOLLOW.
                for simbolo in follow[esquerda]:

                    adicionar_acao(
                        numero_estado,
                        simbolo,
                        ("REDUCE", indice_producao)
                    )

    return estados, first, follow, action, goto, conflitos


# ==================================================
# EXIBICAO DOS CONJUNTOS FIRST E FOLLOW
# ==================================================

def exibir_conjuntos(titulo, conjuntos):

    print(f"\n=== {titulo} ===")

    for nao_terminal in sorted(conjuntos):

        simbolos = sorted(conjuntos[nao_terminal])

        print(
            f"{nao_terminal}: "
            f"{{ {', '.join(simbolos)} }}"
        )


# ==================================================
# EXIBICAO DA TABELA ACTION E GOTO
# ==================================================

def exibir_tabela(action, goto):

    print("\n=== TABELA ACTION ===")

    for estado, acoes in enumerate(action):

        if not acoes:
            continue

        print(f"\nEstado {estado}:")

        for simbolo, acao in sorted(acoes.items()):

            if acao[0] == "SHIFT":
                descricao = f"S{acao[1]}"

            elif acao[0] == "REDUCE":
                descricao = f"R{acao[1]}"

            else:
                descricao = "ACC"

            print(f"  {simbolo} -> {descricao}")

    print("\n=== TABELA GOTO ===")

    for estado, transicoes in enumerate(goto):

        if not transicoes:
            continue

        print(f"\nEstado {estado}:")

        for simbolo, destino in sorted(transicoes.items()):

            print(f"  {simbolo} -> {destino}")


# ==================================================
# VERIFICACAO DE CONFLITOS
# ==================================================

def exibir_conflitos(conflitos):

    print("\n=== VERIFICACAO DE CONFLITOS ===")

    if not conflitos:

        print("Nenhum conflito encontrado! A gramatica e SLR(1).")

        return

    print(f"Total de conflitos encontrados: {len(conflitos)}")

    for conflito in conflitos:

        print(
            f"Estado {conflito['estado']}, "
            f"simbolo {conflito['simbolo']}: "
            f"{conflito['acao_existente']} "
            f"X {conflito['nova_acao']}"
        )


# ==================================================
# EXECUCAO DOS TESTES
# ==================================================

if __name__ == "__main__":

    (
        estados,
        first,
        follow,
        action,
        goto,
        conflitos
    ) = construir_tabela()

    print("=== ANALISE DA TABELA SLR(1) ===")

    print("\nQuantidade de estados:", len(estados))

    exibir_conjuntos("CONJUNTOS FIRST", first)

    exibir_conjuntos("CONJUNTOS FOLLOW", follow)

    exibir_tabela(action, goto)

    exibir_conflitos(conflitos)
