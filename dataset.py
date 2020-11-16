import datetime
import logging
import quandl
import scipy

from datetime import date


class FREDDataset:
    def __init__(self, headers, start_date, end_date, api_key):
        self.headers = headers
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        quandl.ApiConfig.api_key = api_key

        # TODO (christian.abbott):
        # To scale to larger datasets, use pagination and don't store everything in memory at once.
        # This is currently not an issue because the dataset is small and pandas is memory optimized.
        try:
            self.dataframe = quandl.get(
                self.headers,
                start_date=f"{self.start_date}",
                end_date=f"{self.end_date}")
            self.dataframe = self.dataframe[::-1]
            self.dataframe.columns = [header.split("/")[-1] for header in self.headers]
        except Exception as e:
            logging.fatal("Error retrieving data from Quandl. Aborting.")
            raise e
