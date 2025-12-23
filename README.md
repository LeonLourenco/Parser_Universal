# Parser Universal para Gramáticas da Hierarquia de Chomsky

> Um parser de força bruta baseado em Busca em Profundidade (DFS) com otimização heurística, capaz de processar gramáticas de qualquer tipo da Hierarquia de Chomsky (Tipos 0, 1, 2 e 3).

## Descrição

Este projeto implementa um parser universal que, dada uma gramática formal $G$ e uma palavra $\omega$, determina se $\omega \in L(G)$ através de simulação exaustiva de derivações.

## Características Principais

* ✅ **Universal:** Suporta todos os 4 tipos da Hierarquia de Chomsky.
* ✅ **Busca em Profundidade (DFS):** Otimizada para gramáticas altamente recursivas onde a BFS falharia por falta de memória.
* ✅ **Otimização de Poda (Pruning):** Heurística de verificação de prefixo para cortar caminhos inválidos cedo.
* ✅ **Flexível:** Parâmetros configuráveis para profundidade, memória e otimização.

## Fundamentação Teórica

### Por que Busca em Profundidade (DFS)?

Inicialmente projetado com BFS (Busca em Largura), o parser foi migrado para DFS (usando estrutura de Pilha) para lidar com a **Explosão Combinatória** em gramáticas complexas, como a Forma Normal de Chomsky (FNC).

Em regras recursivas como `S -> SS`, a BFS consome memória exponencial ($O(b^d)$) tentando armazenar todas as combinações possíveis de um nível simultaneamente. A DFS mergulha em um caminho único, consumindo memória linear ($O(d)$) proporcional à profundidade da derivação. Isso permite encontrar soluções em árvores profundas onde a BFS travaria o sistema por exaustão de RAM.

### Otimização: Poda por Prefixo

Para evitar que a DFS se perca em caminhos infinitos ou incorretos, implementamos uma Poda (*Pruning*):

1.  Antes de adicionar um novo estado à pilha, verificamos se o início da string gerada (o prefixo de terminais) corresponde ao início da palavra alvo.
2.  Se não corresponder, o ramo inteiro é descartado imediatamente.

## Como Usar

### Instalação

Nenhuma dependência externa é necessária. Basta ter **Python 3.7+** instalado.

### Executando os Testes

Para rodar a bateria de testes incluída (Fibonacci, Regular, CSG, Irrestrita e FNC):

```bash
python grammar_parser.py
```
## Usando em seu Próprio Código
```python
from grammar_parser import GrammarParser

# 1. Configure o Parser
parser = GrammarParser(
    start_symbol='S',
    max_depth=100,      # DFS permite profundidades maiores
    max_states=200000
)

# 2. Defina a Gramática
grammar = """
S -> aSb:
S -> eps:
"""

parser.parse_grammar(grammar)

# 3. Teste uma palavra
# use_pruning=True é recomendado para Tipos 1, 2 e 3
palavra = "aaabbb"
pertence, derivacao = parser.parse(palavra, use_pruning=True)

if pertence:
    print("✓ Palavra aceita!")
    print("Derivação:", parser.format_derivation(derivacao))
else:
    print("✗ Palavra rejeitada")
```
## Formato da Gramática

### Sintaxe
`LHS -> RHS: comentário opcional`

### Regras de Escrita
* **Separador:** Use `->` para separar lado esquerdo e direito.
* **Vazio:** Use `eps`, `epsilon` (ou `ε` / `λ`).
* **Terminais:** Letras minúsculas e dígitos (`a-z`, `0-9`).
* **Não-terminais:** Letras maiúsculas (`A-Z`).

## Casos de Teste Incluídos

### Cenário 1: Desafio de Fibonacci (CFG - Tipo 2)
Gramática livre de contexto complexa onde a contagem de 'a's e 'b's segue a sequência de Fibonacci.

### Cenário 2: Linguagem Regular (Tipo 3)
Linguagem simples $a^*b$.

### Cenário 3: $a^n b^n c^n$ (CSG - Tipo 1)
A clássica linguagem sensível ao contexto que não pode ser gerada por autômatos de pilha, pois requer a contagem simultânea de três grupos de símbolos.

### Cenário 4: Gramática Irrestrita (Tipo 0)
Demonstra regras que alteram ou consomem terminais no meio da string (ex: `bCd -> X`).

> **⚠️ Nota Importante:** Neste caso, a otimização de poda (`use_pruning`) deve ser **DESATIVADA**, pois a verificação de prefixo falha quando terminais podem desaparecer.

**Gramática:**
```text
S -> abCde
bCd -> X
aXe -> afinal
```
* **Entrada:** `afinal`
* **Configuração:** `use_pruning=False`
* **Resultado:** ✓ Aceita

### Caso de Estudo: Forma Normal de Chomsky (FNC)

Teste de estresse com a gramática de parênteses balanceados. Devido à regra recursiva `S -> SS`, este caso gera estados exponencialmente. Ele serve para demonstrar a superioridade da **DFS + Poda** sobre a BFS em termos de consumo de memória para este tipo de problema.

## Parâmetros de Configuração

| Parâmetro | Descrição |
| :--- | :--- |
| **`use_pruning`** | **True (Padrão):** Verifica se o prefixo da string atual corresponde à palavra alvo. Essencial para performance em gramáticas recursivas (Tipos 1, 2, 3).<br><br>**False:** Obrigatório para Gramáticas Irrestritas (Tipo 0) onde regras podem deletar ou modificar terminais já gerados. |
| **`max_depth`** | Profundidade máxima da árvore de derivação. Na DFS, isso atua como um limite rígido para forçar o *backtracking* (voltar e tentar outro caminho). |
| **`max_states`** | Número máximo de passos totais permitidos antes de abortar a execução. Previne travamentos por loops infinitos. |

## 🎓 Autor

Desenvolvido como parte de atividade acadêmica sobre **Teoria da Computação**.