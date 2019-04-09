import io
import pandas as pd

from celestrak_data import CelestrakData


class SpaceWeather(CelestrakData):
    _df_observed = pd.DataFrame()
    _df_predicted = pd.DataFrame()

    _column_widths = [4, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 4, 6, 2, 6, 6, 6, 6, 6]
    _columns = [
        'year', 'month', 'day', 'BSRN', 'ND', 'Kp (0000-0300 UT)', 'Kp (0300-0600 UT)', 'Kp (0600-0900 UT)',
        'Kp (0900-1200 UT)', 'Kp (1200-1500 UT)', 'Kp (1500-1800 UT)', 'Kp (1800-2100 UT)',
        'Kp (2100-0000 UT)', 'Kp Sum', 'Ap (0000-0300 UT)', 'Ap (0300-0600 UT)', 'Ap (0600-0900 UT)',
        'Ap (0900-1200 UT)', 'Ap (1200-1500 UT)', 'Ap (1500-1800 UT)', 'Ap (1800-2100 UT)',
        'Ap (2100-0000 UT)', 'Ap Avg', 'Cp', 'C9', 'ISN', 'Adj F10.7', 'Q', 'Adj Ctr81', 'Adj Lst81',
        'Obs F10.7', 'Obs Ctr81', 'Obs Lst81'
    ]

    @property
    def df_observed(self):
        """ get the historical space weather observations as a dataframe """
        if not isinstance(self._df_observed, pd.DataFrame):
            raise TypeError
        if self._df_observed.empty:
            raise ValueError
        return self._df_observed

    @df_observed.setter
    def df_observed(self, value):
        """ set the observed space weather as a dataframe """
        if not isinstance(value, pd.DataFrame):
            raise TypeError
        if value.empty:
            raise ValueError
        self._df_observed = value

    @property
    def df_predicted(self):
        """ get the predicted data as a dataframe """
        if not isinstance(self._df_predicted, pd.DataFrame):
            raise TypeError
        if self._df_predicted.empty:
            raise ValueError
        return self._df_predicted

    @df_predicted.setter
    def df_predicted(self, value):
        """ set the predicted data as a dataframe """
        if not isinstance(value, pd.DataFrame):
            raise TypeError
        if value.empty:
            raise ValueError
        self._df_predicted = value

    def __init__(self):
        super(SpaceWeather, self).__init__()
        self._txt_to_dfs()

    def _txt_to_dfs(self):
        """ break the data tables from the text files downloaded into dataframes """
        data = self._read_txt_string()
        data_observed_string = data.split(self._observed_begin_key + '\r\n')[1].split(self._observed_end_key)[0]
        df_observed = pd.read_fwf(
            io.StringIO(data_observed_string),
            names=self._columns,
            widths=self._column_widths,
            parse_dates=[[0, 1, 2]],  # parse the separate year, month and day columns
            infer_datetime_format=True,
            index_col='year_month_day',
        )
        df_observed.index.name = 'epoch'
        data_predicted_string = data.split(self._predicted_begin_key + '\r\n')[1].split(self._predicted_end_key)[0]
        df_predicted = pd.read_fwf(
            io.StringIO(data_predicted_string),
            names=self._columns,
            widths=self._column_widths,
            parse_dates=[[0, 1, 2]],  # parse the separate year, month and day columns
            infer_datetime_format=True,
            index_col='year_month_day',
        )
        df_predicted.index.name = 'epoch'
        self.df_observed = df_observed
        self.df_predicted = df_predicted
        # return df_observed, df_predicted
