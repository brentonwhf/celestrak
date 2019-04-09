from space_weather import SpaceWeather


class SpaceWeatherAll(SpaceWeather):
    @property
    def url(self):
        """ get the url endpoint where the data exists """
        return "https://celestrak.com/SpaceData/SW-All.txt"

    def __init__(self):
        super(SpaceWeatherAll, self).__init__()