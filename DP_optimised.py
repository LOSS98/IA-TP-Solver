"""
Ce code est une version optimisée de l'algorithme de Davis-Putnam. Au fil du code, vous trouverez des commentaires, commençant par 'Optimisation' qui expliquent les optimisations apportées. Ces optimisations permettent de réduire le temps d'exécution de l'algorithme.
"""

from collections import Counter


def is_tautologie(clause):
    clause_set = set(clause)
    for i in clause:
        if -i in clause_set:
            return True
    return False


def regle_1(clauses):
    """Règle 1 : oter tautologie -> clause contenant l et non l"""
    return [c for c in clauses if not is_tautologie(c)]


def ote_val_from_clauses(clauses, value):
    """Supprime la valeur value de toutes les clauses"""
    return [[i for i in c if i != value] for c in clauses]


def ote_clauses_with_val(clauses, value):
    """Supprime les clauses contenant la valeur value"""
    return [c for c in clauses if value not in c]


def regle_2(clauses):
    """Règle 2 : clause contient 1 seul littéral -> enlever les clauses le contenant, 
    et enlever l'apparition de son inverse ailleurs"""
    # Optimisation: tri des clauses par longueur pour trouver plus rapidement les clauses unitaires
    clauses.sort(key=len)

    for c in clauses:
        if len(c) == 1:
            value = c[0]
            clauses2 = ote_clauses_with_val(clauses, value)
            clauses3 = ote_val_from_clauses(clauses2, -value)
            return clauses3
    return clauses


def count_literals(clauses):
    """Compte les occurrences de chaque littéral dans les clauses"""
    counter = Counter()
    for c in clauses:
        counter.update(c)
    return counter


def exist_in_clauses(value, clauses):
    """Retourne vrai si la valeur value existe dans au moins une clause"""
    for c in clauses:
        if value in c:
            return True
    return False


def single_lit(clauses):
    """Retourne un littéral qui apparaît dans des clauses mais dont l'opposé n'apparaît jamais"""
    # Optimisation: utilisation de Counter pour un comptage plus rapide
    counter = count_literals(clauses)

    for lit in counter:
        if -lit not in counter:
            return lit
    return 0


def regle_3(clauses):
    """Règle 3 : 1 littéral apparaît dans des clauses, son inverse n'apparaît jamais 
    -> enlever les clauses le contenant"""
    lit = single_lit(clauses)
    if lit != 0:
        clauses2 = ote_clauses_with_val(clauses, lit)
        return clauses2
    return clauses


def bigger_clauses(clauses):
    """Retourne les clauses qui contiennent d'autres clauses"""
    clauses2 = []
    # Optimisation: tri des clauses par longueur pour une vérification plus rapide des sous-ensembles
    sorted_clauses = sorted(clauses, key=len)

    for i, c2 in enumerate(sorted_clauses):
        for c in sorted_clauses[i + 1:]:
            if set(c2).issubset(set(c)):
                clauses2.append(c)

    return clauses2


def regle_4(clauses):
    """Règle 4 : si une clause est contenue dans d'autres -> enlever les autres"""
    clauses2 = bigger_clauses(clauses)
    clauses3 = [c for c in clauses if c not in clauses2]
    return clauses3


def get_not_single(clauses):
    """Retourne un littéral l dont son inverse apparaît également"""
    # Optimisation: choisir le littéral avec la plus haute occurrence
    counter = count_literals(clauses)

    literals = sorted(counter.keys(), key=lambda x: counter[x], reverse=True)

    for lit in literals:
        if -lit in counter:
            return lit
    return 0


def regle_5(clauses):
    """Règle 5 : Créer des mondes -> choisir un littéral l dont son inverse apparaît également
    -> créer 2 formules,
    - F1) contenant les clauses de F sauf celles contenant l
         et où les apparitions de ¬l sont ôtées
    - F2) contenant les clauses de F sauf celles contenant ¬l
      et où les apparitions de l sont ôtées
    """
    l = get_not_single(clauses)
    if l != 0:
        clauses21 = ote_clauses_with_val(clauses, l)
        clauses31 = ote_val_from_clauses(clauses21, -l)
        clauses22 = ote_clauses_with_val(clauses, -l)
        clauses32 = ote_val_from_clauses(clauses22, l)
        return (clauses31, clauses32)
    return None


def formules_egales(f1, f2):
    """Retourne vrai si les formules f1 et f2 sont identiques"""
    # Optimisation: utilisation d'ensembles pour la comparaison
    if len(f1) != len(f2):
        return False

    f1_set = {tuple(sorted(c)) for c in f1}
    f2_set = {tuple(sorted(c)) for c in f2}

    return f1_set == f2_set


# Cache pour la mémorisation
formula_cache = {}

cpt = 0
verbose = False
start_time = 0


def DP(clauses):
    """Retourne vrai si la formule est satisfiable (algorithme DP)"""
    global cpt, start_time
    cpt += 1

    # Optimisation: mémorisation pour les sous-problèmes répétés
    clauses_tuple = tuple(tuple(sorted(c)) for c in sorted(clauses, key=lambda x: tuple(sorted(x))))
    if clauses_tuple in formula_cache:
        return formula_cache[clauses_tuple]

    if verbose:
        print("résolution de ", clauses)

    # Détection précoce de succès/échec
    if len(clauses) == 0:
        if verbose:
            print("succès")
        formula_cache[clauses_tuple] = True
        return True

    if [] in clauses:
        if verbose:
            print("échec")
        formula_cache[clauses_tuple] = False
        return False

    # Application des règles dans l'ordre (optimisé)
    clr1 = regle_1(clauses)
    if len(clr1) == 0:
        if verbose:
            print("succès")
        formula_cache[clauses_tuple] = True
        return True
    if [] in clr1:
        if verbose:
            print("échec")
        formula_cache[clauses_tuple] = False
        return False

    clr2 = regle_2(clr1)
    if len(clr2) == 0:
        if verbose:
            print("succès")
        formula_cache[clauses_tuple] = True
        return True
    if [] in clr2:
        if verbose:
            print("échec")
        formula_cache[clauses_tuple] = False
        return False
    if not formules_egales(clr1, clr2):
        result = DP(clr2)
        formula_cache[clauses_tuple] = result
        return result

    clr3 = regle_3(clr2)
    if len(clr3) == 0:
        if verbose:
            print("succès")
        formula_cache[clauses_tuple] = True
        return True
    if [] in clr3:
        if verbose:
            print("échec")
        formula_cache[clauses_tuple] = False
        return False
    if not formules_egales(clr2, clr3):
        result = DP(clr3)
        formula_cache[clauses_tuple] = result
        return result

    clr4 = regle_4(clr3)
    if len(clr4) == 0:
        if verbose:
            print("succès")
        formula_cache[clauses_tuple] = True
        return True
    if [] in clr4:
        if verbose:
            print("échec")
        formula_cache[clauses_tuple] = False
        return False
    if not formules_egales(clr3, clr4):
        result = DP(clr4)
        formula_cache[clauses_tuple] = result
        return result

    result_regle_5 = regle_5(clr4)
    if result_regle_5:
        clr51, clr52 = result_regle_5
        mondes_unis = DP(clr51) or DP(clr52)
        if verbose:
            print("fin résolution de ", clauses)
        formula_cache[clauses_tuple] = mondes_unis
        return mondes_unis

    # Si nous arrivons ici, aucun progrès n'a été fait
    formula_cache[clauses_tuple] = False
    return False