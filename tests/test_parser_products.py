from pathlib import Path

from robot.parser import parse_products

FIXTURE = Path(__file__).parent / "fixtures" / "category_page.html"


def charger():
    return parse_products(FIXTURE.read_text(encoding="utf-8"), category_id=266)


def test_le_bloc_sans_prix_est_ignore():
    assert len(charger()) == 4


def test_produit_normal():
    p = charger()[0]
    assert (p.id, p.name, p.price) == (16444, "AIL FILET 500G", 4.79)
    assert (p.unit_price, p.unit_label) == (9.58, "kg")
    assert p.in_stock is True
    assert p.category_id == 266
    assert p.url.endswith("16444-ail-filet-500g.html")


def test_prix_au_kilo_invalide_devient_none():
    p = charger()[1]
    assert p.id == 2001
    assert p.price == 1.99
    assert p.unit_price is None and p.unit_label is None


def test_libelle_absent_garde_la_valeur():
    p = charger()[2]
    assert (p.unit_price, p.unit_label) == (14.17, None)


def test_rupture_de_stock():
    assert charger()[3].in_stock is False
