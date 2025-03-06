from left_factor_grammar import *

if __name__ == "__main__":
    # We store the grammar in a dictionary of lists-of-lists form.
    # For "S -> i E t S | i E t S e S | a", we do:
    grammar = {
        "S": [
            ["i", "E", "t", "S"],
            ["i", "E", "t", "S", "e", "S"],
            ["a"]
        ],
        "E": [
            ["b"]
        ]
    }

    print("Original Grammar:")
    for A, prods in grammar.items():
        print(f"  {A} -> " + " | ".join(" ".join(p) for p in prods))

    # Perform left-factoring
    factored_grammar = left_factor_grammar(grammar)

    print("\nLeft-Factored Grammar:")
    for A, prods in factored_grammar.items():
        print(f"  {A} -> " + " | ".join(" ".join(p) for p in prods))