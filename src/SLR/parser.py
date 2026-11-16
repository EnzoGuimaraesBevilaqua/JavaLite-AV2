
from SLR.itens import PRODUCOES
from SLR.tabela import construir_tabela


class ParserSLR:

    def __init__(self, tokens):
        self.tokens = tokens

        (
            self.estados,
            self.first,
            self.follow,
            self.action,
            self.goto,
            self.conflitos
        ) = construir_tabela()

    def analisar(self):

        # Verifica se a tabela SLR(1) possui conflitos.
        if self.conflitos:
            print("Erro: a tabela SLR(1) possui conflitos!")

            for conflito in self.conflitos:
                print(
                    f"Estado {conflito['estado']}, "
                    f"simbolo {conflito['simbolo']}: "
                    f"{conflito['acao_existente']} x "
                    f"{conflito['nova_acao']}"
                )

            return False

        # Verifica se a sequencia de tokens termina em EOF.
        if not self.tokens or self.tokens[-1].tipo != "EOF":
            print(
                "Codigo rejeitado! "
                "Sequencia de tokens incompleta: "
                "marcador EOF ausente."
            )
            return False

        pilha_estados = [0]
        posicao = 0

        while True:

            # Protecao contra acesso fora da lista de tokens.
            if posicao >= len(self.tokens):
                print(
                    "Codigo rejeitado! "
                    "Fim inesperado da sequencia de tokens."
                )
                return False

            estado_atual = pilha_estados[-1]
            token_atual = self.tokens[posicao]

            tipo_token = token_atual.tipo

            acao = self.action[estado_atual].get(tipo_token)

            # Nenhuma acao encontrada: erro sintatico.
            if acao is None:

                esperados = sorted(self.action[estado_atual].keys())

                print("Codigo rejeitado!")
                print(
                    f"Linha {token_atual.linha}, "
                    f"coluna {token_atual.coluna}: "
                    f"token inesperado '{token_atual.lexema}' "
                    f"ao analisar o estado {estado_atual}. "
                    f"Esperado um dos seguintes: "
                    f"{', '.join(esperados)}."
                )

                return False

            tipo_acao = acao[0]

            # SHIFT: desloca o token e muda de estado.
            if tipo_acao == "SHIFT":

                proximo_estado = acao[1]

                pilha_estados.append(proximo_estado)
                posicao += 1

            # REDUCE: aplica uma producao da gramatica.
            elif tipo_acao == "REDUCE":

                indice_producao = acao[1]

                nao_terminal, producao = PRODUCOES[indice_producao]

                quantidade_simbolos = len(producao)

                if quantidade_simbolos > 0:
                    del pilha_estados[-quantidade_simbolos:]

                estado_atual = pilha_estados[-1]

                proximo_estado = self.goto[estado_atual].get(nao_terminal)

                if proximo_estado is None:
                    print(
                        "Erro interno: transicao GOTO "
                        f"nao encontrada para {nao_terminal}."
                    )
                    return False

                pilha_estados.append(proximo_estado)

            # ACCEPT: programa sintaticamente correto.
            elif tipo_acao == "ACCEPT":

                print(
                    "Codigo aceito! "
                    "Nenhum erro sintatico encontrado."
                )

                return True


if __name__ == "__main__":
    print("Parser SLR(1) carregado com sucesso!")