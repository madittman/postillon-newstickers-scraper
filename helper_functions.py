import sys
import time

import requests

from exceptions.exceptions import MaxRetriesReachedError


def get_response_with_retry(
    url: str, initial_backoff: int = 5, max_retries: int = 5
) -> requests.Response:
    """Get response from URL with retry logic."""
    response: requests.Response = requests.get(url)

    backoff: int = initial_backoff
    for attempt in range(max_retries):
        if response.status_code == 429:
            print(
                f"> Too many requests for URL '{url}'\n"
                + f"Sleeping for {backoff} seconds...\n",
                file=sys.stderr,
            )
            time.sleep(backoff)
            backoff *= 2
            response = requests.get(url)
    if response.status_code == 429:
        raise MaxRetriesReachedError(
            f"URL '{url}' responses with status code '429 Too Many Requests' after {max_retries} retries"
        )

    # Raise error for 4xx or 5xx responses
    response.raise_for_status()

    return response
