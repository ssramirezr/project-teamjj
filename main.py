def compute_firsts(productions):
    first = {non_terminal: set() for non_terminal in productions}
    marcados = set()

    def compute_first(symbol):
        if symbol in first and first[symbol]:
            return first[symbol]

        if not symbol.isupper():
            return {symbol}

        if symbol in marcados:
            return first[symbol]

        marcados.add(symbol)

        result = set()
        for production in productions[symbol]:
            if production == 'e':
                result.add('e')
            else:
                for sym in production:
                    sym_first = compute_first(sym)
                    result.update(sym_first - {'e'})
                    if 'e' not in sym_first:
                        break
                else:
                    result.add('e')
        first[symbol] = result
        marcados.remove(symbol)
        return result

    for non_terminal in productions:
        compute_first(non_terminal)

    return first

def compute_follows(productions, first):
    follow = {non_terminal: set() for non_terminal in productions}
    start_symbol = next(iter(productions))
    follow[start_symbol].add('$')

    def follow_non_terminal(non_terminal):
        for nt in productions:
            for production in productions[nt]:
                for i, symbol in enumerate(production):
                    if symbol == non_terminal:
                        rest = production[i+1:]
                        if rest:
                            for next_symbol in rest:
                                if next_symbol.isupper():
                                    follow[symbol].update(first[next_symbol] - {'e'})
                                    if 'e' in first[next_symbol]:
                                        continue
                                    else:
                                        break
                                else:
                                    follow[symbol].add(next_symbol)
                                    break
                            else:
                                follow[symbol].update(follow[nt])
                        else:
                            follow[symbol].update(follow[nt])

    for _ in range(len(productions)):
        for non_terminal in productions:
            follow_non_terminal(non_terminal)

    return follow

def main():
    Output = []
    c = int(input())
    for _ in range(c):
        m = int(input())
        productions = {}
        for _ in range(m):
            line = input().strip().split()
            non_terminal = line[0]
            rules = line[1:]
            productions[non_terminal] = rules

        first = compute_firsts(productions)
        follow = compute_follows(productions, first)

        for non_terminal in sorted(first):
            first_set = ','.join(sorted(first[non_terminal]))
            Output.append(f"First({non_terminal}) - {{{first_set}}}")

        for non_terminal in sorted(follow):
            follow_set = ','.join(sorted(follow[non_terminal]))
            Output.append(f"Follow({non_terminal}) - {{{follow_set}}}")

    for o in Output:
        print(o)

if __name__ == "__main__":
    main()


    for o in Output:
        print(o)

if __name__ == "__main__":
    main()
