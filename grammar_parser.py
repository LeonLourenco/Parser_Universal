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