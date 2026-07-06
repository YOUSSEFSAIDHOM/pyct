import time
import requests
import sys

def get_with_retry(url, params=None, max_attempts=3, wait=2):

    """
    Instead of attempting to retrieve studies and failing,
    This enables you to retry until successful.

    Args:
        url (str) : The base URL for the API

        params (dict) : The parameters for the search may include condition, interventions etc

        max_attempts (int)

        wait (int) : how long you wait between each attempt in seconds

    Returns:

        request.Response : can then be maniuplated as a pandas dataframe

    Raises:
        If all else fails, a HTTPError is raised, with the last error printed to terminal
        
    """

    last_error = None

    for attempt in range(1, max_attempts+1):

        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            print(f"Succeeded in {attempt}/{max_attempts} attempts")
            return resp

        except requests.HTTPError as e:
            last_error = e
            status_code = e.response.status_code

            # Retrying 4xx errors e.g. 404 or 400 won't succeed
            # ...Except for error 429 which is 'too many requests'

            if 400 <= status_code < 500 and status_code != 429:
                raise

            print(f"Attempt {attempt}/{max_attempts} has failed with {status_code}")

            waiting(wait)

        except requests.ConnectionError as e:
            last_error = e
            print(f"Attempt {attempt}/{max_attempts} failed due to a connection error")

            waiting(wait)

        except requests.Timeout as e:
            last_error = e
            print(f"Attempt {attempt}/{max_attempts} failed, request timed out") 

    raise requests.HTTPError(f"{max_attempts}/{max_attempts} attemps failed :(\nLast Error:\n\t{last_error} ")

def waiting(wait):
    """
    Procedure for the waiting text 'animation'
    """
    while wait > 0:
        sys.stdout.write("\r" + f"Retrying in {wait}s")
        time.sleep(1)
        wait -= 1
        sys.stdout.flush()
    print()