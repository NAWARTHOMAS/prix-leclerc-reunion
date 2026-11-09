from robot.parser import parse_unit_price


def test_prix_au_kilo_normal():
    assert parse_unit_price("9.58 € / kg") == (9.58, "kg")


def test_libelle_en_majuscule_est_mis_en_minuscule():
    assert parse_unit_price("1.79 € / Kg") == (1.79, "kg")


def test_libelle_absent():
    assert parse_unit_price("14.17 € /") == (14.17, None)


def test_valeur_invalide_inf():
    assert parse_unit_price("INF € / ") == (None, None)


def test_texte_vide():
    assert parse_unit_price("") == (None, None)


def test_virgule_decimale():
    assert parse_unit_price("2,59 € / L") == (2.59, "l")
