import time

import requests

from .crawler import BASE_URL


class BlockedError(RuntimeError):
    """Le site nous refuse (403 ou 429) : on s'arrête sans insister."""


class Fetcher:
    def __init__(
        self,
        session=None,
        base_url: str = BASE_URL,
        contact: str = "",
        timeout: int = 30,
        retries: int = 3,
        sleep=time.sleep,
    ):
        self.session = session or requests.Session()
        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries
        self.sleep = sleep
        self.user_agent = f"prix-leclerc-reunion/1.0 (+{contact})"

    def __call__(self, path: str) -> str:
        url = self.base_url + path
        last_error = None
        for attempt in range(1, self.retries + 1):
            try:
                response = self.session.get(
                    url,
                    headers={"User-Agent": self.user_agent},
                    timeout=self.timeout,
                )
            except requests.RequestException as error:
                last_error = error
                if attempt < self.retries:
                    self.sleep(2 ** attempt)
                continue
            if response.status_code in (403, 429):
                raise BlockedError(f"Accès refusé ({response.status_code}) pour {url}")
            if response.status_code >= 500:
                last_error = RuntimeError(f"Erreur serveur {response.status_code}")
                if attempt < self.retries:
                    self.sleep(2 ** attempt)
                continue
            response.raise_for_status()
            return response.text
        raise RuntimeError(f"Échec après {self.retries} essais pour {url} : {last_error}")
