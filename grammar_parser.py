from collections import deque
from typing import List, Tuple, Optional, Set

class GrammarParser:
    """
    Parser universal para gramáticas formais usando BFS.
    """
    
    def __init__(self, start_symbol: str = 'S', max_depth: int = 50, max_states: int = 100000):
        self.productions: List[Tuple[str, str]] = []
        self.start_symbol = start_symbol
        self.max_depth = max_depth
        self.max_states = max_states
    
    def parse_grammar(self, grammar_text: str) -> None:
        """Faz o parsing de uma gramática em formato texto."""
        self.productions = []
        
        for line in grammar_text.strip().split('\n'):
            line = line.strip()
            if not line: continue
            
            # Remove comentários
            if ':' in line:
                line = line.split(':')[0].strip()
            
            if '->' not in line: continue
            
            lhs, rhs = line.split('->', 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            
            # Trata epsilon
            if rhs in ['ε', 'λ']:
                rhs = ''
            
            self.productions.append((lhs, rhs))
            
    def find_all_occurrences(self, text: str, pattern: str) -> List[int]:
        """Encontra todas as ocorrências de um padrão em um texto."""
        positions = []
        start = 0
        while True:
            pos = text.find(pattern, start)
            if pos == -1: break
            positions.append(pos)
            start = pos + 1
        return positions
    
    def apply_production(self, current: str, lhs: str, rhs: str) -> List[str]:
        """Aplica uma produção em todas as posições possíveis."""
        results = []
        positions = self.find_all_occurrences(current, lhs)
        for pos in positions:
            new_string = current[:pos] + rhs + current[pos + len(lhs):]
            results.append(new_string)
        return results
    
    def parse(self, target_word: str, verbose: bool = True) -> Tuple[bool, Optional[List[str]]]:
        """Verifica se uma palavra pertence à linguagem (BFS)."""
        queue = deque([(self.start_symbol, [self.start_symbol])])
        visited: Set[str] = {self.start_symbol}
        states_explored = 0
        
        while queue and states_explored < self.max_states:
            current, path = queue.popleft()
            states_explored += 1
            
            if current == target_word:
                if verbose: print(f"✓ Palavra encontrada após explorar {states_explored} estados!")
                return True, path
            
            # Heurísticas de poda
            if len(path) > self.max_depth: continue
            if len(current) > len(target_word) * 3: continue
            
            for lhs, rhs in self.productions:
                if lhs in current:
                    derived = self.apply_production(current, lhs, rhs)
                    for new_string in derived:
                        if new_string not in visited or len(path) < 10:
                            visited.add(new_string)
                            new_path = path + [new_string]
                            queue.append((new_string, new_path))
        
        if verbose: print(f"✗ Palavra não encontrada após explorar {states_explored} estados.")
        return False, None
    
    def format_derivation(self, derivation: List[str]) -> str:
        return ' ⇒ '.join(derivation)

def test_grammar(name: str, grammar: str, test_word: str, expected: bool) -> bool:
    print(f"\n{'='*70}\nTESTE: {name}\n{'='*70}")
    print(f"Palavra de entrada: '{test_word}'")
    print(f"Resultado esperado: {'Sim' if expected else 'Não'}\n")
    
    parser = GrammarParser(max_depth=100, max_states=200000)
    parser.parse_grammar(grammar)
    
    print(f"Gramática carregada com {len(parser.productions)} produções:")
    for lhs, rhs in parser.productions:
        rhs_display = rhs if rhs else 'ε'
        print(f"  {lhs} → {rhs_display}") # Nota: Contém Unicode
    
    print(f"\nIniciando busca BFS...\n")
    belongs, derivation = parser.parse(test_word, verbose=True)
    
    print()
    if belongs:
        print("✓ RESULTADO: Sim, pertence a L(G)")
        print("\nCadeia de derivação:")
        print(parser.format_derivation(derivation))
    else:
        print("✗ RESULTADO: Não foi possível derivar a palavra")
    
    success = belongs == expected
    print(f"\n{'✓ TESTE PASSOU' if success else '✗ TESTE FALHOU'}")
    return success