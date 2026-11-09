import json
from datetime import datetime, timezone

from robot.run import STORES, run_store

HOME = '<a href="/st-benoit/153-frais">Frais</a>'
PAGE = (
    '<ul><li class="ajax_block_product">'
    '<a class="product-name" href="https://x/1-p.html">P1</a>'
    '<div class="grid-left-bottom"><meta itemprop="price" content="2.50">'
    '<link itemprop="availability" href="https://schema.org/InStock">'
    "<strong>2.50 € / kg</strong></div>"
    '<a data-id-product="1"></a></li></ul>'
)


def test_liste_des_magasins():
    assert STORES == ["riviere-des-pluies"]


def test_run_store_ecrit_le_fichier(tmp_path):
    pages = {"/st-benoit/": HOME, "/st-benoit/153-frais": PAGE, "/st-benoit/153-frais?p=2": PAGE}
    n = run_store(
        "st-benoit",
        lambda chemin: pages[chemin],
        tmp_path,
        datetime(2026, 11, 9, tzinfo=timezone.utc),
        sleep=lambda s: None,
    )
    assert n == 1
    contenu = json.loads((tmp_path / "st-benoit.json").read_text(encoding="utf-8"))
    assert contenu["products"][0]["name"] == "P1"
    assert contenu["products"][0]["price"] == 2.5
