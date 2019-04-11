import pytest
import typing
from datetime import datetime, timedelta

from space_weather_all import SpaceWeatherAll


@pytest.fixture(scope='function')
def client():
    class Client:
        sw = SpaceWeatherAll()
    return Client()


# def test_url(client):
#     """ test the getting of the url """
#     assert client.sw.url == "https://celestrak.com/SpaceData/SW-All.txt"
#
#
# def test_read_txt_bytes(client):
#     """ test the reading of the data as bytes """
#     bytes = client.sw._read_txt_bytes()
#     assert isinstance(bytes, typing.ByteString)
#
#
# def test_read_txt_string(client):
#     """ test the downloading of the text file and returning of the data as a string """
#     string = client.sw._read_txt_string()
#     assert isinstance(string, str)
#
#
# def test_f107(client):
#     """ test the getting of the F10.7 data """
#     epoch1 = datetime(year=1957, month=10, day=1)
#     f107_1 = client.sw.f107(epoch1)
#     assert isinstance(f107_1, float)
#     assert f107_1 == 269.3
#     # test the case when the epoch is out of bounds
#     epoch2 = client.sw.df_observed.index.get_level_values('epoch').min() - timedelta(days=1)
#     with pytest.raises(ValueError):
#         result2 = client.sw.f107(epoch2)
#
#
# def test_f107a(client):
#     """ test the getting of the F10.7 data """
#     epoch1 = datetime(year=1957, month=10, day=1)
#     f107_1 = client.sw.f107a(epoch1)
#     assert isinstance(f107_1, float)
#     assert f107_1 == 266.6
#     # test the case when the epoch is out of bounds
#     epoch2 = client.sw.df_observed.index.get_level_values('epoch').min() - timedelta(days=1)
#     with pytest.raises(ValueError):
#         result2 = client.sw.f107a(epoch2)


# def test_ap_series(client):
#     """ test the getting of the F10.7 data """
#     ap_series = client.sw._ap_series()
#     assert True
#


def test_ap_index(client):
    """ test the getting of a specific ap index based on a precise epoch """
    epoch0 = datetime(year=1957, month=10, day=3, hour=1, minute=7, second=6)
    result0 = client.sw._ap_index(epoch0)
    assert result0 == 12
    # test the case when the epoch is on the limit
    epoch1 = datetime(year=1957, month=10, day=3, hour=3, minute=0, second=0)
    result1 = client.sw._ap_index(epoch1)
    assert result1 == 7
    # test the second period
    epoch2 = datetime(year=1957, month=10, day=3, hour=4, minute=7, second=6)
    result2 = client.sw._ap_index(epoch2)
    assert result2 == 7
    # test the case when the epoch is on the limit
    epoch3 = datetime(year=1957, month=10, day=3, hour=6, minute=0, second=0)
    result3 = client.sw._ap_index(epoch3)
    assert result3 == 5
    # test the third period
    epoch4 = datetime(year=1957, month=10, day=3, hour=7, minute=7, second=6)
    result4 = client.sw._ap_index(epoch4)
    assert result4 == 5
    # test the case when the epoch is on the limit
    epoch5 = datetime(year=1957, month=10, day=3, hour=9, minute=0, second=0)
    result5 = client.sw._ap_index(epoch5)
    assert result5 == 18
    # test the fourth period
    epoch6 = datetime(year=1957, month=10, day=3, hour=10, minute=7, second=6)
    result6 = client.sw._ap_index(epoch6)
    assert result6 == 18
    # test the case when the epoch is on the limit
    epoch7 = datetime(year=1957, month=10, day=3, hour=12, minute=0, second=0)
    result7 = client.sw._ap_index(epoch7)
    assert result7 == 22
    # test the fifth period
    epoch8 = datetime(year=1957, month=10, day=3, hour=13, minute=7, second=6)
    result8 = client.sw._ap_index(epoch8)
    assert result8 == 22
    # test the case when the epoch is on the limit
    epoch9 = datetime(year=1957, month=10, day=3, hour=15, minute=0, second=0)
    result9 = client.sw._ap_index(epoch9)
    assert result9 == 39
    # test the sixth period
    epoch10 = datetime(year=1957, month=10, day=3, hour=16, minute=7, second=6)
    result10 = client.sw._ap_index(epoch10)
    assert result10 == 39
    # test the case when the epoch is on the limit
    epoch11 = datetime(year=1957, month=10, day=3, hour=18, minute=0, second=0)
    result11 = client.sw._ap_index(epoch11)
    assert result11 == 32
    # test the seventh period
    epoch12 = datetime(year=1957, month=10, day=3, hour=19, minute=7, second=6)
    result12 = client.sw._ap_index(epoch12)
    assert result12 == 32
    # test the case when the epoch is on the limit
    epoch13 = datetime(year=1957, month=10, day=3, hour=21, minute=0, second=0)
    result13 = client.sw._ap_index(epoch13)
    assert result13 == 15
    # test the fourth period
    epoch14 = datetime(year=1957, month=10, day=3, hour=22, minute=7, second=6)
    result14 = client.sw._ap_index(epoch14)
    assert result14 == 15
    # test the case when the date is not valid
    epoch15 = client.sw.df_observed.index.get_level_values('epoch').min() - timedelta(days=1)
    with pytest.raises(ValueError):
        client.sw._ap_index(epoch15)
    # test the case when the date is not valid
    epoch16 = client.sw.df_predicted.index.get_level_values('epoch').max() + timedelta(days=1)
    with pytest.raises(ValueError):
        client.sw._ap_index(epoch16)
    # test the case when the hour is zero
    epoch17 = datetime(year=1957, month=10, day=3, hour=0, minute=0, second=0)
    result17 = client.sw._ap_index(epoch17)
    assert result17 == 12


def test_ap_array(client):
    """ test the assembly of the ap array """
    epoch1 = datetime(year=1958, month=2, day=11, hour=8, minute=7, second=6)
    ap_array = client.sw.ap_array(epoch1)
    assert ap_array[0] == 199
    assert ap_array[1] == 300
    assert ap_array[2] == 236
    assert ap_array[3] == 400
    assert ap_array[4] == 32
    assert ap_array[5] == (39 + 48 + 9 + 7 + 6 + 22 + 27 + 15) / 8.0
    assert ap_array[6] == (27 + 18 + 12 + 12 + 7 + 27 + 27 + 27) / 8.0
