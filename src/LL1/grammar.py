
# ==========================================
# GRAMATICA JAVALITE
# ==========================================

# Uma lista vazia [] representa epsilon (producao vazia).

GRAMATICA = {

    "PROGRAM": [
        ["MAIN_BLOCK", "EOF"]
    ],

    "MAIN_BLOCK": [
        ["MAIN", "OPEN_PAR", "CLOSE_PAR", "BLOCK"]
    ],

    "BLOCK": [
        ["OPEN_BRACE", "STATEMENTS", "CLOSE_BRACE"]
    ],

    "STATEMENTS": [
        ["STATEMENT", "STATEMENTS"],
        []
    ],

    "STATEMENT": [
        ["DECLARATION"],
        ["ASSIGNMENT"],
        ["IF_STATEMENT"],
        ["WHILE_STATEMENT"],
        ["READ_STATEMENT"],
        ["PRINT_STATEMENT"]
    ],

    "DECLARATION": [
    ["TYPE", "ID", "DECLARATION_TAIL"]
],

"DECLARATION_TAIL": [
    ["ASSIGN", "EXPRESSION", "SEMI"],
    ["SEMI"]
],

    "TYPE": [
        ["INT"],
        ["FLOAT"],
        ["BOOLEAN"],
        ["STRING"]
    ],

    "ASSIGNMENT": [
        ["ID", "ASSIGN", "EXPRESSION", "SEMI"]
    ],

    "IF_STATEMENT": [
        [
            "IF", "OPEN_PAR", "CONDITION",
            "CLOSE_PAR", "BLOCK", "ELSE_PART"
        ]
    ],

    "ELSE_PART": [
        ["ELSE", "BLOCK"],
        []
    ],

    "WHILE_STATEMENT": [
        [
            "WHILE", "OPEN_PAR", "CONDITION",
            "CLOSE_PAR", "BLOCK"
        ]
    ],

    "READ_STATEMENT": [
        ["READ", "OPEN_PAR", "ID", "CLOSE_PAR", "SEMI"]
    ],

    "PRINT_STATEMENT": [
        ["PRINT", "OPEN_PAR", "EXPRESSION", "CLOSE_PAR", "SEMI"]
    ],

    "CONDITION": [
        ["LOGICAL_OR"]
    ],

    "LOGICAL_OR": [
        ["LOGICAL_AND", "LOGICAL_OR_TAIL"]
    ],

    "LOGICAL_OR_TAIL": [
        ["OR", "LOGICAL_AND", "LOGICAL_OR_TAIL"],
        []
    ],

    "LOGICAL_AND": [
        ["LOGICAL_NOT", "LOGICAL_AND_TAIL"]
    ],

    "LOGICAL_AND_TAIL": [
        ["AND", "LOGICAL_NOT", "LOGICAL_AND_TAIL"],
        []
    ],

    "LOGICAL_NOT": [
        ["NOT", "LOGICAL_NOT"],
        ["CONDITION_ATOM"]
    ],

    "CONDITION_ATOM": [
        ["EXPRESSION", "COMPARISON_TAIL"]
    ],

    "COMPARISON_TAIL": [
        ["COMPARISON_OPERATOR", "EXPRESSION"],
        []
    ],

    "COMPARISON_OPERATOR": [
        ["EQUAL"],
        ["NOT_EQUAL"],
        ["GREATER"],
        ["LESS"],
        ["GREATER_EQ"],
        ["LESS_EQ"]
    ],

    "EXPRESSION": [
        ["ADDITIVE"]
    ],

    "ADDITIVE": [
        ["MULTIPLICATIVE", "ADDITIVE_TAIL"]
    ],

    "ADDITIVE_TAIL": [
        ["PLUS", "MULTIPLICATIVE", "ADDITIVE_TAIL"],
        ["MINUS", "MULTIPLICATIVE", "ADDITIVE_TAIL"],
        []
    ],

    "MULTIPLICATIVE": [
        ["POWER_EXPR", "MULTIPLICATIVE_TAIL"]
    ],

    "MULTIPLICATIVE_TAIL": [
        ["MULT", "POWER_EXPR", "MULTIPLICATIVE_TAIL"],
        ["DIV", "POWER_EXPR", "MULTIPLICATIVE_TAIL"],
        ["MOD", "POWER_EXPR", "MULTIPLICATIVE_TAIL"],
        []
    ],

    "POWER_EXPR": [
        ["FACTOR", "POWER_TAIL"]
    ],

    "POWER_TAIL": [
        ["POWER", "POWER_EXPR"],
        []
    ],

    "FACTOR": [
        ["ID"],
        ["INTEGER"],
        ["REAL"],
        ["STRING_LITERAL"],
        ["TRUE"],
        ["FALSE"],
        ["OPEN_PAR", "EXPRESSION", "CLOSE_PAR"]
    ]

}


# ==========================================
# CONFIGURACOES DA GRAMATICA
# ==========================================

SIMBOLO_INICIAL = "PROGRAM"

EPSILON = "ε"


# ==========================================
# IDENTIFICACAO DOS NAO TERMINAIS
# ==========================================

NAO_TERMINAIS = set(GRAMATICA.keys())


# ==========================================
# IDENTIFICACAO DOS TERMINAIS
# ==========================================

TERMINAIS = set()

for producoes in GRAMATICA.values():

    for producao in producoes:

        for simbolo in producao:

            if simbolo not in NAO_TERMINAIS:
                TERMINAIS.add(simbolo)


# ==========================================
# EXIBICAO DA GRAMATICA
# ==========================================

def exibir_gramatica():

    print("=== GRAMATICA JAVALITE ===\n")

    for nao_terminal, producoes in GRAMATICA.items():

        alternativas = []

        for producao in producoes:

            if producao:
                alternativas.append(" ".join(producao))
            else:
                alternativas.append(EPSILON)

        print(
            f"{nao_terminal} -> "
            + " | ".join(alternativas)
        )
