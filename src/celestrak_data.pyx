# distutils: language = c++
# cython: language_level=3

import requests
import pandas as pd


cdef class CelestrakData:

    property df_observed:
        def __get__(self):
            """ get the dataframe of observed data points """
            raise NotImplementedError

    property df_predicted:
        def __get__(self):
            """ get the dataframe of predicted data points """
            raise NotImplementedError

    property number_of_observations:
        def __get__(self):
            """ get the number of observations within the observations dataframe """
            return self.df_observed.size[0]

    def __cinit__(self):
        self._observed_begin_key = "BEGIN OBSERVED"
        self._observed_end_key = "END OBSERVED"
        self._predicted_begin_key = "BEGIN DAILY_PREDICTED"
        self._predicted_end_key = "END DAILY_PREDICTED"
        self._df_observed = pd.DataFrame()
        self._df_predicted = pd.DataFrame()

    def __init__(self):
        self._txt_to_dfs()

    cpdef str url(self):
        """ return the unique url associated with the data of interest """
        raise NotImplementedError

    cdef object _read_txt_response(self):
        """
            download the txt file and return the data as a requests response

            Returns:
                (requests.response):        the response from the request to download the data
        """
        cdef object sess = requests.Session()
        cdef object response = sess.get(self.url())
        response.raise_for_status()
        return response

    cdef str _read_txt_string(self):
        """ convert the data response to a string """
        return self._read_txt_response().text

    cdef object _read_txt_bytes(self):
        """
            read the data text files and return the data as bytes

            Returns:
                (io.Bytes):     the text file as bytes
        """
        return self._read_txt_response().content

    cdef void _txt_to_dfs(self):
        """ convert the tables of data within the text file to individual dataframes """
        raise NotImplementedError

    def forecast(self, epoch, **kwargs):
        """
            predict a data value based on an extrapolation of the current data

            Args:
                epoch (datetime.date):      the date of the data that is desired

            Returns:

        """
        raise NotImplementedError

    def __getitem__(self, object epoch):
        """
            get a historical data value based on the input date else predict a data value to within a
                tolerable accuracy

            Args:
                epoch (datetime.datetime):      the date of the data that is desired

            Returns:
                (pandas.Series):            the row of data associated with the input epoch
        """
        if epoch < self.df_observed.index.get_level_values('epoch').min():
            raise ValueError
        if epoch > self.df_predicted.index.get_level_values('epoch').max():
            raise ValueError
        cdef object epoch_date = pd.Timestamp(year=epoch.year, month=epoch.month, day=epoch.day)
        if epoch_date <= self.df_observed.index.get_level_values('epoch').max():
            return self.df_observed.loc[self.df_observed.index.get_level_values('epoch') == epoch_date]
        elif epoch_date <= self.df_predicted.index.get_level_values('epoch').max():
            return self.df_predicted.loc[self.df_predicted.index.get_level_values('epoch') == epoch_date]
        else:
            raise ValueError