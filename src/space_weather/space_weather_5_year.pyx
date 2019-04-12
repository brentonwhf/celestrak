# distutils: language = c++
# cython: language_level=3

from src.space_weather.space_weather cimport SpaceWeather


cdef class SpaceWeather5Year(SpaceWeather):

    def __cinit__(self):
        pass

    def __init__(self):
        super().__init__()

    cpdef str url(self):
        """ return the unique url associated with the data of interest """
        return u"https://celestrak.com/SpaceData/SW-Last5Years.txt"