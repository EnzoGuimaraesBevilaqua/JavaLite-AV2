
from LL1.grammar import GRAMATICA, SIMBOLO_INICIAL
from LL1.tabela import construir_tabela


class ParserLL1:

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.tabela, self.conflitos = construir_tabela()
        self.erros = []

    def token_atual(self):
        if self.posicao >= len(self.tokens):
            return None

        return self.tokens[self.posicao]

    def analisar(self):

        # Reinicializa o estado para permitir novas analises.
        self.posicao = 0
        self.erros = []

        # Verifica se a tabela LL(1) possui conflitos.
        if self.conflitos:

            self.erros.append(
                "A gramatica possui conflitos e nao pode ser "
                "utilizada pelo parser LL(1)."
            )

            for conflito in self.conflitos:
                
                nao_terminal, simbolo, producao_existente, nova_producao = conflito

                self.erros.append(
                    f"Conflito no nao terminal {nao_terminal}, "
                    f"simbolo {simbolo}: "
                    f"{producao_existente} x {nova_producao}."
                )

            return False, self.erros

        # Verifica se a sequencia de tokens termina em EOF.
        if not self.tokens or self.tokens[-1].tipo != "EOF":

            self.erros.append(
                "Sequencia de tokens incompleta: "
                "marcador EOF ausente."
            )

            return False, self.erros

        # Pilha inicial do analisador.
        pilha = [SIMBOLO_INICIAL]

        while pilha:

            topo = pilha[-1]
            token = self.token_atual()

            if token is None:
                self.erros.append(
                    "Fim inesperado da sequencia de tokens."
                )
                return False, self.erros

            tipo_token = token.tipo

            # Caso 1: o topo da pilha e um terminal.
            if topo not in GRAMATICA:

                if topo == tipo_token:
                    pilha.pop()
                    self.posicao += 1

                else:
                    self.erros.append(
                        f"Linha {token.linha}, coluna {token.coluna}: "
                        f"esperado '{topo}', mas encontrado "
                        f"'{token.lexema or 'fim do arquivo'}'."
                    )
                    return False, self.erros

            # Caso 2: o topo da pilha e um nao terminal.
            else:

                producao = self.tabela.get(topo, {}).get(tipo_token)

                if producao is None:

                    esperados = sorted(
                        self.tabela.get(topo, {}).keys()
                    )

                    self.erros.append(
                        f"Linha {token.linha}, coluna {token.coluna}: "
                        f"token inesperado "
                        f"'{token.lexema or 'fim do arquivo'}' "
                        f"ao analisar {topo}. "
                        f"Esperado um dos seguintes: "
                        f"{', '.join(esperados)}."
                    )

                    return False, self.erros

                # Remove o nao terminal da pilha.
                pilha.pop()

                # Insere a producao na ordem inversa.
                # Uma lista vazia representa epsilon.
                for simbolo in reversed(producao):
                    pilha.append(simbolo)

        # A analise so e aceita se todos os tokens foram consumidos.
        if self.posicao == len(self.tokens):
            return True, self.erros

        token = self.token_atual()

        self.erros.append(
            f"Linha {token.linha}, coluna {token.coluna}: "
            "existem tokens restantes apos o fim da analise."
        )

        return False, self.erros
