import pytest
import typing

from space_weather_all import SpaceWeatherAll


@pytest.fixture(scope='function')
def client():
    class Client:
        sw = SpaceWeatherAll()
    return Client()


def test_url(client):
    """ test the getting of the url """
    assert client.sw.url == "https://celestrak.com/SpaceData/SW-All.txt"


def test_read_txt_bytes(client):
    """ test the reading of the data as bytes """
    bytes = client.sw._read_txt_bytes()
    assert isinstance(bytes, typing.ByteString)


def test_read_txt_string(client):
    """ test the downloading of the text file and returning of the data as a string """
    string = client.sw._read_txt_string()
    assert isinstance(string, str)
