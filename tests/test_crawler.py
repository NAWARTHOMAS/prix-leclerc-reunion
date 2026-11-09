from robot.crawler import crawl_store, discover_categories

HOME = """
<a href="https://www.drivezeclerc.re/st-benoit/266-fruits-et-legumes">Fruits</a>
<a href="/st-benoit/153-frais">Frais</a>
<a href="/le-tampon/153-frais">Autre magasin</a>
<a href="/st-benoit/panier">Panier</a>
<a href="/st-benoit/153-frais">Frais (doublon)</a>
"""


def page(ids):
    items = "".join(
        f'<li class="ajax_block_product">'
        f'<a class="product-name" href="https://x/{i}-p.html">P{i}</a>'
        f'<div class="grid-left-bottom"><meta itemprop="price" content="1.00">'
        f'<link itemprop="availability" href="https://schema.org/InStock">'
        f"<strong>1.00 € / kg</strong></div>"
        f'<a data-id-product="{i}"></a></li>'
        for i in ids
    )
    return f"<ul>{items}</ul>"


def test_decouverte_garde_les_categories_du_magasin_une_seule_fois():
    assert discover_categories(HOME, "st-benoit") == [
        (153, "/st-benoit/153-frais"),
        (266, "/st-benoit/266-fruits-et-legumes"),
    ]


def test_pagination_s_arrete_quand_il_n_y_a_plus_de_nouveau_produit():
    pages = {
        "/st-benoit/153-frais": page([1, 2]),
        "/st-benoit/153-frais?p=2": page([3]),
        "/st-benoit/153-frais?p=3": page([3]),
    }
    appels = []

    def fetch(chemin):
        appels.append(chemin)
        return pages[chemin]

    produits = crawl_store(
        "st-benoit", [(153, "/st-benoit/153-frais")], fetch, sleep=lambda s: None
    )
    assert sorted(p.id for p in produits) == [1, 2, 3]
    assert appels == [
        "/st-benoit/153-frais",
        "/st-benoit/153-frais?p=2",
        "/st-benoit/153-frais?p=3",
    ]


def test_produit_present_dans_deux_categories_garde_une_fois():
    pages = {
        "/s/1-a": page([1, 2]),
        "/s/1-a?p=2": page([1, 2]),
        "/s/2-b": page([2, 3]),
        "/s/2-b?p=2": page([2, 3]),
    }
    produits = crawl_store(
        "s",
        [(1, "/s/1-a"), (2, "/s/2-b")],
        lambda chemin: pages[chemin],
        sleep=lambda s: None,
    )
    assert sorted(p.id for p in produits) == [1, 2, 3]
    assert next(p for p in produits if p.id == 2).category_id == 1


def test_pause_entre_chaque_requete():
    pauses = []
    pages = {"/s/1-a": page([1]), "/s/1-a?p=2": page([1])}
    crawl_store(
        "s", [(1, "/s/1-a")], lambda c: pages[c], sleep=pauses.append, delay=1.5
    )
    assert pauses == [1.5]
