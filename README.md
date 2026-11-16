# JavaLite

Projeto acadêmico de implementação de um analisador léxico e de dois analisadores sintáticos para uma linguagem de programação simplificada, denominada **JavaLite**.

O projeto foi desenvolvido em Python e implementa os métodos de análise sintática **LL(1)** e **SLR(1)**, utilizando uma mesma linguagem e uma mesma sequência de tokens para permitir a comparação entre as duas abordagens.

## 1. Objetivo do projeto

O objetivo é desenvolver um compilador em sua etapa inicial, contemplando a análise léxica e a análise sintática de programas escritos em JavaLite.

O sistema realiza três etapas principais:

1. **Análise léxica:** identifica os lexemas presentes no código-fonte e os classifica em tokens.
2. **Análise sintática LL(1):** verifica se a sequência de tokens pertence à gramática utilizando análise preditiva descendente.
3. **Análise sintática SLR(1):** verifica a mesma sequência de tokens utilizando análise ascendente baseada em estados LR(0) e conjuntos FOLLOW.

Os dois analisadores sintáticos são implementados diretamente em Python, sem a utilização de bibliotecas externas de geração de parsers.

## 2. Sobre a linguagem JavaLite

JavaLite é uma linguagem simplificada, inspirada na sintaxe da linguagem Java. Seu objetivo é fornecer um conjunto de estruturas suficiente para demonstrar o funcionamento dos analisadores léxico e sintático.

### 2.1 Tipos de dados

A linguagem contempla os seguintes tipos:

- `int`: números inteiros.
- `float`: números reais.
- `boolean`: valores lógicos (`true` e `false`).
- `string`: literais de texto.

### 2.2 Estruturas da linguagem

São reconhecidos os seguintes recursos:

- Declaração de variáveis, com ou sem inicialização.
- Bloco principal de execução `main()`.
- Atribuição de valores a variáveis.
- Estruturas condicionais `if` e `else`.
- Estrutura de repetição `while`.
- Comando de entrada `read()`.
- Comando de saída `print()`.
- Expressões aritméticas.
- Expressões relacionais e lógicas.
- Expressões com parênteses e precedência entre operadores.

### 2.3 Operadores reconhecidos

**Aritméticos:**

| Operador | Operação |
|---|---|
| `+` | Adição |
| `-` | Subtração |
| `*` | Multiplicação |
| `/` | Divisão |
| `%` | Resto da divisão |
| `**` | Potenciação |

**Relacionais:**

| Operador | Operação |
|---|---|
| `==` | Igualdade |
| `!=` | Diferença |
| `>` | Maior que |
| `<` | Menor que |
| `>=` | Maior ou igual |
| `<=` | Menor ou igual |

**Lógicos:**

| Operador | Operação |
|---|---|
| `&&` | E lógico |
| `||` | OU lógico |
| `!` | Negação lógica |

### 2.4 Limitações da linguagem

JavaLite representa um subconjunto simplificado de Java. Portanto, nem todos os recursos da linguagem original estão implementados.

O projeto concentra-se nos elementos necessários para demonstrar a análise léxica e sintática, não contemplando, nesta versão, recursos como funções definidas pelo usuário, estruturas `for` e `do/while`, nem análise semântica ou execução do código-fonte.

## 3. Estrutura do projeto

A organização dos arquivos está dividida em exemplos, análise léxica e módulos específicos para cada método de análise sintática.

```text
JavaLite AV2/
│
├── examples/
│   ├── 01_declaracoes.jlite
│   ├── 02_expressoes_aritmeticas.jlite
│   ├── 03_condicoes_logicas.jlite
│   ├── 04_estruturas_controle.jlite
│   ├── 05_comandos_io.jlite
│   ├── 06_programa_completo.jlite
│   ├── 07_expressao_invalida.jlite
│   └── 08_erro_lexico.jlite
│
└── src/
    ├── main.py
    ├── lexer.py
    │
    ├── LL1/
    │   ├── grammar.py
    │   ├── first_follow.py
    │   ├── tabela.py
    │   └── parser.py
    │
    └── SLR/
        ├── grammar.py
        ├── itens.py
        ├── tabela.py
        └── parser.py
```

### Descrição dos módulos

**Arquivo `lexer.py`**

Implementa o analisador léxico, responsável por percorrer o código-fonte, reconhecer palavras reservadas, identificadores, números, literais de texto, operadores e símbolos. Também identifica e registra erros léxicos, informando a linha e a coluna em que ocorrem.

**Pasta `LL1/`**

Contém a implementação do analisador sintático LL(1):

- `grammar.py`: define a gramática utilizada pelo analisador.
- `first_follow.py`: calcula os conjuntos FIRST e FOLLOW.
- `tabela.py`: constrói e exibe a tabela de análise preditiva LL(1), verificando conflitos.
- `parser.py`: implementa o reconhecimento sintático utilizando pilha e tabela LL(1).

**Pasta `SLR/`**

Contém a implementação do analisador sintático SLR(1):

- `grammar.py`: prepara a gramática aumentada para a análise SLR(1).
- `itens.py`: implementa a construção dos itens LR(0), o fechamento (CLOSURE), a função GOTO e os estados do autômato.
- `tabela.py`: calcula FIRST e FOLLOW e constrói as tabelas ACTION e GOTO, verificando conflitos.
- `parser.py`: implementa o reconhecimento sintático ascendente utilizando pilha de estados e ações de deslocamento, redução e aceitação.

**Arquivo `main.py`**

Integra os três componentes principais do projeto. Carrega um arquivo de exemplo, executa a análise léxica e, caso não existam erros léxicos, encaminha a sequência de tokens para os analisadores LL(1) e SLR(1).

## 4. Requisitos para execução

Para executar o projeto, é necessário ter:

- Python instalado.
- Terminal ou ambiente de desenvolvimento capaz de executar arquivos Python.
- Sistema operacional compatível com a execução do Python.

Não são necessárias bibliotecas externas para a implementação dos analisadores.

## 5. Como executar o projeto

Abra o terminal na pasta raiz do projeto e entre na pasta `src`:

```powershell
cd .\src
```

### 5.1 Executar a análise completa

Para executar o analisador léxico e os dois analisadores sintáticos, utilize:

```powershell
python -X utf8 main.py
```

O arquivo de entrada é definido pela variável `ARQUIVO`, localizada no início de `main.py`.

Por padrão, é possível selecionar um dos arquivos da pasta `examples`, por exemplo:

```python
ARQUIVO = "06_programa_completo.jlite"
```

Para analisar outro exemplo, basta alterar o nome do arquivo nessa variável.

O programa executará as seguintes etapas:

1. Carregamento do código-fonte.
2. Análise léxica.
3. Verificação de erros léxicos.
4. Análise sintática LL(1), caso não existam erros léxicos.
5. Análise sintática SLR(1), caso não existam erros léxicos.

Se forem encontrados erros léxicos, a análise sintática não será executada.

### 5.2 Executar a tabela LL(1)

Para executar o módulo responsável pelo cálculo dos conjuntos e pela construção da tabela LL(1), utilize:

```powershell
python -X utf8 -m LL1.tabela
```

Esse comando calcula os conjuntos FIRST e FOLLOW, constrói a tabela de análise preditiva LL(1) e verifica a existência de conflitos na gramática.

### 5.3 Executar a tabela SLR(1)

Para executar o módulo responsável pela construção da tabela SLR(1), utilize:

```powershell
python -X utf8 -m SLR.tabela
```

Esse comando calcula os conjuntos FIRST e FOLLOW, constrói os estados e as transições do autômato LR(0), gera as tabelas ACTION e GOTO e verifica a existência de conflitos na tabela SLR(1).

## 6. Funcionamento dos analisadores sintáticos

### 6.1 Analisador LL(1)

O analisador LL(1) utiliza uma abordagem descendente preditiva. Seu funcionamento é baseado em uma pilha e em uma tabela de análise sintática.

Para sua implementação, a gramática passou pelas seguintes etapas:

1. Eliminação de ambiguidades.
2. Definição de precedência e associatividade dos operadores.
3. Eliminação da recursividade à esquerda.
4. Fatoração da gramática.

Em seguida, são calculados os conjuntos FIRST e FOLLOW, utilizados na construção da tabela LL(1).

Durante a análise, o parser consulta a tabela para determinar qual produção deve ser aplicada, comparando os símbolos da pilha com os tokens recebidos.

Caso a sequência seja reconhecida completamente, o código é aceito. Caso contrário, é apresentada uma mensagem de erro sintático.

### 6.2 Analisador SLR(1)

O analisador SLR(1) utiliza uma abordagem ascendente baseada em estados e itens LR(0).

Sua implementação contempla:

1. Construção da gramática aumentada.
2. Construção dos itens LR(0).
3. Cálculo do fechamento (CLOSURE).
4. Implementação da função GOTO.
5. Construção dos estados e transições do autômato.
6. Cálculo dos conjuntos FIRST e FOLLOW.
7. Construção das tabelas ACTION e GOTO.

Durante a análise, o parser utiliza uma pilha de estados e consulta a tabela ACTION para realizar as operações:

- **SHIFT:** desloca o próximo token e avança para outro estado.
- **REDUCE:** aplica uma produção da gramática.
- **ACCEPT:** indica que a sequência de tokens foi reconhecida.

As operações GOTO determinam o próximo estado após uma redução.

As reduções são inseridas na tabela SLR(1) utilizando os conjuntos FOLLOW dos não terminais correspondentes.

## 7. Exemplos e testes

O projeto possui oito arquivos de exemplo para verificar o funcionamento do analisador léxico e dos dois analisadores sintáticos.

| Arquivo | Conteúdo | Resultado esperado |
|---|---|---|
| `01_declaracoes.jlite` | Declarações de variáveis e tipos de dados | Aceito |
| `02_expressoes_aritmeticas.jlite` | Operações e expressões aritméticas | Aceito |
| `03_condicoes_logicas.jlite` | Operadores relacionais e lógicos | Aceito |
| `04_estruturas_controle.jlite` | Estruturas condicionais e repetição | Aceito |
| `05_comandos_io.jlite` | Comandos de entrada e saída | Aceito |
| `06_programa_completo.jlite` | Combinação dos recursos da linguagem | Aceito |
| `07_expressao_invalida.jlite` | Erro na construção de uma expressão aritmética | Rejeitado |
| `08_erro_lexico.jlite` | Presença de caractere não reconhecido | Erro léxico |

Os seis primeiros exemplos verificam construções válidas da linguagem e devem ser aceitos pelos dois analisadores sintáticos.

O sétimo exemplo apresenta uma expressão aritmética inválida. Nesse caso, a análise léxica é concluída sem erros, mas os analisadores LL(1) e SLR(1) rejeitam o código por erro sintático.

O oitavo exemplo apresenta um caractere não reconhecido pelo lexer. Nesse caso, o erro é identificado durante a análise léxica e a análise sintática não é executada.

## 8. Considerações finais

O projeto JavaLite demonstra a implementação de diferentes estratégias de análise sintática aplicadas a uma mesma linguagem de programação.

A utilização dos métodos LL(1) e SLR(1) permite observar as diferenças entre uma abordagem descendente preditiva e uma abordagem ascendente baseada em deslocamentos e reduções.

A implementação também demonstra a integração entre análise léxica e análise sintática, além da construção de conjuntos, tabelas e estados necessários ao funcionamento dos algoritmos.

O projeto foi desenvolvido com foco nos conceitos estudados na disciplina de Autômatos e Compiladores.
