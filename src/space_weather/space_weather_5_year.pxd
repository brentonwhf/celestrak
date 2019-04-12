# distutils: language = c++
# cython: language_level=3

from src.space_weather.space_weather cimport SpaceWeather


cdef class SpaceWeather5Year(SpaceWeather):

    pass