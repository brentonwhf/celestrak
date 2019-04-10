import pytest
import pandas as pd
from datetime import datetime, date, timedelta

from space_weather_5year import SpaceWeather5Year


@pytest.fixture(scope='function')
def client():
    class Client:
        sw = SpaceWeather5Year()
    return Client()


def test_df_observed(client):
    """ test the conversion of data tables within the text file into separate dataframes """
    # test the default value
    df = client.sw.df_observed
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape[1] == 30
    assert df.index.name == 'epoch'
    # test the setting of an invalid df_observed
    with pytest.raises(ValueError):
        client.sw.df_observed = pd.DataFrame()
    with pytest.raises(TypeError):
        client.sw.df_observed = 'test'
    # test the getting of an invalid df_observed
    client.sw._df_observed = pd.DataFrame()
    with pytest.raises(ValueError):
        test = client.sw.df_observed
    client.sw._df_observed = 'test'
    with pytest.raises(TypeError):
        test = client.sw.df_observed


def test_df_predicted(client):
    """ test the conversion of data tables within the text file into separate dataframes """
    # test the default value
    df = client.sw.df_predicted
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape[1] == 30
    assert df.index.name == 'epoch'
    # test the setting of an invalid df_predicted
    with pytest.raises(ValueError):
        client.sw.df_predicted = pd.DataFrame()
    with pytest.raises(TypeError):
        client.sw.df_predicted = 'test'
    # test the getting of an invalid df_predicted
    client.sw._df_predicted = pd.DataFrame()
    with pytest.raises(ValueError):
        test = client.sw.df_predicted
    client.sw._df_predicted = 'test'
    with pytest.raises(TypeError):
        test = client.sw.df_predicted


def test_get_item(client):
    """ test the getting of an item based on the input date """
    # test the case for a date object
    datetime_ref = datetime.utcnow()
    datetime1 = datetime_ref - timedelta(days=400, hours=3, minutes=4, seconds=5, microseconds=6)
    result1 = client.sw[datetime1]
    assert len(result1.index.get_level_values('epoch')) == 1
    assert pd.to_datetime(result1.index.get_level_values('epoch')[0]).date() == datetime1.date()
    # test the case when the input timestamp is the minimum value and a timestamp object
    datetime2 = pd.Timestamp(client.sw.df_observed.index.get_level_values('epoch').min())
    result2 = client.sw[datetime2]
    assert len(result2.index.get_level_values('epoch')) == 1
    assert pd.to_datetime(result2.index.get_level_values('epoch')[0]).date() == datetime2.date()
    # test the case when the input datetime is less than the minimum datetime
    datetime3 = datetime2 - timedelta(days=1)
    with pytest.raises(ValueError):
        result3 = client.sw[datetime3]
    # test the case when the datetime is equal to the maximum observed datetime
    datetime4 = pd.Timestamp(client.sw.df_observed.index.get_level_values('epoch').max())
    result4 = client.sw[datetime4]
    assert len(result4.index.get_level_values('epoch')) == 1
    assert pd.to_datetime(result4.index.get_level_values('epoch')[0]).date() == datetime4.date()
    # test the case when the datetime is greater than the maximum observed datetime
    datetime5 = datetime4 + timedelta(days=1)
    result5 = client.sw[datetime5]
    assert len(result5.index.get_level_values('epoch')) == 1
    assert pd.to_datetime(result5.index.get_level_values('epoch')[0]).date() == datetime5.date()
    # test the case when the datetime is equal to the maximum predicted datetime
    datetime6 = pd.Timestamp(client.sw.df_predicted.index.get_level_values('epoch').max())
    result6 = client.sw[datetime6]
    assert len(result6.index.get_level_values('epoch')) == 1
    assert pd.to_datetime(result6.index.get_level_values('epoch')[0]).date() == datetime6.date()
    # test the case when the datetime is greater than the predicted values
    datetime7 = pd.Timestamp(client.sw.df_predicted.index.get_level_values('epoch').max()) + timedelta(days=1)
    with pytest.raises(ValueError):
        result7 = client.sw[datetime7]