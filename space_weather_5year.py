from space_weather import SpaceWeather


class SpaceWeather5Year(SpaceWeather):
    @property
    def url(self):
        """ get the url """
        return "https://celestrak.com/SpaceData/SW-Last5Years.txt"

    def __init__(self):
        super(SpaceWeather5Year, self).__init__()
