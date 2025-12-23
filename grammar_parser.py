"""
Parser Universal para Gramáticas da Hierarquia de Chomsky
Implementação usando Busca em Largura (BFS)

Este módulo implementa um parser de força bruta capaz de processar
gramáticas de qualquer tipo da Hierarquia de Chomsky (0, 1, 2, 3).
"""

from collections import deque
from typing import List, Tuple, Optional, Set


class GrammarParser:
    """
    Parser universal para gramáticas formais usando BFS.
    
    Attributes:
        productions: Lista de tuplas (LHS, RHS) representando regras gramaticais
        start_symbol: Símbolo inicial da gramática (padrão: 'S')
        max_depth: Profundidade máxima de derivação para evitar loops infinitos
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
        
        Formato esperado:
        - Regras: LHS -> RHS:
        - Comentários: após ':'
        - Epsilon: ε ou λ
        - Terminais: minúsculas/dígitos
        - Não-terminais: maiúsculas
        
        Args:
            grammar_text: String contendo as regras da gramática
        """
        self.productions = []
        
        for line in grammar_text.strip().split('\n'):
            # Remove espaços em branco no início e fim
            line = line.strip()
            
            # Ignora linhas vazias
            if not line:
                continue
            
            # Remove comentários (tudo após ':' no final da regra)
            if ':' in line:
                line = line.split(':')[0].strip()
            
            # Verifica se a linha contém uma produção
            if '->' not in line:
                continue
            
            # Separa LHS e RHS
            lhs, rhs = line.split('->', 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            
            # Converte epsilon/lambda para string vazia
            if rhs in ['ε', 'λ']:
                rhs = ''
            
            self.productions.append((lhs, rhs))
    
    def find_all_occurrences(self, text: str, pattern: str) -> List[int]:
        """
        Encontra todas as ocorrências de um padrão em um texto.
        
        Args:
            text: Texto onde buscar
            pattern: Padrão a ser encontrado
            
        Returns:
            Lista de índices onde o padrão ocorre
        """
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
        """
        Aplica uma produção em todas as posições possíveis de uma string.
        
        Args:
            current: String atual
            lhs: Lado esquerdo da produção
            rhs: Lado direito da produção
            
        Returns:
            Lista de todas as strings derivadas possíveis
        """
        results = []
        positions = self.find_all_occurrences(current, lhs)
        
        for pos in positions:
            # Substitui o LHS pelo RHS na posição encontrada
            new_string = current[:pos] + rhs + current[pos + len(lhs):]
            results.append(new_string)
        
        return results

    def is_promising(self, current_string: str, target_word: str) -> bool:
        """
        Verifica se a string atual ainda tem chance de virar a palavra alvo.
        Retorna False se ela já tiver erros óbvios.
        """
        # 1. Poda por Tamanho Excessivo
        # Se a string atual é maior que o alvo e só tem terminais, já falhou.
        # (Para gramáticas com regras que aumentam tamanho, como S -> SS)
        if len(current_string) > len(target_word) + 5: # Tolerância pequena
            return False

        # 2. Poda por Prefixo (A mais importante!)
        # Extrai a parte inicial da string que só contém terminais
        terminal_prefix = ""
        for char in current_string:
            if char.isupper() or char.isdigit(): # Assume que Uppercase/Digitos são Não-Terminais
                break
            terminal_prefix += char
        
        # Verifica se o começo da string bate com o alvo
        if not target_word.startswith(terminal_prefix):
            return False
            
        return True
    
    def parse(self, target_word: str, verbose: bool = True, use_pruning: bool = True) -> Tuple[bool, Optional[List[str]]]:
        """
        Verifica se uma palavra pertence à linguagem gerada pela gramática.
        
        Usa BFS para explorar todas as derivações possíveis até encontrar
        a palavra alvo ou atingir os limites de busca.
        
        Args:
            target_word: Palavra a ser verificada
            verbose: Se True, imprime informações de debug
            
        Returns:
            Tupla (pertence, derivacao) onde:
            - pertence: True se a palavra foi encontrada
            - derivacao: Lista com a cadeia de derivação (ou None)
        """
        # Fila para BFS: cada elemento é (string_atual, caminho_de_derivação)
        queue = deque([(self.start_symbol, [self.start_symbol])])
        
        # Conjunto para evitar revisitar estados (otimização)
        visited: Set[str] = {self.start_symbol}
        
        states_explored = 0
        
        while queue and states_explored < self.max_states:
            current, path = queue.pop()
            states_explored += 1
            
            # Verifica se encontrou a palavra alvo
            if current == target_word:
                if verbose:
                    print(f"✓ Palavra encontrada após explorar {states_explored} estados!")
                return True, path
            
            # Poda: não expande strings muito maiores que o alvo
            # (heurística para evitar explosão combinatória)
            if len(path) > self.max_depth:
                continue
            
            if len(current) > len(target_word) * 3:
                continue
            
            # Tenta aplicar cada produção
            for lhs, rhs in self.productions:
                # Verifica se o LHS está presente na string atual
                if lhs in current:
                    # Gera todas as derivações possíveis aplicando esta produção
                    derived = self.apply_production(current, lhs, rhs)
                    
                    for new_string in derived:
                        # OTIMIZAÇÃO: Só aplica se estiver ativada E o caminho não for promissor
                        if use_pruning and not self.is_promising(new_string, target_word):
                            continue

                        # Evita revisitar estados já explorados
                        if new_string not in visited or len(path) < 10:
                            visited.add(new_string)
                            new_path = path + [new_string]
                            
                            # Dica: Para buscas profundas, use append (Pilha)
                            # Para buscas rasas, use appendleft (Fila)
                            # Como a regra S->SS é profunda, tente tratar como pilha aqui:
                            queue.append((new_string, new_path))
        
        if verbose:
            print(f"✗ Palavra não encontrada após explorar {states_explored} estados.")
        
        return False, None
    
    def format_derivation(self, derivation: List[str]) -> str:
        """
        Formata uma cadeia de derivação para exibição.
        
        Args:
            derivation: Lista de strings representando cada passo
            
        Returns:
            String formatada com símbolos de derivação
        """
        return ' ⇒ '.join(derivation)


def test_grammar(name: str, grammar: str, test_word: str, expected: bool, use_pruning: bool = True) -> bool:
    """
    Testa uma gramática com uma palavra específica.
    
    Args:
        name: Nome do teste
        grammar: Texto da gramática
        test_word: Palavra a ser testada
        expected: Resultado esperado (True/False)
        use_pruning: Se True, ativa a poda por prefixo (não usar em Gramáticas Irrestritas/Tipo 0)
        
    Returns:
        True se o teste passou
    """
    print(f"\n{'='*70}")
    print(f"TESTE: {name}")
    print(f"{'='*70}")
    print(f"Palavra de entrada: '{test_word}'")
    print(f"Resultado esperado: {'Sim' if expected else 'Não'}")
    print(f"Otimização (Poda): {'Ativada' if use_pruning else 'Desativada'}")
    print()
    
    parser = GrammarParser(max_depth=100, max_states=200000)
    parser.parse_grammar(grammar)
    
    print(f"Gramática carregada com {len(parser.productions)} produções:")
    for lhs, rhs in parser.productions:
        rhs_display = rhs if rhs else 'ε'
        print(f"  {lhs} → {rhs_display}")
    
    print(f"\nIniciando busca BFS...")
    
    # Passando o parâmetro de poda para o parser
    belongs, derivation = parser.parse(test_word, verbose=True, use_pruning=use_pruning)
    
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

def main():
    """
    Função principal que executa todos os casos de teste.
    """
    print("="*70)
    print("PARSER UNIVERSAL PARA GRAMÁTICAS DA HIERARQUIA DE CHOMSKY")
    print("Implementação: Busca em Largura (BFS)")
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
    
    # CENÁRIO 1: Desafio de Fibonacci (Livre de Contexto)
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
        "Cenário 1 - Fibonacci (CFG)",
        fibonacci_grammar,
        "aaaaaabbbbbbbb",
        True,
        use_pruning=True
    ))
    
    # CENÁRIO 2: Linguagem Regular Simples
    regular_grammar = """
    S -> aS:
    S -> b:
    """
    results.append(test_grammar(
        "Cenário 2 - Linguagem Regular (a*b)",
        regular_grammar,
        "aaab",
        True,
        use_pruning=True
    ))
    
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
    results.append(test_grammar(
        "Cenário 3 - a^n b^n c^n (CSG)",
        context_sensitive,
        "aabbcc",
        True,
        use_pruning=True
    ))
    
    # CENÁRIO 4: Gramática Irrestrita (Tipo 0)
    unrestricted_grammar = """
    S -> abCde:
    bCd -> X:
    aXe -> afinal:
    """
    results.append(test_grammar(
        "Cenário 4 - Gramática Irrestrita (Tipo 0)",
        unrestricted_grammar,
        "afinal",
        True,
        use_pruning=False
    ))
    
    # Sumário final
    print("\n" + "="*70)
    print("SUMÁRIO DOS TESTES")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Testes passados: {passed}/{total}")
    print(f"Taxa de sucesso: {(passed/total)*100:.1f}%")
    print("="*70)


if __name__ == "__main__":
    main()
