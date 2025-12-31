"""
Parser Universal para Gramáticas da Hierarquia de Chomsky
Implementação usando Busca em Profundidade (DFS)

Este módulo implementa um parser de força bruta capaz de processar
gramáticas de qualquer tipo da Hierarquia de Chomsky (0, 1, 2, 3).
"""

from collections import deque
from typing import List, Tuple, Optional, Set


class GrammarParser:
    """
    Parser universal para gramáticas formais usando DFS (Iterative Deepening/Stack).
    
    Attributes:
        productions: Lista de tuplas (LHS, RHS) representando regras gramaticais
        start_symbol: Símbolo inicial da gramática (padrão: 'S')
        max_depth: Profundidade máxima de derivação (Hard limit para DFS)
        max_states: Número máximo de estados a explorar
    """
    
    def __init__(self, start_symbol: str = 'S', max_depth: int = 50, max_states: int = 2000000000):
        self.productions: List[Tuple[str, str]] = []
        self.start_symbol = start_symbol
        self.max_depth = max_depth
        self.max_states = max_states
    
    def parse_grammar(self, grammar_text: str) -> None:
        """
        Faz o parsing de uma gramática em formato texto.
        """
        self.productions = []
        
        for line in grammar_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                line = line.split(':')[0].strip()
            
            if '->' in line:
                separator = '->'
            elif '→' in line:
                separator = '→'
            else:
                continue
            
            lhs, rhs = line.split(separator, 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            
            if rhs in ['ε', 'λ']:
                rhs = ''
            
            self.productions.append((lhs, rhs))

    def identify_grammar_type(self) -> str:
        """
        Identifica o tipo da gramática na Hierarquia de Chomsky (0, 1, 2, 3).
        """
        is_type_1 = True
        is_type_2 = True
        is_type_3 = True

        for lhs, rhs in self.productions:
            if len(lhs) != 1 or not lhs.isupper():
                is_type_2 = False
                is_type_3 = False
            
            if is_type_3:
                if len(rhs) > 2:
                    is_type_3 = False
                elif len(rhs) == 2 and not (rhs[0].islower() and rhs[1].isupper()):
                    is_type_3 = False
                elif len(rhs) == 1 and not rhs.islower():
                    is_type_3 = False
                elif len(rhs) == 0:
                    pass 

            if len(lhs) > len(rhs) and rhs != '':
                is_type_1 = False
            
        if is_type_3:
            return "Tipo 3 (Regular)"
        if is_type_2:
            return "Tipo 2 (Livre de Contexto)"
        if is_type_1:
            return "Tipo 1 (Sensível ao Contexto)"
        return "Tipo 0 (Irrestrita)"
    
    def find_all_occurrences(self, text: str, pattern: str) -> List[int]:
        positions = []
        start = 0
        while True:
            pos = text.find(pattern, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        return positions
    
    def apply_production(self, current: str, lhs: str, rhs: str) -> List[str]:
        results = []
        positions = self.find_all_occurrences(current, lhs)
        for pos in positions:
            new_string = current[:pos] + rhs + current[pos + len(lhs):]
            results.append(new_string)
        return results

    def is_promising(self, current_string: str, target_word: str) -> bool:
        if len(current_string) > len(target_word) + 5:
            return False

        terminal_prefix = ""
        for char in current_string:
            if char.isupper() or char.isdigit():
                break
            terminal_prefix += char
        
        if not target_word.startswith(terminal_prefix):
            return False
        return True
    
    def parse(self, target_word: str, verbose: bool = True, use_pruning: bool = True) -> Tuple[bool, Optional[List[str]]]:
        """
        Verifica se uma palavra pertence à linguagem gerada pela gramática.
        Usa DFS (Busca em Profundidade) para explorar derivações.
        """
        # Fila para DFS (Pilha): cada elemento é (string_atual, caminho_de_derivação)
        queue = deque([(self.start_symbol, [self.start_symbol])])
        visited: Set[str] = {self.start_symbol}
        states_explored = 0
        
        while queue and states_explored < self.max_states:
            # pop() sem argumentos remove da direita (LIFO -> Pilha -> DFS)
            current, path = queue.pop()
            states_explored += 1
            
            if current == target_word:
                if verbose:
                    print(f"✓ Palavra encontrada após explorar {states_explored} estados!")
                return True, path
            
            # Limite rígido de profundidade é crucial para DFS não entrar em loop infinito
            if len(path) > self.max_depth:
                continue
            
            if len(current) > len(target_word) * 3:
                continue
            
            for lhs, rhs in self.productions:
                if lhs in current:
                    derived = self.apply_production(current, lhs, rhs)
                    for new_string in derived:
                        if use_pruning and not self.is_promising(new_string, target_word):
                            continue

                        if new_string not in visited or len(path) < 10:
                            visited.add(new_string)
                            new_path = path + [new_string]
                            # append() adiciona na direita
                            queue.append((new_string, new_path))
        
        if verbose:
            print(f"✗ Palavra não encontrada após explorar {states_explored} estados.")
        return False, None
    
    def format_derivation(self, derivation: List[str]) -> str:
        return ' ⇒ '.join(derivation)


def test_grammar(name: str, grammar: str, test_word: str, expected: bool, use_pruning: bool = True) -> bool:
    print(f"\n{'='*70}")
    print(f"TESTE: {name}")
    print(f"{'='*70}")
    print(f"Palavra de entrada: '{test_word}'")
    print(f"Resultado esperado: {'Sim' if expected else 'Não'}")
    
    parser = GrammarParser(max_depth=100, max_states=200000)
    parser.parse_grammar(grammar)
    
    grammar_type = parser.identify_grammar_type()
    print(f"Classificação Detectada: {grammar_type}")
    print(f"Otimização (Poda): {'Ativada' if use_pruning else 'Desativada'}")
    print("-" * 30)

    print(f"Gramática carregada com {len(parser.productions)} produções:")
    for lhs, rhs in parser.productions:
        rhs_display = rhs if rhs else 'ε'
        print(f"  {lhs} → {rhs_display}")
    
    print(f"\nIniciando busca DFS...")
    belongs, derivation = parser.parse(test_word, verbose=True, use_pruning=use_pruning)
    
    print()
    if belongs:
        print("✓ RESULTADO: Sim, pertence a L(G)")
        print("\nCadeia de derivação:")
        print(parser.format_derivation(derivation))
    else:
        print("✗ RESULTADO: Não foi possível derivar a palavra")
    
    success = belongs == expected
    
    if not success:
        print(f"\n✗ ERRO NO TESTE: Esperava {expected}, obteve {belongs}")
    else:
        print(f"\n✓ TESTE PASSOU")
    
    return success

def main():
    print("="*70)
    print("PARSER UNIVERSAL - COM DETECÇÃO DE HIERARQUIA DE CHOMSKY")
    print("Implementação: Busca em Profundidade (DFS) com Verificação de Tipos")
    print("="*70)
    
    results = []
    
    # QUESTÃO 3: Forma Normal de Chomsky (FNC)
    
    # Tradução da solução matemática para o formato do parser:
    # L1=(, R1=), L2=[, R2=]
    fnc_grammar = """
    L1 -> (
    R1 -> )
    L2 -> [
    R2 -> ]
    S -> SS
    S -> L1R1
    S -> L2R2
    S -> L1C1
    C1 -> SR1
    S -> L2C2
    C2 -> SR2
    """

    # Teste A: Caso Simples de Aninhamento "([()])"
    # Derivação esperada (lógica): S => L1C1 => (SR1 => (L2C2) => ([SR2]) => ([L1R1]) => ([()])
    results.append(test_grammar(
        "Q3 - FNC Balanceamento (Aninhamento)",
        fnc_grammar,
        "([()])",
        True,
        use_pruning=True
    ))

    # Teste B: Caso de Concatenação "()[]"
    # Regra S -> SS é crucial aqui
    results.append(test_grammar(
        "Q3 - FNC Balanceamento (Concatenação)",
        fnc_grammar,
        "()[]",
        True,
        use_pruning=True
    ))

    # Teste C: Caso Inválido "([)"
    # Não deve ser aceito pois falta fechar o colchete e o parêntese
    results.append(test_grammar(
        "Q3 - FNC Balanceamento (Inválido)",
        fnc_grammar,
        "([)",
        False,
        use_pruning=True
    ))
    
    # CENÁRIO 1: FIBONACCI (CFG)
    fibonacci_grammar = """
    S -> aAB:
    A -> aA:
    A -> F1:
    F1 -> aF2b:
    F2 -> X:
    X -> aXb:
    X -> b:
    B -> bB:
    B -> ε:
    """
    
    results.append(test_grammar(
        "Cenário 1A - Fibonacci (CFG) - 6 'a's (Falso Positivo)",
        fibonacci_grammar,
        "aaaaaabbbbbbbb",
        True, 
        use_pruning=True
    ))

    print("\n>>> ATENÇÃO: O teste abaixo foi projetado para demonstrar a falha da CFG <<<")
    results.append(test_grammar(
        "Cenário 1B - Prova de Falha (Validação Numérica)",
        fibonacci_grammar,
        "aaaaaa", 
        False,    
        use_pruning=True
    ))
    
    # CENÁRIO 2: Linguagem Regular Simples
    regular_grammar = """
    S -> aS:
    S -> b:
    """
    results.append(test_grammar("Cenário 2 - Regular", regular_grammar, "aaab", True))
    
    # CENÁRIO 3: a^n b^n c^n (Sensível ao Contexto)
    context_sensitive = """
    S -> aSBC:
    S -> aBC:
    CB -> BC:
    aB -> ab:
    bB -> bb:
    bC -> bc:
    cC -> cc:
    """
    results.append(test_grammar("Cenário 3 - CSG", context_sensitive, "aabbcc", True))
    
    # CENÁRIO 4: Gramática Irrestrita (Tipo 0)
    unrestricted_grammar = """
    S -> abCde:
    bCd -> X:
    aXe -> afinal:
    """
    results.append(test_grammar("Cenário 4 - Irrestrita", unrestricted_grammar, "afinal", True, use_pruning=False))
    
    print("\n" + "="*70)
    print("SUMÁRIO DOS TESTES")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Testes passados: {passed}/{total}")
    
    if passed < total:
        print("\nNOTA: A falha no 'Cenário 1B' é esperada e prova a limitação da gramática.")
    print("="*70)


if __name__ == "__main__":
    main()