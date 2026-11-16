
from dataclasses import dataclass


# ==========================================
# ESTRUTURA DOS TOKENS
# ==========================================

@dataclass
class Token:
    tipo: str
    lexema: str
    linha: int
    coluna: int


# ==========================================
# PALAVRAS RESERVADAS
# ==========================================

PALAVRAS_RESERVADAS = {
    "main": "MAIN",
    "int": "INT",
    "float": "FLOAT",
    "boolean": "BOOLEAN",
    "string": "STRING",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "read": "READ",
    "print": "PRINT",
    "true": "TRUE",
    "false": "FALSE"
}


# ==========================================
# OPERADORES COM MAIS DE UM CARACTERE
# ==========================================

OPERADORES_COMPOSTOS = {
    "**": "POWER",
    "&&": "AND",
    "||": "OR",
    "==": "EQUAL",
    "!=": "NOT_EQUAL",
    ">=": "GREATER_EQ",
    "<=": "LESS_EQ"
}


# ==========================================
# OPERADORES E SIMBOLOS SIMPLES
# ==========================================

SIMBOLOS = {
    ";": "SEMI",
    ",": "COMMA",
    "(": "OPEN_PAR",
    ")": "CLOSE_PAR",
    "{": "OPEN_BRACE",
    "}": "CLOSE_BRACE",
    "=": "ASSIGN",
    ">": "GREATER",
    "<": "LESS",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULT",
    "/": "DIV",
    "%": "MOD",
    "!": "NOT"
}


# ==========================================
# ANALISADOR LEXICO
# ==========================================

class Lexer:

    def __init__(self, codigo):
        self.codigo = codigo
        self.posicao = 0
        self.linha = 1
        self.coluna = 1

        self.tokens = []
        self.erros = []

    def atual(self):
        if self.posicao >= len(self.codigo):
            return None

        return self.codigo[self.posicao]

    def proximo(self):
        if self.posicao + 1 >= len(self.codigo):
            return None

        return self.codigo[self.posicao + 1]

    def avancar(self):
        caractere = self.atual()

        self.posicao += 1

        if caractere == "\n":
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1

        return caractere

    def adicionar_token(self, tipo, lexema, linha, coluna):
        self.tokens.append(
            Token(tipo, lexema, linha, coluna)
        )

    def analisar(self):

        while self.atual() is not None:

            caractere = self.atual()

            # Ignorar espaços e quebras de linha
            if caractere in " \t\r\n":
                self.avancar()
                continue

            linha_inicial = self.linha
            coluna_inicial = self.coluna

            # ==================================
            # IDENTIFICADORES E PALAVRAS RESERVADAS
            # ==================================

            if caractere.isalpha() or caractere == "_":

                inicio = self.posicao

                while (
                    self.atual() is not None
                    and (
                        self.atual().isalnum()
                        or self.atual() == "_"
                    )
                ):
                    self.avancar()

                lexema = self.codigo[inicio:self.posicao]

                tipo = PALAVRAS_RESERVADAS.get(lexema, "ID")

                self.adicionar_token(
                    tipo, lexema, linha_inicial, coluna_inicial
                )

                continue

            # ==================================
            # NUMEROS INTEIROS E REAIS
            # ==================================

            if caractere.isdigit():

                inicio = self.posicao

                while (
                    self.atual() is not None
                    and self.atual().isdigit()
                ):
                    self.avancar()

                tipo = "INTEGER"

                if (
                    self.atual() == "."
                    and self.proximo() is not None
                    and self.proximo().isdigit()
                ):
                    self.avancar()

                    while (
                        self.atual() is not None
                        and self.atual().isdigit()
                    ):
                        self.avancar()

                    tipo = "REAL"

                lexema = self.codigo[inicio:self.posicao]

                self.adicionar_token(
                    tipo, lexema, linha_inicial, coluna_inicial
                )

                continue

            # ==================================
            # LITERAIS DE TEXTO
            # ==================================

            if caractere == '"':

                self.avancar()
                inicio = self.posicao - 1

                while (
                    self.atual() is not None
                    and self.atual() != '"'
                    and self.atual() != "\n"
                ):

                    if self.atual() == "\\" and self.proximo() is not None:
                        self.avancar()

                    self.avancar()

                if self.atual() == '"':

                    self.avancar()

                    lexema = self.codigo[inicio:self.posicao]

                    self.adicionar_token(
                        "STRING_LITERAL",
                        lexema,
                        linha_inicial,
                        coluna_inicial
                    )

                else:

                    self.erros.append(
                        f"Linha {linha_inicial}, coluna {coluna_inicial}: "
                        "literal de texto não finalizado."
                    )

                continue

            # ==================================
            # OPERADORES COMPOSTOS
            # ==================================

            dois_caracteres = (
                caractere + self.proximo()
                if self.proximo() is not None
                else None
            )

            if dois_caracteres in OPERADORES_COMPOSTOS:

                self.avancar()
                self.avancar()

                self.adicionar_token(
                    OPERADORES_COMPOSTOS[dois_caracteres],
                    dois_caracteres,
                    linha_inicial,
                    coluna_inicial
                )

                continue

            # ==================================
            # OPERADORES E SIMBOLOS SIMPLES
            # ==================================

            if caractere in SIMBOLOS:

                self.avancar()

                self.adicionar_token(
                    SIMBOLOS[caractere],
                    caractere,
                    linha_inicial,
                    coluna_inicial
                )

                continue

            # ==================================
            # CARACTERE DESCONHECIDO
            # ==================================

            self.erros.append(
                f"Linha {linha_inicial}, coluna {coluna_inicial}: "
                f"caractere não reconhecido '{caractere}'."
            )

            self.avancar()

        # ======================================
        # FIM DA ENTRADA
        # ======================================

        self.adicionar_token(
            "EOF",
            "",
            self.linha,
            self.coluna
        )

        return self.tokens, self.erros
