import requests
import pandas as pd
from tqdm import tqdm
import datetime
from utils import get_with_retry


class ClinicalTrials:
    """
    PYCT is a Python-wrapper for the ClinicalTrials.gov API
    which supports full pagination, mutliple query fields and built-in export options

    Basic usage:

        ct = ClinicalTrials()
        df = ct.get_studies(conditions="Alzheimer", intervention="Non-pharmacological")
        ct.to_csv(df, "trials.csv")

    """

    # Base URL for the ClinicalTrials API
    BASE  = "https://clinicaltrials.gov/api/v2"

    def __init__(self):
        info = self._get_api_info()
        self.api_version = info.get("apiVersion")
        self.last_updated = info.get("dataTimestamp")

    def __repr__(self):
        return (
            f"PYCT | "
            f"ClinicalTrials API v{self.api_version} | "
            f"Data base last updated {self.last_updated}"
        )

    # ---------------------------- #
    #       Public methods         #
    # ---------------------------- #

    def get_studies(self,
                    condition = None,
                    intervention = None,
                    term = None, 
                    status = None,
                    page_size=1000):

        """
        Retrieves all the studies that match with a given query

        Args:
            condition (str) : e.g. "Dementia", "Covid"

            intervention (str) : e.g. "excercise", "ECT"

            term (str) : General keyword search across all fields

            status (str) : Studies may have one of the following recuirtment statuses:
                - RECRUITING, COMPLETED, NOT_YET_RECRUITING, ACTIVE_NOT_RECRUITING, and TERMINATED

            page_size (int) : Number of results per page (max 1000). Defaults to 1000.

        Returns:
            A pandas data frame
        """

        params = {"format":"json", "pageSize":page_size}

        params["query.cond"] = condition if condition is not None else None
        params["query.intr"] = intervention if intervention is not None else None
        params["query.term"] = term if term is not None else None
        params["filter.status"] = status if status is not None else None

        params = {k: v for k, v in params.items() if v is not None}

        return self._paginate(params)

    def get_study(self, nct):
        """
        All studies can be identified with an NCT number. This method allows you to fetch one study
        
        Args:
            nct (str) : eg. NCT06210035

        Returns:
            dict: the full study record as a dictionary

        Raises:
            requests.HTTPError: A HTTP error code if something goes wrong, e.g. (404) If study is not found
        """
        resp = get_with_retry(f"{self.BASE}/studies/{nct}")
        return resp.json()


    # ---------------------------- #
    #       Private methods        #
    # ---------------------------- #

    def _get_api_info(self):
        """
        Returns API version and date last updated.
        """
        resp = requests.get(f"{self.BASE}/version")
        resp.raise_for_status()
        return resp.json()

    def _paginate(self, params):
        """
        Handle pagination automatically

        It fetches all pages from the /studies endpoint, by passing the limit using a nextPageToken,
        and returns a single combined DataFrame.

        Args:
            params (dict) : Query parameters to send with each request

        Returns:
            A pandas dataframe, all pages combined.
        """

        all_dfs = []

        with tqdm(desc="Fetching studies", unit="page") as pbar:
            while True:
                resp = get_with_retry(f"{self.BASE}/studies", params=params)
                data = resp.json()

                studies = data.get("studies", [])
                if not studies:
                    break

                all_dfs.append(pd.json_normalize(studies))

                pbar.update(1)
                pbar.set_postfix({"Found ": sum(len(d) for d in all_dfs)})

                next_token = data.get("nextPageToken")
                if not next_token:
                    break

                params["pageToken"] = next_token


        if not all_dfs:
            return pd.DataFrame()

        return pd.concat(all_dfs, ignore_index=True)

    # ---------------------------- #
    #       Export methods         #
    # ---------------------------- #

    def to_csv(self, df, filename=None):

        if not filename:
            filename = f"studies_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        df.to_csv(filename, index=False)
        print(f"{len(df)} saved to {filename}")

    def to_excel(self, df, filename=None):

        if not filename:
            filename = f"studies_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        df.to_excel(filename, index=False)
        print(f"{len(df)} saved to {filename}")

    def to_json(self, df, filename=None, indent=2):
        if not filename:
            filename = f"studies_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        df.to_json(filename, orient="records" ,indent=2)
        print(f"{len(df)} saved to {filename}")

