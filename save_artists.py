from apputil import Genius
import pandas as pd
from multiprocessing import Pool

ACCESS_TOKEN = "mM0WebFw8tppEufdTk1MvicVfBm0MVitCzTrsaxitH47nkt_nuBUdxVoLBgmNNlY"
genius = Genius(ACCESS_TOKEN)


def fetch_artist(term):
    try:
        artist_data = genius.get_artist(term)
        artist = artist_data["response"]["artist"]

        return {
            "search_term": term,
            "artist_name": artist.get("name"),
            "artist_id": artist.get("id"),
            "followers_count": artist.get("followers_count")
        }

    except Exception:
        return {
            "search_term": term,
            "artist_name": None,
            "artist_id": None,
            "followers_count": None
        }


if __name__ == "__main__":

    with open("artists.txt", "r") as file:
        artist_list = [line.strip() for line in file if line.strip()]

    # Use 4 processes (adjust if needed)
    with Pool(4) as pool:
        results = pool.map(fetch_artist, artist_list)

    df = pd.DataFrame(results)
    df.to_csv("artists_output.csv", index=False)

    print("Saved to artists_output.csv")
