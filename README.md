# TP-Solver - Résolution SAT avec DP et DPLL
**Khalil MZOUGHI et Lorick DESERT<br>
3A FISA INFO - INSA Hauts-de-France**

Ce TP implémente et compare deux algorithmes de résolution de problèmes de satisfiabilité (SAT) : l'algorithme de Davis-Putnam (DP) optimisé et l'algorithme de Davis-Putnam-Logemann-Loveland (DPLL).

## Structure du projet

- `DP_optimised.py` : Implémentation optimisée de l'algorithme DP
- `DPLL.py` : Implémentation de l'algorithme DPLL
- `main.py` : Interface pour tester les algorithmes sur différents fichiers CNF
- `uf_files/` : Dossier contenant les fichiers de test au format DIMACS
  - `uf50-*.cnf` : Formules satisfiables (50 variables, ~218 clauses)
  - `uuf50-*.cnf` : Formules insatisfiables (50 variables, ~218 clauses)
  - `uuf150-01.cnf` : Formule insatisfiable plus complexe (150 variables, 645 clauses)

## Comment exécuter

1. Assurez-vous d'avoir Python installé sur votre système.
2. Clonez ou téléchargez ce dépôt.
3. Placez-vous dans le répertoire du projet.
4. Exécutez le programme principal :

```bash
python main.py
```

5. Un menu interactif s'affichera vous permettant de :
   - Tester tous les fichiers
   - Tester un fichier spécifique
   - Tester tous les fichiers sauf uuf150-01.cnf (qui prend plus de temps)
   - Quitter le programme

## Résumé des résultats

Les tests montrent que l'algorithme DPLL est significativement plus performant que l'algorithme DP, à la fois en termes de temps d'exécution et de nombre d'appels récursifs :

- **Ratio temps DPLL/DP** : 0.06 (DPLL est environ 17.8 fois plus rapide)
- **Ratio appels DPLL/DP** : 0.14 (DPLL effectue environ 7.2 fois moins d'appels récursifs)

### Comparaison globale des performances

| Métrique | DP | DPLL | Amélioration |
|----------|-------|--------|--------------|
| Temps total (s) | 1709.52 | 96.24 | 17.8× |
| Appels totaux | 896,789 | 124,329 | 7.2× |

### Analyse par type de formule

#### Formules satisfiables (uf50-*.cnf)

| Statistique | DP | DPLL | Amélioration |
|-------------|-------|--------|--------------|
| Appels min | 50 | 13 | 3.8× |
| Appels max | 1168 | 180 | 6.5× |
| Appels moyens | 335.3 | 83.7 | 4.0× |
| Temps min (s) | 0.036 | 0.003 | 12.0× |
| Temps max (s) | 0.546 | 0.044 | 12.4× |
| Temps moyen (s) | 0.175 | 0.019 | 9.2× |

Pour les formules satisfiables, DPLL montre une amélioration importante mais moins spectaculaire que pour les formules insatisfiables. Cela s'explique par le fait que pour une formule satisfiable, les deux algorithmes peuvent "trouver rapidement" une solution dès qu'une affectation valide est découverte.

#### Formules insatisfiables de taille standard (uuf50-*.cnf)

| Statistique | DP | DPLL | Amélioration |
|-------------|-------|--------|--------------|
| Appels min | 569 | 108 | 5.3× |
| Appels max | 1567 | 292 | 5.4× |
| Appels moyens | 991.0 | 191.7 | 5.2× |
| Temps min (s) | 0.298 | 0.027 | 11.0× |
| Temps max (s) | 0.830 | 0.067 | 12.4× |
| Temps moyen (s) | 0.513 | 0.046 | 11.2× |

Pour les formules insatisfiables de taille standard, DPLL montre une amélioration considérable par rapport à DP, avec une réduction du nombre d'appels d'environ 5.2 fois et une accélération du temps d'exécution d'environ 11.2 fois.

#### Formule complexe insatisfiable (uuf150-01.cnf)

| Métrique | DP | DPLL | Amélioration |
|----------|-------|--------|--------------|
| Appels | 883,526 | 121,585 | 7.3× |
| Temps (s) | 1702.64 | 95.59 | 17.8× |

C'est sur ce cas complexe que la différence entre les deux algorithmes est la plus frappante. DPLL résout la formule en moins de 2 minutes alors que DP nécessite près de 28 minutes. Cette différence montre que l'efficacité de DPLL s'accentue avec la complexité du problème.

## Conclusions

1. DPLL surpasse systématiquement DP sur tous les types de formules testées.

2. L'avantage de DPLL s'accentue avec la taille et la complexité des formules, ce qui le rend particulièrement adapté aux problèmes SAT de grande taille.

3. L'amélioration est particulièrement notable pour les formules insatisfiables, où DPLL évite d'explorer de larges portions de l'espace de recherche.

4. Les deux algorithmes utilisent la mémorisation pour éviter de recalculer les résultats de sous-problèmes déjà résolus, mais DPLL génère moins de sous-problèmes grâce à ses mécanismes de simplification plus avancés.