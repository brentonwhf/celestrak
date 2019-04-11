import io
import pandas as pd
import numpy as np
from datetime import timedelta, datetime

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

    @property
    def ap_series(self):
        """ get the ap time series """
        return self._ap_series()

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

    def _ap_series(self):
        """
            convert the 3 hourly ap data into a single continuous timestamped series
        """
        df = pd.DataFrame(
            self.df_observed.loc[:,
            [
                'Ap (0000-0300 UT)',
                'Ap (0300-0600 UT)',
                'Ap (0600-0900 UT)',
                'Ap (0900-1200 UT)',
                'Ap (1200-1500 UT)',
                'Ap (1500-1800 UT)',
                'Ap (1800-2100 UT)',
                'Ap (2100-0000 UT)'
            ]].stack(),
            columns=['3_hour_ap_index']
        )
        df.index = df.index.set_names('ap_period', level=1)

        def houriser(row):
            epoch_ref = row['epoch']
            hours = epoch_ref + timedelta(hours=float(row['ap_period'][4:6]))
            return hours

        df = df.reset_index(drop=False)
        df['epoch'] = df.apply(houriser, axis=1)
        return df.set_index(['epoch', 'ap_period'], drop=True)

    def _ap_index(self, epoch):
        """ get the ap index for a particular epoch """
        # epoch_date = datetime(year=epoch.year, month=epoch.month, day=epoch.day)
        # if epoch_date < self.df_observed.index.get_level_values('epoch').min():
        #     raise ValueError
        # if epoch_date > self.df_predicted.index.get_level_values('epoch').max():
        #     raise ValueError
        if epoch.hour < 3:
            col = 'Ap (0000-0300 UT)'
        elif epoch.hour < 6:
            col = 'Ap (0300-0600 UT)'
        elif epoch.hour < 9:
            col = 'Ap (0600-0900 UT)'
        elif epoch.hour < 12:
            col = 'Ap (0900-1200 UT)'
        elif epoch.hour < 15:
            col = 'Ap (1200-1500 UT)'
        elif epoch.hour < 18:
            col = 'Ap (1500-1800 UT)'
        elif epoch.hour < 21:
            col = 'Ap (1800-2100 UT)'
        else:
            col = 'Ap (2100-0000 UT)'
        return self[epoch][col].values[0]


    def f107a(self, epoch):
        """
            the 81 day average F10.7 flux (centred on the day of the epoch)

            Args:
                epoch (datetime.datetime):  the current datetime

            Returns:
                (float):                    the 81 day f107 index associated with the epoch
        """
        return self[epoch]['Obs Ctr81'].values[0]

    def f107(self, epoch):
        """
            daily F10.7 flux for the previous day

            Args:
                epoch (datetime.datetime):  the current datetime

            Returns:
                (float):                    the daily f107 index associated with the epoch
        """
        return self[epoch]['Obs F10.7'].values[0]

    def ap_daily(self, epoch):
        """
            magnetic flux index (daily)

            Args:
                epoch (datetime.datetime):  the current datetime

            Returns:
                (float):                    the daily ap index associated with the epoch
        """
        return self[epoch]['Ap Avg'].values[0]

    def ap_array(self, epoch):
        """
            array containing the magnetic index values

            Args:
                epoch (datetime.datetime):  the current datetime

            Returns:
                (np.array):     [
                                    daily AP,
                                    3 hour AP index for the current time,
                                    3 hour AP index for 3 hours before the current time,
                                    3 hour AP index for 6 hours before the current time,
                                    3 hour AP index for 9 hours before the current time,
                                    Average of eight 3 hour AP indicies from 12 to 33 hours prior to the current time,
                                    Average of eight 3 hour AP indicies from 36 to 57 hours prior to the current time,
                                ]
        """
        ap_array = np.zeros((7,), dtype=np.float64)
        # ap_timeseries = self.ap_series
        epoch_ap_current = datetime(year=epoch.year, month=epoch.month, day=epoch.day) \
                           + timedelta(hours=(epoch.hour // 3) * 3)
        ap_timedelta = timedelta(hours=3)
        # the daily average ap index for the current day
        ap_array[0] = self[epoch]['Ap Avg'].values[0]
        # 3 hour index for the current epoch
        ap_array[1] = self._ap_index(epoch_ap_current)
        ap_array[2] = self._ap_index(epoch_ap_current - ap_timedelta)
        ap_array[3] = self._ap_index(epoch_ap_current - 2*ap_timedelta)
        ap_array[4] = self._ap_index(epoch_ap_current - 3*ap_timedelta)
        ap_array[5] = np.mean([self._ap_index(epoch_ap_current - i*ap_timedelta) for i in range(4, 12)])
        ap_array[6] = np.mean([self._ap_index(epoch_ap_current - i*ap_timedelta) for i in range(12, 20)])
        return ap_array
