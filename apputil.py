import requests
import pandas as pd


class Genius:

    BASE_URL = "https://api.genius.com"
    """"A simple wrapper for the Genius API to fetch artist information."""
    def __init__(self, access_token):
        self.access_token = access_token

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def get_artist(self, search_term):
        """
        Takes a search term, performs a search to find the artist ID,
        and then fetches the artist information.
        """
        search_data = self._make_request(
            "/search",
            params={"q": search_term}
        )

        # Extract artist id from the first hit if available
        try:
            artist_id = search_data["response"]["hits"][0]["result"]["primary_artist"]["id"]
        except (KeyError, IndexError):
            return None

        artist_data = self._make_request(f"/artists/{artist_id}")

        return artist_data

    def get_artists(self, search_terms):
        """
        Takes a list of search terms and returns a DataFrame
        with artist information for each.
        """

        rows = []

        for term in search_terms:
            try:
                artist_data = self.get_artist(term)

                artist = artist_data["response"]["artist"]

                rows.append({
                    "search_term": term,
                    "artist_name": artist.get("name"),
                    "artist_id": artist.get("id"),
                    "followers_count": artist.get("followers_count")
                })

            except Exception:
                rows.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        return pd.DataFrame(rows)