def longest_common_prefix(strs):
    """
    Finds the longest common prefix among a list of lists.
    Returns a list of symbols representing that prefix.
    """
    if not strs:
        return []
    prefix = strs[0]
    for s in strs[1:]:
        # Zip together to find common prefix
        temp = []
        for x, y in zip(prefix, s):
            if x == y:
                temp.append(x)
            else:
                break
        prefix = temp
        if not prefix:
            break
    return prefix

def left_factor_grammar(grammar):
    """
    If multiple alternatives share a prefix, factor it out.
    """
    new_rules = {}
    next_index = 1  # for naming new nonterminals like A'

    for A, productions in grammar.items():
        if len(productions) < 2:
            # Nothing to factor if only one production
            continue

        # 1) Find the longest common prefix among ALL productions of A
        prefix = longest_common_prefix(productions)

        # 2) If there's no common prefix (or only length 0), skip factoring
        if not prefix:
            continue

        # 3) Create a new nonterminal A' to hold the remainder expansions
        new_nonterminal = A + "'" + str(next_index)
        next_index += 1

        # 4) Split out the remainder from each production
        remainders = []
        for prod in productions:
            remainder = prod[len(prefix):]
            # If the remainder is empty, we store ε
            remainders.append(remainder if remainder else ["ε"])

        # 5) Replace all of A's old productions with just one factored rule:
        #       A -> prefix A'
        grammar[A] = [prefix + [new_nonterminal]]

        # 6) Add the new nonterminal's productions:
        new_rules[new_nonterminal] = remainders

    # Merge newly created rules into the grammar
    grammar.update(new_rules)
    return grammar