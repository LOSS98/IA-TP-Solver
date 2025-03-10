"""
Implémentation corrigée de l'algorithme DPLL (Davis-Putnam-Logemann-Loveland).
Cette version résout correctement les problèmes SAT et identifie correctement les formules insatisfiables.
"""

from collections import Counter

# Cache pour mémorisation
dpll_cache = {}
dpll_cpt = 0

def count_literals(clauses):
    """Compte les occurrences de chaque littéral dans les clauses"""
    counter = Counter()
    for c in clauses:
        counter.update(c)
    return counter

def unit_propagation(clauses):
    """
    Applique la propagation unitaire
    Retourne une formule simplifiée et un drapeau indiquant si une contradiction a été trouvée
    """
    result = list(clauses)  # Copie des clauses
    assigned = {}  # Littéraux assignés

    # Fonction pour rechercher et assigner des clauses unitaires
    def find_unit_clauses():
        for i, clause in enumerate(result):
            if len(clause) == 1:
                lit = clause[0]
                # Si on a déjà assigné le littéral opposé, contradiction
                if -lit in assigned:
                    return True, lit  # Contradiction
                assigned[lit] = True
                return False, lit  # Pas de contradiction, littéral trouvé
        return False, None  # Pas de clause unitaire trouvée

    # Tant qu'on trouve des clauses unitaires, continuer à propager
    while True:
        contradiction, unit_lit = find_unit_clauses()
        if contradiction:
            return [], True  # Contradiction trouvée
        if unit_lit is None:
            break  # Plus de clauses unitaires

        # Supprimer les clauses contenant le littéral assigné
        new_clauses = []
        for clause in result:
            if unit_lit in clause:
                continue  # Clause satisfaite, on la supprime
            # Si la clause contient le littéral opposé, on le retire
            if -unit_lit in clause:
                new_clause = [l for l in clause if l != -unit_lit]
                if not new_clause:  # Clause vide = contradiction
                    return [], True
                new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)

        result = new_clauses

        # Si formule vide, c'est satisfait
        if not result:
            return [], False

    return result, False

def pure_literal_elimination(clauses):
    """
    Élimine les littéraux purs
    Retourne une formule simplifiée
    """
    if not clauses:
        return clauses

    # Trouver tous les littéraux et leur négation
    all_literals = set()
    neg_literals = set()

    for clause in clauses:
        for lit in clause:
            all_literals.add(lit)
            neg_literals.add(-lit)

    # Les littéraux purs sont ceux qui n'apparaissent pas dans leur forme négative
    pure_lits = all_literals - neg_literals

    if not pure_lits:
        return clauses

    # Supprimer les clauses contenant les littéraux purs
    result = []
    for clause in clauses:
        if any(lit in pure_lits for lit in clause):
            continue  # Clause satisfaite par un littéral pur
        result.append(clause)

    return result

def choose_literal(clauses):
    """Choisit un littéral pour la division de cas en utilisant l'heuristique DLIS
    (Dynamic Largest Individual Sum)"""
    # Compter les occurrences
    counter = Counter()
    for clause in clauses:
        counter.update(clause)

    # Choisir le littéral le plus fréquent
    if counter:
        return max(counter.items(), key=lambda x: x[1])[0]
    return None

def DPLL(clauses):
    """
    Algorithme DPLL amélioré pour la satisfiabilité
    """
    global dpll_cpt
    dpll_cpt += 1

    # Case de base: formule vide
    if not clauses:
        return True

    # Case de base: clause vide
    if any(len(clause) == 0 for clause in clauses):
        return False

    # Mémorisation
    clauses_tuple = tuple(tuple(sorted(c)) for c in sorted(clauses, key=lambda x: tuple(sorted(x))))
    if clauses_tuple in dpll_cache:
        return dpll_cache[clauses_tuple]

    # 1. Propagation unitaire
    simplified_clauses, contradiction = unit_propagation(clauses)
    if contradiction:
        dpll_cache[clauses_tuple] = False
        return False

    # Si toutes les clauses sont satisfaites
    if not simplified_clauses:
        dpll_cache[clauses_tuple] = True
        return True

    # 2. Élimination des littéraux purs
    simplified_clauses = pure_literal_elimination(simplified_clauses)

    # Si toutes les clauses sont satisfaites
    if not simplified_clauses:
        dpll_cache[clauses_tuple] = True
        return True

    # Si les clauses ont changé, réappliquer DPLL
    if simplified_clauses != clauses:
        result = DPLL(simplified_clauses)
        dpll_cache[clauses_tuple] = result
        return result

    # 3. Division de cas
    literal = choose_literal(simplified_clauses)

    # Essayer avec le littéral positif
    positive_result = DPLL(simplified_clauses + [[literal]])
    if positive_result:
        dpll_cache[clauses_tuple] = True
        return True

    # Essayer avec le littéral négatif
    negative_result = DPLL(simplified_clauses + [[-literal]])

    dpll_cache[clauses_tuple] = negative_result
    return negative_result