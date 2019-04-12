# distutils: language = c++
# cython: language_level=3


cdef class CelestrakData:

    cdef object _df_observed
    cdef object _df_predicted

    cdef str _observed_begin_key
    cdef str _observed_end_key
    cdef str _predicted_begin_key
    cdef str _predicted_end_key

    cpdef str url(self)
    cdef object _read_txt_response(self)
    cdef str _read_txt_string(self)
    cdef object _read_txt_bytes(self)
    cdef void _txt_to_dfs(self)
