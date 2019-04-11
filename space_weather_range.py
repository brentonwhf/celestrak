from space_weather_all import SpaceWeatherAll


class SpaceWeatherRange(SpaceWeatherAll):
    
    @property
    def epoch_min(self):
        """ get the most historic date that data is being considered """
        return self._epoch_min

    @property
    def epoch_max(self):
        """ get the most recent date that data is being considered """
        return self._epoch_max

    @property
    def df_predicted(self):
        """ overwrite the default behaviour for the predicted data """
        raise NotImplementedError("A historical date range of data cannot predict future values")

    @df_predicted.setter
    def df_predicted(self, value):
        """ overwrite the default behaviour for setting the predicted data """
        raise NotImplementedError("A historical date range of data cannot predict future values")

    def __init__(self, epoch_min, epoch_max):
        """
            Args:
                epoch_min (datetime.datetime):      the most historic date that data should be considered
                epoch_max (datetime.datetime):      the most recent date that data should be considered
        """
        super().__init__()
        self._epoch_min = epoch_min
        self._epoch_max = epoch_max
        self.df_observed = self.df_observed.loc[self.df_observed.index.get_level_values('epoch') <= epoch_max]
        self.df_observed = self.df_observed.loc[self.df_observed.index.get_level_values('epoch') >= epoch_min]
        self._df_predicted = None
