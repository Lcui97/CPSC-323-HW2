def common_prefix(prod1, prod2):
    """
    Full disclosure - This code with created with consultation from ChatGPT o3 Model.
    Model provided pseudocode for marked sectioins, and helped with trouble shooting.
    
    Returns the longest common prefix (as a list of symbols)
    between two productions (lists of symbols).
    """
    prefix = []
    for x, y in zip(prod1, prod2):
        if x == y:
            prefix.append(x)
        else:
            break
    return prefix

def left_factor_grammar(grammar):
    """
    PSEUDOCODE PROVIDED BY CHATGPT
    
    Performs left-factoring on the given grammar until no more
    factoring opportunities remain.
    """
    changed = True
    new_nonterminal_index = 1

    while changed:
        changed = False

        # We might add new nonterminals, so iterate over a snapshot of current keys
        for A in list(grammar.keys()):
            productions = grammar[A]

            # We try to find any subset of productions that share a non-empty prefix
            # that is longer than 1 symbol or that appears in more than one production.
            # We'll group expansions by their *first* symbol(s) to detect common prefixes.

            # Step 1: Sort productions into buckets by their first symbol
            prefix_map = {}
            for prod in productions:
                first = prod[0] if prod else 'ε'  # if production is empty
                prefix_map.setdefault(first, []).append(prod)

            # Step 2: For each bucket, see if there's more than one production
            # that might share a deeper prefix (beyond the first symbol).
            for first_symbol, same_first_prods in list(prefix_map.items()):
                if len(same_first_prods) < 2:
                    continue  # nothing to factor if only one production in this bucket

                # Find the longest common prefix among all these expansions
                # Example: iEtS and iEtSeS -> common prefix is [i, E, t, S]
                prefix = same_first_prods[0]
                for p in same_first_prods[1:]:
                    prefix = common_prefix(prefix, p)
                    if not prefix:
                        break

                # If prefix is empty or just the first symbol, we only factor if
                # it actually helps. Typically we want a prefix of length >= 1.
                # In many examples, even length 1 is enough if it truly factors out.
                if len(prefix) == 0:
                    continue

                # We have a real factoring opportunity:
                #  S -> prefix remainder1 | prefix remainder2 | ...
                # becomes
                #  S -> prefix NEW_NONTERM
                #  NEW_NONTERM -> remainder1 | remainder2 | ...
                new_nonterminal = A + "'" + str(new_nonterminal_index)
                new_nonterminal_index += 1

                # Gather the remainders for each production that shared this prefix
                remainders = []
                for p in same_first_prods:
                    # Remainder is what's left after removing the common prefix
                    remainder = p[len(prefix):]
                    # If remainder is empty, we represent it as ['ε']
                    remainders.append(remainder if remainder else ['ε'])

                # Remove those old expansions from A
                for p in same_first_prods:
                    productions.remove(p)

                # Add the factored production to A: prefix + [new_nonterminal]
                # (Unless prefix was ε, but typically we expect at least one symbol.)
                if prefix == ['ε']:
                    # This would be unusual, but let's handle it:
                    new_prod = [new_nonterminal]
                else:
                    new_prod = prefix + [new_nonterminal]
                productions.append(new_prod)

                # Define the new nonterminal's expansions
                grammar[new_nonterminal] = remainders

                changed = True
                break  # Re-start factoring from scratch for safety

            if changed:
                # We modified the grammar for A, so break out and re-check from top
                break
    return grammar
