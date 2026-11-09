import json
from datetime import datetime, timezone

import pytest

from robot.models import Product
from robot.writer import SuspiciousDropError, build_payload, write_store_file

MAINTENANT = datetime(2026, 11, 9, 22, 0, 5, tzinfo=timezone.utc)


def produit(i):
    return Product(i, f"P{i}", 1.0, 1.0, "kg", True, 1, f"https://x/{i}.html")


def test_payload_trie_par_id_et_compte():
    payload = build_payload("st-benoit", [produit(3), produit(1)], MAINTENANT)
    assert payload["schema_version"] == 1
    assert payload["store"] == "st-benoit"
    assert payload["generated_at"] == "2026-11-09T22:00:05+00:00"
    assert payload["count"] == 2
    assert [p["id"] for p in payload["products"]] == [1, 3]


def test_ecriture_cree_le_dossier_et_le_fichier(tmp_path):
    payload = build_payload("st-benoit", [produit(1)], MAINTENANT)
    chemin = write_store_file(tmp_path / "data", payload)
    assert chemin.name == "st-benoit.json"
    assert json.loads(chemin.read_text(encoding="utf-8"))["count"] == 1


def test_garde_fou_refuse_un_fichier_presque_vide(tmp_path):
    gros = build_payload("s", [produit(i) for i in range(10)], MAINTENANT)
    write_store_file(tmp_path, gros)
    petit = build_payload("s", [produit(1)], MAINTENANT)
    with pytest.raises(SuspiciousDropError):
        write_store_file(tmp_path, petit)
    assert json.loads((tmp_path / "s.json").read_text(encoding="utf-8"))["count"] == 10


def test_une_baisse_raisonnable_est_acceptee(tmp_path):
    write_store_file(tmp_path, build_payload("s", [produit(i) for i in range(10)], MAINTENANT))
    write_store_file(tmp_path, build_payload("s", [produit(i) for i in range(6)], MAINTENANT))
    assert json.loads((tmp_path / "s.json").read_text(encoding="utf-8"))["count"] == 6
