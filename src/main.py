
from pathlib import Path

from lexer import Lexer
from LL1.parser import ParserLL1
from SLR.parser import ParserSLR


# Caminho da pasta examples.
PASTA_EXEMPLOS = Path(__file__).parent.parent / "examples"

# Nome do arquivo que sera analisado.
ARQUIVO = "08_erro_lexico.jlite"

# Leitura do codigo-fonte.
caminho = PASTA_EXEMPLOS / ARQUIVO
codigo = caminho.read_text(encoding="utf-8")

print(f"Arquivo analisado: {ARQUIVO}")

# Primeira etapa: analise lexica.
lexer = Lexer(codigo)
tokens, erros_lexicos = lexer.analisar()

print("\n=== ANALISE LEXICA ===")

if erros_lexicos:
    for erro in erros_lexicos:
        print(erro)

    print("\nAnalise sintatica nao executada.")

else:
    print("Nenhum erro lexico encontrado!")

    # Segunda etapa: analise sintatica LL(1).
    print("\n=== ANALISE SINTATICA LL(1) ===")

    parser_ll1 = ParserLL1(tokens)
    aceito_ll1, erros_sintaticos = parser_ll1.analisar()

    if aceito_ll1:
        print("Codigo aceito! Nenhum erro sintatico encontrado.")
    else:
        print("Codigo rejeitado!")

        for erro in erros_sintaticos:
            print(erro)

    # Terceira etapa: analise sintatica SLR(1).
    print("\n=== ANALISE SINTATICA SLR(1) ===")

    parser_slr = ParserSLR(tokens)
    parser_slr.analisar()
