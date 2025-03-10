import os
import time
from collections import defaultdict
import sys

try:
    import DP_optimised
    import DPLL
except ImportError:
    print(
        "Erreur: Impossible d'importer les modules. Assurez-vous que DP_optimised.py et DPLL.py sont dans le même dossier.")
    sys.exit(1)


def lire_cnf(fichier):
    """
    Lit un fichier CNF en format DIMACS et retourne une liste de listes représentant les clauses.
    """
    clauses = []

    with open(fichier, 'r') as f:
        for ligne in f:
            if ligne.startswith("%"):
                break
            if ligne.startswith('c') or ligne.startswith('p'):
                continue

            literals = list(map(int, ligne.split()))

            if literals and literals[-1] == 0:
                literals.pop()

            if literals:
                clauses.append(literals)

    return clauses


def run_dp_test(clauses, name="Test"):
    """Exécute DP sur un jeu de clauses et affiche les statistiques"""
    # Réinitialisation des variables globales
    DP_optimised.cpt = 0
    DP_optimised.formula_cache = {}

    start_time = time.time()
    try:
        result = DP_optimised.DP(clauses)
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"\n--- Résultats {name} ---")
        print(f"Satisfiable: {result}")
        print(f"Nombre d'appels: {DP_optimised.cpt}")
        print(f"Temps d'exécution: {execution_time:.6f} secondes")

        return result, DP_optimised.cpt, execution_time
    except Exception as e:
        print(f"Erreur lors du test de {name}: {e}")
        return None, 0, 0


def run_dpll_test(clauses, name="Test"):
    """Exécute DPLL sur un jeu de clauses et affiche les statistiques"""
    # Réinitialisation des variables globales
    DPLL.dpll_cpt = 0
    DPLL.dpll_cache = {}

    start_time = time.time()
    try:
        result = DPLL.DPLL(clauses)
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"\n--- Résultats DPLL {name} ---")
        print(f"Satisfiable: {result}")
        print(f"Nombre d'appels: {DPLL.dpll_cpt}")
        print(f"Temps d'exécution: {execution_time:.6f} secondes")

        return result, DPLL.dpll_cpt, execution_time
    except Exception as e:
        print(f"Erreur lors du test de {name}: {e}")
        return None, 0, 0


def scanner_dossier(dossier="uf_files"):
    """Scanne le dossier spécifié et retourne la liste des fichiers CNF."""
    if not os.path.exists(dossier):
        print(f"Erreur: Le dossier {dossier} n'existe pas.")
        return []

    fichiers = [f for f in os.listdir(dossier) if f.endswith('.cnf')]
    return sorted(fichiers)


def afficher_menu(fichiers):
    """Affiche un menu avec les fichiers disponibles."""
    print("\n===== MENU =====")
    print("0. Tester tous les fichiers")
    for i, fichier in enumerate(fichiers, 1):
        print(f"{i}. {fichier}")
    print(f"{len(fichiers) + 1}. Tester tous les fichiers sauf uuf150-01.cnf")
    print(f"{len(fichiers) + 2}. Quitter")

    choix = -1
    while choix < 0 or choix > len(fichiers) + 1:
        try:
            choix = int(input("\nEntrez votre choix: "))
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")

    return choix


def executer_test(fichier, dossier="uf_files"):
    """Exécute les tests DP et DPLL sur un fichier spécifique."""
    chemin_fichier = os.path.join(dossier, fichier)
    print(f"\n===== Test de {fichier} =====")

    try:
        clauses = lire_cnf(chemin_fichier)
        print(f"Nombre de clauses: {len(clauses)}")

        # Test avec DP optimisé
        dp_result, dp_calls, dp_time = run_dp_test(clauses, f"{fichier} DP")

        # Test avec DPLL
        dpll_result, dpll_calls, dpll_time = run_dpll_test(clauses, f"{fichier} DPLL")

        return {
            'fichier': fichier,
            'satisfiable_dp': dp_result,
            'satisfiable_dpll': dpll_result,
            'appels_dp': dp_calls,
            'appels_dpll': dpll_calls,
            'temps_dp': dp_time,
            'temps_dpll': dpll_time
        }
    except Exception as e:
        print(f"Erreur lors du test de {fichier}: {e}")
        return None


def afficher_recap(resultats):
    """Affiche un récapitulatif des résultats des tests."""
    if not resultats:
        print("\nAucun résultat à afficher.")
        return

    print("\n===== RÉCAPITULATIF DES TESTS =====")
    print(
        f"{'Fichier':<15} {'Satisfiable (DP)':<20} {'Satisfiable (DPLL)':<20} {'Appels DP':<15} {'Appels DPLL':<15} {'Temps DP (s)':<15} {'Temps DPLL (s)':<15}")
    print("-" * 115)

    total_dp_time = 0
    total_dpll_time = 0
    total_dp_calls = 0
    total_dpll_calls = 0

    for res in resultats:
        if res:
            # Format corrigé
            print(
                f"{res['fichier']:<15} {str(res['satisfiable_dp']):<20} {str(res['satisfiable_dpll']):<20} {res['appels_dp']:<15} {res['appels_dpll']:<15} {res['temps_dp']:.6f} {res['temps_dpll']:.6f}")
            total_dp_time += res['temps_dp']
            total_dpll_time += res['temps_dpll']
            total_dp_calls += res['appels_dp']
            total_dpll_calls += res['appels_dpll']

    print("-" * 115)
    # Format corrigé
    print(
        f"{'TOTAL':<15} {'':<20} {'':<20} {total_dp_calls:<15} {total_dpll_calls:<15} {total_dp_time:.6f} {total_dpll_time:.6f}")

    # Comparaison des performances
    print("\n===== COMPARAISON DES PERFORMANCES =====")
    if total_dp_time > 0 and total_dpll_time > 0:
        ratio_temps = total_dpll_time / total_dp_time
        print(f"Ratio temps DPLL/DP: {ratio_temps:.2f} ({'plus rapide' if ratio_temps < 1 else 'plus lent'})")

    if total_dp_calls > 0 and total_dpll_calls > 0:
        ratio_appels = total_dpll_calls / total_dp_calls
        print(f"Ratio appels DPLL/DP: {ratio_appels:.2f} ({'moins d\'appels' if ratio_appels < 1 else 'plus d\'appels'})")


def main():
    # Scanner le dossier pour trouver les fichiers CNF
    fichiers = scanner_dossier()

    if not fichiers:
        print("Aucun fichier CNF trouvé dans le dossier uf_files.")
        return

    resultats = []

    while True:
        choix = afficher_menu(fichiers)

        if choix == 0:
            # Tester tous les fichiers
            print("\nTest de tous les fichiers...")
            resultats = []
            for fichier in fichiers:
                resultat = executer_test(fichier)
                if resultat:
                    resultats.append(resultat)
            afficher_recap(resultats)
        elif choix == len(fichiers) + 1:
            # Tester tous les fichiers sauf uuf150-01.cnf
            print("\nTest de tous les fichiers sauf uuf150-01.cnf...")
            resultats = []
            for fichier in fichiers:
                if fichier != "uuf150-01.cnf":
                    resultat = executer_test(fichier)
                    if resultat:
                        resultats.append(resultat)
            afficher_recap(resultats)
        elif choix == len(fichiers) + 2:
            # Quitter
            print("\nAu revoir!")
            break
        else:
            # Tester un fichier spécifique
            fichier = fichiers[choix - 1]
            resultat = executer_test(fichier)
            if resultat:
                resultats = [resultat]
                afficher_recap(resultats)


if __name__ == "__main__":
    main()