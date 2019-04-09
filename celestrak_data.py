from abc import ABC, abstractmethod
import pandas as pd
import requests


class CelestrakData(ABC):
    _observed_begin_key = "BEGIN OBSERVED"
    _observed_end_key = "END OBSERVED"
    _predicted_begin_key = "BEGIN DAILY_PREDICTED"
    _predicted_end_key = "END DAILY_PREDICTED"

    @property
    @abstractmethod
    def url(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def df_observed(self):
        """ get the observed data as a dataframe """
        raise NotImplementedError

    @property
    @abstractmethod
    def df_predicted(self):
        """ get the predicted data as a dataframe """
        raise NotImplementedError

    @property
    def number_of_observations(self):
        """ get the number of observations """
        return self.df_observed.size[0]

    def __init__(self):
        super(CelestrakData, self).__init__()

    def _read_txt_response(self):
        """
            download the txt file and return the data as a requests response

            Returns:
                (requests.response):        the response from the request to download the data
        """
        sess = requests.Session()
        response = sess.get(self.url)
        response.raise_for_status()
        return response

    def _read_txt_string(self):
        response = self._read_txt_response()
        return response.text

    def _read_txt_bytes(self):
        """
            read the data text files and return the data as bytes

            Returns:
                (io.Bytes):     the text file as bytes
        """
        response = self._read_txt_response()
        return response.content

    @abstractmethod
    def _txt_to_dfs(self):
        """ convert the tables of data within the text file to individual dataframes """
        raise NotImplementedError

    def __getitem__(self, epoch):
        """
            get a historical data value based on the input date else predict a historical data value to within a
                tolerable accuracy

            Args:
                epoch (datetime.date):      the date of the data that is desired

            Returns:

        """
        if epoch < self.df_observed.index.get_level_values('epoch').min():
            raise ValueError
        # TODO: determine what the upper limit for epoch is
        if epoch > self.df_predicted.index.get_level_values('epoch').max():
            raise ValueError
        epoch_date = pd.Timestamp(year=epoch.year, month=epoch.month, day=epoch.day)
        if epoch_date <= self.df_observed.index.get_level_values('epoch').max():
            return self.df_observed.loc[self.df_observed.index.get_level_values('epoch') == epoch_date]
        else:
            # TODO: predict future spaceweather using an interpolation or other method
            raise NotImplementedError
