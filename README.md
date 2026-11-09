# Prix Leclerc Réunion

Relevé quotidien des prix publics du drive E.Leclerc Rivière des Pluies
(drivezeclerc.re), pour l'appli « Courses au budget » (Studio Biboup).

## Données
Un fichier dans `data/` : `riviere-des-pluies.json` (magasin unique pour l'instant).
Format (version 1) : `schema_version`, `store`, `generated_at`, `count`, `products[]`
avec `id`, `name`, `price`, `unit_price`, `unit_label`, `in_stock`, `category_id`, `url`.
**Les identifiants produits sont propres à chaque magasin.**

## Règles du robot
Pages de catégories uniquement (pas la recherche, interdite par le robots.txt du site),
1,5 s entre deux requêtes, arrêt immédiat sur 403/429.

## Accord de Leclerc
Accord déclaré par Thomas le 2026-11-09. À compléter : date, interlocuteur,
portée exacte (copie quotidienne / dépôt public / publication de l'appli).

## Mesures (2026-11-09, depuis un PC, magasin Rivière des Pluies)
Passage complet : 2 595 produits, 18 catégories contenant des produits,
11 min 42 s, fichier de 670 Ko. Aucun produit « hors stock » rencontré :
le site semble masquer les produits indisponibles.
