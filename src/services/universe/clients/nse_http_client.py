import requests


class NSEHttpClient:
    """
    Handles communication with NSE.

    Responsible for:
        - maintaining session
        - cookies
        - request headers

    Not responsible for:
        - parsing
        - business logic
    """

    BASE_URL = "https://www.nseindia.com"

    def __init__(self):

        self._session = requests.Session()

        self._session.headers.update(
            {
                "User-Agent":
                    "Mozilla/5.0",
                "Accept":
                    "application/json,text/csv,*/*",
                "Accept-Language":
                    "en-US,en;q=0.9",
                "Referer":
                    "https://www.nseindia.com/",
            }
        )

        # Establish cookies
        self._session.get(
            self.BASE_URL,
            timeout=15,
        )

    def download(self, url: str) -> str:

        response = self._session.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        return response.text