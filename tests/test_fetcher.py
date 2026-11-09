import pytest
import requests

from robot.fetcher import BlockedError, Fetcher


class Reponse:
    def __init__(self, code, texte=""):
        self.status_code = code
        self.text = texte

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


class FausseSession:
    def __init__(self, reponses):
        self.reponses = list(reponses)
        self.appels = []

    def get(self, url, headers=None, timeout=None):
        self.appels.append((url, headers))
        element = self.reponses.pop(0)
        if isinstance(element, Exception):
            raise element
        return element


def test_succes_renvoie_le_texte_et_signe_la_requete():
    session = FausseSession([Reponse(200, "<html>ok</html>")])
    fetch = Fetcher(session=session, contact="thomas@example.org", sleep=lambda s: None)
    assert fetch("/st-benoit/153-frais") == "<html>ok</html>"
    url, headers = session.appels[0]
    assert url == "https://www.drivezeclerc.re/st-benoit/153-frais"
    assert headers["User-Agent"] == "prix-leclerc-reunion/1.0 (+thomas@example.org)"


def test_403_leve_blockederror_sans_reessayer():
    session = FausseSession([Reponse(403)])
    fetch = Fetcher(session=session, sleep=lambda s: None)
    with pytest.raises(BlockedError):
        fetch("/x")
    assert len(session.appels) == 1


def test_erreur_serveur_puis_succes():
    session = FausseSession([Reponse(503), Reponse(200, "ok")])
    pauses = []
    fetch = Fetcher(session=session, sleep=pauses.append)
    assert fetch("/x") == "ok"
    assert pauses == [2]


def test_abandon_apres_trois_essais():
    session = FausseSession([Reponse(500), Reponse(500), Reponse(500)])
    fetch = Fetcher(session=session, sleep=lambda s: None)
    with pytest.raises(RuntimeError):
        fetch("/x")
    assert len(session.appels) == 3


def test_erreur_reseau_est_reessayee():
    session = FausseSession([requests.ConnectionError("coupé"), Reponse(200, "ok")])
    fetch = Fetcher(session=session, sleep=lambda s: None)
    assert fetch("/x") == "ok"
