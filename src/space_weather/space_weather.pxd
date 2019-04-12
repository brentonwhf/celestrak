# distutils: language = c++
# cython: language_level=3

import numpy as np
cimport numpy as np

from src.celestrak_data cimport CelestrakData


cdef class SpaceWeather(CelestrakData):

    cdef np.ndarray _column_widths
    cdef list _columns

    cdef object _ap_series(self)
    cpdef double ap_index(self, object epoch) except *
    cpdef double f107a(self, object epoch) except *
    cpdef double f107(self, object epoch) except *
    cpdef double ap_daily(self, object epoch) except *
    cpdef np.ndarray[np.float64_t, ndim=1] ap_array(self, object epoch)