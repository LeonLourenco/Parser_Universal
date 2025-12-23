# Parser Universal para Gramáticas da Hierarquia de Chomsky

Um parser de força bruta baseado em **Busca em Largura (BFS)** capaz de processar gramáticas de qualquer tipo da Hierarquia de Chomsky (Tipos 0, 1, 2 e 3).

## Descrição

Este projeto implementa um parser universal que, dada uma gramática formal $G$ e uma palavra $\omega$, determina se $\omega \in L(G)$ através de simulação exaustiva de todas as derivações possíveis.

### Características Principais

- ✅ Suporta **todos os tipos** da Hierarquia de Chomsky
- ✅ Gramáticas Regulares (Tipo 3)
- ✅ Gramáticas Livres de Contexto (Tipo 2)
- ✅ Gramáticas Sensíveis ao Contexto (Tipo 1)
- ✅ Gramáticas Irrestritas/Recursivamente Enumeráveis (Tipo 0)
- ✅ Implementação com BFS para exploração sistemática
- ✅ Exibição completa da cadeia de derivação
- ✅ Proteção contra loops infinitos

## Por que Busca em Largura (BFS)?

A escolha de BFS para este parser é fundamentada em princípios teóricos sólidos:

### Completude do Algoritmo

Para gramáticas dos **Tipos 0 e 1**, onde as produções podem ter regras arbitrárias (inclusive com LHS > RHS), a BFS garante:

1. **Exploração Sistemática**: Todas as derivações de profundidade $k$ são exploradas antes das de profundidade $k+1$
2. **Menor Caminho**: Se existe uma derivação para a palavra, encontraremos a mais curta
3. **Semi-decidibilidade**: Para gramáticas Tipo 0, se a palavra pertence à linguagem, o algoritmo eventualmente a encontrará

### Vantagem sobre DFS

Uma busca em profundidade (DFS) poderia entrar em loops infinitos em ramificações recursivas antes de explorar outras possibilidades viáveis. A BFS evita este problema explorando todas as possibilidades de cada nível antes de avançar.

### Trade-offs

- **Vantagem**: Completude e garantia de encontrar a derivação mais curta
- **Desvantagem**: Alto consumo de memória para gramáticas ambíguas
- **Solução**: Limites de profundidade e número de estados para garantir terminação

## Como Usar

### Instalação

Nenhuma dependência externa é necessária. Basta ter Python 3.7+ instalado.

```bash
# Clone ou baixe o arquivo
python grammar_parser.py
```

### Executando os Testes Padrão

```bash
python grammar_parser.py
```

Isto executará automaticamente os 4 cenários de teste incluídos.

### Testando sua Própria Gramática

```python
from grammar_parser import GrammarParser

# Crie uma instância do parser
parser = GrammarParser(
    start_symbol='S',    # Símbolo inicial
    max_depth=50,        # Profundidade máxima de derivação
    max_states=100000    # Número máximo de estados a explorar
)

# Defina sua gramática
grammar = """
S -> aSb:
S -> ε:
"""

# Faça o parsing da gramática
parser.parse_grammar(grammar)

# Teste uma palavra
palavra = "aaabbb"
pertence, derivacao = parser.parse(palavra)

if pertence:
    print("✓ Palavra aceita!")
    print("Derivação:", parser.format_derivation(derivacao))
else:
    print("✗ Palavra rejeitada")
```

## Formato da Gramática

### Sintaxe

```
LHS -> RHS: comentário opcional
```

### Regras

- **Separador**: Use `->` entre lado esquerdo e direito
- **Fim de regra**: Marque com `:` (tudo após é comentário)
- **Epsilon**: Use `ε` ou `λ` para representar a palavra vazia
- **Terminais**: Letras minúsculas e dígitos (a-z, 0-9)
- **Não-terminais**: Letras maiúsculas (A-Z)

### Exemplos

```
# Gramática Regular: a*b
S -> aS: loop de 'a'
S -> b: finaliza com 'b'

# Gramática Sensível ao Contexto: a^n b^n c^n
S -> aSBC: adiciona símbolos
S -> aBC: base
CB -> BC: permuta para ordenar
aB -> ab: converte não-terminal
bB -> bb: propaga conversão
bC -> bc: inicia conversão de C
cC -> cc: propaga C
```

## Casos de Teste Incluídos

### Cenário 1: Desafio de Fibonacci (CFG)

**Tipo**: Gramática Livre de Contexto

**Descrição**: Aceita palavras no formato $a^m a^{F_n} b^{F_n} b^p$ onde $F_n$ é um número de Fibonacci.

```
Gramática:
S -> aAB
A -> aA | F1
F1 -> aF2b
F2 -> X
X -> aXb | b
B -> bB | ε

Entrada: aaaaaabbbbbbbb
Resultado: ✓ Aceita
```

### Cenário 2: Linguagem Regular (Tipo 3)

**Tipo**: Gramática Regular

**Descrição**: Linguagem $L = \{a^n b \mid n \geq 0\}$

```
Gramática:
S -> aS | b

Entrada: aaab
Resultado: ✓ Aceita
```

### Cenário 3: $a^n b^n c^n$ (CSG - Tipo 1)

**Tipo**: Gramática Sensível ao Contexto

**Descrição**: A clássica linguagem $L = \{a^n b^n c^n \mid n \geq 1\}$

```
Gramática:
S -> aSBC | aBC
CB -> BC
aB -> ab
bB -> bb
bC -> bc
cC -> cc

Entrada: aabbcc
Resultado: ✓ Aceita
```

### Cenário 4: Gramática Irrestrita (Tipo 0)

**Tipo**: Gramática Recursivamente Enumerável

**Descrição**: Demonstra regras que **encurtam** a string (LHS > RHS).

```
Gramática:
S -> abCde
bCd -> X         (3 símbolos → 1 símbolo)
aXe -> afinal

Entrada: afinal
Resultado: ✓ Aceita

Derivação: S ⇒ abCde ⇒ aXe ⇒ afinal
```

## Parâmetros de Configuração

### `max_depth`

- **Padrão**: 50
- **Descrição**: Profundidade máxima da cadeia de derivação
- **Quando ajustar**: Aumente para palavras que requerem muitas derivações

### `max_states`

- **Padrão**: 100.000
- **Descrição**: Número máximo de estados únicos a explorar
- **Quando ajustar**: Aumente para gramáticas muito ambíguas

### Exemplo de Ajuste

```python
# Para gramáticas complexas
parser = GrammarParser(max_depth=200, max_states=500000)
```

## Complexidade

### Temporal

- **Pior caso**: $O(b^d)$ onde:
  - $b$ = fator de ramificação (número médio de derivações por estado)
  - $d$ = profundidade da solução

### Espacial

- **Memória**: $O(b^d)$ para armazenar a fila e estados visitados

### Otimizações Implementadas

1. **Conjunto de visitados**: Evita reprocessar estados idênticos
2. **Poda por tamanho**: Descarta derivações muito maiores que o alvo
3. **Limites configuráveis**: Previne explosão combinatória

## Conceitos Teóricos

### Hierarquia de Chomsky

| Tipo | Nome | Restrições | Autômato |
|------|------|------------|----------|
| 3 | Regular | $A \to aB$ ou $A \to a$ | Finito |
| 2 | Livre de Contexto | $A \to \alpha$ | Pilha |
| 1 | Sensível ao Contexto | $\|\alpha\| \leq \|\beta\|$ em $\alpha \to \beta$ | Linear Limitado |
| 0 | Recursivamente Enumerável | Sem restrições | Turing |

### Decidibilidade

- **Tipos 2 e 3**: Problema de pertinência é **decidível** (sempre termina)
- **Tipo 1**: Decidível, mas complexidade PSPACE-completo
- **Tipo 0**: **Semi-decidível** (se pertence, encontra; se não pertence, pode não terminar)

## Contribuindo

Para adicionar novos testes:

```python
# No final da função main()
test_grammar(
    "Meu Teste",
    """
    S -> aSa:
    S -> bSb:
    S -> ε:
    """,
    "aabbaa",
    True
)
```

## Referências

- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*
- Sipser, M. (2012). *Introduction to the Theory of Computation*
- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (BFS Algorithm)

## Licença

Este projeto é disponibilizado para fins educacionais. Sinta-se livre para usar e modificar.

## Autor

Desenvolvido como parte de uma atividade universitária sobre Teoria da Computação e Linguagens Formais da UFRPE.
