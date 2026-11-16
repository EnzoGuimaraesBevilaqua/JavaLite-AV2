
from LL1.grammar import (
    GRAMATICA as GRAMATICA_BASE,
    TERMINAIS as TERMINAIS_BASE
)

SIMBOLO_INICIAL_AUMENTADO = "INICIO_AUMENTADO"

# Criamos uma copia da gramatica LL(1),
# sem modificar o arquivo original.
GRAMATICA_AUMENTADA = {
    nao_terminal: [list(producao) for producao in producoes]
    for nao_terminal, producoes in GRAMATICA_BASE.items()
}

# Ajustamos a producao inicial para o SLR(1).
GRAMATICA_AUMENTADA["PROGRAM"] = [["MAIN_BLOCK"]]

# Adicionamos o novo simbolo inicial.
GRAMATICA_AUMENTADA[SIMBOLO_INICIAL_AUMENTADO] = [["PROGRAM"]]

NAO_TERMINAIS = set(GRAMATICA_AUMENTADA.keys())

# EOF sera utilizado como marcador externo de fim da entrada.
TERMINAIS = set(TERMINAIS_BASE) - {"EOF"}


def exibir_gramatica_aumentada():
    print("=== GRAMATICA AUMENTADA PARA SLR(1) ===")

    for nao_terminal, producoes in GRAMATICA_AUMENTADA.items():
        for producao in producoes:
            direita = " ".join(producao) if producao else "ε"
            print(f"{nao_terminal} -> {direita}")


if __name__ == "__main__":
    exibir_gramatica_aumentada()
